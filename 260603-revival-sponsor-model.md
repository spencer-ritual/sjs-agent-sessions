# Revival Sponsor Model

## Updated Context

If `PrecompileConsumer` is the contract creating the persistent agent, then
`PrecompileConsumer` owning that spawned agent is correct. The bug is not that
`PrecompileConsumer` appears in the ownership path.

The problem is that Reth currently uses `AgentHeartbeat.owner` as the revival
payment sponsor. When `AgentHeartbeat.owner == PrecompileConsumer`, the revival
commitment tries to reserve from:

```text
reserveFrom(PrecompileConsumer, AgentHeartbeat, ...)
```

That fails because `PrecompileConsumer` has not approved `AgentHeartbeat` as a
`RitualWallet` spender.

## Proposed Fast Path

Use the heartbeat `agentAddress` itself as the revival payment sponsor.

The agent address is already recorded in `AgentHeartbeat`:

```solidity
AgentRecord {
    address owner;
    address agentAddress;
    ...
}
```

Registrations are keyed by `msg.sender`, and the contract stores:

```solidity
agentAddress: msg.sender
```

So Reth can use `AgentRecord.agentAddress` as the sponsor for the revival
precompile input instead of using `AgentRecord.owner`.

## Why This Works

The automatic revival async caller is `AgentHeartbeat`. The wallet rule is:

```solidity
reserveFrom(sponsor, caller, ...)
```

If `sponsor != caller`, then `sponsor` must approve `caller`.

With the proposed model:

```text
sponsor = agentAddress
caller  = AgentHeartbeat
```

The spawned agent already has access to the DKMS-derived key for `agentAddress`
because it registers and heartbeats on-chain as that address. During registration
or startup, the agent can also approve:

```text
RitualWallet.approve(AgentHeartbeat, maxAllowance)
```

from `agentAddress`.

Then revival can reserve from:

```text
reserveFrom(agentAddress, AgentHeartbeat, ...)
```

without requiring `PrecompileConsumer` to sign an approval.

## Required Funding

Approving is not enough by itself. `agentAddress` also needs available
`RitualWallet` balance.

For a local traffic-gen test, the EOA can fund the agent wallet with:

```text
RitualWallet.depositFor(agentAddress)
```

Then the agent, using its own DKMS-derived key, approves `AgentHeartbeat`.

## Resulting Roles

This keeps the roles separate:

- `PrecompileConsumer`: app/contract owner of the spawned agent.
- `agentAddress`: on-chain heartbeat namespace and revival payment sponsor.
- `AgentHeartbeat`: automatic revival caller, approved by `agentAddress`.
- EOA traffic user: can fund `agentAddress` with `depositFor`, but does not need
  to be the recorded heartbeat owner.

## Minimal Implementation Shape

1. Leave `PrecompileConsumer` ownership semantics intact.
2. Change Reth revival input construction to use the recorded `agentAddress` as
   the persistent-agent sponsor.
3. Add an agent startup/registration step that approves `AgentHeartbeat` from the
   `agentAddress` `RitualWallet`.
4. In the local revival test, ensure `agentAddress` has `RitualWallet` balance
   before killing the holder-A container.
