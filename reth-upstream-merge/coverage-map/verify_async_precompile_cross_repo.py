#!/usr/bin/env python3
"""
Static cross-repo contract: each Ritual async/SPC precompile address must match
`ALL_ASYNC_PRECOMPILE_METADATA.capability_tag` in ritual-precompile-addresses,
the numeric TEE registry `Capability` u8 (via AsyncPrecompileCapabilityTag repr),
executor selection in traffic-gen, and localnet CAPABILITIES wiring in
ritual-node-internal configgen.

Run from repo root `sjs-agent-sessions/reth-upstream-merge`:
  python3 coverage-map/verify_async_precompile_cross_repo.py

Exit 0 if all checks pass; non-zero on mismatch. This is machine-checkable proof
that does not require live traffic.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RETH_LIB = (
    Path("/home/ritual/repos/ritual-reth-internal-v2.2.0-port")
    / "crates/ritual-precompile-addresses/src/lib.rs"
)
TRAFFIC_ROOT = Path("/home/ritual/repos/traffic-gen-internal")
NODE_DOCKER = Path("/home/ritual/repos/ritual-node-internal/configgen/docker.py")

TAG_U8 = {
    "HttpCall": 0,
    "Llm": 1,
    "ZkCall": 5,
    "ImageCall": 7,
    "AudioCall": 8,
    "VideoCall": 9,
    "Fhe": 10,
    "AutonomousAgent": 11,
}

# Python executor selection string as emitted in traffic-gen.
CAP_PY_BY_TAG = {
    "HttpCall": "Capability.HTTP_CALL",
    "Llm": "Capability.LLM",
    "ZkCall": "Capability.ZK_CALL",
    "ImageCall": "Capability.IMAGE_CALL",
    "AudioCall": "Capability.AUDIO_CALL",
    "VideoCall": "Capability.VIDEO_CALL",
    "Fhe": "Capability.FHE",
}

DOCKER_SUBSTR_BY_TAG = {
    "HttpCall": "Capability.HTTP_CALL",
    "Llm": "Capability.LLM",
    "ZkCall": "Capability.ZK_CALL",
    "ImageCall": "Capability.IMAGE_CALL",
    "AudioCall": "Capability.AUDIO_CALL",
    "VideoCall": "Capability.VIDEO_CALL",
    "Fhe": "Capability.FHE",
}

CONST_SUFFIX = {
    "HTTP_CALL_PRECOMPILE": "0801",
    "LLM_CALL_PRECOMPILE": "0802",
    "LONG_RUNNING_HTTP_PRECOMPILE": "0805",
    "ZK_TWO_PHASE_PRECOMPILE": "0806",
    "FHE_PRECOMPILE": "0807",
    "IMAGE_CALL_PRECOMPILE": "0818",
    "AUDIO_CALL_PRECOMPILE": "0819",
    "VIDEO_CALL_PRECOMPILE": "081a",
    "DKMS_KEY_PRECOMPILE": "081b",
    "SOVEREIGN_AGENT_PRECOMPILE": "080c",
    "PERSISTENT_AGENT_PRECOMPILE": "0820",
}

# Per-address proof surfaces (traffic-gen + docker substring for that family).
CONTRACT_ROWS: list[dict] = [
    {
        "suffix": "0801",
        "tag": "HttpCall",
        "traffic_files": ["src/action/x402_http_call.py", "src/action/private_io.py"],
    },
    {"suffix": "0802", "tag": "Llm", "traffic_files": ["src/action/llm_call.py"]},
    {
        "suffix": "0805",
        "tag": "HttpCall",
        "traffic_files": ["src/action/long_running_echo.py", "src/action/x402_long_running_echo.py"],
    },
    {
        "suffix": "0806",
        "tag": "ZkCall",
        "traffic_files": ["src/action/zk_two_phase.py", "src/action/scheduled_zk_two_phase.py"],
    },
    {"suffix": "0807", "tag": "Fhe", "traffic_files": ["src/action/fhe_inference.py"]},
    {"suffix": "0818", "tag": "ImageCall", "traffic_files": ["src/action/image_call.py"]},
    {"suffix": "0819", "tag": "AudioCall", "traffic_files": ["src/action/audio_call.py"]},
    {"suffix": "081a", "tag": "VideoCall", "traffic_files": ["src/action/video_call.py"]},
    {
        "suffix": "081b",
        "tag": "HttpCall",
        "traffic_files": ["tests/test_dkms_key_precompile_e2e.py", "src/action/x402_dkms_http_call.py"],
    },
    {
        "suffix": "080c",
        "tag": "HttpCall",
        "traffic_files": ["src/action/launch_sovereign_agent.py", "src/action/sovereign_agent.py"],
    },
    {
        "suffix": "0820",
        "tag": "HttpCall",
        "traffic_files": ["src/action/launch_persistent_agent.py", "src/action/spawn_agent.py"],
    },
]


def parse_reth_metadata(lib: str) -> dict[str, str]:
    out: dict[str, str] = {}
    pat = re.compile(
        r"AsyncPrecompileMetadata\s*\{\s*address:\s*(\w+),"
        r".*?capability_tag:\s*AsyncPrecompileCapabilityTag::(\w+),",
        re.DOTALL,
    )
    for addr_const, tag in pat.findall(lib):
        suf = CONST_SUFFIX.get(addr_const)
        if suf:
            out[suf] = tag
    return out


def main() -> int:
    errors: list[str] = []
    if not RETH_LIB.is_file():
        errors.append(f"missing Reth lib {RETH_LIB}")
        print("verify_async_precompile_cross_repo: FAIL", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        return 1

    lib_text = RETH_LIB.read_text(encoding="utf-8")
    reth_meta = parse_reth_metadata(lib_text)
    expected_addrs = {r["suffix"] for r in CONTRACT_ROWS}
    if set(reth_meta.keys()) != expected_addrs:
        errors.append(
            f"Reth metadata address set mismatch: got {sorted(reth_meta.keys())} want {sorted(expected_addrs)}"
        )

    docker_text = NODE_DOCKER.read_text(encoding="utf-8") if NODE_DOCKER.is_file() else ""

    for row in CONTRACT_ROWS:
        suf = row["suffix"]
        tag = row["tag"]
        if reth_meta.get(suf) != tag:
            errors.append(f"0x{suf}: Reth metadata tag {reth_meta.get(suf)!r} != expected {tag!r}")

        if tag not in TAG_U8:
            errors.append(f"0x{suf}: unknown capability tag {tag!r} (add TAG_U8)")

        cap_needle = CAP_PY_BY_TAG[tag]
        for rel in row["traffic_files"]:
            p = TRAFFIC_ROOT / rel
            if not p.is_file():
                errors.append(f"missing traffic file {p}")
                continue
            body = p.read_text(encoding="utf-8")
            if cap_needle not in body:
                errors.append(f"{p}: expected `{cap_needle}` for 0x{suf} / {tag}")

        dneedle = DOCKER_SUBSTR_BY_TAG.get(tag)
        if dneedle and dneedle not in docker_text:
            errors.append(f"0x{suf}: {NODE_DOCKER} missing `{dneedle}` for localnet executors")

    if errors:
        print("verify_async_precompile_cross_repo: FAIL", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print(f"verify_async_precompile_cross_repo: OK ({len(CONTRACT_ROWS)} precompiles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
