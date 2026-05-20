# Chain Deployment Infra K3s to Docker Design

## Context

- The original transcript-derived task notes were moved to `sjs-agent-sessions/k3s-to-docker-migration/task-description.md`.
- Target repo: `chain-deployment-infra`.
- Starting branch: `origin/arshan/delta-fixes-and-validator-setup`.
- Acceptance path: generate and launch a gold-standard sim with `chain-deployment-infra/quick_deploys/gold_standard.sh`, then run the generated deployment through `src/run/run_deployment.sh` and verify the system works.
- Compatibility target: full K3s removal. Breaking changes are acceptable; do not preserve a backwards-compatible K3s mode.
- Step renaming target: remove or bypass the K3s step 6 so it never runs, but do not do broad downstream step renumbering just for neatness.
- Log policy: every Docker container must use `json-file` log rotation with `max-size=1g` and `max-file=5`.

Current repo shape from inspection:

- `quick_deploys/gold_standard.sh` generates the gold-standard deployment config and tells the operator to run `./src/run/run_deployment.sh ./examples/gold-standard`.
- `src/run/run_deployment.sh` still runs step 6 as `src/6_kubernetes/6_kubernetes.sh full "$OUT_DIR"`, then runs step 7 as `src/7_chain_deploy/7_chain_deploy.sh "$OUT_DIR"`.
- `src/6_kubernetes/6_kubernetes.sh` installs K3s, writes `out/<deployment>/6_kubernetes/combination_<n>/machines.json`, stores kubeconfig, uploads kubeconfig and SSH material to GCS, and labels cluster nodes.
- `src/7_chain_deploy/7_chain_deploy.sh` currently copies `machines.json` from `6_kubernetes`, and `src/7_chain_deploy/7_2_chain_deploy.sh` expects a kubeconfig, creates Kubernetes Docker registry secrets, pre-pulls images with K8s machinery, and applies EL/CL pods.
- `src/7_chain_deploy/node_deployment.sh` generates EL/CL Kubernetes pod specs from templates, applies them with `kubectl`, waits for readiness, and deploys RPC proxies with Kubernetes.
- `src/7_chain_deploy/7_3_sidecar_deploy.sh` deploys K8s sidecars, including the echo sidecar. Gold standard enables `--echo-sidecars 1`, so echo is directly in the acceptance surface.
- `out/gs260427-01` is a recent enough generated deployment to use as a concrete reference. Its procurement manifest contains sidecar types `dkms-gcp-tdx`, `echo`, `executor-go-gcp-tdx`, `executor-phala`, `executor-zk-phala`, `streaming-service-gcp-tdx`, and `vllm-proxy-gcp-tdx`. Of the K8s sidecar types handled by `7_3_sidecar_deploy.sh`, only `echo` appears.
- `src/9_traffic_gen/9_1_traffic_gen_deploy.sh` generates traffic-gen pod specs, maps traffic-gen VM IPs to Kubernetes node names, applies pods, and waits on `app=traffic-gen`.
- `src/11_start_deployment/11_1_traffic_gen_start.sh` starts traffic by calling the traffic-gen HTTP API on host IPs at port `30105`. This can likely survive if Docker traffic-gen containers preserve the same host API contract.
- `Makefile` targets `restart-chain` and `restart-traffic` select deployments by `6_kubernetes` output and call K8s-oriented quick scripts.
- Existing Docker migration helpers live under `src/helpers/k8s_to_docker`. `migrate_node_remote.sh` uses SSH fan-out to a validator VM, and `migrate_node.sh` captures live K3s pod/container state, renders `/etc/ritual/migration/docker-compose.yml`, stops K3s, and starts Docker Compose.
- Existing Docker recovery and log-rotation helpers already assume Docker Compose on migrated nodes, including `ensure_docker_log_rotation.sh`, `restore_node_from_snapshot_docker_remote.sh`, `snapshot_recovery_docker.sh`, and `snapshot_cas_recovery_docker.sh`.
- Recoverability is still partially K8s-based: `src/7_chain_deploy/7_7_recoverability_deploy.sh` deploys a recovery-trigger DaemonSet.
- Legacy remote-ops helpers still assume kubeconfig and `kubectl`, including CL/EL upgrade and snapshot restore scripts under `src/helpers/remote_ops`.

## Design Plan

