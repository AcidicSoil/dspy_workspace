# RPG-Build-Assistant (ZeroRepo + RPG)

> A graph-driven, test-first workflow that turns ambiguous natural-language specs into a persistent **Repository Planning Graph (RPG)** and builds repositories in **topological order** with **TDD**. (Guide: Overview; Paper §1–§4).

---

## What this is

- **RPG:** A structured, persistent blueprint encoding capabilities, folders/files, data-flows, and executable interfaces in one graph—resolving NL ambiguity for long-horizon repo generation. (Paper §3.1–§3.3; Fig. 1).
- **ZeroRepo pipeline:** Proposal-level → Implementation-level → Graph-guided code generation (topological traversal + tests). (Paper Fig. 1; §4).
- **Operational build guide:** Concrete SOPs/IDs for planning, validation gates, and CI-friendly execution. (Guide Trace Matrix).

**Primary artifacts:** RPG store, feature-tree index, generation logs, test corpus, metrics dashboard. (Checklist §1).

---

## Core concepts

- **RPG nodes & edges.** Nodes span capability → folder → file → class/function. Edges capture hierarchy, **typed inter-module I/O**, and **intra-module file order**; graph must be a DAG. (Paper §3.1–§3.3.2; Fig. 1B; Guide IMPL-003/004).
- **Adaptive interfaces.** Each leaf maps to **one** interface (function when independent, class when interdependent). (Guide IMPL-006; Paper §3.3.2).
- **Topological, test-first build.** Traverse the RPG in topo order; derive a unit test **before** implementation; commit **only on green**; run selective regression/integration as subgraphs complete. (Guide GEN-001/002/003/004/005; Paper §4 & Appx C).

---

## Why RPG (evidence)

RPG improves planning stability, scales near-linearly in functionality/LOC, and speeds localization vs. NL-only approaches. (Paper §6–§8; Tables/Figures).

---

## Repository structure (conceptual mapping)

- **L0 – Functionality graph:** Cohesive modules from a feature tree (exploit/explore + dedupe). (Paper §3.2).
- **L1 – Folders / L2 – Files:** Map modules→folders, group cohesive files, preserve semantic cohesion, reduce coupling. (Paper §3.3.1; Fig. 1B.1).
- **Full RPG:** Add typed data-flows & file order; abstract base classes; design leaf interfaces. (Paper §3.3.2; Guide IMPL-003/004/005/006).

> Example layout in the paper illustrates `src/data_load`, `src/algos`, `src/eval`, with file- and function-augmented nodes. (Paper Fig. 1B).

---

## Workflow (SOPs + gates)

**Discover → Design → Build → Validate → Benchmark → Monitor** (Guide taxonomy).

1. **Discover**
   Define project spec & acceptance metrics. *(DSC-001)*
2. **Design — Implementation-level**

   - Encode inter-module **typed I/O** data-flows; ensure DAG. *(IMPL-003)*
   - Define intra-module file ordering. *(IMPL-004)*
   - Abstract base classes/shared types. *(IMPL-005)*
   - One interface per leaf (docstring with purpose/args/returns). *(IMPL-006)*
3. **Build — Graph-guided TDD**

   - Create reproducible **BUILD_QUEUE** via topological sort. *(GEN-001; Paper §4)*
   - Auto-derive a unit test from each interface/spec **before** coding. *(GEN-002)*
   - Implement minimal code to pass; **commit only on green**; run regression for impacted nodes; add integration tests per subgraph. *(GEN-003/004/005; Appx C)*
4. **Validate — Metrics & diagnosis**
   Majority-vote semantic checks; attribute failures (impl vs test/env); compute **Coverage, Novelty, Pass Rate, Voting Rate, Files, LOC, Tokens**. *(Paper §5.1–D.3.1; Guide VAL)*
5. **Benchmark**
   Evaluate against RepoCraft tasks & baselines using the above metrics. *(Paper §5–§6; Checklist §5–§6)*
6. **Monitor**
   Track near-linear growth (features/LOC); alert on plateau; correlate with pass rate. *(MON-004)*

---

## Getting started (dev tooling)

Use the recommended Python tooling for a clean CI loop:

- **Env & deps:** `uv`
- **Lint/format:** `ruff`
- **Types:** `mypy`
- **Tests:** `pytest`
- **Security lint:** `bandit`
- **Logging:** `loguru`
  (Agent playbook tooling rubric).

> Example (local): `uv pip install ruff mypy pytest bandit loguru && ruff check . && mypy . && pytest -q && bandit -r .` (Agent playbook).

---

## Quality gates & metrics

- **Build gates:** DAG valid; interface docs complete; topo order persisted; commit only on green; selective regression; subgraph integration tests. (Guide IMPL-003/006; GEN-001..005).
- **Evaluation metrics:**

  - **Coverage** (category hit ratio), **Novelty** (OOD rate), **Pass Rate**, **Voting Rate**, and code-scale (**Files**, **Normalized LOC**, **Tokens**)—exact formulas in Appx D.3.1. (Paper §5.1–D.3.1).

---

## Agents & roles (optional)

Planner → Implementer → Builder → Verifier → Orchestrator, with optional Retriever/Localizer. Includes tool permissions and HITL gates. (Agents roster & SOPs).

---

## Contributing

- Follow **topological TDD** and commit only when tests pass locally and in CI. (Guide GEN-001/003; Paper §4).
- Keep module cohesion high; prefer functions to classes unless state is shared. (Guide IMPL-006).
- Run lint/type/security checks before PRs. (Agents tooling).

---

## Roadmap & appendices

- Proposal-level retrieval & diversity (Appx A).
- Implementation patterns & skeletons (Appx B).
- Localization, editing, and staged testing (Appx C).
- RepoCraft taxonomy & metrics (Appx D).
- Result tables & worked examples (Appx E). (Checklist “Appendices”).

---

## Citation map (quick pointers)

- **RPG structure & pipeline:** Paper §3–§4; Fig. 1.
- **Data-flows / order edges / interfaces:** Guide **IMPL-003/004/006**.
- **Topo build + TDD + commit policy:** Guide **GEN-001/002/003**; Paper §4, Appx C.
- **Metrics (Coverage/Novelty/Pass/Vote/Scale):** Paper §5.1–Appx D.3.1.
- **Scaling & localization benefits:** Paper §6–§7 (tables/analysis).

---

### License

TBD (not specified in the Build Guide/Whitepaper). If needed, add governance scans (SBOM, licenses, secrets) per operational practices. (Agents governance).

---

**RPG mapping:** This README encodes the project’s Discover→Design→Build→Validate→Benchmark→Monitor flow and cites Guide IDs + Paper sections at each step for traceability. (Guide Trace Matrix; Paper Fig. 1).
