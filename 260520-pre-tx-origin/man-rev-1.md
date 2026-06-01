# Manual Review 1: Remove Duplicate Detector Helpers

Context: `ritual-reth-internal` PR 407 adds sender-provenance logic in `crates/ritual/async/src/detector.rs`. The ownership policy is directionally useful, but some of the new helper code duplicates existing canonical logic and should be removed or factored out before merging.

## Required Cleanup

### 0. Revert `crates/ritual/async-inspector/src/inspector.rs` changes

Revert the PR changes in `crates/ritual/async-inspector/src/inspector.rs`.

Specifically remove the new REVM integration-style unit test scaffolding added under `#[cfg(test)] mod tests`, including:

- the added `revm` imports
- `fn install_contract(...)`
- `inspector_records_contract_address_for_direct_precompile_call`
- `inspector_records_proxy_address_through_delegatecall_wrapper`
- the hand-written opcode bytecode vectors used by those tests

Reason: these tests are too low-level and unmaintainable for this file. They encode EVM call/delegatecall setup with long raw opcode arrays, which makes the test intent hard to audit and fragile across REVM/opcode helper changes. The behavior they are trying to protect is sender provenance for async commitments, and that should be caught at a higher level where the full transaction path is visible, for example detector-level tests and existing/new E2E tests covering scheduled async calls through `ScheduledConsumer`.

Do not replace these with more bytecode-heavy tests in `async-inspector`. Keep `async-inspector` focused on simple invariant tests for `AsyncPrecompileInspector::async_call_result`; exercise caller attribution through higher-level async detector or E2E coverage.

### 1. Remove local Scheduler execute calldata parsing from `detector.rs`

Remove these additions from `crates/ritual/async/src/detector.rs`:

- `const SCHEDULER_EXECUTE_SELECTOR: [u8; 4] = [0x56, 0x01, 0xea, 0xea];`
- `fn scheduled_execute_call_id(tx: &TxScheduled) -> Option<u64>`

Replace them with a shared helper in `crates/ritual/scheduled-verification/src/lib.rs`, for example:

```rust
pub const SCHEDULER_EXECUTE_SELECTOR: [u8; 4] = [0x56, 0x01, 0xea, 0xea];

pub fn scheduler_execute_call_id(input: &[u8]) -> Option<u64> {
    if input.len() < 36 || input[..4] != SCHEDULER_EXECUTE_SELECTOR {
        return None;
    }

    Some(U256::from_be_slice(&input[4..36]).to::<u64>())
}
```

Then update `detector.rs` to call:

```rust
let call_id = scheduler_execute_call_id(&signed.tx().input)?;
```

Also update `crates/transaction-pool/src/pool/mod.rs`, which currently has its own private `scheduler_call_id_from_scheduled_tx` with the same selector. That function should delegate to the shared `scheduler_execute_call_id(tx.transaction.input())` helper instead of carrying its own selector/parser.

Reason: Scheduler ABI parsing should have one implementation. Otherwise txpool and async detection can drift if `Scheduler.execute(...)` calldata changes.

### 2. Remove local async-precompile address matching from `direct_async_call_fallback`

The PR adds a manual `matches!` list in `direct_async_call_fallback`:

- `HTTP_CALL_PRECOMPILE`
- `LLM_CALL_PRECOMPILE`
- `LONG_RUNNING_HTTP_PRECOMPILE`
- `ZK_TWO_PHASE_PRECOMPILE`
- `FHE_PRECOMPILE`
- `SOVEREIGN_AGENT_PRECOMPILE`
- `IMAGE_CALL_PRECOMPILE`
- `AUDIO_CALL_PRECOMPILE`
- `VIDEO_CALL_PRECOMPILE`
- `DKMS_KEY_PRECOMPILE`
- `PERSISTENT_AGENT_PRECOMPILE`

Replace that manual list with the canonical address set already used by `AsyncPrecompileInspector`:

```rust
if !ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES.contains(&to) {
    return None;
}
```

If `ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES` is not currently re-exported by `reth_ritual_async_inspector`, re-export it from `crates/ritual/async-inspector/src/lib.rs` and import it in `detector.rs`.