- Goal: make `chain-deployment-infra` deploy and operate the gold-standard sim without creating or relying on K3s, while replacing every K3s-backed service path exercised by the deployment with Docker-based equivalents.
- Main design direction: use SSH fan-out plus Docker Compose as the durable orchestration shape. This follows the existing `src/helpers/k8s_to_docker` migration path, but the new deploy flow must be Docker-first rather than “bootstrap K3s, then migrate.”
- Step 6 design:
  - Stop calling `src/6_kub ernetes/6_kubernetes.sh` from `src/run/run_deployment.sh`.
  - Do not create kubeconfig, K3s cluster state, or `6_kubernetes` as the required downstream source of truth.
  - Preserve required non-K3s side effects from the old step 6 path only if they are still needed, especially machine inventory and any GCS/metadata uploads that later services consume.
  - Do not rename later steps unless a small local edit makes that natural.
- Step 7 chain-node design:
  - Change `7_chain_deploy` to source machine inventory from procurement or merged deployment artifacts instead of `6_kubernetes/combination_<n>/machines.json`.
  - Keep Docker host preparation inside step 7 as an idempotent helper/subphase, rather than introducing a new numbered step 6 replacement.
  - Replace EL/CL pod-spec generation and `kubectl apply` with Docker Compose generation and SSH deployment per validator VM.
  - Reuse the proven parts of `migrate_node.sh` as the reference for container names, data paths, Compose layout, Fluent Bit wiring, stop/start order, and smoke checks.
  - Factor shared Compose-rendering logic out of the migration helper if needed, so fresh deployment and live migration do not drift into two incompatible Docker layouts.
  - Ensure Docker and the Compose plugin are installed or verified on target hosts before deployment.
  - Ensure Docker registry login and image pull happen before container start.
- Sidecar design:
  - Replace K8s sidecar pods with Docker containers or Compose services deployed over SSH to the appropriate machines.
  - Treat echo as mandatory for the gold-standard acceptance path because `gold_standard.sh` passes `--echo-sidecars 1` and traffic generation uses echo URLs.
  - Preserve the externally visible echo contract: host IP with port `30301`, including x402 endpoints used by traffic generation.
  - Remove non-gold-standard K8s sidecar branches and stale config knobs: `onnx_inference`, `signature_verification`, `accelerator-ne`, `executor-ne`, legacy `verifier`, `wormhole`, `sgx`/`sgx-client`, and `misc_ops`/`misc-ops`.
  - Keep heterogeneous/TDX sidecars in the 7.3b path; `dkms-gcp-tdx`, `executor-go-gcp-tdx`, `executor-phala`, `executor-zk-phala`, `streaming-service-gcp-tdx`, and `vllm-proxy-gcp-tdx` are live in the reference output and are not part of the dead K8s sidecar cleanup.
- Traffic-gen design:
  - Replace `src/9_traffic_gen/9_1_traffic_gen_deploy.sh` pod generation with Docker deployment to traffic-gen VMs.
  - Preserve the traffic-gen HTTP API on host port `30105`, because `src/11_start_deployment/11_1_traffic_gen_start.sh` already drives traffic through direct HTTP calls to machine IPs.
  - Keep existing traffic config generation and image-tag replacement behavior where possible, but change deployment and cleanup from `kubectl` to SSH/Docker.
  - Update `make restart-traffic` to rebuild or accept the traffic-gen image, update configs, redeploy Docker traffic containers, and restart traffic without using kubeconfig or pods.
- Helper Makefile target design:
  - Inspect the full `Makefile` for operator commands that still select `6_kubernetes`, call `kubectl`, require kubeconfig, or route through K8s quick scripts.
  - Update `make restart-chain` so it no longer selects `6_kubernetes` or calls K8s cleanup scripts.
  - Update `make restart-traffic` so it no longer selects `6_kubernetes` or deletes/redeploys K8s pods.
  - Update any other relevant Makefile helper targets whose current behavior is part of normal chain deployment, traffic generation, debugging, recovery, or restart operations.
  - Recoverability and Mission Control remote-ops helpers are in scope when they are exposed through relevant make/helper commands that operators are expected to keep using after K3s removal.
  - Clearly mark any non-acceptance legacy targets that still require follow-up if they are not needed for gold-standard deployment or the relevant operator command set.
- Log-rotation design:
  - Centralize Docker log rotation in one shared helper or sourced function.
  - Apply `json-file` `max-size=1g` and `max-file=5` before starting every Docker-managed service.
  - Prefer both daemon-level defaults and per-Compose service `logging` blocks where practical, so newly created containers and explicit Compose services cannot silently drift.
  - Keep the operation idempotent: rerunning deployment or restart targets should reassert log rotation and recreate containers only when required.
- Recoverability and remote-ops design:
  - For Dockerized nodes, prefer existing Docker recovery helpers over K8s restore pods.
  - Treat K8s recovery-trigger DaemonSet and kubeconfig-based remote ops as incompatible with the target architecture.
  - Either replace them with SSH/Docker equivalents in this branch or explicitly keep them out of the gold-standard acceptance path with a follow-up note.
