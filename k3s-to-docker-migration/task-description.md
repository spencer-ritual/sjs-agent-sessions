# Chain Deployment Infra K3s to Docker Refactor Planning Notes

Sources:

- Spencer x Arshan transcript, 2026-05-04 10:58 EDT.
- Arshan Slack follow-up, 2026-05-04 11:10 EDT.

## Context

- Spencer is taking the K3s/Kubernetes removal task for chain-deployment-infra (CDI) so it does not become an urgent blocker later in the week.
- The task is to refactor the existing chain-deployment-infra chain deployment workflow away from K3s and onto Docker.
- The migration surface is broader than one service. Arshan explicitly called out all services using K3s, including traffic generation, blockchain nodes, and the echo service. The transcript also mentioned chain or validator node workflows and `ritual-node-internal` as surfaces to verify.
- Existing make targets and helper files are part of the operator workflow and need to be updated when their implementation assumes K3s.
- `make restart-chain` and `make restart-traffic` are specifically relevant operator targets for this refactor.
- Arshan expects that many restart-oriented targets may not be deeply K3s-specific, but log-pulling and debugging helpers are likely tied to K3s and need attention.
- Arshan said to start from `origin/arshan/delta-fixes-and-validator-setup`.
- The Docker migration must account for log growth. Arshan saw a production-like deployment accumulate roughly a terabyte of logs after running without log rotation.
- Arshan fixed that previous log issue by making the migration or rollout script idempotently reconfigure Docker with the correct logging settings.
- Arshan mentioned removing “step six” from the relevant flow because it is no longer necessary. The transcript and Slack note do not identify where step six is defined.
- Renaming later steps after removing step six is not required. Arshan called that low value and invasive, so the plan should not treat renumbering as necessary unless it falls out naturally from a small local edit.
- Acceptance is simulation-based, not a local network task. The migration should be verified by launching a sim with `chain-deployment-infra/quick_deploys/gold_standard.sh` and confirming the deployed system works.
- The intended outcome is full K3s removal in this branch. Breaking changes are acceptable, and the plan should not preserve backwards compatibility with K3s workflows.
- The preferred Docker orchestration shape should be inferred from the existing step 7 implementation rather than treated as an open product/design question.

## Design Plan

- Goal: refactor chain-deployment-infra's chain deployment workflow from K3s/Kubernetes to Docker while preserving the operator workflows used to run, restart, inspect, and debug the system.
- Primary planning output: identify every K3s-dependent chain-deployment-infra service, script, helper file, and make target; define the Docker replacement shape; and record remaining questions before implementation planning begins.
- Arshan instruction: remove K3s/Kubernetes and replace it with Docker.
- Arshan instruction: make the migration a full removal of K3s paths, with no backwards-compatible K3s mode.
- Arshan instruction: change every chain-deployment-infra workflow that uses K3s, not just the first obvious service.
- Arshan instruction: include all services using K3s.
- Arshan instruction: include traffic generation in the migration surface.
- Arshan instruction: include blockchain node workflows in the migration surface.
- Arshan instruction: include chain and validator node workflows if they are separate from the blockchain node workflow in the codebase.
- Arshan instruction: include `ritual-node-internal` if the CDI workflow currently uses it through K3s.
- Arshan instruction: include the echo service.
- Arshan instruction: start from `origin/arshan/delta-fixes-and-validator-setup`.
- Arshan instruction: update helper files and make targets as part of the migration.
- Arshan instruction: update the helper Makefile targets.
- Arshan instruction: check and preserve or update `make restart-chain`.
- Arshan instruction: check and preserve or update `make restart-traffic`.
- Arshan instruction: update log-pulling and debugging targets that currently depend on K3s.
- Arshan instruction: configure log rotation on every Docker container.
- Arshan instruction: use an explicit Docker log rotation policy of five max files and one gigabyte per file.
- Arshan instruction: make Docker logging configuration idempotent so repeated runs enforce the intended settings.
- Arshan instruction: remove “step six” so it never runs.
- Arshan instruction: do not spend effort renaming downstream steps after step six is removed; it is not necessary and Arshan considers it low value and invasive.
- Key workstreams:
  - Inventory chain-deployment-infra K3s usage across traffic gen, blockchain nodes, chain or validator nodes, `ritual-node-internal`, echo service, scripts, manifests, make targets, and log tooling.
  - Map each K3s-backed component to the Docker lifecycle that should replace it, using step 7 as the local convention for orchestration shape.
  - Preserve or update operator workflows for start, stop, restart, traffic generation, log inspection, and debugging, especially `make restart-chain` and `make restart-traffic`.
  - Remove obsolete deployment step six without doing a broad downstream step-renaming cleanup.
  - Ensure every Docker container has bounded logs using five max files and one gigabyte per file, and that the configuration is enforced idempotently.
  - Define a verification path that launches a sim with `chain-deployment-infra/quick_deploys/gold_standard.sh` and proves traffic generation, chain or validator nodes, echo service, and debugging workflows still work after K3s is removed.
- Structural simplification check:
  - The durable target should be one Docker-based chain-deployment-infra deployment path, with K3s paths removed rather than preserved.
  - Do not add temporary K3s compatibility unless implementation discovery reveals a hard blocker that must be explicitly escalated.
  - Helper targets should share common Docker setup where practical, rather than duplicating container options and log configuration across scripts.
  - Log rotation should be configured through a durable common mechanism so individual containers do not drift.

## Ambiguities To Resolve

- Which repository or repositories contain the chain-deployment-infra deployment scripts, make targets, and service definitions?
- What exactly is “step six,” and where is it defined?
- What is the complete service inventory using K3s today beyond traffic gen, blockchain or validator nodes, `ritual-node-internal`, and echo service?
- Which make targets are considered public operator interface and must preserve names and behavior?
