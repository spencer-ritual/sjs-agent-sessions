# erc721-follow-on

Source roadmap: `/home/ritual/repos/dkms/docs/AGENT_IDENTITY_PROTOTYPE_PLAN.md`, specifically `Step 4: ERC-721 Follow-On`.

This is the tokenized-identity step: we keep the chain-issued `agentId` anchor, but represent it as an ERC-721 token so ownership of an agent is defined by NFT ownership and transferable via standard ERC-721 transfers.

Assumption: Step 3 (explicit slot claim / active holder binding) is already landed. `agentId` is the authoritative identity anchor, `AgentHeartbeat` is the `agentId`-keyed assignment+liveness contract, and dKMS enforces active-holder authorization. Step 4 does not undo any of that.

## Design Plan
- Goal: represent each chain-issued `agentId` as an ERC-721 token (`tokenId == agentId`) so the NFT holder is the canonical owner of the agent, ownership can be transferred by transferring the NFT, and DKMS key continuity and active-holder enforcement are preserved across transfer.
- Main workstreams:
  1. `ritual-sc-internal`: fold ERC-721 into the existing `AgentIdentityRegistry` so the registry *is* the NFT contract; `tokenId == agentId`; `ownerOf(tokenId)` is the canonical owner.
  2. mint path: `allocateAgentId` continues to produce chain-issued IDs and mints the NFT to the same address it currently assigns as owner (`identityOwner`, which must match `msg.sender` or `tx.origin`).
  3. transfer semantics: standard ERC-721 transfers are allowed at any time, including while the `AgentHeartbeat` slot is `ACTIVE`. Transfer does not touch the active binding; transfer never grants operational authority on its own.
  4. downstream reads: any code today that reads "owner of this `agentId`" is updated to read `ownerOf(tokenId)` from the merged registry. Anything that reads "active holder" continues to read `AgentHeartbeat` unchanged.
  5. DKMS and runtime: derivation stays keyed on `agentId` (`= tokenId`), so keys are stable across ownership transfer. Authorization stays keyed on Step 3 active-holder binding, so transferring the NFT does not grant key access.
  6. local-network validation: prove mint on launch, transfer with `ACTIVE` slot, key continuity across transfer, and that the new owner must go through `recall` + fresh claim to gain operational control.
- Key decisions (all resolved):
  1. `tokenId == agentId`, single value, single contract.
  2. `ownerOf(tokenId)` is the canonical agent owner. The standalone `owner` field on `AgentIdentity` is removed (breaking change OK).
  3. ERC-721 is merged into `AgentIdentityRegistry`. No separate wrapper contract.
  4. Initial owner on mint is whoever is determined as owner today in `allocateAgentId` — the passed-in `identityOwner`, which must match `msg.sender` or `tx.origin`.
  5. Transfers are allowed at any time, including during an `ACTIVE` slot. The runtime binding is not touched on transfer. New owner can call `recall` at any time to vacate the slot and let a fresh claim under their control take over.
  6. Full ERC-721 approvals are allowed: `approve`, `setApprovalForAll`, `safeTransferFrom`, operator-based transfers.
  7. DKMS derivation is stable across transfer (keys are `agentId`-scoped, not owner-scoped). Transfer never rotates keys.
  8. Step 3 active-holder binding is the only source of operational authority; NFT ownership is never an auth source on its own.
  9. Mint is chain-authored only: the existing `allocateAgentId` flow is the sole mint path. No external minting API.
  10. No retroactive migration. Breaking changes are acceptable; pre-existing `agentId` state does not need to be preserved.
  11. `tokenURI` / metadata is deferred to Step 5.
  12. No ERC-4337.
- Risks and dependencies:
  1. Depends on Step 3 being landed: without `agentId`-keyed `AgentHeartbeat` and active-holder-gated dKMS, the "transfer never grants authority" guarantee cannot hold.
  2. Any remaining consumer that still reads the old owner field (rather than `ownerOf`) will silently disagree with NFT ownership after transfer. Audit scope must cover all reads.
  3. Transferring during an `ACTIVE` slot means the new owner temporarily has title but not operational control. This is intentional but must be documented clearly in product UX to avoid confusion.
  4. Full approval surface (`setApprovalForAll`) means operators can move agents. This is accepted, but product and security surface should acknowledge that the approval authority is equivalent to custody.
  5. Storage layout change to `AgentIdentityRegistry` is a breaking change under UUPS. With the user's "no retroactive, breaking changes OK" stance, redeploy is fine, but any localnet/genesis pipelines that snapshot the old contract's state need to be updated.

## Ambiguities To Resolve
_All initial ambiguities resolved:_
- Resolved: transfers are allowed at any time, including during `ACTIVE`; active binding is not touched.
- Resolved: initial owner on mint is the same address we assign as owner today in `allocateAgentId`.
- Resolved: merge ERC-721 into `AgentIdentityRegistry`.
- Resolved: full ERC-721 approvals are allowed.
- Resolved: `tokenURI` / metadata moves to Step 5.
- Resolved: no retroactive migration; breaking changes OK.

