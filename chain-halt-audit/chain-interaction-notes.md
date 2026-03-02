# Chain Interaction Notes — Ritual Local Network

Notes for agents building/sending transactions to the local Ritual dev chain.

---

## Connection

| Parameter | Value |
|-----------|-------|
| RPC URL | `http://localhost:8545` |
| Chain ID | `1979` (0x7bb) |
| Block time | ~2s |
| Consensus | PoA (inject `async_geth_poa_middleware` if using sync web3) |

Multiple nodes run on sequential ports: `8545`, `8546`, `8547`, `8548`.

### Verify chain is alive
```bash
curl -s -X POST http://localhost:8545 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

---

## Funded Accounts

| Role | Address | Private Key |
|------|---------|-------------|
| Faucet (primary) | `0xe60dc774077dceD3F9EA2C0bde81c2F44f171412` | `0xb21e915e5b3fcbddb87c5e5dd69fcfe089c046931dac43983dfe577d6c4b1d7a` |
| Faucet (fallback) | — | `ea2392b90453129e747ab0df9133dc5b4be9aa023f99c0c83a56fffe009a43d6` |

The primary faucet has an enormous balance (~0x5555... wei). Use it for all test transactions.

Source: `traffic-gen-internal/src/core/config.py:132`

---

## Python Environment

All traffic-gen scripts use the venv at:
```
/home/ritual/repos/traffic-gen-internal/.venv/
```

Run scripts from `traffic-gen-internal/` like:
```bash
cd /home/ritual/repos/traffic-gen-internal
.venv/bin/python3 path/to/script.py
```

Relevant packages available in venv: `web3`, `eth_account`, `eth_abi`

---

## Sending Transactions (web3.py async pattern)

```python
from web3 import AsyncWeb3

w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider("http://localhost:8545"))

FAUCET_KEY = "0xb21e915e5b3fcbddb87c5e5dd69fcfe089c046931dac43983dfe577d6c4b1d7a"
acct = w3.eth.account.from_key(FAUCET_KEY)

chain_id  = await w3.eth.chain_id          # 1979
nonce     = await w3.eth.get_transaction_count(acct.address)
gas_price = await w3.eth.gas_price

tx = {
    "from":     acct.address,
    "to":       "0x<target>",
    "data":     "0x<calldata_hex>",
    "gas":      500_000,
    "gasPrice": gas_price,
    "nonce":    nonce,
    "chainId":  chain_id,
    "value":    0,
}

signed   = w3.eth.account.sign_transaction(tx, FAUCET_KEY)
tx_hash  = await w3.eth.send_raw_transaction(signed.raw_transaction)
receipt  = await w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
```

Use `asyncio.wait_for(..., timeout=35)` if testing for chain halts — a non-responding chain will never return a receipt.

---

## Precompile Addresses

Ritual's custom precompiles live in the 0x0800-0x081F range.

| Precompile | Address | Type |
|-----------|---------|------|
| LLM Call | `0x0000000000000000000000000000000000000802` | Async SPC |
| Image Call (T2I) | `0x0000000000000000000000000000000000000818` | Multimodal |
| Audio Call (T2A) | `0x0000000000000000000000000000000000000819` | Multimodal |
| Video Call (T2V) | `0x000000000000000000000000000000000000081A` | Multimodal |
| FHE | `0x0000000000000000000000000000000000000807` | Encrypted compute |
| DKMS Key | `0x000000000000000000000000000000000000081B` | Key management |

Source: `ritual-sc-internal/src/utils/PrecompileConsumer.sol:42-48`,
        `ritual-reth-internal/crates/ritual-async-fees/src/constants.rs:95-102`

Precompiles are called directly with raw calldata (no function selector prefix).

---

## Multimodal Precompile Calldata Layout

All three multimodal precompiles (Image/Audio/Video) share the same 18-field ABI:

```
Field  0: address  executor
Field  1: uint256  ttl
Field  2: bytes    user_public_key          ← dynamic
Field  3: address  commitment_validator
Field  4: address  inclusion_validator
Field  5: uint256  poll_interval_blocks
Field  6: uint256  max_poll_block
Field  7: address  delivery_target
Field  8: bytes4   delivery_selector
Field  9: uint256  delivery_gas_limit
Field 10: uint256  delivery_max_fee_per_gas
Field 11: uint256  delivery_max_priority_fee_per_gas
Field 12: uint256  delivery_value
Field 13: uint256  reserved
Field 14: string   model                    ← dynamic
Field 15: (uint8,bytes,string,bytes32,uint32,uint32,bool)[]  inputs  ← dynamic
Field 16: (uint8,uint32,uint32,uint32,bool,uint16,uint16,uint32,uint8,string)  OutputConfig  ← dynamic (has string)
Field 17: bytes    encrypted_storage_payment  ← dynamic
```

**OutputConfig sub-fields** (tuple at field 16):
```
Word 0: uint8   output_type          (0=text, 1=image, 2=audio, 3=video)
Word 1: uint32  width / max_param1
Word 2: uint32  height / max_param2
Word 3: uint32  duration_ms / max_param3
Word 4: bool    encrypt_output
Word 5: uint16  num_inference_steps  ← C1 panic target
Word 6: uint16  guidance_scale_x100
Word 7: uint32  seed
Word 8: uint8   fps                  ← C1 panic target (secondary)
Word 9: string  negative_prompt (offset pointer)
```

The Rust parser (`extract_output_ux_params_from_input`, lib.rs:830) only reads:
- Word 16 of the overall head → ABI offset pointer to OutputConfig bytes
- Words 5 and 8 within the OutputConfig sub-encoding → steps and fps

All other fields can be zero for a minimal test payload.

**Minimal calldata construction** (no eth_abi needed):
```python
HEAD_LEN   = 18 * 32   # 576 bytes
OUTPUT_LEN = 10 * 32   # 320 bytes
payload    = bytearray(HEAD_LEN + OUTPUT_LEN)   # 896 bytes, all zeros

