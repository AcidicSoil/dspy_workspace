# Background-Orchestrated Agent with DSPy Control + Repository Planning Graph (RPG)

## 0) Scope & Summary

We specify a background agent that (a) **plans** with a Repository Planning Graph (RPG) and (b) **executes** with **DSPy** programs compiled/optimized for retrieval, tool use, and artifact write-back. The system encodes repo-scale plans as a **typed DAG** (capabilities → folders/files → functions/classes) and generates/updates code in **topological order** with **test-driven gates** and majority-vote validation; it tracks performance and cost via traces, metrics, and dashboards.

---

## 1) Inputs

* **{repo_context}** — repo name, default branch, language(s), policy constraints, owners.
* **{code_host_api}** — GitHub/GitLab/Bitbucket base URL + PAT/OAuth scopes (repo, contents, checks), rate limits.
* **{issue_tracker}** — Jira/GitHub Issues API base URL + scopes; project key/labels for evidence linking.
* **{embeddings_store}** — vector DB (e.g., pgvector/FAISS/Milvus) containing feature tree paths + embeddings.

---

## 2) RPG Model

### 2.1 Types

**Nodes** (union): `capability`, `folder`, `file`, `class`, `function`.
**Edges** (union):

* `hierarchy` (containment),
* `data_flow` (typed IO between modules),
* `order` (intra-module file/compile/load ordering).
  This dual-semantics graph aligns functional planning with concrete repo structure and enforces a **topological order** for execution.

### 2.2 Required fields

* **Node**: `{id, type, name, fqpath, doc, status∈{planned,active,done}, priority∈{P0,P1,P2}, owner, evidence[{type:issue|pr|spec, url}], version, created_at, updated_at}`
* **Edge**: `{id, type, from, to, attrs}`, where `attrs` for `data_flow` includes `{data_id, data_type, transformation}`; `order` is acyclicity-enforced.

