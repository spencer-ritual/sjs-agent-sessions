# Skill Reflection

## Planning Artifact Path Validation

- Trigger: During upstream merge planning, I initially wrote `sjs-agent-sessions` content under `ritual-reth-internal/sjs-agent-sessions/` instead of the repo-level `/home/ritual/repos/sjs-agent-sessions/<feature>/design.md` path required by `.cursor/skills/planning/SKILL.md`.
- Existing gap: I applied the user's phrase "start an upstream merge md in sjs-agent-sessions" from memory before re-reading the planning skill, even though workspace rules define `plan this` / planning-style requests as skill-triggered and the skill carries the artifact path contract.
- Candidate update: Before creating any planning artifact named or described as an `sjs-agent-sessions` plan, re-read `.cursor/skills/planning/SKILL.md` and verify the exact path and required headers. If a user asks for an `md` rather than explicitly saying "plan," still check the planning skill when the artifact is an implementation/design planning artifact.
- Scope: Applies to repo-local planning artifacts and other skill-owned artifact locations. It should not prevent ordinary scratch notes when the user provides an explicit path.
- Evidence: The misplaced file was corrected into `/home/ritual/repos/sjs-agent-sessions/upstream-merge-dependencies/design.md`, and the repo-local copy was deleted after the user pointed out the mismatch.
- Promotion status: Not promoted yet.
