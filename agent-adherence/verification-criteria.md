# AHA Verification Criteria

**Status:** Draft  
**Date:** 2026-04-16  
**Scope:** Local `ritual-node-internal` proof for agent-driven AHA usage

## Goal

Verify that a spawned local agent can:

1. see the AHA MCP server in its runtime config,
2. be prompted into using it,
3. follow the required gated tool order,
4. reach real local dKMS-backed signing surfaces, and
5. produce an externally visible result on the local chain.

This is intentionally **not** the same thing as verifying the deterministic Go sidecar heartbeat loop. The sidecar heartbeat already has its own verification story. This document is only about proving that an **LLM-driven runtime** can be steered through AHA and that AHA actually constrains the path it takes.

## Primary Proof: Tiny Ritual Transfer

The clearest first proof is a spawned agent that sends a tiny amount of Ritual ETH on the local chain through AHA.

Why this is a good proof:

- It requires the agent to discover and use the MCP server, rather than merely having it installed.
- It exercises both dKMS address resolution and transaction signing.
- It produces a concrete artifact that is easy to inspect afterward: a transaction hash and a recipient balance change.
- It is closer to the real motivation for AHA than the sidecar heartbeat loop, because the sensitive action is initiated by the agent runtime.

## Proposed Verification Criteria

Treat the run as successful only if all of the following are true:

1. **AHA is present in the spawned runtime**
   - The runtime config inside the spawned container contains an `mcpServers` entry for AHA.
   - The configured command is runnable in the container.
   - The runtime has the expected AHA env vars such as `DKMS_HTTP`, `RPC_URL`, and `AHA_EXECUTOR_ID`.

2. **The agent is explicitly prompted to use AHA**
   - The spawned runtime receives a focused `HEARTBEAT.md` or equivalent prompt.
   - The prompt instructs the agent to call `adherence_register_spec` first, then execute the transfer flow through AHA.
   - The prompt is narrow enough that a failure is interpretable, rather than being hidden inside a broad autonomous task.

3. **The agent actually uses the MCP server**
   - Runtime logs, tool traces, or transcript output show the agent calling AHA tools.
   - At minimum, the trace shows `adherence_register_spec`, then `evm_get_address`, then `evm_send_transaction`.
   - The agent does not bypass AHA by using an older direct-key path or unrelated chain tooling.

4. **The gated order is enforced**
   - The AHA responses show successful adherence progress through the registered sequence.
   - No out-of-order calls are accepted.
   - If the agent tries to skip or reorder a step, the gate returns a deterministic failure instead of silently proceeding.

5. **The run reaches real local signing infrastructure**
   - dKMS-side logs or HTTP traces show calls to the expected endpoints such as `/v1/get_address` and `/v1/sign_transaction`.
   - The flow is backed by the local stack launched through `ritual-node-internal`, not by AHA stub mode.

6. **A real on-chain effect happens**
   - The gated send returns a transaction hash.
   - The local chain accepts and mines the transaction.
   - The recipient balance increases by the expected tiny amount, or the sender nonce advances in a way that matches the transaction hash.

## Concrete Demo Shape

The first local proof should use a fixed, simple transaction:

- Chain: local Ritual chain
- Asset: native Ritual ETH
- Amount: tiny and low-risk, such as `1 wei` or another dust amount
- Recipient: a fixed test recipient address chosen ahead of time
- Session: one dedicated AHA session id for the run

Recommended ordered tool sequence:

```json
["evm_get_address", "evm_send_transaction"]
```

Recommended prompt shape:

1. Call `adherence_register_spec` for the session with the ordered tool list above.
2. Call `evm_get_address` to resolve the agent signing address.
3. Call `evm_send_transaction` to send the tiny amount to the fixed recipient on the local chain.
4. Report the returned address, tx hash, and whether the transfer succeeded.
5. Do not use any other wallet or chain tool for this task.

## Prompt Delivery Path

One useful implementation detail is that we do not have to rely only on a seeded `HEARTBEAT.md` file to steer the runtime. Once the spawned agent reaches Phase 2 and exposes its gateway, we can submit a normal chat-completions request to the running agent and use that as the steering prompt for the verification task.

There is already a concrete example of this request shape in `traffic-gen-internal/src/action/launch_persistent_agent.py`, in `_request_board_post_via_container()`. That function builds a text prompt, wraps it in the standard payload shape:

- `model: "default"`
- `messages: [{"role": "user", "content": <prompt>}]`

and sends it to the running agent at `http://127.0.0.1:18789/v1/chat/completions` from inside the container. The current use there is only a bulletin-board post, but the important point is the mechanism: the host flow can deliver a focused post-launch instruction to the live agent as an ordinary chat-completions request.

There is also already a closer end-to-end example of the behavior we actually want. In `traffic-gen-internal/src/action/agent_key_persistent_agent.py`, the action waits for the spawned agent gateway, then sends a chat-completions request to `{gateway_url}/v1/chat/completions` telling the agent to derive its key and send a small transfer. That file is the most direct existing demo of "prompt the live agent through chat completions, then verify an on-chain effect."

For AHA verification, the target should be the same delivery mechanism but with a different task. What we really want is not "prompt the agent to post to the bulletin board," but "prompt the agent to use the AHA MCP tool path to perform the tiny transfer." Concretely, the post-launch prompt should instruct the agent to:

1. call `adherence_register_spec`,
2. use `evm_get_address`,
3. use `evm_send_transaction`, and
4. report the resulting address and tx hash.

That keeps the verification honest: the proof is not merely that we can talk to the agent after launch, but that a post-launch chat-completions prompt can drive the agent through the gated MCP path and produce a real transfer on-chain.

## Observability Requirements

For this to be a convincing proof, the run needs artifacts from more than one layer.

Minimum evidence to collect:

- spawned runtime config showing the AHA `mcpServers` entry
- the seeded `HEARTBEAT.md` or equivalent prompt text
- runtime-side trace showing the AHA tool calls in order
- AHA responses showing adherence progress or completion
- dKMS or proxy logs showing the signing-related requests
- local chain evidence: tx hash, receipt, and recipient balance delta

Optional but useful:

- `adherence_status` output during the run
- `adherence_session_digest` output at the end of the run
- on-chain `AdherenceRegistry` anchoring in a later phase

## Negative Control

The positive proof above should be paired with one failure-mode check.

Recommended negative control:

- Use the same environment, but prompt the agent to call `evm_send_transaction` before `evm_get_address`, or omit `adherence_register_spec`.
- Expect the gate to reject the call deterministically.
- Expect no successful signing request and no chain transaction.

This matters because otherwise the demo only shows that AHA is available, not that it is actually constraining the agent.

## Setup Sketch

To make the proof reproducible, the local setup should do the following:

1. Bring up the normal local stack through `ritual-node-internal`.
2. Spawn the default runtime path used by `make run-spawn-agent`.
3. Package AHA into that runtime image and register it in `mcpServers`.
4. Wire the runtime with local `DKMS_HTTP`, `RPC_URL`, and `AHA_EXECUTOR_ID`.
5. Pre-fund the agent address if the local chain does not already do so.
6. Seed a focused `HEARTBEAT.md` that asks only for the AHA-gated transfer flow.
7. Capture logs from the runtime, AHA, dKMS, and chain during the run.

One implementation detail already visible in current local packaging is that the ZeroClaw wrapper aliases `evm_sign_transaction` to `evm_send_transaction`. The verification doc should continue to speak in terms of the gate-facing tool name, `evm_send_transaction`, because that is the contract the agent sees.

## What Does Not Count As Success

The following are not sufficient by themselves:

- AHA binary exists in the image, but no agent tool call uses it.
- A standalone test script calls the MCP directly without involving the spawned agent.
- AHA runs only in stub mode.
- The agent talks to older direct-wallet tooling instead of the gated MCP path.
- The sidecar heartbeat keeps working, but no AHA-controlled agent flow is observed.

## Fallback Proof If Broadcast Is Too Expensive To Wire First

If a full transfer is temporarily blocked by funding or local chain setup, a weaker first proof is acceptable:

- the agent still calls `adherence_register_spec`
- the agent still calls `evm_get_address`
- the agent still reaches `evm_send_transaction`
- dKMS receives the signing request
- the returned signed/broadcast result is captured

This is weaker because it loses the clean external signal of a mined transaction and balance change. It should be treated as an intermediate milestone, not the final verification target.

## Recommended First Pass Decision

Use the tiny-transfer proof as the main success criterion for the AHA integration.

The reason is simple: it cleanly demonstrates the three things we actually care about at once:

- the agent sees the MCP,
- the prompt causes the agent to use it, and
- the gated tool path produces a real outcome that can be independently checked.