# Word 16: point to OutputConfig data immediately after the head
output_offset = HEAD_LEN
payload[16*32 : 17*32] = output_offset.to_bytes(32, "big")

# OutputConfig word 5: num_inference_steps
steps_start = output_offset + 5 * 32           # byte 576 + 160 = 736
payload[steps_start : steps_start + 32] = my_steps_value.to_bytes(32, "big")

# OutputConfig word 8: fps
fps_start = output_offset + 8 * 32             # byte 576 + 256 = 832
payload[fps_start : fps_start + 32] = my_fps_value.to_bytes(32, "big")
```

Guard in the parser: `output_offset < HEAD_LEN` returns `Err` (not panic), so the offset
must be ≥ 576. Setting it to exactly 576 (= HEAD_LEN) is the canonical minimal value.

Source: `ritual-reth-internal/crates/ritual-async-fees/src/lib.rs:749-914`,
        tests at lib.rs:1696 confirm the layout.

---

## Existing Traffic-Gen Infrastructure

For full end-to-end image/video calls with proper PrecompileConsumer contract:

```bash
cd /home/ritual/repos/traffic-gen-internal
make run-scheduled-echo          # Full E2E scheduled tx test
```

For lower-level examples:
- `src/action/image_call.py` — Python ImageCall action class
- `src/action/video_call.py` — VideoCall
- `src/blockchain/web3_client.py` — `StakeWeightedWeb3Client` with retry/failover
- `src/core/config.py` — `ServiceConfig`, env vars, faucet key

---

## Transaction Types

The chain supports:
- **Type 2 (EIP-1559)**: standard, use `maxFeePerGas` + `maxPriorityFeePerGas`
- **Type 0 (legacy)**: use `gasPrice`; simpler for one-off scripts
- **Type 0x77 (Passkey)**: Ritual custom type for P-256 signed txs — see `src/blockchain/passkey_encoder.py`

**IMPORTANT:** The chain rejects legacy Type 0 transactions with `-32003: transaction type not supported`.
Always use EIP-1559 (Type 2) with `maxFeePerGas` + `maxPriorityFeePerGas`.

For `cast`, omit `--legacy`. For web3.py, omit `gasPrice` and use:
```python
base_fee     = (await w3.eth.get_block("latest"))["baseFeePerGas"]
priority_fee = w3.to_wei(1, "gwei")
max_fee      = base_fee * 2 + priority_fee
# use maxFeePerGas=max_fee, maxPriorityFeePerGas=priority_fee in the tx dict
```
