#!/usr/bin/env python3
"""Regenerate functionality-flow atoms from downstream source evidence.

The flow markdown provides labels and traffic context. Promoted atom evidence must
come from the downstream source file that owns the behavior.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path


ROOT = Path("/home/ritual/repos/sjs-agent-sessions/reth-upstream-merge")
COVERAGE = ROOT / "coverage-map"
FILES_DIR = COVERAGE / "files"
OLD_REPO = Path("/home/ritual/repos/ritual-reth-internal")
AUDIT_DIR = COVERAGE / "functionality-flow-audit"


def load_index_by_path() -> dict[str, int]:
    rows = (ROOT / "ritual-reth-internal-downstream-from-divergence.name-status.txt").read_text().splitlines()
    out: dict[str, int] = {}
    for idx, line in enumerate(rows, start=1):
        parts = line.split("\t")
        if len(parts) == 2:
            path = parts[1]
        elif len(parts) >= 3:
            path = parts[-1]
        else:
            continue
        out[path] = idx
    return out


def load_file_records() -> tuple[dict[int, tuple[Path, dict]], int]:
    records: dict[int, tuple[Path, dict]] = {}
    removed = 0
    for path in sorted(FILES_DIR.glob("file-*.json")):
        rec = json.loads(path.read_text())
        atoms = rec.get("atoms", [])
        kept = [a for a in atoms if not a.get("functionality_flow_derived")]
        removed += len(atoms) - len(kept)
        rec["atoms"] = kept
        rec["atoms_total"] = len(kept)
        for atom in kept:
            atom["atoms_total"] = len(kept)
        records[rec["file_index"]] = (path, rec)
    return records, removed


def source_snippet(source_path: str, pattern: str, before: int = 3, after: int = 18) -> tuple[str, str]:
    source = OLD_REPO / source_path
    text = source.read_text(errors="replace")
    lines = text.splitlines()
    rx = re.compile(pattern)
    match = 0
    for idx, line in enumerate(lines):
        if rx.search(line):
            match = idx
            break
    lo = max(0, match - before)
    hi = min(len(lines), match + after + 1)
    return f"{source_path}:{lo + 1}-{hi}", "\n".join(lines[lo:hi])


def parse_candidates() -> list[dict]:
    # Fields:
    # path | pattern | source_kind | risk_tags csv | flow_titles csv | semantic_claim
    table = r"""
