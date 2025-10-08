RPG_REPOSITORY_PLANNING_GRAPH.pdf

A) Human-readable Plan (Markdown)
=================================

**Overview.** This plan turns the _RPG: Repository Planning Graph_ whitepaper into a deduplicated, provider-agnostic, step-by-step build guide. It covers: (1) defining the RPG schema; (2) proposal- and implementation-level graph construction; (3) graph-guided, test-driven code generation; and (4) evaluation/monitoring (RepoCraft-style). Assumptions: Python repos, any LLM, any vector DB/graph DB, any CI. RPG_REPOSITORY_PLANNING_GRAPH

**Primary Purpose assumed:** _Operationalize RPG/ZeroRepo to generate full repositories from scratch using a unified planning graph and graph-guided TDD._ RPG_REPOSITORY_PLANNING_GRAPH

**Audience/Actors assumed:** Research Engineer, Software Architect, QA/Testing, PM, DevOps.
**Constraints assumed:** provider-agnostic, offline-friendly, reproducible, acyclic data-flows, test-gated commits, license-safe inputs.
**Preferred Taxonomy used:** **Discover → Design → Build → Validate → Benchmark → Monitor**.
**Priority Policy:** P0 blocker (must), P1 important, P2 nice-to-have.

* * *

Instruction List (grouped by taxonomy)
--------------------------------------

### Discover

- **ID:** DSC-001
    **Topic:** Discover
    **Instruction:** Define <PROJECT\_SPEC> with goals, scope, constraints, and acceptance metrics.
    **Acceptance Criteria:** Doc includes <GOALS>, <NON\_GOALS>, <CONSTRAINTS>, <METRICS>; reviewed by <STAKEHOLDERS>.
    **Dependencies:** —
    **Priority:** P0
    **Risks & Mitigations:** Ambiguity → add examples and anti-requirements.
    **Source:** ¶2 — “generating complete repositories… demands coherent… planning.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** markdown repo template

- **ID:** DSC-002
    **Topic:** Discover
    **Instruction:** Specify RPG schema with <NODE\_TYPES>, <EDGE\_TYPES>, required fields, and DAG constraint.
    **Acceptance Criteria:** JSON Schema covers nodes {capability, folder, file, class, function} and edges {hierarchy, data\_flow, order}; validates acyclicity.
    **Dependencies:** DSC-001
    **Priority:** P0
    **Risks & Mitigations:** Over-generalization → start minimal; iterate.
    **Source:** ¶6 — “nodes specify… files, classes, and functions… edges encode… data flows… order.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** generic schema validator; graph DB

- **ID:** DSC-003
    **Topic:** Discover
    **Instruction:** Assemble <FEATURE\_TREE\_SOURCE> and embed nodes into <VECTOR\_DB>.
    **Acceptance Criteria:** ≥1M features loaded or configured; embeddings stored with path metadata; latency < <EMBED\_QPS>.
    **Dependencies:** DSC-001
    **Priority:** P0
    **Risks & Mitigations:** Bias/skew → record level distribution; add sampling.
    **Source:** ¶7 — “Feature Tree… 1.5M capabilities… embedded… vector database.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** any embedding model; FAISS/pgvector/milvus


* * *

### Design (Proposal-level)

- **ID:** PROP-001
    **Topic:** Proposal Design
    **Instruction:** Retrieve top-k feature paths for <PROJECT\_SPEC> into <CANDIDATES\_EXPLOIT>.
    **Acceptance Criteria:** Query returns k paths with similarity scores and full hierarchical paths.
    **Dependencies:** DSC-003
    **Priority:** P0
    **Risks & Mitigations:** Narrow recall → expand synonyms.
    **Source:** ¶8 — “retrieve top-k feature paths… aligned with the user goal.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** vector search

- **ID:** PROP-002
    **Topic:** Proposal Design
    **Instruction:** Sample unvisited ontology regions into <CANDIDATES\_EXPLORE>.
    **Acceptance Criteria:** At least <N\_EXPL> diverse paths not overlapping existing subtree (> <RHO> threshold).
    **Dependencies:** DSC-003
    **Priority:** P0
    **Risks & Mitigations:** Irrelevance → diversity-aware rejection sampling.
    **Source:** ¶8/¶21 — “exploration ensures diversity… rejection mechanism.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** weighted sampler

- **ID:** PROP-003
    **Topic:** Proposal Design
    **Instruction:** Filter, rank, and merge candidates using <LLM\_FILTER\_PROMPT>.
    **Acceptance Criteria:** Merged set deduped; rationale captured per path; audit log stored.
    **Dependencies:** PROP-001, PROP-002
    **Priority:** P0
    **Risks & Mitigations:** LLM drift → batch self-check.
    **Source:** ¶8/Algorithm 2 — “LLM… filter… self-checks… insert paths.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** any LLM; prompt templatizer

