# Ritual Reputation NFT — POC Plan

## Context for a Fresh Session

Spencer wants to build a POC dApp on **Ritual Chain (chain ID 1979)** using the skills bundle at:

```
/home/ritual/repos/.cursor/skills/ritual-dapp-skills/
```

That repo (`ritual-foundation/ritual-dapp-skills`) is the canonical, up-to-date set of skills + agents (`ritual-dapp-builder`, `ritual-dapp-debugger`) for building Ritual dApps. It maps user goals to specific precompile addresses and produces an end-to-end build (contracts → frontend → backend → tests → deploy). When resuming, the entry point for the agent is:

```
Read the file /home/ritual/repos/.cursor/skills/ritual-dapp-skills/skills/ritual/SKILL.md
and follow its instructions.

WALLET: 0x<funded_wallet>

<paste the "POC Spec" section from this doc as the build prompt>
```

---

## The Idea

A reputation layer where you describe who you are in a free-form prompt — your name, anything you want the agent to know, optional handles, links, claims to fame — and an on-chain agent goes and does real, open-ended research about you on the open internet (Google, Wikipedia, whatever surfaces). You get an NFT with three reputation scores: **crypto, academia, pop culture**.

---

## Why This Is Ritual-Native

Reputation oracles on other chains are basically "an oracle that checks one website." This is fundamentally different: the on-chain agent does **complex, multi-step research** — plan queries, fetch many sources, read them, weigh them, write down citations, score against a rubric — and the *entire* reasoning loop runs inside the contract, inside a TEE. No off-chain server, no trusted operator. The score is signed by the chain. That kind of "agentic oracle" only works on Ritual.

---

## POC Scope (the smallest thing that demonstrates the idea)

One direct sovereign-agent flow, one screen, one NFT.

1. **Sovereign Agent** (`0x080C`) — this is the only contract-facing async primitive in v1. The contract launches one sovereign-agent job and handles the callback.
2. **HTTP / Long-running HTTP** (`0x0801` / `0x0805`) — the agent can use these internally to fetch search results and source pages.
3. **No separate standalone LLM contract flow in v1** — scoring stays inside the sovereign agent rather than being modeled as a separate contract-level `0x0802` pipeline.

That's the whole feature list. Everything else is in the "Possible Improvements" section below.

### Output
**One ERC-721 NFT per wallet**, with rescans updating the same token in place, with three score traits:
- `crypto` (0–100)
- `academia` (0–100)
- `popCulture` (0–100)

Plus a small on-chain evidence array (citation URLs + short quotes) so the score is auditable. The exact evidence footprint should be chosen during implementation with a strong bias toward the fastest credible POC.

---

## Architecture (kept deliberately tiny)

### Contracts (Solidity, deployed to chain 1979)

| Contract | Responsibility |
|---|---|
| `ReputationNFT.sol` | ERC-721. Holds `mapping(tokenId => Reputation { uint8 crypto; uint8 academia; uint8 popCulture; Citation[] evidence })` plus wallet-to-token tracking so each wallet has one token. Exposes `requestScan(string prompt)` — the prompt is the user's free-form self-description — which launches the Sovereign Agent in direct mode, with a callback that mints on first scan and updates in place on rescan. |

That's it. One contract. Direct single-contract caller mode, not factory-backed harnesses, for the POC.

### Agent Flow (Sovereign Agent loop)

```
1. Read the user's free-form self-description prompt from requestScan
2. Inside the sovereign-agent run: extract candidate identifiers from the prompt
   (name, handles, affiliations, claims, distinctive phrases) and plan a search strategy
3. For each dimension {crypto, academia, pop_culture}:
   a. Build open-ended search queries from the prompt + the extracted
      identifiers + the dimension rubric
      (e.g., "<name> ethereum", "<name> wikipedia", "<name> site:scholar.google.com",
       "<handle> github", whatever the agent decides is worth checking)
   b. Use whatever search/fetch path gets to a working POC fastest
      (single search API, direct source fetches, or both)
   c. (Long) HTTP: run searches, follow promising links
      (Wikipedia entries, profile pages, papers, news, etc. — agent's choice)
   d. Score 0-100 + return a minimal evidence bundle with the sources it actually used
4. Return {scores, citations} via callback
5. ReputationNFT.mintOrUpdate(user, scores, citations)
```

The point: the agent is **not** restricted to a fixed set of handles. It plans its own queries from the user's prompt and follows whatever's useful — Wikipedia, scholar profiles, news, GitHub, X, personal sites. That open-endedness is the "complex agentic oracle" part of the demo.

### Frontend (Next.js + wagmi)

One page:
- Input: a single free-form textarea — "Tell us about yourself: name, what you do, anything you want the agent to know. Handles, links, claims to fame all welcome but not required."
- Placeholder example: *"I'm Jane Doe, a Solidity researcher at Ritual Foundation. I post as @janedoe on X, github.com/janedoe, and I co-authored the EIP-1234 spec."*
- Button: **Scan me**
- Live progress UI for the 9-state async machine (per `ritual-dapp-frontend` skill): planning → searching → reading → scoring → minting
- Result: NFT card with 3 score bars + a list of citation links