- Verification design:
  - Add a cheap static preflight layer before spending cloud/runtime time.
  - Run syntax and import checks for edited scripts: `bash -n` for shell entrypoints/helpers and `python3 -m py_compile` for Python config-generation code.
  - Add or run a static acceptance-path scan that fails if Docker-first paths still reference common Kubernetes/K3s terms: `kubectl`, `KUBECONFIG`, `kubeconfig`, `kubernetes`, `k8s`, `k3s`, `6_kubernetes`, `pod`, `pod.yaml`, `daemonset`, `deployment.yaml`, `nodeSelector`, `hostPath`, `containerd`, `crictl`, `helm`, or K8s cleanup scripts. Scope this to `run_deployment.sh`, the step scripts it invokes, Docker restart helpers, traffic-gen deploy/start helpers, and the relevant Makefile targets.
  - Maintain an allowlist for intentional references outside the Docker-first acceptance path: historical docs, task notes, removed/dead-code checks, archived migration helpers, and explicit error messages that reject obsolete K8s config. Any allowlisted hit should have a reason.
  - Also run the broader repo audit the operator used to expose residual cleanup debt:
    ```bash
    rg -n "kubectl" chain-deployment-infra \
      -g '!*.md' \
      -g '!out/**' \
      -g '!docs/**' \
      -g '!quick_deploys/**'
    ```
    Remaining hits outside the acceptance path are not necessarily launch blockers, but they should be classified as either disabled/rejecting legacy paths or dead K8s helper code.
  - Cleanup reminder after the first successful Docker launch: delete or quarantine remaining legacy K8s helper files so the broad audit above goes quiet. Known buckets include old observability sub-scripts, Blockscout/RPC proxy/bootnode Kubernetes helpers, and the recovery-trigger implementation that still shells out to `kubectl`.
  - Validate the deployment artifact graph: step 7, traffic-gen, echo, `restart-chain`, and `restart-traffic` must source machine inventory from procurement/merged/step-7 artifacts, not `6_kubernetes`.
  - Use `out/gs260427-01` and newly generated gold-standard config as static fixtures: assert live sidecar types map to an implemented deployer (`echo` or 7.3b heterogeneous/TDX), and assert obsolete K8s sidecar knobs fail loudly rather than generating undeployable machines.
  - Validate generated Docker Compose before remote start: run `docker compose -f <file> config` for every generated compose file where Docker Compose is available, and otherwise parse enough YAML/JSON to assert service names, images, ports, volumes, env, restart policy, and logging blocks are present.
  - Assert log-rotation configuration statically: every generated Compose service has `json-file` `max-size=1g` and `max-file=5`, and the host-prep helper reasserts matching Docker daemon defaults.
  - Add a dry-run/preflight mode where practical for SSH fan-out helpers: resolve target hosts, images, compose paths, ports, and commands without connecting or starting containers. This should catch bad inventory shape and missing fields before cloud execution.
  - After static preflight passes, run `quick_deploys/gold_standard.sh` to generate config.
  - Run `src/run/run_deployment.sh ./examples/gold-standard`.
  - Runtime acceptance: verify no K3s setup occurs, no kubeconfig is required, and no acceptance-path script calls `kubectl`.
  - Runtime acceptance: verify validator nodes are running Docker containers with bounded logs.
  - Runtime acceptance: verify echo service responds on host port `30301`.
  - Runtime acceptance: verify traffic-gen containers expose the API on host port `30105` and traffic starts successfully.
  - RPC exposure follow-up: the Docker-first chain deploy removed the old Kubernetes per-node RPC proxy, so EL host APIs are exposed directly on validator VMs unless the separate RPC Envoy Mesh is enabled. After the first successful direct-path launch, try a deployment with `--enable-rpc-envoy-mesh true` and/or ask Stelios whether direct EL host APIs are acceptable for gold-standard sims or whether Envoy should become the default security boundary.
  - Runtime acceptance: verify `make restart-chain` and `make restart-traffic` work through Docker paths.

Structural simplification check:

- The durable target is one Docker-based deployment mechanism, not a long-lived K3s path plus a Docker overlay.
- The existing live migration script should inform the Docker shape, but fresh deploy should not depend on first creating K3s pods to capture their specs.
- If compatibility shims are needed to keep old output paths temporarily, they should be local, deleted quickly, and not exposed as an operator mode.
- Runtime service definitions should converge on shared Docker/Compose helpers so chain nodes, echo, traffic gen, and recovery operations do not each invent separate container conventions.

## Ambiguities To Resolve

- None currently. Planning is complete enough to begin implementation.