- **ID:** PROP-004
    **Topic:** Proposal Design
    **Instruction:** Refactor subtree into modules maximizing cohesion, minimizing coupling.
    **Acceptance Criteria:** Modules have clear boundaries; taxonomy justification per move recorded.
    **Dependencies:** PROP-003
    **Priority:** P0
    **Risks & Mitigations:** Over-fragmentation → merge pass.
    **Source:** ¶9 — “partitions… into cohesive modules… cohesion and coupling.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** graph partitioner

- **ID:** PROP-005
    **Topic:** Proposal Design
    **Instruction:** Persist the functionality graph as RPG layer L0 with version <RPG\_VER>.
    **Acceptance Criteria:** L0 saved; checksum; diffable; CI loads without errors.
    **Dependencies:** PROP-004
    **Priority:** P0
    **Risks & Mitigations:** Schema drift → add migration script.
    **Source:** ¶4 — “persistent and evolvable representation.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** git LFS; graph DB


* * *

### Design (Implementation-level)

- **ID:** IMPL-001
    **Topic:** Implementation Design
    **Instruction:** Map L0 modules to folder layout under <ROOT\_DIR>/src as L1 folder nodes.
    **Acceptance Criteria:** Each module ↔ one folder; mapping table with subtree names; path lint passes.
    **Dependencies:** PROP-005
    **Priority:** P0
    **Risks & Mitigations:** Over-nesting → cap depth.
    **Source:** ¶10 — “assigning each subgraph a dedicated directory namespace.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** code scaffolder

- **ID:** IMPL-002
    **Topic:** Implementation Design
    **Instruction:** Group intermediate nodes into files; create L2 file nodes.
    **Acceptance Criteria:** Files contain cohesive features; naming per PEP8; ≤ <MAX\_FILES\_PER\_DIR> unless subfolders added.
    **Dependencies:** IMPL-001
    **Priority:** P0
    **Risks & Mitigations:** Cross-file coupling → regroup.
    **Source:** ¶11 — “assigning files to intermediate nodes… preserve semantic cohesion.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** file planner

- **ID:** IMPL-003
    **Topic:** Implementation Design
    **Instruction:** Encode inter-module data-flow edges with typed I/O; ensure DAG.
    **Acceptance Criteria:** Edges include {from,to,data\_id,data\_type,transformation}; cycle check passes.
    **Dependencies:** IMPL-001
    **Priority:** P0
    **Risks & Mitigations:** Hidden cycles → topological check in CI.
    **Source:** ¶12 — “typed input–output flows… impose a topological order.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** DAG/graph validator

- **ID:** IMPL-004
    **Topic:** Implementation Design
    **Instruction:** Define intra-module file order edges for build/load constraints.
    **Acceptance Criteria:** Order edges exist for each module; no contradictions; linter validates.
    **Dependencies:** IMPL-002
    **Priority:** P1
    **Risks & Mitigations:** Brittle imports → lazy load.
    **Source:** ¶6/¶12 — “intra-module file ordering… precedes…” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** import graph analyzer

- **ID:** IMPL-005
    **Topic:** Implementation Design
    **Instruction:** Abstract shared patterns into <BASE\_CLASSES> and shared data structures.
    **Acceptance Criteria:** Base types defined only for recurring patterns; adoption rate ≥ <ADOPTION\_RATE>.
    **Dependencies:** IMPL-003
    **Priority:** P1
    **Risks & Mitigations:** Premature abstraction → justify with usage.
    **Source:** ¶13 — “abstract… base classes… enforce interface consistency.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** UML generator

- **ID:** IMPL-006
    **Topic:** Implementation Design
    **Instruction:** For each leaf feature, design exactly one interface (func or class) with docstring.
    **Acceptance Criteria:** One interface/leaf; docstrings include args/returns; no bodies (pass).
    **Dependencies:** IMPL-002, IMPL-003, IMPL-005
    **Priority:** P0
    **Risks & Mitigations:** Over-classing → prefer functions for stateless ops.
    **Source:** ¶14 & Appendix B.1 — “adaptive mapping… functions vs classes; prompt template.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** interface generator


* * *

### Build (Graph-guided TDD)

- **ID:** GEN-001
    **Topic:** Build
    **Instruction:** Topologically sort RPG and plan build queue <BUILD\_QUEUE>.
    **Acceptance Criteria:** Queue respects all edges; snapshot stored; reproducible order.
    **Dependencies:** IMPL-003, IMPL-004
    **Priority:** P0
    **Risks & Mitigations:** Nondeterminism → seed & persist order.
    **Source:** ¶15 — “traverses the RPG in topological order.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** topo-sort lib