### 2.3 JSON Schema (excerpt)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "RepositoryPlanningGraph",
  "type": "object",
  "required": ["nodes", "edges", "metadata"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["rpg_version", "created_by", "checksum"],
      "properties": {
        "rpg_version": {"type": "string"},
        "created_by": {"type": "string"},
        "checksum": {"type": "string"}
      }
    },
    "nodes": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id","type","name","status","priority"],
        "properties": {
          "id":{"type":"string"},
          "type":{"enum":["capability","folder","file","class","function"]},
          "name":{"type":"string"},
          "fqpath":{"type":"string"},
          "doc":{"type":"string"},
          "status":{"enum":["planned","active","done"]},
          "priority":{"enum":["P0","P1","P2"]},
          "owner":{"type":"string"},
          "evidence":{"type":"array","items":{"type":"object","properties":{
            "type":{"enum":["issue","pr","spec"]},"url":{"type":"string","format":"uri"}}}},
          "version":{"type":"string"},
          "created_at":{"type":"string","format":"date-time"},
          "updated_at":{"type":"string","format":"date-time"}
        }
      }
    },
    "edges": {
      "type":"array",
      "items":{
        "type":"object",
        "required":["id","type","from","to"],
        "properties":{
          "id":{"type":"string"},
          "type":{"enum":["hierarchy","data_flow","order"]},
          "from":{"type":"string"},
          "to":{"type":"string"},
          "attrs":{"type":"object"}
        }
      }
    }
  }
}
```

Acyclicity is validated on every write; versioned persistence uses `graph_store.persist(graph, version)` with checksum + URI.

### 2.4 CRUD & Versioning

* **Create/Update**: schema check → DAG check → persist; migration scripts handle schema drift (CI gate).
* **Read**: filtered by `{module|owner|status}`; support time-travel reads via `version`.
* **Delete**: soft-delete with tombstones; edge rewire blocked unless DAG remains acyclic.
* **Priority mapping**: P0/P1/P2 in RPG maps to external tracker `high/medium/low` without changing upstream fields.

### 2.5 Example (for **{sample_repo}**)

```json
{
  "metadata": {"rpg_version":"0.2.0","created_by":"agent","checksum":"sha256:..."},
  "nodes":[
    {"id":"cap.algos","type":"capability","name":"Algorithms","status":"active","priority":"P0","owner":"team-ml","evidence":[]},
    {"id":"fold.algos","type":"folder","name":"src/algos","status":"active","priority":"P0"},
    {"id":"file.linear","type":"file","name":"src/algos/linear.py","status":"planned","priority":"P0"},
    {"id":"class.base","type":"class","name":"BaseEstimator","fqpath":"src/algos/base.py:BaseEstimator","status":"active","priority":"P1"},
    {"id":"func.lasso","type":"function","name":"lasso_regression","fqpath":"src/algos/linear.py:lasso_regression","status":"planned","priority":"P0",
     "evidence":[{"type":"issue","url":"{issue_tracker}/browse/ML-42"}]}
  ],
  "edges":[
    {"id":"h1","type":"hierarchy","from":"cap.algos","to":"fold.algos"},
    {"id":"h2","type":"hierarchy","from":"fold.algos","to":"file.linear"},
    {"id":"h3","type":"hierarchy","from":"fold.algos","to":"class.base"},
    {"id":"o1","type":"order","from":"class.base","to":"file.linear"},
    {"id":"d1","type":"data_flow","from":"cap.data_loading","to":"cap.algos","attrs":{"data_id":"X,y","data_type":"ndarray"}}
  ]
}
```

This mirrors the paper’s example (data_loading → algorithms → evaluation) and uses `order` edges to coordinate file build order.

---

## 3) DSPy Programs

### 3.1 Signatures (planner, retriever, tool-caller, summarizer)

Use DSPy modules with declarative `Signature`s; each compiles to a concrete program (LLM + tools) and supports callbacks/tracing.

* **Planner** `PlanRepo(Signature)`
  Inputs: `{goal_spec, constraints, topk_exploit:int, explore_rho:float}`
  Outputs: `{modules:list, capabilities:list, rationale:str}`
  Role: exploit (vector_db.search) + explore (sample_reject) + LLM filter/merge; emits **RPG L0**.

* **Retriever** `GroundFeatures(Signature)`
  Inputs: `{queries:list[str]}` → Outputs: `{feature_paths:list, scores:list[float]}`; backs the planner’s exploit step via {embeddings_store}.

* **Tool-Caller** `BuildStep(Signature)`
  Inputs: `{rpg_slice, target_leaf}` → Outputs: `{unit_test, implementation, result}`
  Behavior: topological build queue; **derive unit test → implement → selective regression → integrate**.

* **Summarizer** `EvidenceBrief(Signature)`
  Inputs: `{run_logs, metrics}` → Outputs: `{release_notes, risks, next_actions}`; emits human-readable reports.

**Callbacks/Tracing.** Register DSPy callbacks (e.g., to log ReAct steps) and enable MLflow autolog to capture **optimizer params, program states, datasets, traces**. Do **not** mutate inputs/outputs in callbacks; copy first.

### 3.2 Optimization & Evaluation

* Optimize prompts & few-shot sets with DSPy optimizers; track progress/metrics via MLflow (`mlflow.dspy.autolog()`), including intermediate prompts and trial metrics.
* Program-level evaluation uses majority-vote semantic checks (n=5; 2 rounds) + execution tests; record pass/vote/coverage metrics per RepoCraft style.

### 3.3 Caching & Failure Recovery

* **Caching:**

  * Retrieval cache keyed by `{goal_spec hash, topk, rho}`.
  * Tool outputs cached by `{leaf_id, signature_hash}` with TTL.
  * Prompt/result cache in artifact store; invalidate on `rpg_version` change.
* **Recovery:**

  * Tool retries with exponential backoff (2 attempts), stop on budget/walltime breach.
  * Failure attribution pipeline: **impl vs test/env**, auto-remediate env/test, escalate otherwise.

---

## 4) Execution Flow

### 4.1 Event triggers → pipeline

* **Triggers:** repo push, issue label (`agent:plan`), webhook from {issue_tracker}, or cron.
* **Flow (ASCII):**

```
[Trigger] -> [Planner: exploit+explore+merge -> RPG L0]
            -> [Implementer: folders/files + data_flows + order -> RPG Full]
            -> [Builder: topo queue -> (unit -> implement -> regression) -> integration]
            -> [Verifier: vote + metrics + diagnosis]
            -> [Report/Release or Iterate/Escalate]