crates/ritual-precompile-addresses/src/lib.rs|ALL_SPC_BLOCK_VERIFIED_PRECOMPILE_ADDRESSES|consensus_constant|precompile,consensus-constant,async-fsm,verifier|Source Inventory;Short-Running Async SPC Trace;Long-Running Two-Phase Trace|The canonical precompile-address catalog keeps all dApp-facing SPC-verified and two-phase addresses in one source of truth, covering HTTP, LLM, long HTTP, ZK, FHE, multimodal, DKMS, sovereign-agent, and persistent-agent flows.
crates/ritual-precompile-codecs/src/http_call.rs|pub struct HTTPCallRequest|encoding_rule|encoding,rpc,async-fsm,precompile|http_call;x402_dkms_http_call;Secret, Private Output, And dKMS Trace|HTTP async payload decoding preserves the ExecutorRequest base fields, encrypted secret arrays, user public key, URL, method, headers, and optional body expected by HTTP and X402 HTTP traffic.
crates/ritual-precompile-codecs/src/llm_call.rs|pub struct LLMCallRequest|encoding_rule|encoding,rpc,async-fsm,executor-selection|llm_call;llm_call_streaming;Short-Running Async SPC Trace|LLM async payload decoding preserves the 30-field request shape while extracting executor, encrypted secrets, TTL, user public key, messages JSON, and model for shared RPC and builder validation.
crates/ritual-precompile-codecs/src/long_running.rs|pub struct DeliveryConfig|encoding_rule|encoding,async-fsm,payload,precompile|Long-Running Two-Phase Trace|Long-running delivery config decoding preserves callback target, selector, gas, fee caps, and value as the common Phase 2 callback contract between the executor, payload builder, and AsyncDelivery.deliver.
crates/ritual-precompile-codecs/src/long_running.rs|pub fn from_abi\(data|encoding_rule|encoding,rpc,async-fsm,negative-path|long_running_echo;x402_dkms_long_running_http|Long-running HTTP decoding extracts delivery configuration and the URL, poll URL, and result URL needed to validate and poll two-phase HTTP jobs without changing the shipped ABI layout.
crates/ritual-precompile-codecs/src/long_running.rs|pub fn from_zk_abi|encoding_rule|encoding,async-fsm,verifier,precompile|zk_two_phase;scheduled_zk_two_phase|ZK two-phase delivery decoding reads the max proof block and delivery callback fields from the ZK ABI so Phase 2 proof delivery uses the same callback contract as long-running HTTP.
crates/ritual-precompile-codecs/src/long_running.rs|pub fn from_sovereign_agent_abi|encoding_rule|encoding,async-fsm,executor-selection|Sovereign Agent Precompile Trace|Sovereign-agent delivery decoding uses the agent-specific ABI layout to extract max poll block and callback fields without depending on the long-HTTP field offsets.
crates/ritual-precompile-codecs/src/long_running.rs|pub fn from_persistent_agent_abi|encoding_rule|encoding,async-fsm,executor-selection|Persistent Agent Lifecycle Trace|Persistent-agent delivery decoding uses the 0x0820 ABI layout to extract max spawn block and callback fields used when spawning a long-running agent instance.
crates/ritual-precompile-codecs/src/long_running.rs|pub fn from_fhe_abi|encoding_rule|encoding,async-fsm,fees,precompile|FHE / Private Compute Trace|FHE delivery decoding reads the 19-field FHE request layout and max inference block so encrypted Phase 2 output delivery can be priced and settled deterministically.
crates/ritual-precompile-codecs/src/long_running.rs|pub fn extract_fhe_output_size|encoding_rule|encoding,fees,async-fsm|FHE / Private Compute Trace;Product Economics Compatibility|FHE Phase 2 result decoding extracts the encrypted output size from the delivery result, making output-size fee calculation depend on the delivered result struct rather than external metadata.
crates/ritual-precompile-codecs/src/persistent_agent.rs|pub struct PersistentAgentRequest|encoding_rule|encoding,async-fsm,executor-selection|Persistent Agent Lifecycle Trace;Factory-Backed Agent Deployment|Persistent-agent request decoding preserves the base executor fields, max spawn block, delivery config, model/provider/runtime settings, storage refs, and RPC URLs required to spawn OpenClaw or Hermes agents.
crates/ritual-precompile-codecs/src/persistent_agent.rs|pub struct PersistentAgentResponse|encoding_rule|encoding,async-fsm,negative-path|Persistent Agent Lifecycle Trace|Persistent-agent responses round-trip instance id, endpoint, checkpoint CID, and error message so Phase 2 delivery can distinguish successful spawns from spawn failures.
crates/ritual-precompile-codecs/src/sovereign_agent.rs|pub struct SovereignAgentRequest|encoding_rule|encoding,async-fsm,executor-selection|Sovereign Agent Precompile Trace;Agent Orchestrator Surface|Sovereign-agent request decoding preserves TTL, poll and deadline fields, delivery config, agent type, prompt, model, tools, max turns, max tokens, and RPC URLs used by multi-step agent flows.
crates/ritual-async/src/validation.rs|fn validate_base_fields|error_path|async-fsm,rpc,negative-path,consensus-constant|Admission And Validation Compatibility;Secret, Private Output, And dKMS Trace|Shared async payload validation rejects zero executors, zero or over-limit TTLs, malformed ECIES secret blobs, and compressed or wrong-size user public keys before RPC, builder, or verifier depend on the payload.
crates/ritual-async/src/validation.rs|pub fn try_decode_precompile_data|state_transition|async-fsm,rpc,precompile,encoding|Short-Running Async SPC Trace;Long-Running Two-Phase Trace|Async precompile data extraction routes HTTP, LLM, sovereign-agent, persistent-agent, DKMS, and generic ExecutorRequest payloads through their dedicated decoders before validating executor and TTL.
crates/ritual-async/src/validation.rs|pub fn extract_two_phase_deadline|encoding_rule|async-fsm,encoding,scheduled,negative-path|Long-Running Two-Phase Trace;Scheduled Execution Trace|Two-phase deadline extraction uses precompile-specific ABI offsets for sovereign-agent, persistent-agent, long-running HTTP, ZK, FHE, and multimodal requests, and returns no deadline for non-two-phase precompiles.
crates/ritual-async/src/validation.rs|pub fn validate_two_phase_deadline|error_path|async-fsm,negative-path,consensus-constant|Long-Running Two-Phase Trace|Two-phase deadline validation requires the Phase 2 deadline offset to be strictly greater than TTL so Phase 2 delivery cannot expire before Phase 1 settlement.
crates/ritual-async/src/validation.rs|pub fn validate_async_payload|state_transition|async-fsm,rpc,precompile,negative-path|Admission And Validation Compatibility|Async payload validation enforces max input size and routes precompile-specific URL, model, prompt, multimodal, FHE, DKMS, and agent checks from one shared validation surface.
crates/rpc/rpc/src/async_tx_validator.rs|RPC-level validation exists|error_path|rpc,async-fsm,negative-path|Short-Running Async SPC Trace;Admission And Validation Compatibility|RPC async validation is explicitly a user-feedback layer that delegates consensus-relevant payload checks to shared validation so invalid async traffic receives descriptive errors without becoming the authority over builder or verifier behavior.
crates/rpc/rpc/src/async_tx_validator.rs|pub\(crate\) fn validate_executor_registration|state_transition|rpc,executor-selection,precompile,negative-path|Executor And Operator Surface Compatibility|RPC executor registration checks map each async precompile to its required TEE capability, allowing sovereign and persistent agents to use HTTP or LLM executors while enforcing media, ZK, FHE, and HTTP capabilities.
crates/rpc/rpc/src/async_tx_validator.rs|pub\(crate\) fn validate_wallet_for_async|error_path|rpc,fees,async-fsm,negative-path|Admission And Validation Compatibility;Product Economics Compatibility|RPC wallet validation calls the same commitment wallet verifier as the builder and translates insufficient balance, lock duration, and model failures into user-facing async validation errors.
crates/rpc/rpc/src/async_tx_validator.rs|pub\(crate\) fn validate_two_phase_deadline|error_path|rpc,async-fsm,negative-path|Long-Running Two-Phase Trace|RPC two-phase deadline validation delegates deadline extraction and offset-vs-TTL checks to the shared async validation module instead of maintaining a separate deadline rule.
crates/ritual-async-fees/src/lib.rs|pub fn calculate_agent_fees_phase2_work|state_transition|fees,async-fsm,executor-selection|Sovereign Agent Precompile Trace;Product Economics Compatibility|Sovereign-agent Phase 2 pricing charges actual work through iterations and tool calls, with zero commitment and inclusion fees because Phase 1 already paid them.
crates/ritual-async-fees/src/lib.rs|pub fn calculate_image_fees_phase2|state_transition|fees,async-fsm,precompile|Multimodal Precompile Trace;Product Economics Compatibility|Image Phase 2 pricing uses model-specific per-pixel and minimum fees plus UX step multipliers, and returns executor fee only after Phase 1.
crates/ritual-async-fees/src/lib.rs|pub fn video_escrow_lockup|state_transition|fees,async-fsm,precompile|Multimodal Precompile Trace;Product Economics Compatibility|Video escrow pricing reserves worst-case max resolution and duration with model-specific pixel-second fees and step and FPS multipliers before long-running video work is admitted.
crates/ritual-scheduled-verification/src/lib.rs|C1|state_transition|scheduled,verifier,consensus-constant,negative-path|Scheduled Execution Trace|Scheduled transaction verification defines C1-C11 constraints, including existence, state, timing, system sender, target, funds, uniqueness, and predicate behavior as consensus checks.
crates/ritual-scheduled-verification/src/lib.rs|EXPECTED_SIGNATURE_R|consensus_constant|scheduled,encoding,verifier,consensus-constant|Scheduled Execution Trace|Scheduled transactions bypass normal signature verification only through the fixed dummy signature r=0, s=0, v=false expected by verifier logic.
crates/ritual-scheduled-verification/src/lib.rs|pub struct ScheduledCall|state_transition|scheduled,payload,verifier,encoding|Scheduled Execution Trace|Scheduler state hydration preserves target, caller, start block, num calls, frequency, gas, TTL, max fees, value, call data, and call id read from Scheduler contract storage.
crates/ritual-scheduled-verification/src/lib.rs|pub fn compute_max_block_number_u64|state_transition|scheduled,consensus-constant,negative-path|Scheduled Execution Trace|Scheduled execution timing computes expected block, per-execution TTL deadline, and overall expiry from start block, frequency, num calls, and TTL using saturating arithmetic.
crates/ritual-scheduled-verification/src/lib.rs|pub enum FilterResult|error_path|scheduled,payload,negative-path|Scheduled Execution Trace|Scheduled filtering separates permanent removal reasons from temporary retry reasons, keeping too-early, insufficient-funds, and predicate failures retryable while dropping invalid state, target, signature, and executed calls.
crates/ritual-spc-signature/src/lib.rs|pub fn is_spc_block_verified_precompile|consensus_constant|async-fsm,verifier,precompile,consensus-constant|Short-Running Async SPC Trace;Long-Running Two-Phase Trace|SPC verification membership delegates to the canonical address allowlist so RPC, builder, and verifier cannot drift on which async precompiles require SPC proof checking.
crates/ritual-spc-signature/src/lib.rs|pub fn construct_signature_payload|encoding_rule|encoding,verifier,async-fsm|Short-Running Async SPC Trace;Executor And Operator Surface Compatibility|SPC signature payload construction uses sorted compact JSON with hex strings without 0x prefixes for block number, tx hash, precompile address, input, output, previous block context, and error.
crates/ritual-spc-signature/src/lib.rs|pub fn normalize_recovery_id|error_path|verifier,negative-path,encoding|Short-Running Async SPC Trace|SPC signature verification accepts recovery ids 0/1 and Ethereum-style 27/28 only, rejecting malformed recovery IDs instead of normalizing arbitrary values.
crates/storage/codecs/src/alloy/transaction/async_settlement.rs|delivery_spc_calls|encoding_rule|encoding,async-fsm,storage|Long-Running Two-Phase Trace;Receipt And Client Surface Compatibility|Async settlement compact storage preserves both delivery SPC calls and settlement SPC calls while converting empty vectors back to None to keep RLP identity stable.
crates/storage/codecs/src/alloy/transaction/txtype.rs|Self::Passkey|encoding_rule|encoding,storage,consensus-constant|Scheduled Execution Trace;Short-Running Async SPC Trace;Passkey / P-256 Trace|Compact transaction type encoding preserves extended identifiers for scheduled, async commitment, async settlement, and passkey transactions instead of collapsing them into upstream Ethereum transaction types.
crates/storage/codecs/src/alloy/transaction/passkey.rs|pub\(crate\) struct TxPasskey|encoding_rule|encoding,storage,precompile|Passkey / P-256 Trace|Passkey compact storage preserves chain id, nonce, gas, fees, kind, value, access list, settlement transaction, optional SPC calls, and trailing input for P-256 and WebAuthn transactions.
crates/transaction-pool/src/pool/async_pool.rs|fn extract_max_poll_block_raw|state_transition|txpool,async-fsm,encoding,negative-path|Long-Running Two-Phase Trace|The async pool extracts resolved Phase 2 deadlines from precompile-specific ABI slots, including long HTTP, sovereign agent, FHE, persistent agent, and ZK layouts.
crates/transaction-pool/src/pool/async_pool.rs|pub enum AsyncState|state_transition|txpool,async-fsm|Short-Running Async SPC Trace;Long-Running Two-Phase Trace|The async pool state machine distinguishes AwaitingExecution, Fulfilled, AwaitingDelivery, and DeliveryReady so short async settlement and long-running Phase 2 delivery do not share an ambiguous state.
crates/transaction-pool/src/pool/async_pool.rs|pub struct AsyncTxMeta|state_transition|txpool,async-fsm,verifier,encoding|Long-Running Two-Phase Trace;Executor And Operator Surface Compatibility|Async pool metadata keeps the original tx, commitment tx, precompile address/input, state, execution result/proof, commit block, delivery result/proof, and ZK proof needed to bridge Phase 1 and Phase 2.
crates/ethereum/payload/src/lib.rs|enum WorkClass|state_transition|payload,async-fsm,scheduled,negative-path|Builder Obligation Compatibility;Scheduled Execution Trace|Payload building classifies heartbeat, obligations, async simulations, commitments, fulfilled async, delivery, sequencing rights, regular transactions, and diagnostics under one deadline and demotion policy.
crates/ethereum/payload/src/lib.rs|Phase 0b: Heartbeat checkAndRevive|state_transition|payload,scheduled,async-fsm|Persistent Agent Heartbeat And Revival Trace|Heartbeat revival runs as a payload-builder phase that hydrates tracker state from contract storage on cold start and only injects checkAndRevive work when expired agents exist.
crates/ethereum/payload/src/lib.rs|let scheduler = ritual_scheduling::SynchronousScheduler::instance|state_transition|payload,scheduled,consensus-constant|Scheduled Execution Trace|Payload building hydrates scheduled state from the synchronous scheduler or forced contract scan before computing obligations against parent state and the global build deadline.
crates/ethereum/payload/src/lib.rs|Collected async transactions at start of block building|state_transition|payload,async-fsm,txpool,negative-path|Short-Running Async SPC Trace;Builder Obligation Compatibility|Payload building collects async candidates at the start of block building and records collection stats, deadline fallback, scheduled candidate count, simulated count, accepted count, and skipped-due-to-deadline count.
crates/ethereum/payload/src/lib.rs|Phase B: Collect Fulfilled Async Transactions|state_transition|payload,async-fsm,negative-path|Short-Running Async SPC Trace;Builder Obligation Compatibility|Fulfilled async collection is skipped when the global deadline has passed and capped by RETH_MAX_FULFILLED_ASYNC_PER_BLOCK, allowing settlements to roll to later blocks instead of overrunning payload construction.
crates/ethereum/payload/src/lib.rs|Batch-read SPC verification data|state_transition|payload,async-fsm,verifier|Short-Running Async SPC Trace;Executor And Operator Surface Compatibility|Fulfilled async processing batch-reads SPC verification data before per-transaction processing and falls back to per-tx verification only if the batch read fails.
crates/ethereum/payload/src/lib.rs|collecting Phase 2 delivery transactions|state_transition|payload,async-fsm,verifier,negative-path|Long-Running Two-Phase Trace|Phase 2 delivery collection reads each delivery-ready job from AsyncJobTracker, defers jobs whose Phase 1 is not settled, and skips missing on-chain jobs instead of trusting pool state alone.
crates/ethereum/payload/src/lib.rs|Skipping Phase 2 delivery: pool precompile input hash|error_path|payload,async-fsm,verifier,negative-path|Long-Running Two-Phase Trace|Phase 2 delivery settlement checks pool metadata against contract state for precompile input hash, commit block, and precompile address before constructing a delivery transaction.
crates/ethereum/payload/src/lib.rs|CONSENSUS CRITICAL: Check Phase 2 settlement expiry|error_path|payload,async-fsm,consensus-constant,negative-path|Long-Running Two-Phase Trace|Phase 2 delivery expiry uses the contract expiry block, computed as max commit block plus TTL or Phase 2 deadline, so proposer-side inclusion cannot diverge from verifier-side contract checks.
crates/ethereum/payload/src/lib.rs|pub fn create_phase2_delivery_settlement|state_transition|payload,async-fsm,verifier,encoding|Long-Running Two-Phase Trace;zk_two_phase|Phase 2 delivery settlement construction verifies a delivery result exists, packs ZK result and proof together for ZK jobs, extracts the TEE address from the Phase 1 commitment, and creates the system settlement from contract job data.
crates/ethereum/payload/src/lib.rs|Agent/Sovereign Agent Phase 2 pricing|state_transition|payload,fees,async-fsm,precompile|Long-Running Two-Phase Trace;Product Economics Compatibility;Multimodal Precompile Trace|Phase 2 delivery pricing branches by precompile: sovereign agents charge work-based fees, media and FHE charge result-derived fees or DA-error fees, persistent agents charge spawn fees, and HTTP/ZK use block-based pricing.
crates/ethereum/payload/src/lib.rs|AsyncDelivery\.deliver|encoding_rule|payload,async-fsm,fees,encoding|Long-Running Two-Phase Trace|Phase 2 delivery settlement encodes an AsyncDelivery.deliver call and pays only the executor fee, with validator fees set to zero because Phase 1 already paid validators.
crates/ethereum/payload/src/lib.rs|Injected SPC calls into Passkey transaction|state_transition|payload,encoding,async-fsm|Passkey / P-256 Trace;Short-Running Async SPC Trace|Payload building injects SPC call data into passkey transactions when replaying fulfilled async outputs so passkey/P-256 transactions can carry the same settlement context as normal async transactions.
crates/ethereum/payload/src/lib.rs|Phase E: Tip-Maximizing Sort \+ Sequencing Rights|call_ordering|payload,executor-selection,negative-path|sequencing_rights_simple;Builder Obligation Compatibility|Payload sorting applies tip-maximizing ordering together with sequencing-rights policy and can demote sequencing-rights work when the build deadline is exceeded.
""".strip()
    candidates: list[dict] = []
    for row in table.splitlines():
        path, pattern, kind, tags, flows, claim = row.split("|", 5)
        candidates.append(
            {
                "source_path": path,
                "pattern": pattern,
                "source_kind": kind,
                "risk_tags": tags.split(","),
                "flow_titles": flows.split(";"),
                "semantic_claim": claim,
            }
        )
    return candidates


def main() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    index_by_path = load_index_by_path()
    file_records, removed = load_file_records()

    existing_claims = {
        atom.get("semantic_claim", "").strip().lower()
        for _, rec in file_records.values()
        for atom in rec.get("atoms", [])
    }
    seen_claims: set[str] = set()
    raw_rows = []
    curated_rows = []

    for idx, candidate in enumerate(parse_candidates(), start=1):
        source_path = candidate["source_path"]
        file_index = index_by_path[source_path]
        hunk_hint, snippet = source_snippet(source_path, candidate["pattern"])
        raw_id = f"flow-raw-grounded-{idx:04d}"
        raw = {
            "record_type": "flow_raw_atom",
            "raw_flow_id": raw_id,
            "source_path": source_path,
            "file_index": file_index,
            "flow_titles": candidate["flow_titles"],
            "source_kind": candidate["source_kind"],
            "semantic_claim": candidate["semantic_claim"],
            "source_hunk_hint": hunk_hint,
            "source_snippet": snippet,
            "risk_tags": candidate["risk_tags"],
            "high_risk": True,
            "grounding": "downstream_source",
            "notes": "Raw functionality-flow candidate generated by retracing the documented flow against downstream source/diff-owned files.",
        }
        norm = candidate["semantic_claim"].strip().lower()
        if norm in seen_claims or norm in existing_claims:
            raw["curation_decision"] = "covered_by_existing_atom"
            raw["curation_reason"] = "duplicate_semantic_claim"
        else:
            raw["curation_decision"] = "promote"
            raw["curation_reason"] = "source_grounded_behavior"
            seen_claims.add(norm)
            curated_rows.append(
                {
                    "record_type": "flow_derived_atom",
                    "functionality_flow_derived": True,
                    "functionality_flow_grounded": True,
                    "file_index": file_index,
                    "source_path": source_path,
                    "source_hunk_hint": hunk_hint,
                    "source_kind": candidate["source_kind"],
                    "source_snippet": snippet,
                    "semantic_claim": candidate["semantic_claim"],
                    "high_risk": True,
                    "risk_tags": candidate["risk_tags"],
                    "mapping_status": "missing",
                    "destinations": [],
                    "equivalence_argument": None,
                    "required_change": "Verify and restore this source-grounded functionality-flow invariant in the v2.2 port, or provide precise destination evidence and update the mapping.",
                    "test_strategy": "flow_equivalence_regression",
                    "negative_test_candidate": f"Replay the smallest {', '.join(candidate['flow_titles'])} scenario that exercises this source-owned behavior and fail if the v2.2 port omits or changes it.",
                    "adversarial_review": {"required": True, "status": "not_requested", "review_record_id": None},
                    "review_required": True,
                    "flow_titles": candidate["flow_titles"],
                    "source_flow_ids": [raw_id],
                    "notes": "Curated from functionality-flow-traces.md by retracing the flow against downstream source; source_snippet is from the downstream repo, not the markdown document.",
                }
            )
        raw_rows.append(raw)

    by_path = Counter()
    for atom in curated_rows:
        _, rec = file_records[atom["file_index"]]
        atoms = rec.setdefault("atoms", [])
        next_idx = max([a.get("atom_index", 0) for a in atoms] or [0]) + 1
        atom["atom_index"] = next_idx
        atom["record_id"] = f"file-{atom['file_index']:04d}-atom-{next_idx:04d}"
        atoms.append(atom)
        rec["atoms_total"] = len(atoms)
        for a in atoms:
            a["atoms_total"] = len(atoms)
        tags = set(rec.get("tags", []))
        tags.update(atom["risk_tags"])
        tags.update(["high-risk", "non-exact", "needs-review"])
        rec["tags"] = sorted(tags)
        by_path[atom["source_path"]] += 1

    for path, rec in file_records.values():
        path.write_text(json.dumps(rec, indent=2, sort_keys=False) + "\n")

    (AUDIT_DIR / "raw-flow-derived-atoms.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in raw_rows) + "\n"
    )
    (AUDIT_DIR / "curated-flow-derived-atoms.jsonl").write_text(
        "\n".join(json.dumps(r, sort_keys=True) for r in curated_rows) + "\n"
    )
    (AUDIT_DIR / "flow-curation-decisions.jsonl").write_text(
        "\n".join(
            json.dumps(
                {
                    "raw_flow_id": r["raw_flow_id"],
                    "source_path": r["source_path"],
                    "semantic_claim": r["semantic_claim"],
                    "decision": r["curation_decision"],
                    "reason": r["curation_reason"],
                    "grounding": r["grounding"],
                },
                sort_keys=True,
            )
            for r in raw_rows
        )
        + "\n"
    )

    reasons = Counter("promote" if r["curation_decision"] == "promote" else r["curation_reason"] for r in raw_rows)
    report = [
        "# Functionality-Flow Atom Curation Report",
        "",
        "- Method: retraced documented flows against downstream source files; markdown sections were used only as flow labels.",
        f"- Existing functionality-flow atoms replaced: {removed}",
        f"- Raw grounded candidates: {len(raw_rows)}",
        f"- Promoted raw rows: {len(curated_rows)}",
        f"- Curated grouped atoms: {len(curated_rows)}",
        f"- Inserted atoms: {len(curated_rows)}",
        "",
        "## Dropped Or Covered By Reason",
    ]
    report.extend(f"- `{k}`: {v}" for k, v in sorted(reasons.items()))
    report.extend(["", "## Inserted By Source Path"])
    report.extend(f"- `{path}`: {count}" for path, count in by_path.most_common())
    report.extend(
        [
            "",
            "## Grounding Rule",
            "Every promoted atom includes a `source_snippet` read from `/home/ritual/repos/ritual-reth-internal` at the owning downstream `source_path`; no promoted atom uses the markdown body as its evidence snippet.",
        ]
    )
    (AUDIT_DIR / "curation-report.md").write_text("\n".join(report) + "\n")

    queue_additions = ["# Functionality-Flow Review Queue Additions", ""]
    for atom in curated_rows:
        queue_additions.extend(
            [
                f"### File {atom['file_index']:04d}: {atom['source_path']}",
                "",
                f"- Source: `{atom['source_hunk_hint']}`",
                f"- Claim: {atom['semantic_claim']}",
                f"- Flow labels: {', '.join('`' + x + '`' for x in atom['flow_titles'])}",
                f"- Negative test: {atom['negative_test_candidate']}",
                "",
            ]
        )
    (AUDIT_DIR / "review-queue-additions.md").write_text("\n".join(queue_additions))

    index_lines = []
    review_atoms = []
    for file_index in sorted(file_records):
        _, rec = file_records[file_index]
        index_lines.append(
            json.dumps(
                {
                    "record_type": "index_entry",
                    "file_index": rec.get("file_index"),
                    "source_status": rec.get("source_status"),
                    "source_path": rec.get("source_path"),
                    "source_old_path": rec.get("source_old_path"),
                    "file_classification": rec.get("file_classification"),
                    "file_status": rec.get("file_status"),
                    "atoms_total": rec.get("atoms_total", len(rec.get("atoms", []))),
                    "tags": rec.get("tags", []),
                },
                sort_keys=True,
            )
        )
        for atom in rec.get("atoms", []):
            if atom.get("review_required") or atom.get("mapping_status") in {"missing", "blocked"}:
                review_atoms.append((file_index, rec.get("source_path"), atom))
    (COVERAGE / "index.jsonl").write_text("\n".join(index_lines) + "\n")

    queue = [
        "# Coverage Map Review Queue",
        "",
        f"Generated after grounded functionality-flow insertion. Total queued atoms: {len(review_atoms)}",
        "",
    ]
    for file_index, source_path, atom in review_atoms:
        queue.extend(
            [
                f"### File {file_index:04d}: {source_path}",
                "",
                f"- Key: `file_index={file_index}`, `source_path={source_path}`, `record_id={atom.get('record_id')}`",
                f"  - Source hunk: `{atom.get('source_hunk_hint')}`",
                f"  - Mapping status: `{atom.get('mapping_status')}`",
                f"  - Required change: {atom.get('required_change', atom.get('semantic_claim'))}",
                f"  - Negative test: {atom.get('negative_test_candidate')}",
                "",
            ]
        )
    (COVERAGE / "review-queue.md").write_text("\n".join(queue))

    all_recs = [rec for _, rec in file_records.values()]
    all_atoms = [atom for rec in all_recs for atom in rec.get("atoms", [])]
    flow_atoms = [atom for atom in all_atoms if atom.get("functionality_flow_derived")]
    errors = []
    if len(all_recs) != 579:
        errors.append(f"expected 579 file artifacts, found {len(all_recs)}")
    if sorted(rec.get("file_index") for rec in all_recs) != list(range(1, 580)):
        errors.append("file indices are not exactly 1..579")
    if sum(rec.get("atoms_total", 0) for rec in all_recs) != len(all_atoms):
        errors.append("embedded atom counts do not match atoms_total")
    if any(atom.get("functionality_flow_derived") and not atom.get("functionality_flow_grounded") for atom in all_atoms):
        errors.append("functionality flow atom without grounding flag")
    if any(
        atom.get("functionality_flow_derived")
        and "functionality-flow-traces.md section" in str(atom.get("source_hunk_hint", ""))
        for atom in all_atoms
    ):
        errors.append("functionality flow atom still grounded only in markdown section")

    old_summary = {}
    summary_path = COVERAGE / "validation-summary.json"
    if summary_path.exists():
        old_summary = json.loads(summary_path.read_text())
    summary = {
        "generated_at": datetime.now(timezone(timedelta(hours=-4))).isoformat(timespec="seconds"),
        "total_files": len(all_recs),
        "counts_by_file_classification": dict(Counter(rec.get("file_classification", "unknown") for rec in all_recs)),
        "counts_by_file_status": dict(Counter(rec.get("file_status", "unknown") for rec in all_recs)),
        "counts_by_atom_mapping_status": dict(Counter(atom.get("mapping_status", "unknown") for atom in all_atoms)),
        "atoms_total": len(all_atoms),
        "high_risk_atoms_total": sum(1 for atom in all_atoms if atom.get("high_risk")),
        "non_exact_atoms_total": sum(1 for atom in all_atoms if atom.get("mapping_status") != "exact"),
        "adversarial_review_status": dict(Counter(atom.get("adversarial_review", {}).get("status", "unknown") for atom in all_atoms)),
        "human_review_queue_total": len(review_atoms),
    }
    for key in ["curated_test_atom_insertion", "curated_feature_atom_insertion"]:
        if key in old_summary:
            summary[key] = old_summary[key]
    if summary["counts_by_file_status"] == {"unknown": 579} and "counts_by_file_status" in old_summary:
        summary["counts_by_file_status"] = old_summary["counts_by_file_status"]
    summary["curated_functionality_flow_atom_insertion"] = {
        "method": "grounded_downstream_source_retrace",
        "existing_functionality_flow_atoms_replaced": removed,
        "raw_flow_candidates": len(raw_rows),
        "promoted_raw_rows": len(curated_rows),
        "curated_grouped_atoms": len(curated_rows),
        "inserted_atoms": len(curated_rows),
        "dropped_by_reason": dict(reasons),
        "curated_artifacts": [
            "coverage-map/functionality-flow-audit/raw-flow-derived-atoms.jsonl",
            "coverage-map/functionality-flow-audit/curated-flow-derived-atoms.jsonl",
            "coverage-map/functionality-flow-audit/flow-curation-decisions.jsonl",
        ],
    }
    summary["validation_checks"] = {
        "exactly_579_file_artifacts_exist": len(all_recs) == 579,
        "all_expected_file_indices_exist": sorted(rec.get("file_index") for rec in all_recs) == list(range(1, 580)),
        "embedded_atom_counts_match_atoms_total": sum(rec.get("atoms_total", 0) for rec in all_recs) == len(all_atoms),
        "mapped_atoms_have_destination_evidence": all(
            (atom.get("mapping_status") not in {"exact", "renamed_exact", "covered_by_upstream", "moved_to_dependency", "structural_equivalent"})
            or atom.get("destinations")
            for atom in all_atoms
        ),
        "new_functionality_atoms_queued": all(atom.get("review_required") for atom in flow_atoms),
        "functionality_flow_atoms_are_source_grounded": not any(
            atom.get("functionality_flow_derived")
            and "functionality-flow-traces.md section" in str(atom.get("source_hunk_hint", ""))
            for atom in all_atoms
        ),
    }
    summary["validation_errors"] = errors
    summary["notes"] = "Replaced prior markdown-led functionality-flow atoms with source-grounded flow atoms after retracing documented flows against downstream source files."
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=False) + "\n")

    print(
        json.dumps(
            {
                "removed_prior_flow_atoms": removed,
                "raw_grounded_candidates": len(raw_rows),
                "curated_inserted": len(curated_rows),
                "atoms_total": len(all_atoms),
                "flow_atoms_total": len(flow_atoms),
                "review_queue_total": len(review_atoms),
                "validation_errors": errors,
                "top_paths": by_path.most_common(8),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