- **ID:** GEN-002
    **Topic:** Build
    **Instruction:** For each leaf, auto-derive a unit test from its interface/spec.
    **Acceptance Criteria:** Test covers normal & edge inputs; executable via <TEST\_RUNNER>.
    **Dependencies:** IMPL-006
    **Priority:** P0
    **Risks & Mitigations:** Weak tests → mutation testing.
    **Source:** ¶15 — “test-driven development… test is derived… validated.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** test generator

- **ID:** GEN-003
    **Topic:** Build
    **Instruction:** Implement code to pass the unit test; commit only on green.
    **Acceptance Criteria:** Test passes locally and in CI; code style OK; coverage ≥ <MIN\_COV>.
    **Dependencies:** GEN-002
    **Priority:** P0
    **Risks & Mitigations:** Flaky tests → rerun policy.
    **Source:** ¶15 — “Only functions that pass all tests are committed.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** CI runner

- **ID:** GEN-004
    **Topic:** Build
    **Instruction:** On edits, run regression tests for impacted nodes and parents.
    **Acceptance Criteria:** Impact set derived from RPG edges; all prior tests green.
    **Dependencies:** GEN-003
    **Priority:** P0
    **Risks & Mitigations:** Large blast radius → selective test.
    **Source:** ¶17 — “Validated components trigger regression tests upon modification.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** test impact analyzer

- **ID:** GEN-005
    **Topic:** Build
    **Instruction:** Create integration tests for completed subgraphs before release.
    **Acceptance Criteria:** Data-flows executed; contract checks pass; artifacts persisted.
    **Dependencies:** GEN-003
    **Priority:** P1
    **Risks & Mitigations:** Orchestration failures → synthetic fixtures.
    **Source:** ¶17 — “completed subgraphs undergo integration tests.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** integration harness


* * *

### Validate

- **ID:** VAL-001
    **Topic:** Validation
    **Instruction:** Add LLM majority-vote semantic validator for algorithm presence.
    **Acceptance Criteria:** 5-vote majority result logged; confidence ≥ <VOTE\_THRESHOLD>.
    **Dependencies:** GEN-003
    **Priority:** P1
    **Risks & Mitigations:** Judge variance → temperature 0 & tie-break rules.
    **Source:** ¶17 & D.3 — “majority-vote checking… two rounds/5 votes.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** evaluator LLM

- **ID:** VAL-002
    **Topic:** Validation
    **Instruction:** Implement failure attribution: implementation vs test/env; auto-remediate latter.
    **Acceptance Criteria:** Errors labeled; env/test issues retried ≤ <N\_REMEDIATIONS>; logs kept.
    **Dependencies:** GEN-003
    **Priority:** P1
    **Risks & Mitigations:** Mislabeling → add heuristics & review.
    **Source:** ¶17 — “majority-vote diagnosis… handle environment or test issues.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** log analyzer

- **ID:** VAL-003
    **Topic:** Validation
    **Instruction:** Compute Coverage, Novelty, Pass Rate, Voting Rate, Files, LOC, Tokens.
    **Acceptance Criteria:** Metrics computed per formulas (D.3.1); stored in <METRICS\_STORE>.
    **Dependencies:** PROP-005, GEN-003
    **Priority:** P0
    **Risks & Mitigations:** Category drift → fixed centroids + human audit.
    **Source:** ¶19 & D.3.1 — “Coverage… Novelty… Pass/Voting… Code-level statistics.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** metrics job


* * *

### Benchmark

- **ID:** BMR-001
    **Topic:** Benchmark
    **Instruction:** Build task set by parsing reference tests into <TASKS> with NL descriptions.
    **Acceptance Criteria:** > <N\_TASKS> tasks with input/outputs; trivial cases filtered.
    **Dependencies:** DSC-001
    **Priority:** P1
    **Risks & Mitigations:** Leakage → anonymize names.
    **Source:** ¶18 & D.2 — “derive tasks from reference repositories… filter trivial.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** test parser

- **ID:** BMR-002
    **Topic:** Benchmark
    **Instruction:** Run localization → validation → execution loop per task.
    **Acceptance Criteria:** For each task: candidate found or absence recorded; test adapted; result stored.
    **Dependencies:** BMR-001, VAL-001
    **Priority:** P1
    **Risks & Mitigations:** False negatives → retry budget.
    **Source:** D.3 — “Stage 1 localization… Stage 2 voting… Stage 3 execution.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** harness runner


* * *

### Monitor & Operate

