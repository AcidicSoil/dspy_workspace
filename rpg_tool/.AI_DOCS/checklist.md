# 1. Introduction — scope & artifacts

*Map to paper §1.*

- State the tool’s purpose: “Turn ambiguous NL specs into a persistent Repository Planning Graph (RPG) that drives scalable repo generation.” Record this as a README-like scope note.
- Declare primary artifacts and IDs: RPG store, feature tree index, generation logs, test corpus, metrics dashboard.
- Define success criteria you’ll compute later: functional coverage, novelty, pass/vote accuracy, and code scale.

# 2. Related Work — baseline inventory

*Map to paper §2.*

- Catalog comparator systems (multi-agent, workflow, terminal agents) and fix their configurations for reproducibility.
- Write a one-pager on what RPG contributes beyond natural-language planning (structure, persistence, data-flow).

# 3. Repository Planning Graph Construction — end-to-end contract

*Map to paper §3.*

- Establish a single canonical RPG store (transactional) with versioning and snapshots.
- Install validators you must pass before any codegen: DAG acyclicity, required fields, dependency closure, module boundary integrity. Gate codegen on “all green.”

## 3.1 RPG Structure — schema & invariants

*Map to paper §3.1.*

- Define node schema (capability, folder, file, class, function) with dual semantics and required fields: `id, kind, path/name, signature, inputs, outputs, deps, tests, status`.
- Define edge types: (a) hierarchical containment, (b) inter-module typed data-flows, (c) intra-module file-order edges.
- Implement topological ordering over all executable leaves; persist topo index.

## 3.2 Proposal-Level Construction — functionality graph

*Map to paper §3.2 and Appx A.*

- Connect to a large Feature Tree (vector DB with path metadata). Implement exploit (top-k retrieval) + explore (unvisited sampling) loop; include diversity-aware rejection sampling.
- Refactor retrieved paths into cohesive modules (maximize cohesion, minimize coupling); reject duplicates, resolve overlaps, and eliminate orphans.
- Emit a **Functionality Graph** artifact with module notes and gap list.

## 3.3 Implementation-Level Construction — from plan to RPG

*Map to paper §3.3.*

### 3.3.1 File Structure Encoding — skeleton

*Map to paper §3.3.1.*

- Map modules → folders; mid-level capabilities → files; define naming rules.
- Emit a **skeleton diff** (+folders, +files) with module↔folder mapping.
- Re-run validators: file-path consistency; no stray modules.

### 3.3.2 Data-Flow & Functions Encoding — interfaces

*Map to paper §3.3.2.*

- Add inter-module typed I/O edges and intra-module order constraints; regenerate topo order.
- Abstract recurring patterns into base classes/shared types; record inheritance and contracts.
- For each leaf feature, choose class vs function; specify signatures, typed inputs/outputs, and docstrings; link to upstream/downstream contracts.

# 4. Graph-Guided Code Generation — TDD + localization

*Map to paper §4 and Appx C.*

- Traverse leaves in topo order; for each node generate a unit test from its docstring & contracts, then implement minimal code to pass.
- If a test fails, localize with (i) RPG-guided fuzzy search, (ii) repo code view, (iii) dependency explorer; patch and retest; commit only on pass.
- Maintain regression and boundary integration tests; keep edit logs.

# 5. Experiment Setup — benchmark & metrics

*Map to paper §5, §5.1–§5.3.*

- **Benchmark selection**: fix target repos/categories; anonymize if needed. (§5.1.1)
- **Metrics implementation**: coverage (category hit ratio), novelty (OOD rate), accuracy (pass & vote), code scale (files, normalized LOC, tokens). (§5.1.2, D.3.1)
- **Task construction pipeline**: parse test trees, stratified sample, filter trivial tests, generate NL task specs + ground-truth tests. (§5.1.3, D.2)
- **Baselines**: script configurations and iteration budgets for multi-agent, workflow, and terminal agents. (§5.2)
- **Implementation details**: fix iteration counts, localization retries, voting rounds; log seeds and environment. (§5.3)

# 6. Main Results — reporting template

*Map to paper §6.*

- Prepare a standard table and plots comparing coverage, novelty, pass/vote, and scale vs baselines; include qualitative examples of complex dependencies induced by RPG.

# 7. Analysis — ablations & scaling

*Map to paper §7, §7.1–§7.3.*

- **Scalability**: track features/LOC vs iteration; verify near-linear trends; alert on stagnation. (§7.1)
- **Stability & innovation**: plot coverage and novelty across rounds; sample and audit novel features for coherence. (§7.2)
- **Localization efficiency**: ablate with/without RPG tools; report step counts and variance. (§7.3)

# 8. Conclusion — operational checklist close-out

*Map to paper §8.*

- Summarize whether RPG improved planning consistency, scaling, and localization efficiency in your runs; list next extensibility targets (new domains, larger trees).

# Appendices — implementable assets

*Map to paper Appx A–E.*

## A. Proposal-Level (Algorithms, Process, Prompts)

- Implement diversity-aware rejection sampling and exploit/explore subtree builder; expose knobs (temperature, overlap ρ, budgets). (Appx A.1–A.2)
- Package prompt templates for exploit/explore/missing-features with variables for project context; unit-test their JSON outputs. (Appx A.3)

## B. Implementation-Level (Prompts, Skeleton, Patterns)

- Provide prompt templates for: data-flow DAG design, raw skeleton mapping, subgraph→base class abstraction, and feature→interface mapping; lint outputs against validators. (Appx B.1)
- Store exemplar skeleton diffs and interface specs; extract recurrent patterns for reuse. (Appx B.2–B.3)

## C. Graph-Guided Generation (Localization, Editing, Testing)

- Ship a toolset: `view_file_interface_feature_map`, `get_interface_content`, `expand_leaf_node_info`, `search_interface_by_functionality`, plus structured **edit** operations (whole class, method, function, imports). (Appx C.1–C.2)
- Implement the staged testing pipeline: unit → regression → integration, with LLM-judged diagnosis and automated test/environment repair. (Appx C.4)
- Log complete localization & editing trajectories for audit. (Appx C.3, C.5)

## D. RepoCraft Details (Data, Pipeline, Taxonomy, Metrics)

- Reproduce repository selection & anonymization; persist dataset cards. (Appx D.1)
- Automate task harvesting from tests, hierarchical categorization, and sampling; export tasks as NL + tests. (Appx D.2)
- Implement the 3-stage evaluation agent (localize → vote → adapt/execute tests) and metric formulas. (Appx D.3, D.3.1)
- Load the ground-truth taxonomy for coverage/novelty calculation; add OOD centroid logic. (Appx D.4)

## E. Results (Configs, Detailed Tables, Examples)

- Freeze baseline configs; generate per-repo tables; include worked examples for coverage/novelty and localization behavior. (Appx E.1–E.4)

---

### Cross-cutting extensibility hooks

- **RPG I/O**: JSON/YAML export, migration scripts, and diffing between RPG versions.
- **Pluggable trees**: support alternative feature ontologies and hybrid retrieval (symbolic + vector).
- **Policy knobs**: gating rules (e.g., minimum validator set), test-first budgets, retry caps, novelty thresholds.
- **Dashboards**: CI panels for Coverage/Novelty/Pass/Vote/Scale with iteration timelines. (Maps to §5.1.2, §6–§7.)

> Use the section taxonomy above as your table of contents when you stand up the repo for this tooling so each checklist maps 1:1 to the paper’s “notions.”