Reason: async detection should not maintain a second precompile allowlist. The fallback should use the same source of truth as the inspector.

### 3. Move `get_scheduled_consumer_address` out of `detector.rs`

Remove the local helper:

```rust
fn get_scheduled_consumer_address() -> Address {
    std::env::var("SCHEDULED_CONSUMER_ADDRESS")
        .ok()
        .and_then(|addr_str| addr_str.parse().ok())
        .unwrap_or_else(|| "0x48ba49c2fFee9845E467143feC8Ed7B36A434694".parse().expect("valid address"))
}
```

Replace it with a shared contract address helper next to the other scheduler-related address helpers, likely in `crates/ritual/scheduled-verification/src/lib.rs`:

```rust
pub fn get_scheduled_consumer_address() -> Address {
    std::env::var("SCHEDULED_CONSUMER_ADDRESS")
        .ok()
        .and_then(|addr_str| addr_str.parse().ok())
        .unwrap_or_else(|| address!("48ba49c2fFee9845E467143feC8Ed7B36A434694"))
}
```

Then import it in `detector.rs` from `reth_ritual_scheduled_verification`.

Reason: detector logic should not own deployed contract address defaults. Keeping address accessors together makes future genesis/address updates less error-prone.

### 4. Add a `JobSender` comment explaining the correct construction pattern

Add a comment near `JobSender` in `crates/ritual/async-types/src/lib.rs` explaining why detector-side helpers like `job_sender_from_precompile_caller(Address)` are not allowed.

The comment should say that `JobSender` represents the canonical async job owner only after it has been encoded into an async commitment or read from registry storage. A helper that accepts a bare `Address`, even if named after precompile caller provenance, gives callers a way to wrap transaction signers, system senders, scheduled callers, or RPC/debug addresses as job owners with no compiler signal.

The comment should also document the correct detector pattern:

1. Detector code may choose a plain `Address` to encode into `AsyncJobTracker.addJob(... sender ...)`.
2. Normal async calls should choose the immediate precompile caller captured by the inspector.
3. The narrow blessed scheduled path may choose the original scheduled caller after proving Scheduler/ScheduledConsumer provenance.
4. After constructing the commitment, recover `JobSender` by decoding the commitment with `commitment_job_sender(...)`.

Do not add or keep a shared helper like `job_sender_from_precompile_caller(Address) -> JobSender`. If readability is needed in detector code, use a detector-local helper that returns `Address`, such as `effective_async_commitment_sender_address(...)`, not `JobSender`.

### 5. Route wallet billing through `JobSender`

The billed wallet is always the async job owner. Do not introduce a separate scheduled billing path that bills `TxScheduled.caller` independently from the commitment's `Job.sender`.

Remove these additions from `crates/ritual/async/src/wallet.rs`:

- `fn billed_wallet_address(...)`
- `fn scheduled_wallet_payer(...)`
- `fn billed_wallet_address_from_scheduled_caller(...)`
- the tests that assert scheduled wallet billing prefers `TxScheduled.caller`

In `check_user_wallet_balance_with_provider`, use the existing commitment-derived owner:

```rust
let user_address = async_result.job_sender.as_address();
```

Also remove the verifier-side duplicate billing branch in `crates/ritual/block-verification/src/lib.rs`:

```rust
let billed_wallet_address = match &original_tx {
    OriginalTransaction::Scheduled(signed) => signed.tx().caller,
    _ => sender.as_address(),
};
```

and pass the commitment-derived sender directly:

```rust
sender.as_address()
```

Reason: wallet billing, nonce locking, and commitment ownership should all use the same canonical async job owner. If scheduled execution needs to attribute ownership to the original scheduled caller, that address should be selected before commitment construction and encoded as `AsyncJobTracker.addJob(... sender ...)`; after that, all billing and verification should flow through `JobSender`.

### 6. Use `JobSender` for async-pool ownership and locking

Update `crates/transaction-pool/src/pool/async_pool.rs` so canonical async ownership/locking is based on the commitment's decoded `Job.sender`, not `original_tx.signer_ref()`.

Add `JobSender` to `AsyncCommitmentData`:

```rust
pub struct AsyncCommitmentData<C> {
    pub original_tx: Recovered<C>,
    pub job_sender: JobSender,
    // existing fields...
}
```

Populate it in the Ritual `AsyncPoolConsensus` implementation by decoding the async commitment:

```rust
let job_sender = reth_ritual_async_fees::commitment_job_sender(self)?;
```

Then replace async-lock ownership lookups that currently use:

```rust
let sender = *commitment.original_tx.signer_ref();
```

with:

```rust
let sender = commitment.job_sender;
```

Rename the internal pool fields/helpers to make the semantics clear:

- `sender_index` -> `job_sender_index`
- `locks_sender` -> `locks_job_sender`
- `is_sender_locked(...)` should either accept `JobSender`, or explicitly convert only at the external transaction-admission boundary where the pending transaction signer is being checked against async job owners.

Keep raw `Address` / `original_tx.signer_ref()` only where the code is explicitly reconstructing or validating the original transaction signer. Do not use the origin signer as the async owner.

Reason: the pool's async lock is about active async job ownership. That owner is the `Job.sender` encoded in the canonical commitment, which may differ from the recovered signer for scheduled/system-origin flows.

### 7. Apply the same `JobSender` boundary in `ritual-reth-nodebuilder-internal` PR 156

In `ritual-reth-nodebuilder-internal` PR 156, keep the same pre-commitment vs post-commitment ownership boundary.

Before an async commitment exists, nodebuilder/RPC may only have the address that will be encoded into `AsyncJobTracker.addJob(... sender ...)`. Keep that as a plain `Address`, but name it explicitly, for example:

```rust
commitment_sender_address
```

or:

```rust
async_owner_address
```

Do not call this value generic `user_address` or `msg_sender` in validation code if it is being used as the future commitment owner. Those names make it too easy to confuse transaction signers, precompile callers, wallet payers, and canonical async owners.

After an async commitment exists, use `JobSender` everywhere the code means canonical async owner. In PR 156, that includes:

- same-block duplicate async commitment checks in `crates/node/src/payload.rs`
- async pool metadata consumed by settlement construction in `crates/node/src/payload.rs`
- post-execution async commitment verification in `crates/node/src/rpc.rs`

Do not import or use `job_sender_from_precompile_caller` in nodebuilder tests or production code. That repeats the same bad pattern as in `ritual-reth-internal`: it lets test code manufacture `JobSender` from a bare `Address`, which weakens the type boundary and encourages production code to do the same.

For nodebuilder tests that need a `JobSender`, build an async commitment and decode it with `commitment_job_sender(...)`, or use test metadata that already carries a commitment-derived `JobSender`. Do not construct one directly from an address.

Reason: nodebuilder should consume the async ownership abstraction produced by reth instead of re-deriving sender provenance rules. The only place raw precompile-caller provenance belongs is before commitment construction, as the `Address` that will be encoded into the commitment. Once encoded, all duplicate checks, wallet/billing decisions, pool ownership, settlement construction, and verification should flow through `JobSender`.

### 8. Revert `ritual-alloy-evm-internal` PR 63 nonce-check skip

Revert the changes in `ritual-alloy-evm-internal` PR 63.

Specifically revert the nonce-check bypass in `crates/ritual-evm/src/eth/block.rs`:

- `fn should_skip_nonce_check_for_fulfilled_async_replay(...)`
- the temporary `cfg.disable_nonce_check` swap around normal transaction execution
- the tests asserting fulfilled async replay skips nonce checks

Reason: this looks like a workaround for an issue from the previous approach where the agent was still trying to use the precompile-consumer path instead of switching to direct traffic. With the direct-traffic design, we should not need to weaken normal nonce validation in the EVM execution layer.

This change is also too broad as written: it disables nonce checks for any non-system transaction with non-empty `spc_calls`, rather than for a narrowly typed and already-verified fulfilled async replay path. That makes runtime SPC attachment control the EVM nonce rule, which is the wrong abstraction and creates avoidable consensus risk.

If fulfilled async replay still fails after the direct-traffic changes, debug that path directly instead of keeping this nonce bypass. The fix should be in how fulfilled replay transactions are constructed/selected, not in a generic EVM nonce-check exception.