- **ID:** MON-001
    **Topic:** Monitor
    **Instruction:** Enforce DAG acyclicity and schema validation in CI on every RPG change.
    **Acceptance Criteria:** CI blocks cycles/schema violations; report lists offending edges/nodes.
    **Dependencies:** DSC-002, IMPL-003
    **Priority:** P0
    **Risks & Mitigations:** Slow checks → cache results.
    **Source:** ¶12 — “impose a topological order… DAG.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** CI job

- **ID:** MON-002
    **Topic:** Monitor
    **Instruction:** Log localization steps and tool calls for auditability.
    **Acceptance Criteria:** Each step recorded with inputs/outputs; PII scrubbed; replayable.
    **Dependencies:** GEN-001
    **Priority:** P2
    **Risks & Mitigations:** Verbose logs → sampling.
    **Source:** C.3 — “representative logs… tool invocations… termination results.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** structured logging

- **ID:** MON-003
    **Topic:** Governance
    **Instruction:** Add license and security checks for generated code and dependencies.
    **Acceptance Criteria:** SBOM created; license policy enforced; secrets scan clean.
    **Dependencies:** GEN-003
    **Priority:** P0
    **Risks & Mitigations:** False positives → allowlist with review.
    **Source:** (general compliance risk implied by large-scale gen) RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** SBOM, license scanner

- **ID:** MON-004
    **Topic:** Monitor
    **Instruction:** Track scaling metrics over iterations (features, LOC) to detect stagnation.
    **Acceptance Criteria:** Plots show near-linear growth or flag plateau; regression alerts.
    **Dependencies:** VAL-003
    **Priority:** P2
    **Risks & Mitigations:** Metric gaming → cross-check with pass rate.
    **Source:** ¶7.1/7.2 — “near-linear growth of functionalities and LOC.” RPG_REPOSITORY_PLANNING_GRAPH
    **Tool Suggestions:** metrics dashboard


* * *

Trace Matrix (Source Paragraph → Instruction IDs)
-------------------------------------------------

- **¶2** → DSC-001

- **¶4** → PROP-005

- **¶6** → DSC-002, IMPL-004

- **¶7** → DSC-003

- **¶8** → PROP-001, PROP-002, PROP-003

- **¶9** → PROP-004

- **¶10** → IMPL-001

- **¶11** → IMPL-002

- **¶12** → IMPL-003, MON-001

- **¶13** → IMPL-005

- **¶14** → IMPL-006

- **¶15** → GEN-001, GEN-002, GEN-003

- **¶17** → GEN-004, GEN-005, VAL-002

- **¶18** → BMR-001

- **¶19** → VAL-003

- **D.2/D.3** → BMR-001, BMR-002, VAL-001

- **C.3** → MON-002

- **7.1/7.2** → MON-004


> Key phrases (quoted ≤20 words) appear under each instruction’s **Source** field.

* * *