### Backend
Default to **no backend** for v1. Add a minimal `AsyncJobTracker` watcher per `ritual-dapp-backend` skill only if frontend polling proves too painful for the progress UI.

### File Layout

```
ritual-rep/
├── contracts/
│   ├── src/ReputationNFT.sol
│   ├── script/Deploy.s.sol
│   └── test/ReputationNFT.t.sol      // vm.mockCall for precompiles
├── frontend/
│   ├── app/page.tsx                  // the one screen
│   ├── components/
│   │   ├── ScanForm.tsx
│   │   ├── ScanProgress.tsx          // 9-state machine
│   │   └── ReputationCard.tsx
│   └── lib/spcCalls.ts
└── README.md
```

---

## User Journey

1. Open the dApp, connect wallet.
2. Write a short prompt about yourself — name, what you do, optional handles/links/claims to fame, anything that helps the agent find you.
3. Click **Scan me** → one tx that launches the on-chain Sovereign Agent.
4. Progress UI streams: planning → searching → reading → scoring → minting.
5. NFT shows up on first scan, or updates in place on rescan: 3 scores + citations the agent actually used.

---

## Possible Improvements (cool ideas, out of scope for this POC)

These are intentionally deferred. Each is a clean, additive layer on top of the POC — none require rewriting the core.

1. **On-chain image generation for NFT artwork** — `0x0818`. Generative crest where visual elements scale with the three scores (circuit motifs for crypto, laurel/ink for academia, neon for pop culture). Big visual demo wow factor.
2. **Social-account ownership proofs (challenge-string)** — to stop people from claiming to be Vitalik, the agent issues a per-scan random challenge string and asks the user to post it from each account they claim (e.g., a tweet from @claimedhandle, a public GitHub gist, a TXT record on a personal site). The agent then fetches via HTTP and verifies the string is there. Lightweight, no extra precompile needed — just uses the HTTP precompile already in the POC.
3. **Cross-chain key binding** — `0x0009` (Ed25519). For users claiming a non-EVM address (e.g., Solana), verify a real cryptographic signature on-chain instead of a web2 challenge. Converts "I claim to control 0xSol..." into "I cryptographically control 0xSol..."
4. **Persistent Agent + Scheduler — auto-refreshing reputation** — `0x0820` + Scheduler system contract. Each user gets a persistent agent that remembers prior scans, and the Scheduler triggers incremental rescans every (e.g.) 30 days. Reputation decays without refresh and updates itself in the background. This is the version that feels alive.
5. **Secrets (ECIES + ACL) for private-data scans** — user supplies LinkedIn/Twitter OAuth tokens encrypted to the TEE pubkey; agent reads gated content (DM count, follower quality, private repos) without anyone seeing the keys.
6. **Soulbound (ERC-5192)** — make the NFT non-transferable so reputation can't be sold.

---

## Open Questions (resolve during build)

Search source, exact evidence footprint, and final model/config selection should be decided during implementation with a strong bias toward the fastest credible POC rather than maximum completeness.

1. **Rubric.** Hardcode in `ReputationNFT.sol` constructor for v1.
2. **Sybil.** For the POC, anyone can claim to be whoever they want — no identity verification at all. Reputations should be labeled as "self-claimed" in the UI so this is honest. Improvements #2 (challenge-string proofs) and #3 (cross-chain key binding) are how this gets fixed later.
3. **Scan cost.** Estimate via `ritual-dapp-wallet` skill and show required `RitualWallet` deposit before scan.

---

## How to Resume in a Fresh Session

Paste this verbatim into a new Cursor / Claude Code session:

> Read the file `/home/ritual/repos/.cursor/skills/ritual-dapp-skills/skills/ritual/SKILL.md` and follow its instructions.
>
> WALLET: 0x<funded_wallet>
>
> Build me the POC described in `/home/ritual/repos/sjs-agent-sessions/ritual-reputation-nft-poc.md`. Use the "POC Scope" section as the authoritative feature list. Use the simplest single-contract direct sovereign-agent flow for v1. Keep scoring inside the sovereign agent. Treat search-provider choice and on-chain evidence size as implementation-time decisions biased toward the fastest credible POC. One NFT per wallet; rescans update it in place. Treat everything under "Possible Improvements" as explicitly out of scope.

The builder agent will load the projection skill, map this spec to a direct sovereign-agent-centered flow (`0x080C`, with HTTP / long-running HTTP support as needed), pick the right `α` skills (overview, precompiles, agents, longrunning/http, contracts, wallet, frontend, deploy, testing, and backend only if needed), and execute in phases with checkpoints in `.ritual-build/progress.json`.