```

This is the canonical three-stage pipeline with topological traversal and test gates.

### 4.2 Program compile/run → artifact write-back

* Compile DSPy programs with current config; run with callbacks & MLflow.
* **Artifacts**: `<RPG_L0.json>`, `<RPG_FULL.json>`, code diffs, tests, `<EVAL_REPORT>`, `<METRICS.json>`, release notes.
* Persist RPG versions and repo changes; emit CI checks.

### 4.3 Telemetry

* **Logging fields**: `ts, run_id, agent, tool, input_hash, output_hash, duration_ms, cost, redactions[]`; redact PII; store raw in vault.

---

## 5) Observability

### 5.1 Traces & Metrics

* **Traces**: DSPy MLflow integration captures optimizer params, prompt states, datasets, execution traces, and model responses.
* **Metrics**: Coverage, Novelty, Pass Rate, Voting Rate, Files, LOC, Tokens—computed per definitions; store in metrics store.

### 5.2 Cost

* Log **token/compute** per tool call and total **cost** per stage; enforce budget gates at orchestration layer.

### 5.3 Minimal Dashboard (widgets)

* **Run Summary:** pass/vote %, latency P50/P95, cost/run.
* **Plan Health:** L0/L1/L2 diff, DAG validity, coverage trend.
* **Scaling Charts:** near-linear growth expectations for features/LOC; alert on plateau.

---

## 6) Interfaces

### 6.1 CLI (examples)

```
rpg plan --goal "{repo_context}" --k 50 --rho 0.2 --out rpg_l0.json
rpg implement --in rpg_l0.json --out rpg_full.json
rpg build --graph rpg_full.json --select leaf:func.lasso
rpg verify --repo . --tasks tasks.json --out metrics.json
```

Backed by the tool catalog: `vector_db.search`, `feature_tree.sample_reject`, `graph_store.persist`, `graph.validate_dag`, `tests.run`, `evaluator.vote`, `metrics.compute`.

### 6.2 REST (excerpt)

* `POST /rpg/v1/plan` → `{rpg_l0_uri, checksum}`
* `POST /rpg/v1/implement` → `{rpg_full_uri}`
* `POST /rpg/v1/build` → `{run_id, artifacts[]}`
* `POST /rpg/v1/verify` → `{metrics}`
* `GET /rpg/v1/graphs/{version}` → graph JSON

### 6.3 Webhooks

* **/events/code_host** (push, PR, check_run)
* **/events/issue_tracker** (label, state change)

### 6.4 Auth

* REST: OAuth2 (client creds) or PAT; Webhooks: HMAC secret; tool adapters inherit upstream auth scopes (read/write/approve gates). HITL required on sensitive ops.

---

## 7) Test Plan

### 7.1 Unit (RPG ops)

* **Schema**: validate node/edge enums and required fields.
* **DAG**: cycle detection on `order` and `data_flow`.
* **CRUD**: versioned persist + checksum; migration diff test.

### 7.2 Golden tasks (DSPy)

* Fixed seed/intents & expected summaries; evaluate Planner filter/merge quality and Builder tool-use; track via MLflow.

### 7.3 E2E Scenario

* Trigger → L0 → Full → Build (unit→regression→integration) → Verify (vote+execute) → Release; assert artifact set & metrics computed.

### 7.4 Load

* Concurrent topo builds: cap parallelism to `min(CPU_CORES, MAX_PARALLEL_NODES)`; tool retries with backoff (2). SLA alarms on latency/cost breach.

### 7.5 Rollback plan

* Revert to last **green** RPG tag; lock writes; RCA with evidence bundle (logs, votes, failing tests, metrics deltas).

---

## 8) Acceptance Criteria (**{acceptance_criteria}**)

* **Plan correctness ≥ {x}% on {n} tasks**, measured via vote-then-execute harness.
* **P50 end-to-end latency ≤ {y} min** from trigger to release notes.
* **Reproducible traces**: MLflow run with optimizer params, prompt states, datasets, and execution traces present.
* **No DAG cycles**, contracts documented, and selective regression on edits executed.

---

## 9) Out-of-Scope (**{non_goals}**)

Provider-specific API quirks, model leaderboards/benchmarks replication beyond stated KPIs, and bespoke UI/UX design; focus remains on provider-agnostic RPG + DSPy orchestration.

---

## 10) Deliverables

### 10.1 Diagram(s) (ASCII)

```
User/Events
   │
   ▼