## Implementation Plan

1. `ritual-sc-internal`: merge ERC-721 into `AgentIdentityRegistry`
   Objective:
   Make `AgentIdentityRegistry` itself the ERC-721 identity contract so `tokenId == agentId` and `ownerOf(tokenId)` is the canonical agent owner.
   Change:
   Add `ERC721Upgradeable` (and whichever enumerable/approval extensions are needed for the owner index) to `AgentIdentityRegistry`'s inheritance. Keep `Initializable`, `UUPSUpgradeable`, and `OwnableUpgradeable` for admin/upgrade authority. Extend `initialize` to initialize ERC-721 name/symbol. Remove the standalone `owner` field from `AgentIdentity` struct and replace all internal reads with `ownerOf(agentId)`. Remove `_ownerAgentIds` and `getOwnerAgentIds` in favor of ERC-721 enumerable equivalents (or re-implement `getOwnerAgentIds` on top of `balanceOf` / `tokenOfOwnerByIndex`). Preserve the `agentIdByAddress` mapping and `bindAgentAddress` behavior, but gate it on `ownerOf(agentId) == msg.sender` instead of the removed field.
   Constraints:
   No external mint API. Only `allocateAgentId` mints. No retroactive state preservation; breaking storage changes are acceptable. Admin `owner()` (from `OwnableUpgradeable`) must not be confused with per-agent `ownerOf` — they are distinct; add a brief contract-level comment noting this.
   Verification:
   Foundry tests show: `allocateAgentId` mints a token to the caller; `ownerOf(agentId)` matches the initial owner; `getIdentity` no longer carries a standalone `owner`; attempts to bind `agentAddress` from non-owners revert with the existing error path.

2. `ritual-sc-internal`: mint in `allocateAgentId` using today's owner rules
   Objective:
   Keep the existing chain-authored allocation contract as the sole mint path, with unchanged owner-determination semantics.
   Change:
   In `allocateAgentId`, after allocating the new `agentId`, call the internal `_safeMint(identityOwner, agentId)`. Preserve the existing guard that `identityOwner == msg.sender || identityOwner == tx.origin`, the zero-address check, and the `AgentIdAllocated` event. Treat the ERC-721 `Transfer` event emitted by `_safeMint` as the canonical NFT signal; `AgentIdAllocated` may remain for backwards compatibility with Step 1a consumers, or be removed (breaking change OK).
   Constraints:
   Caller may not supply `agentId`/`tokenId`; it is always the freshly allocated monotonic id. No batch mint. No mint from admin.
   Verification:
   Foundry test: `allocateAgentId(alice)` from `alice` emits both `Transfer(0x0 -> alice, agentId)` and `AgentIdAllocated(agentId, alice, alice)`; `ownerOf(agentId) == alice`; allocating from a non-matching `identityOwner` reverts with `IdentityOwnerMismatch`.

3. `ritual-sc-internal`: allow transfers at any time, including during `ACTIVE`, and update approval surface
   Objective:
   Implement standard ERC-721 transferability with full approval support, independent of `AgentHeartbeat` state.
   Change:
   Do not override `_update` / `_beforeTokenTransfer` to block transfers based on `AgentHeartbeat` state. Leave `approve`, `setApprovalForAll`, `transferFrom`, and `safeTransferFrom` at their default ERC-721 behavior. Emit no additional events on transfer beyond the standard ERC-721 `Transfer` / `Approval` / `ApprovalForAll`. `AgentHeartbeat` active-holder state is not read or modified by the registry on transfer.
   Constraints:
   Do not auto-recall on transfer. Do not require `VACANT`. Do not block transfers based on who the active holder is. Ownership transfer must not alter any Step 3 binding.
   Verification:
   Foundry tests: transfer while `AgentHeartbeat` slot is `ACTIVE` succeeds; after transfer, `ownerOf(agentId) == newOwner` and `AgentHeartbeat` still reports the same `ACTIVE` holder with the same credential; operator-based `transferFrom` via `setApprovalForAll` succeeds.