B) Machine-readable JSON
========================

    {
      "instruction_pack": {
        "metadata": {
          "primary_purpose": "Operationalize RPG/ZeroRepo for unified, scalable repository generation via a persistent planning graph and graph-guided TDD.",
          "generated_at": "2025-09-30T00:00:00Z",
          "language": "English",
          "taxonomy_used": "Discover → Design → Build → Validate → Benchmark → Monitor"
        },
        "instructions": [
          {
            "id": "DSC-001",
            "topic": "Discover",
            "instruction": "Define <PROJECT_SPEC> with goals, scope, constraints, and acceptance metrics.",
            "acceptance_criteria": [
              "Doc includes <GOALS>, <NON_GOALS>, <CONSTRAINTS>, <METRICS>",
              "Reviewed by <STAKEHOLDERS>"
            ],
            "dependencies": [],
            "priority": "P0",
            "risks": ["Ambiguity in scope"],
            "mitigations": ["Add examples, anti-requirements"],
            "tool_suggestions": ["markdown template"],
            "source": {
              "paragraph_indexes": [2],
              "key_phrase": "generating complete repositories… demands coherent and reliable planning"
            },
            "tags": ["planning","inputs"]
          },
          {
            "id": "DSC-002",
            "topic": "Discover",
            "instruction": "Specify RPG schema with <NODE_TYPES>, <EDGE_TYPES>, required fields, and DAG constraint.",
            "acceptance_criteria": [
              "JSON Schema validates nodes and edges",
              "Acyclicity check available"
            ],
            "dependencies": ["DSC-001"],
            "priority": "P0",
            "risks": ["Over-general schema"],
            "mitigations": ["Start minimal; iterate"],
            "tool_suggestions": ["schema validator","graph DB"],
            "source": {
              "paragraph_indexes": [6],
              "key_phrase": "nodes specify… files, classes… edges encode… data flows… ordering"
            },
            "tags": ["rpg","schema"]
          },
          {
            "id": "DSC-003",
            "topic": "Discover",
            "instruction": "Assemble <FEATURE_TREE_SOURCE> and embed nodes into <VECTOR_DB>.",
            "acceptance_criteria": [
              "Embeddings stored with path metadata",
              "Query latency < <EMBED_QPS>"
            ],
            "dependencies": ["DSC-001"],
            "priority": "P0",
            "risks": ["Ontology skew"],
            "mitigations": ["Diversity-aware sampling"],
            "tool_suggestions": ["embedding model","vector DB"],
            "source": {
              "paragraph_indexes": [7],
              "key_phrase": "large-scale ontology… nodes embedded… vector database"
            },
            "tags": ["kb","retrieval"]
          },
          {
            "id": "PROP-001",
            "topic": "Proposal Design",
            "instruction": "Retrieve top-k feature paths for <PROJECT_SPEC> into <CANDIDATES_EXPLOIT>.",
            "acceptance_criteria": [
              "k paths with scores and full hierarchical paths"
            ],
            "dependencies": ["DSC-003"],
            "priority": "P0",
            "risks": ["Narrow recall"],
            "mitigations": ["Expand synonyms"],
            "tool_suggestions": ["vector search"],
            "source": {
              "paragraph_indexes": [8],
              "key_phrase": "retrieve top-k feature paths most aligned with the user goal"
            },
            "tags": ["retrieval","exploit"]
          },
          {
            "id": "PROP-002",
            "topic": "Proposal Design",
            "instruction": "Sample unvisited ontology regions into <CANDIDATES_EXPLORE>.",
            "acceptance_criteria": [
              "≥ <N_EXPL> non-overlapping candidate paths"
            ],
            "dependencies": ["DSC-003"],
            "priority": "P0",
            "risks": ["Low precision"],
            "mitigations": ["Diversity-aware rejection sampling"],
            "tool_suggestions": ["sampler"],
            "source": {
              "paragraph_indexes": [8,21],
              "key_phrase": "exploration ensures diversity… diversity-aware rejection mechanism"
            },
            "tags": ["retrieval","explore"]
          },
          {
            "id": "PROP-003",
            "topic": "Proposal Design",
            "instruction": "Filter, rank, and merge candidates using <LLM_FILTER_PROMPT>.",
            "acceptance_criteria": [
              "Merged set deduped with rationales",
              "Batch self-check logs stored"
            ],
            "dependencies": ["PROP-001","PROP-002"],
            "priority": "P0",
            "risks": ["LLM drift"],
            "mitigations": ["Batch self-checks"],
            "tool_suggestions": ["LLM"],
            "source": {
              "paragraph_indexes": [8],
              "key_phrase": "LLM… filter candidates… self-check… insert paths"
            },
            "tags": ["filter","ranking"]
          },
          {
            "id": "PROP-004",
            "topic": "Proposal Design",
            "instruction": "Refactor subtree into modules maximizing cohesion and minimizing coupling.",
            "acceptance_criteria": [
              "Modules have boundary definitions",
              "Move/merge justifications recorded"
            ],
            "dependencies": ["PROP-003"],
            "priority": "P0",
            "risks": ["Over-fragmentation"],
            "mitigations": ["Merge pass"],
            "tool_suggestions": ["graph partitioner"],
            "source": {
              "paragraph_indexes": [9],
              "key_phrase": "partitions functionalities into cohesive modules… cohesion and coupling"
            },
            "tags": ["modularity"]
          },
          {
            "id": "PROP-005",
            "topic": "Proposal Design",
            "instruction": "Persist functionality graph as RPG layer L0 with version <RPG_VER>.",
            "acceptance_criteria": [
              "L0 saved and diffable",
              "Checksum recorded"
            ],
            "dependencies": ["PROP-004"],
            "priority": "P0",
            "risks": ["Schema drift"],
            "mitigations": ["Migration script"],
            "tool_suggestions": ["git","graph DB"],
            "source": {
              "paragraph_indexes": [4],
              "key_phrase": "persistent and evolvable representation that unifies planning"
            },
            "tags": ["versioning"]
          },
          {
            "id": "IMPL-001",
            "topic": "Implementation Design",
            "instruction": "Map L0 modules to folder layout under <ROOT_DIR>/src as L1 folder nodes.",
            "acceptance_criteria": [
              "One folder per module",
              "Mapping table created; lints pass"
            ],
            "dependencies": ["PROP-005"],
            "priority": "P0",
            "risks": ["Over-nesting"],
            "mitigations": ["Cap depth"],
            "tool_suggestions": ["scaffolder"],
            "source": {
              "paragraph_indexes": [10],
              "key_phrase": "assign each subgraph a dedicated directory namespace"
            },
            "tags": ["folders"]
          },
          {
            "id": "IMPL-002",
            "topic": "Implementation Design",
            "instruction": "Group intermediate nodes into files to create L2 file nodes.",
            "acceptance_criteria": [
              "Files are cohesive",
              "PEP8 naming; directory size ≤ <MAX_FILES_PER_DIR>"
            ],
            "dependencies": ["IMPL-001"],
            "priority": "P0",
            "risks": ["Cross-file coupling"],
            "mitigations": ["Regroup features"],
            "tool_suggestions": ["file planner"],
            "source": {
              "paragraph_indexes": [11],
              "key_phrase": "assigning files to intermediate nodes… preserve semantic cohesion"
            },
            "tags": ["files"]
          },
          {
            "id": "IMPL-003",
            "topic": "Implementation Design",
            "instruction": "Encode inter-module data-flow edges with typed inputs and outputs.",
            "acceptance_criteria": [
              "Edges have from,to,data_id,data_type,transformation",
              "DAG validation passes"
            ],
            "dependencies": ["IMPL-001"],
            "priority": "P0",
            "risks": ["Hidden cycles"],
            "mitigations": ["Topological checks"],
            "tool_suggestions": ["DAG validator"],
            "source": {
              "paragraph_indexes": [12],
              "key_phrase": "typed input–output flows connect subgraph roots"
            },
            "tags": ["dataflow"]
          },
          {
            "id": "IMPL-004",
            "topic": "Implementation Design",
            "instruction": "Define intra-module file ordering edges for build/load constraints.",
            "acceptance_criteria": [
              "Order edges exist and have no contradictions"
            ],
            "dependencies": ["IMPL-002"],
            "priority": "P1",
            "risks": ["Brittle imports"],
            "mitigations": ["Lazy loading"],
            "tool_suggestions": ["import graph analyzer"],
            "source": {
              "paragraph_indexes": [6,12],
              "key_phrase": "intra-module file ordering… precedes… outputs propagated"
            },
            "tags": ["ordering"]
          },
          {
            "id": "IMPL-005",
            "topic": "Implementation Design",
            "instruction": "Define <BASE_CLASSES> and shared data structures for recurring patterns.",
            "acceptance_criteria": [
              "Base types justified by reuse",
              "Adoption rate ≥ <ADOPTION_RATE>"
            ],
            "dependencies": ["IMPL-003"],
            "priority": "P1",
            "risks": ["Premature abstraction"],
            "mitigations": ["Usage-driven creation"],
            "tool_suggestions": ["UML"],
            "source": {
              "paragraph_indexes": [13],
              "key_phrase": "abstracted into common data structures or base classes"
            },
            "tags": ["abstractions"]
          },
          {
            "id": "IMPL-006",
            "topic": "Implementation Design",
            "instruction": "Design one interface per leaf feature with docstring; choose func or class.",
            "acceptance_criteria": [
              "Exactly one interface/leaf",
              "Docstring has purpose, args, returns"
            ],
            "dependencies": ["IMPL-002","IMPL-003","IMPL-005"],
            "priority": "P0",
            "risks": ["Over-classing"],
            "mitigations": ["Prefer functions unless stateful"],
            "tool_suggestions": ["interface generator"],
            "source": {
              "paragraph_indexes": [14],
              "key_phrase": "independent features as functions… interdependent… shared classes"
            },
            "tags": ["interfaces"]
          },
          {
            "id": "GEN-001",
            "topic": "Build",
            "instruction": "Topologically sort RPG and create reproducible <BUILD_QUEUE>.",
            "acceptance_criteria": [
              "Queue respects edges",
              "Order persisted and reproducible"
            ],
            "dependencies": ["IMPL-003","IMPL-004"],
            "priority": "P0",
            "risks": ["Nondeterministic order"],
            "mitigations": ["Seed and persist"],
            "tool_suggestions": ["topo sort"],
            "source": {
              "paragraph_indexes": [15],
              "key_phrase": "traverses the RPG in topological order"
            },
            "tags": ["build-plan"]
          },
          {
            "id": "GEN-002",
            "topic": "Build",
            "instruction": "Auto-derive a unit test from each interface/spec before implementation.",
            "acceptance_criteria": [
              "Test executes in <TEST_RUNNER>",
              "Covers normal and edge cases"
            ],
            "dependencies": ["IMPL-006"],
            "priority": "P0",
            "risks": ["Weak tests"],
            "mitigations": ["Mutation testing"],
            "tool_suggestions": ["test generator"],
            "source": {
              "paragraph_indexes": [15],
              "key_phrase": "test-driven development… a test is derived"
            },
            "tags": ["tdd","tests"]
          },
          {
            "id": "GEN-003",
            "topic": "Build",
            "instruction": "Implement code to pass the test; commit only on green.",
            "acceptance_criteria": [
              "Unit test green locally and in CI",
              "Coverage ≥ <MIN_COV>"
            ],
            "dependencies": ["GEN-002"],
            "priority": "P0",
            "risks": ["Flaky tests"],
            "mitigations": ["Rerun policy"],
            "tool_suggestions": ["CI"],
            "source": {
              "paragraph_indexes": [15],
              "key_phrase": "Only functions that pass all tests are committed"
            },
            "tags": ["tdd","commit-policy"]
          },
          {
            "id": "GEN-004",
            "topic": "Build",
            "instruction": "Run regression tests for impacted nodes when code changes.",
            "acceptance_criteria": [
              "Impact set from graph edges",
              "All prior tests green"
            ],
            "dependencies": ["GEN-003"],
            "priority": "P0",
            "risks": ["Large impact sets"],
            "mitigations": ["Selective testing"],
            "tool_suggestions": ["test impact analyzer"],
            "source": {
              "paragraph_indexes": [17],
              "key_phrase": "Validated components trigger regression tests upon modification"
            },
            "tags": ["regression"]
          },
          {
            "id": "GEN-005",
            "topic": "Build",
            "instruction": "Create integration tests per completed subgraph before release.",
            "acceptance_criteria": [
              "Data flows executed end-to-end",
              "Contracts validated"
            ],
            "dependencies": ["GEN-003"],
            "priority": "P1",
            "risks": ["Complex orchestration"],
            "mitigations": ["Synthetic fixtures"],
            "tool_suggestions": ["integration harness"],
            "source": {
              "paragraph_indexes": [17],
              "key_phrase": "completed subgraphs undergo integration tests"
            },
            "tags": ["integration"]
          },
          {
            "id": "VAL-001",
            "topic": "Validation",
            "instruction": "Use majority-vote LLM to validate algorithm presence semantically.",
            "acceptance_criteria": [
              "5-vote majority with confidence ≥ <VOTE_THRESHOLD>"
            ],
            "dependencies": ["GEN-003"],
            "priority": "P1",
            "risks": ["Judge variance"],
            "mitigations": ["Temp=0, tie-break"],
            "tool_suggestions": ["LLM judge"],
            "source": {
              "paragraph_indexes": [17],
              "key_phrase": "majority-vote checking is applied"
            },
            "tags": ["evaluation","semantics"]
          },
          {
            "id": "VAL-002",
            "topic": "Validation",
            "instruction": "Attribute failures to code vs test/env; auto-remediate test/env cases.",
            "acceptance_criteria": [
              "Errors labeled; ≤ <N_REMEDIATIONS> auto fixes attempted"
            ],
            "dependencies": ["GEN-003"],
            "priority": "P1",
            "risks": ["Misattribution"],
            "mitigations": ["Heuristics + review"],
            "tool_suggestions": ["log analyzer"],
            "source": {
              "paragraph_indexes": [17],
              "key_phrase": "distinguishes… and automatically handling the latter"
            },
            "tags": ["triage"]
          },
          {
            "id": "VAL-003",
            "topic": "Validation",
            "instruction": "Compute Coverage, Novelty, Pass Rate, Voting Rate, Files, LOC, Tokens.",
            "acceptance_criteria": [
              "Formulas per spec implemented",
              "Results in <METRICS_STORE>"
            ],
            "dependencies": ["PROP-005","GEN-003"],
            "priority": "P0",
            "risks": ["Category drift"],
            "mitigations": ["Fixed centroids + audit"],
            "tool_suggestions": ["metrics job"],
            "source": {
              "paragraph_indexes": [19],
              "key_phrase": "Coverage… Novelty… Pass Rate… Voting Rate… code statistics"
            },
            "tags": ["metrics"]
          },
          {
            "id": "BMR-001",
            "topic": "Benchmark",
            "instruction": "Parse reference tests into <TASKS> with NL descriptions; filter trivial.",
            "acceptance_criteria": [
              "> <N_TASKS> tasks with inputs/outputs",
              "Non-algorithmic tests removed"
            ],
            "dependencies": ["DSC-001"],
            "priority": "P1",
            "risks": ["Leakage"],
            "mitigations": ["Anonymize names"],
            "tool_suggestions": ["test parser"],
            "source": {
              "paragraph_indexes": [18],
              "key_phrase": "derive tasks from reference repositories… filter out trivial"
            },
            "tags": ["benchmark","tasks"]
          },
          {
            "id": "BMR-002",
            "topic": "Benchmark",
            "instruction": "Run localization → validation → execution loop for each task.",
            "acceptance_criteria": [
              "Candidate localized or absence recorded",
              "Adapted test executed and logged"
            ],
            "dependencies": ["BMR-001","VAL-001"],
            "priority": "P1",
            "risks": ["False negatives"],
            "mitigations": ["Retry budget"],
            "tool_suggestions": ["harness runner"],
            "source": {
              "paragraph_indexes": [18],
              "key_phrase": "localization… validation… execution testing… verify correctness"
            },
            "tags": ["evaluation-loop"]
          },
          {
            "id": "MON-001",
            "topic": "Monitor",
            "instruction": "Validate DAG acyclicity and schema in CI on every RPG change.",
            "acceptance_criteria": [
              "CI blocks cycles and schema violations",
              "Error report lists offending edges"
            ],
            "dependencies": ["DSC-002","IMPL-003"],
            "priority": "P0",
            "risks": ["Slow checks"],
            "mitigations": ["Caching"],
            "tool_suggestions": ["CI job"],
            "source": {
              "paragraph_indexes": [12],
              "key_phrase": "topological order… acyclic structure"
            },
            "tags": ["ci","governance"]
          },
          {
            "id": "MON-002",
            "topic": "Monitor",
            "instruction": "Record localization tool steps and outcomes for audit.",
            "acceptance_criteria": [
              "Structured logs per step",
              "PII scrubbed; replayable"
            ],
            "dependencies": ["GEN-001"],
            "priority": "P2",
            "risks": ["Excessive volume"],
            "mitigations": ["Sampling"],
            "tool_suggestions": ["structured logging"],
            "source": {
              "paragraph_indexes": [28],
              "key_phrase": "logs… demonstrate the end-to-end process… tool invocations"
            },
            "tags": ["audit"]
          },
          {
            "id": "MON-003",
            "topic": "Governance",
            "instruction": "Run license and security checks on generated code and dependencies.",
            "acceptance_criteria": [
              "SBOM created",
              "Licenses compliant; no secrets"
            ],
            "dependencies": ["GEN-003"],
            "priority": "P0",
            "risks": ["False positives"],
            "mitigations": ["Allowlist with review"],
            "tool_suggestions": ["SBOM","license scanner","secret scanner"],
            "source": {
              "paragraph_indexes": [1],
              "key_phrase": "scalable repository generation raises practical governance needs"
            },
            "tags": ["compliance","security"]
          },
          {
            "id": "MON-004",
            "topic": "Monitor",
            "instruction": "Track feature and LOC scaling over iterations; alert on stagnation.",
            "acceptance_criteria": [
              "Dashboards for features and LOC",
              "Alert when slope < <MIN_SLOPE>"
            ],
            "dependencies": ["VAL-003"],
            "priority": "P2",
            "risks": ["Metric gaming"],
            "mitigations": ["Correlate with pass rate"],
            "tool_suggestions": ["dashboard"],
            "source": {
              "paragraph_indexes": [29],
              "key_phrase": "near-linear growth of functionalities and repository size"
            },
            "tags": ["scaling","monitoring"]
          }
        ],
        "trace_matrix": [
          { "paragraph_index": 1, "instruction_ids": ["MON-003"] },
          { "paragraph_index": 2, "instruction_ids": ["DSC-001"] },
          { "paragraph_index": 4, "instruction_ids": ["PROP-005"] },
          { "paragraph_index": 6, "instruction_ids": ["DSC-002","IMPL-004"] },
          { "paragraph_index": 7, "instruction_ids": ["DSC-003"] },
          { "paragraph_index": 8, "instruction_ids": ["PROP-001","PROP-002","PROP-003"] },
          { "paragraph_index": 9, "instruction_ids": ["PROP-004"] },
          { "paragraph_index": 10, "instruction_ids": ["IMPL-001"] },
          { "paragraph_index": 11, "instruction_ids": ["IMPL-002"] },
          { "paragraph_index": 12, "instruction_ids": ["IMPL-003","MON-001"] },
          { "paragraph_index": 13, "instruction_ids": ["IMPL-005"] },
          { "paragraph_index": 14, "instruction_ids": ["IMPL-006"] },
          { "paragraph_index": 15, "instruction_ids": ["GEN-001","GEN-002","GEN-003"] },
          { "paragraph_index": 17, "instruction_ids": ["GEN-004","GEN-005","VAL-002"] },
          { "paragraph_index": 18, "instruction_ids": ["BMR-001","BMR-002"] },
          { "paragraph_index": 19, "instruction_ids": ["VAL-003"] },
          { "paragraph_index": 28, "instruction_ids": ["MON-002"] },
          { "paragraph_index": 29, "instruction_ids": ["MON-004"] }
        ]
      }
    }


_Notes:_ IDs are unique and single-action; placeholders use ASCII angle brackets; risks/mitigations and tool suggestions are provider-agnostic. All items trace back to whitepaper passages (paragraph indices with ≤20-word key phrases). RPG_REPOSITORY_PLANNING_GRAPH

---

