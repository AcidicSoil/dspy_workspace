<!-- path: docs/PROJECT_SPEC.example.md -->
# RPG‑Build‑Assistant — Project Spec (Example)


## Goals

- Parse a markdown **Project Spec** into JSON `{goals[], non_goals[], constraints[], metrics[]}`.
- Fail CI when any required section is missing/empty.


## Non-Goals

- Build the full RPG schema.
- Generate code from the spec.


## Constraints

- Python 3.11; no external deps.
- Runs in CI in < 5s.


## Acceptance Metrics

- Validator returns **OK** for `docs/PROJECT_SPEC.example.md`.
- CI job fails on malformed specs.


### Stakeholders & Review

- **Owner:** Repo Maintainer
- **Stakeholders:** PM, Tech Lead
- **Review Status:** approved


### Context

- Downstream task will use this JSON as input.