4. `ritual-sc-internal`: update `AgentHeartbeat` and other on-chain consumers to read `ownerOf(agentId)`
   Objective:
   Make `AgentHeartbeat` and any other on-chain code rely on the NFT contract as the single source of truth for agent ownership.
   Change:
   Where `AgentHeartbeat` or related contracts currently read "owner of this `agentId`" from the registry struct, replace those reads with `IAgentIdentityRegistry(registry).ownerOf(agentId)`. Active-holder state, claim, heartbeat, recall, and timeout transitions remain unchanged — they continue to operate on `boundHolderKey`, not owner. If any path used to gate an action on "caller is identity owner", it now gates on `msg.sender == ownerOf(agentId)` or an approved operator (`isApprovedForAll` / `getApproved`).
   Constraints:
   Do not merge ownership and active-holder authority. Owner-gated actions (e.g. `recall` by the owner) remain owner-gated via ERC-721 owner/approval checks; holder-gated actions (e.g. `heartbeat` refresh) remain gated on the bound holder credential.
   Verification:
   Contract tests: `recall` can be triggered by the NFT owner or an approved operator; `recall` cannot be triggered by a previous owner after transfer; `heartbeat` still requires matching holder credential regardless of who the current NFT owner is.

5. `dkms` and `executor-go-internal`: switch ownership lookups to `ownerOf(agentId)` without touching `agentId`-keyed derivation
   Objective:
   Route any off-chain "who owns this agent?" query through the merged registry, while leaving `agentId`-keyed key derivation and Step 3 holder checks unchanged.
   Change:
   In `dkms` and `executor-go-internal`, find every place that reads agent ownership (e.g. metadata for logs, policy hooks, or any authorization surface that still consulted the old owner field) and replace it with a call to `ownerOf(agentId)` on the registry. Do not change any `DeriveAgentRootKey` / `GetAgentRootKey` code paths — key derivation remains keyed strictly on `agentId`. Do not change the Step 3 active-holder check in dKMS; owner is never an authorization input for key issuance.
   Constraints:
   Keys must not rotate on transfer. Owner must never be an auth input for key issuance. Any ownership read that used to happen against a cached struct field should be refreshed to reflect `ownerOf` at the time of the check.
   Verification:
   Integration test: derive keys for `agentId` A while `owner == alice`; transfer to `bob`; re-derive for the same `agentId`; confirm identical key material. Separately, confirm that after transfer, `bob` cannot derive without going through `recall` + fresh claim (because Step 3 active holder is still the prior TEE holder, not any principal associated with `bob`).

6. `ritual-node-internal`: update localnet deploy and config for the merged registry
   Objective:
   Make the local network deploy and run the new merged `AgentIdentityRegistry` so end-to-end Step 4 scenarios can be reproduced.
   Change:
   Update the genesis / deployment pipeline and any ABI / resources snapshot (e.g. `resources/el/AgentIdentityRegistry*.json`) to reflect the merged ERC-721 registry. Update any localnet orchestration that reads owner state from the registry to use the new `ownerOf`-based API. No retroactive migration of old `agentId` state is required; a clean redeploy is acceptable.
   Constraints:
   Do not preserve pre-Step-4 registry state. Do not introduce a compatibility shim; the old `owner` struct field is gone.
   Verification:
   `make restart-network` succeeds with the new contract; the resulting registry reports `ownerOf(agentId)` correctly after a fresh `allocateAgentId`; existing Step 1a/1b/2/3 localnet scenarios still pass against the merged registry.

7. `traffic-gen-internal`: add Step 4 transfer and takeover scenario
   Objective:
   Provide a reproducible scenario that proves transferability, key continuity, and non-authority of raw ownership.
   Change:
   Add a traffic-gen flow that: (a) launches a persistent agent and records `agentId`, owner, and a sample derived key; (b) transfers the NFT to a second owner while the slot is still `ACTIVE`; (c) re-derives the key for the same `agentId` and asserts the material is identical; (d) asserts the new owner cannot derive directly or command the active holder without going through `recall`; (e) has the new owner call `recall`, wait for `VACANT`, spawn a new holder, and confirm the new holder can claim and derive.
   Constraints:
   Scenario must assert both positive (key continuity across transfer) and negative (ownership alone does not grant authority) properties. Keep it deterministic for CI.
   Verification:
   `make run-step4-transfer` (or equivalent target) succeeds and prints explicit checks for each of (a)–(e).

8. `ritual-node-internal`: run the Step 4 end-to-end local-network validation
   Objective:
   Prove the full cross-repo Step 4 story on a live local network.
   Change:
   From a fresh `ritual-node-internal` restart with the new contracts and services, run the traffic-gen scenario from step 7. Capture evidence for: mint-on-allocate, transfer during `ACTIVE`, key continuity, non-authority of NFT ownership, and recall-driven re-claim under new owner control.
   Constraints:
   Treat dKMS denial (for any attempt to derive outside the Step 3 bound holder) as authoritative; ownership-transfer log evidence is supporting but not sufficient on its own.
   Verification:
   End-to-end logs and commands demonstrate: `ownerOf` changes on transfer; Step 3 holder does not change on transfer; derived key material is identical before and after transfer; post-transfer recall + re-claim produces an `ACTIVE` binding for a new holder on behalf of the new owner; pre-transfer (original) holder is rejected by dKMS after that recall, per Step 3 semantics.