[Planner] --(vector_db.search + sample_reject + filter/merge)--> RPG L0
   │
   ▼
[Implementer] --(folders/files + data_flow + order + validate_dag)--> RPG Full
   │
   ▼
[Builder] -- topo queue --> [Unit → Implement → Regression] → [Integration]
   │
   ▼
[Verifier] -- vote + execute --> Metrics
   │
   └──> Reports/Release ──> Next Iteration
```

### 10.2 Example Configs

**Agent spec (YAML snippet)**

```yaml
planner:
  k_exploit: 50
  rho_explore: 0.2
  coverage_target: 0.8
builder:
  max_parallel_nodes: 4
  retries: 2
  budgets:
    max_walltime_min: 30
    max_cost_usd: 5.00
metrics:
  vote_threshold: 0.6
  acceptance:
    pass_rate: 0.6
    coverage: 0.8
```

(Parallelism, retries, and gates map to scheduling & quality policies.)

**Feature-tree seed dataset (local)**
`docs/featureTreeSeed.local.json` (ships with repo) — used to bootstrap retrieval when the global tree isn’t available.

### 10.3 Sample Prompts

* **Planner::filter_merge** — “Given goal `{repo_context}`, dedupe candidates, propose missing features, self-check, and partition into cohesive modules; output `{modules, capabilities, rationale}`.” (Implements PROP-003/004.)
* **Builder::unit_test_gen** — “Given interface `{FQN}` and docstring, emit pytest that validates contract & happy-path behavior only.” (GEN-002.)

### 10.4 Seed Task Set

* Derive **golden tasks** by parsing upstream test trees or curated specs; retain NL task descriptions + IO signatures for vote-then-execute evaluation.

---

## 11) Implementation Notes (operational guardrails)

* Always **validate DAG** after adding `order`/`data_flow` edges; block on cycles.
* **Topological build** + **TDD**: derive unit test first; commit only on green; run **selective regression** on impacted nodes; add **integration tests** per completed subgraph.
* **Majority-vote** + diagnosis separates implementation vs env/test failures; cap remedations and escalate with an evidence bundle.
* **Tracing**: enable MLflow for optimizer + program states + traces; use DSPy callbacks to log intermediate reasoning/acting safely (copy inputs).

---

### Appendix: Why RPG + DSPy?

RPG replaces ambiguous NL plans with a **persistent, evolvable** representation spanning proposal→implementation (capabilities, folders/files, interfaces, typed flows & order), enabling **long-horizon** scaling and coherent execution; code is generated in topo order with test gates and vote-then-execute validation.

**End of design doc.**
