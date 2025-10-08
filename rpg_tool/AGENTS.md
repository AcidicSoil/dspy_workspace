# AGENTS.md — {{primary_purpose}}

## 1) Title & Scope

**Scope.** This playbook operationalizes the Repository Planning Graph (RPG) + ZeroRepo method to **plan → build → validate** complete software repositories using a persistent graph that unifies proposal- and implementation-level planning, and graph-guided TDD.
**Assumptions.** {{environment}} provides access to <VECTOR_DB>, <GRAPH_STORE>, <RUNTIME>, <CI>, and <ARTIFACT_STORE>.
**Non-goals.** Provider-specific APIs, model choices, or benchmark replication beyond KPIs defined in {{kpis}}.

---

## 2) System Overview

- **Operating Model.** **Observe → Plan → Act → Verify → Report → (Escalate/Iterate)**.
  RPG encodes capabilities, folders/files, interfaces, and data/data-flow edges; code is generated **in topological order** with **test-driven development** (unit → regression → integration).
- **Autonomy.** {{autonomy}} with HITL gates specified below.
- **Environment.** {{environment}} (repos, data sources, deployment targets).

---

## 3) Agent Roster

For each agent: **Name • Role • Primary Goals • Inputs • Outputs • Success Signals**

1. **Planner** • planning

   - **Goals:** Convert {{primary_purpose}} into an **RPG L0** functionality graph using explore–exploit retrieval from a global Feature Tree; refactor into cohesive modules.
   - **Inputs:** <GOAL_SPEC>, <CONSTRAINTS>, <FEATURE_TREE>, <VECTOR_DB>
   - **Outputs:** <RPG_L0.json> (modules, capabilities), <RISK_LOG>
   - **Success:** Coverage of required functional categories ≥ <COVERAGE_TARGET>.

2. **Implementer** (Executor) • implementation design

   - **Goals:** Map L0 to **folders/files (L1/L2)**; encode **typed inter-module data flows** and **intra-module file ordering**; define leaf interfaces (func/class).
   - **Inputs:** <RPG_L0.json>
   - **Outputs:** <RPG_FULL.json> (folders/files, edges, interfaces), <SKELETON_REPO>
   - **Success:** DAG validation passes; interface docs complete.

3. **Builder** (Executor) • code generation

   - **Goals:** Topologically traverse RPG; **derive tests first**, then implement to green; run selective regression; add integration tests per subgraph.
   - **Inputs:** <RPG_FULL.json>, <TEST_PROMPTS>
   - **Outputs:** <SRC_CODE>, <UNIT_TESTS>, <INTEG_TESTS>
   - **Success:** Pass rate ≥ <PASS_RATE_TARGET>; no broken dependents.

4. **Verifier** • validation & metrics

   - **Goals:** Majority-vote semantic checks for algorithm presence; attribute failures (impl vs test/env); compute Coverage/Novelty/Pass/Voting/LOC/Files/Tokens.
   - **Inputs:** <SRC_CODE>, <TEST_RESULTS>, <TASK_SET>
   - **Outputs:** <EVAL_REPORT>, <METRICS.json>, <DIAGNOSIS_LOG>
   - **Success:** Voting agreement ≥ <VOTE_RATE_TARGET>; metrics computed as spec.

5. **Orchestrator** • coordination

   - **Goals:** Schedule DAG execution, enforce budgets/timeouts, trigger escalations/HITL.
   - **Inputs:** All artifacts above
   - **Outputs:** <RUN_LOG>, <ALERTS>
   - **Success:** SLA conformance: latency ≤ <SLA_LATENCY>, cost ≤ <SLA_BUDGET>.

6. *(Optional)* **Retriever** • knowledge grounding

   - **Goals:** Manage Feature Tree search, diversity-aware exploration, LLM filtering and merge.

7. *(Optional)* **Localizer** • graph-guided search/edit

   - **Goals:** Locate target code via functionality → repository navigation; support graph-guided edits.

---

## 4) Tooling & Permissions

### Tool Catalog

*(Provider-agnostic; replace with {{tools}} where available.)*

1. **vector_db.search**

- **Intent:** Retrieve top-k feature paths (exploit).
- **Input Schema:** `{"query":"<TEXT>","k":<INT>,"filters":{}}`
- **Output Schema:** `{"paths":[{"path":"a/b/c","score":<FLOAT>}]}`
- **Side Effects:** none; reads <VECTOR_DB>
- **Limits/Costs:** <QPS_LIMIT>, <BUDGET_PATH_SEARCH>
- **Failure Modes:** skewed recall, latency spikes
- **Example:** `vector_db.search({"query": "<GOAL_SPEC>", "k": 50})`
- **Source:** Proposal retrieval.

2. **feature_tree.sample_reject**

- **Intent:** Diversity-aware exploration with overlap threshold ρ and retries.
- **Input:** `{"root":"<NODE>","rho":<FLOAT>,"tmax":<INT>}`
- **Output:** `{"paths":[...]}`
- **Side Effects:** none
- **Failure:** insufficient diversity
- **Example:** `feature_tree.sample_reject({"root":"root","rho":0.2,"tmax":10})`
- **Source:** Rejection sampling algorithm.

3. **llm.filter_merge**

- **Intent:** Filter, rank, dedupe candidates; propose missing features; batch self-check.
- **Input:** `{"candidates":[...],"context":{"tree":"<JSON>"}}`
- **Output:** `{"accepted":[...],"rationales":[...]}`
- **Side Effects:** audit log
- **Failure:** drift/inconsistency
- **Example:** `llm.filter_merge({...})`
- **Source:** LLM filtering + self-check.

4. **graph_store.persist**

- **Intent:** Versioned save of RPG L0/L1/L2/full.
- **Input:** `{"graph":"<RPG_JSON>","version":"<RPG_VER>"}`
- **Output:** `{"checksum":"<HEX>","uri":"<URI>"}`
- **Side Effects:** writes <GRAPH_STORE>
- **Failure:** schema mismatch
- **Example:** `graph_store.persist({...})`
- **Source:** Persistent representation.

5. **graph.validate_dag**

- **Intent:** Enforce acyclicity; check inter-/intra-module constraints.
- **Input:** `{"graph":"<RPG_JSON>"}`
- **Output:** `{"ok":true,"errors":[]}`
- **Side Effects:** CI gate
- **Failure:** cycles/contradictions
- **Example:** `graph.validate_dag({...})`
- **Source:** Typed flows & topological order.

6. **repo.scaffold**

- **Intent:** Map modules→folders; features→files; generate skeleton.
- **Input:** `{"graph":"<RPG_L1/L2>","root":"<PATH>"}`
- **Output:** `{"paths":[...]}`
- **Side Effects:** writes <SKELETON_REPO>
- **Failure:** over-nesting
- **Source:** File/folder encoding.

7. **tests.unit.generate**

- **Intent:** Derive unit test from interface/spec docstring.
- **Input:** `{"interface":"<FQN>","spec":"<DOC>"}`
- **Output:** `{"test_file":"<PATH>","code":"<STR>"}`
- **Side Effects:** writes tests
- **Failure:** weak coverage
- **Source:** TDD at leaf nodes.

8. **tests.run**

- **Intent:** Execute unit/regression/integration suite; selective by graph impact.
- **Input:** `{"scope":["unit|regression|integration"],"targets":[...],"impact_from_graph":true}`
- **Output:** `{"pass":<BOOL>,"log":"<URI>","failures":[...]}`
- **Side Effects:** CI status
- **Failure:** env flakiness
- **Source:** Regression & integration gates.

9. **evaluator.vote**

- **Intent:** Majority-vote semantic validation (n=5; 2 rounds).
- **Input:** `{"candidate":"<CODE_URI>","task":"<DESC>"}`
- **Output:** `{"votes":5,"agree":<INT>,"confidence":<FLOAT>}`
- **Side Effects:** cost tokens
- **Failure:** judge variance
- **Source:** Majority-vote validation.

10. **metrics.compute**

- **Intent:** Coverage, Novelty, Pass Rate, Voting Rate, Files, LOC, Tokens (per D.3.1).
- **Input:** `{"repo_uri":"<URI>","taxonomy":"<REF>"}`
- **Output:** `{"coverage":...,"novelty":...,"pass":...,"voting":...,"files":...,"loc":...,"tokens":...}`
- **Side Effects:** writes <METRICS_STORE>
- **Failure:** category drift
- **Source:** Metrics definitions.

11. **rpg.localize / repo.view / dep.trace**

- **Intent:** Graph-guided localization (functionality→code), interface view, dependency trace.
- **Schemas:** simple `{ "query":"<TEXT|FEATURE_PATH>" }` → list of FQNs/paths.
- **Source:** Localization toolset.

12. **governance.scan**

- **Intent:** SBOM, licenses, secrets scan.
- **Source:** Governance risk mitigation (derived).

### Permission Matrix (excerpt)

| Agent \ Tool | vector_db.search | feature_tree.sample_reject | graph_store.persist | tests.run | evaluator.vote | governance.scan |
| ------------ | ---------------: | -------------------------: | ------------------: | --------: | -------------: | --------------: |
| Planner      |            ✅read |                      ✅read |                   ⛔ |         ⛔ |              ⛔ |               ⛔ |
| Implementer  |                ⛔ |                          ⛔ |              ✅write |         ⛔ |              ⛔ |               ⛔ |
| Builder      |                ⛔ |                          ⛔ |                   ⛔ |     ✅exec |              ⛔ |               ⛔ |
| Verifier     |                ⛔ |                          ⛔ |                   ⛔ |     ✅exec |          ✅exec |           ✅exec |
| Orchestrator |           ✅audit |                     ✅audit |            ✅approve |  ✅approve |       ✅approve |        ✅approve |

Sensitive ops (**write/exec/approve**) require HITL if <RISK_LEVEL> ≥ <HITL_THRESHOLD>.

---

## 5) Task Graph & Protocols

### Goal Decomposition (ASCII DAG)

```
[Observe Spec]
   ↓
[Planner: RPG L0 (exploit+explore)]  --> [HITL-Approve?] -->
   ↓
[Implementer: Folders/Files + DataFlows + Interfaces → RPG Full]
   ↓
[Builder: Topo Build Queue → (Unit Test → Implement → Regression) → Integration Tests]
   ↓
[Verifier: Vote + Metrics + Diagnosis]
   ↓
[Report/Release or Iterate/Escalate]
```

**Source:** Three-stage pipeline + topo traversal + testing.

### Message Contracts

- **Request (agent→agent):** `{id, from, to, intent, content, constraints[], artifacts[], deadline, budget}`
- **Response:** `{id, in_reply_to, status, summary, artifacts[], metrics{}, notes}`

- **Error:** `{id, in_reply_to, error_code, error_class, evidence_uri}`

### Scheduling

- **Concurrency:** Max parallelism = min(<CPU_CORES>, <MAX_PARALLEL_NODES>), **respect DAG order**.
- **Retries/Backoff:** Tool-call retries: 2 with exponential backoff (1×, 2×).
- **Time bounds:** <MAX_STAGE_LATENCY> per stage; **stop** on budget/latency breach.

---

## 6) Standard Operating Procedures (SOPs)

### SOP: **Plan** — task breakdown & risk scan

- **WHEN:** <GOAL_SPEC> received.
- **DO:**

  1. Retrieve top-k exploit paths from <VECTOR_DB>.
  2. Sample explore paths via diversity-aware rejection (ρ).
  3. LLM filter/merge; propose missing features; batch self-check; log rationales.
  4. Refactor to cohesive modules (maximize cohesion/minimize coupling).
  5. Persist as **RPG L0** (versioned).
- **CHECK:** `<COVERAGE> ≥ <COVERAGE_TARGET>`; modules non-overlapping; rationale log present.
- **IF FAIL:** Increase k/ρ; expand synonyms; induce missing features; re-run 1–4.
- **ARTIFACTS:** <RPG_L0.json>, <PLAN_LOG>
- **SOURCE:** ¶3.2/Alg.2 “exploit–explore + filter/merge”; ¶3.1 dual-semantics note.

### SOP: **Gather** — retrieval, freshness, provenance

- **WHEN:** Planner requests grounding.
- **DO:**

  1. Ensure Feature Tree embeddings loaded with paths/meta.
  2. Run vector_db.search and sample_reject; attach scores/overlap stats.
  3. Record provenance (source tree node IDs, timestamps).
- **CHECK:** Query latency ≤ <EMBED_QPS>; provenance complete.
- **IF FAIL:** Rebuild embeddings; partition index; cache hot queries.
- **ARTIFACTS:** <RETRIEVAL_LOG>, <PROVENANCE_CSV>
- **SOURCE:** Feature Tree embeddings + metadata.

### SOP: **Build/Execute** — implementation & graph-guided TDD

- **WHEN:** RPG L0 approved.
- **DO:**

  1. Map modules→folders; features→files; create skeleton.
  2. Encode typed inter-module data flows and intra-module file ordering; validate DAG.
  3. Design leaf interfaces (func/class) with docstrings; no bodies.
  4. **Topologically** sort RPG into <BUILD_QUEUE>.
  5. For each leaf: **generate unit test → implement → run → commit only on green**.
  6. On edits: run **selective regression** (impacted parents/children).
  7. For completed subgraphs: add **integration tests**.
- **CHECK:** DAG passes; unit pass ≥ <UNIT_PASS_TARGET>; coverage ≥ <MIN_COV>.
- **IF FAIL:** Localize via rpg.localize/repo.view/dep.trace; patch; rerun tests.
- **ARTIFACTS:** <RPG_FULL.json>, <SRC_CODE>, <TESTS>, <CI_REPORT>
- **SOURCE:** §3.3, §4 (topo + TDD + regression/integration).

#### Testing Pitfalls & Guardrails

##### Common pitfalls

- Writing tests that are tied to implementation details (fragile).
- Over-specifying: testing how instead of what.
- Giant steps: skipping the tiny loop, leading to long failing streaks.
- Mocking everything: lose real behavior; mock only true boundaries.

##### Guardrails that make it work

- Keep acceptance tests few and slow but critical; keep unit tests many and fast.
- Contracts are versioned (backward-compatible by default); breaking changes require a contract test update first.
- Make failures actionable: test names read like requirements, outputs diff JSON bodies/schemas, not logs.

### SOP: **Validate** — metrics & policy checks

- **WHEN:** Build completes for milestone/subgraph.
- **DO:**

  1. Majority-vote semantic check (5 votes; 2 rounds) per task.
  2. Attribute failures: **impl vs test/env**; auto-remediate latter.
  3. Compute **Coverage, Novelty, Pass, Voting, Files, LOC, Tokens** as D.3.1.
  4. Run license/secret scan; generate SBOM.
- **CHECK:** `<PASS_RATE> ≥ <PASS_RATE_TARGET>`, `<VOTING_RATE> ≥ <VOTE_RATE_TARGET>`, no license/sec violations.
- **IF FAIL:** Escalate with evidence bundle; increase retries for env/test up to <N_REMEDIATIONS>.
- **ARTIFACTS:** <EVAL_REPORT>, <METRICS.json>, <SBOM>, <GOV_REPORT>
- **SOURCE:** §5/§D.3.1 metrics; validation pipeline.

### SOP: **Deliver/Report** — release & handoff

- **WHEN:** Metrics hit thresholds or HITL approves.
- **DO:**

  1. Emit release notes: scope, build hash, metrics deltas, known issues.
  2. Publish artifacts to <ARTIFACT_STORE>; tag <RPG_VER>.
  3. Schedule next iteration if coverage gap or backlog exists.
- **CHECK:** Artifacts present; checksums match; dashboards updated.
- **IF FAIL:** Rollback to previous green tag; notify stakeholders.
- **ARTIFACTS:** <RELEASE_NOTES>, <ARTIFACT_MANIFEST>
- **SOURCE:** Persistent RPG & staged iteration.

### SOP: **Monitor** — drift & review cadence

- **WHEN:** Post-release or nightly.
- **DO:**

  1. Enforce DAG/schema validation on every RPG change via CI.
  2. Track near-linear scaling of features/LOC; alert on plateau.
  3. Log localization/tool calls for audit; redact PII.
- **CHECK:** CI clean; slope ≥ <MIN_SLOPE>; audit logs ≥ <MIN_LOG_FIELDS>.
- **IF FAIL:** Quarantine change; root-cause; schedule fix.
- **ARTIFACTS:** <CI_LOGS>, <SCALING_DASHBOARD>, <AUDIT_LOG>
- **SOURCE:** Topological CI; scalability analyses; logging examples.

---

## 7) Decision Policies & Guardrails

- **Quality Gates:**

  - `<PASS_RATE> ≥ <PASS_RATE_TARGET>`; `<VOTING_RATE> ≥ <VOTE_RATE_TARGET>`; `<COVERAGE> ≥ <COVERAGE_TARGET>`; `<NOVELTY> ≤ <NOVELTY_MAX>` unless explicitly allowed.
- **Safety Checks:**

  - Enforce license policy; secrets = 0; SBOM emitted; PII redaction in logs.
- **Cost/Time Budgets:**

  - `<MAX_TOOL_CALLS>`, `<MAX_TOKENS>`, `<MAX_WALLTIME>` per stage; **terminate** on breach with evidence bundle.
- **Escalation Matrix:**

  - *What:* DAG cycles, persistent test/env failures, metric shortfall > <DELTA_THRESHOLD>.
  - *To whom:* {{human_roles}} (PM/Eng/QA/Legal/SME).
  - *Bundle:* `{context, diffs, failing tests, votes, logs, metrics_delta}`.
- **Termination Conditions:**

  - All gates green **or** budget exhausted **or** HITL stop; handoff includes <RPG_FULL.json>, code, tests, metrics.

---

## 8) Collaboration Playbooks

- **Multi-Agent Pattern:** `Planner → Implementer → Builder → Verifier` loop until gates pass; max <N_LOOPS>.
- **Consensus/Critique:** Verifier may trigger 1 critique round with <N_CRITICS>; if unresolved → HITL.
- **HITL Interfaces:** Approval prompts include `{summary, changes, risks, budgets, diffs, metrics}`; “request changes” restarts from affected stage only.
- **Communication Etiquette:** Keep messages ≤ <512 tokens>; include `id, intent, constraints, artifacts`.

---

## 9) Observability & Artifacts

- **Logging Fields:** `ts, run_id, agent, tool, input_hash, output_hash, duration_ms, cost, redactions[]`.
- **Redaction Policy:** Strip PII/secrets; hash examples; store raw only in quarantined vault.
- **Artifacts:**

  - Naming: `<proj>-<stage>-<yyyymmdd>-<hash>.<ext>`; store in `<ARTIFACT_STORE>/<stage>/`.
- **Dashboards/Reviews:**

  - Charts: Coverage, Pass/Vote, LOC growth (expect near-linear under RPG), failure classes; weekly review.

---

## 10) Error Handling & Recovery

- **Error Classes:** `validation`, `quota`, `tool`, `network`, `policy`.
- **Playbooks:**

  - `validation`: localize→fix→rerun tests.
  - `quota`: backoff, reduce k/ρ, compress context.
  - `tool`: retry (2), alternate endpoint, stub.
  - `network`: retry with jitter; cache results.
  - `policy`: quarantine, notify Legal, redact & re-run.
- **Rollback:** Revert to last **green** tag (<RPG_VER_prev>); lock write ops until RCA complete.

---

## 11) Configuration Templates

### Agent Spec (YAML)

```yaml
agents:
  - name: Planner
    role: planning
    inputs: [<GOAL_SPEC>, <CONSTRAINTS>]
    outputs: [<RPG_L0.json>, <RISKS>]
    permissions: [read.vector_db, plan, write.plan_log]
  - name: Implementer
    role: implementation
    inputs: [<RPG_L0.json>]
    outputs: [<RPG_FULL.json>, <SKELETON_REPO>]
    permissions: [write.graph, write.repo, validate.dag]
  - name: Builder
    role: build
    inputs: [<RPG_FULL.json>]
    outputs: [<SRC_CODE>, <TESTS>]
    permissions: [exec.tests, write.code]
  - name: Verifier
    role: verify
    inputs: [<SRC_CODE>, <TEST_RESULTS>, <TASK_SET>]
    outputs: [<EVAL_REPORT>, <METRICS.json>]
    permissions: [exec.vote, exec.metrics, exec.governance]
tools:
  - name: vector_db.search
    intent: retrieve exploit paths
    input_schema: {query: <TEXT>, k: <INT>}
    output_schema: {paths: [<PATH_OBJ>]}
    limits: {rate: <N/min>, budget: <$MAX>}
policies:
  quality_gates:
    - metric: pass_rate
      threshold: <PASS_RATE_TARGET>
    - metric: coverage
      threshold: <COVERAGE_TARGET>
```

### Message Contract (JSON)

```json
{
  "id": "<UUID>",
  "from": "<AGENT>",
  "to": "<AGENT|HUMAN>",
  "intent": "<PLAN|EXECUTE|VERIFY|ESCALATE>",
  "content": "<BRIEF>",
  "constraints": ["<RULE1>", "<RULE2>"],
  "artifacts": ["<URI1>", "<URI2>"]
}
```

---

## 12) Examples (Few-Shot)

**Example A — Planner → Builder handoff**

- **Planner output (abridged):**
  `RPG_L0.json` with modules `{algorithms, evaluation, data_loading}` and candidate paths (k=50 exploit + explore set), refactored into cohesive modules. *(Source: proposal-level construction)*
- **Implementer:** maps to `src/algos`, `src/eval`, `src/data_load`; assigns files; encodes flows `data_load → algos → eval`; defines interfaces `DataLoader`, `LinearModels`.
- **Builder:** topo queue then (unit test → implement → commit on green).

**Example B — Verifier blocks & escalates**

- Voting confirms presence (4/5) but **execution fails**; diagnosis labels **test/env** → auto remediation; if still failing, **escalate** with logs, diffs, and metrics to QA.

---

## 13) Traceability

Below are key sources used; each SOP/policy/tool above includes an inline **SOURCE** with paragraph cue.

- **RPG Structure & Dual Semantics; Inter-/Intra- edges; Topological Order.** §3.1 (“nodes specify… files/classes/functions… edges encode data flows/order”).
- **Proposal-Level Construction:** Feature Tree embeddings; exploit–explore; LLM filter/merge; refactor by cohesion/coupling; Algorithm 2.
- **Implementation-Level Construction:** Folder/file encoding; typed flows; adaptive interfaces (func vs class).
- **Graph-Guided Generation:** Topological traversal; **TDD**; regression & integration testing.
- **Localization & Editing Tools:** rpg-guided search, repo view, dependency exploration.
- **Validation Pipeline:** Majority-vote semantic check; failure attribution; remediation loops.
- **Metrics:** Coverage, Novelty, Pass, Voting, Files/LOC/Tokens (Appendix D.3.1).
- **Governance Additions (SBOM, licenses, secrets):** operational risk mitigation derived in build guide.
- **Scalability & Monitoring:** Near-linear growth expectations; CI DAG validation; logging exemplars.

---

## 14) Temporary Priority Dual-Labeling (Taskmaster + RPG)

**Goal:** Use Taskmaster’s priority for scheduling while making the RPG priority explicit—without changing Taskmaster’s schema.

**Authoritative field (unchanged):** `priority` ∈ `{high, medium, low}`
**RPG mapping:** `P0→high`, `P1→medium`, `P2→low`

### What to do (apply to every task and subtask)

1. **Prefix the title (visible)**

   - Format: `[P*] <Title>`
   - Optional ID: `[P*|<RPG_ID>] <Title>`
   - Examples: `[P0] Initialize repo`, `[P1|DSC-001] Define project spec`

2. **Stamp the details (machine-friendly)**

   - Insert as the **first line** of `details`:

     - `RPG_PRIORITY=P*`
     - Optional: `RPG_ID=<RPG_ID>` on the next line
   - Preserve the rest of `details` as-is after a blank line.

### Do / Don’t

- ✅ **Do** keep `priority` exactly `high|medium|low`.
- ✅ **Do** dual-label with `[P*]` in `title` **and** `RPG_PRIORITY=P*` in `details`.
- ✅ **Do** let subtasks inherit the parent’s P* if their own `priority` is missing.
- ❌ **Don’t** add new top-level fields (e.g., `rpg_priority`) or wrappers.
- ❌ **Don’t** rename or re-case Taskmaster’s `priority` values.

### Quick reference

| RPG | Taskmaster `priority` | Title Prefix | Details Stamp     |
| --- | --------------------- | ------------ | ----------------- |
| P0  | high                  | `[P0]`       | `RPG_PRIORITY=P0` |
| P1  | medium                | `[P1]`       | `RPG_PRIORITY=P1` |
| P2  | low                   | `[P2]`       | `RPG_PRIORITY=P2` |

### Example (before → after)

**Before**

```json
{
  "title": "Initialize repository",
  "priority": "high",
  "details": "Create repo, add README.",
  "subtasks": [
    { "title": "Add CI", "priority": "medium", "details": "Set up basic workflow." }
  ]
}
```

**After**

```json
{
  "title": "[P0] Initialize repository",
  "priority": "high",
  "details": "RPG_PRIORITY=P0\n\nCreate repo, add README.",
  "subtasks": [
    {
      "title": "[P1] Add CI",
      "priority": "medium",
      "details": "RPG_PRIORITY=P1\n\nSet up basic workflow."
    }
  ]
}
```

**Validation checklist (agents):**

- Title starts with `[P0]`, `[P1]`, or `[P2]`.
- `details` first line is `RPG_PRIORITY=P*`.
- Taskmaster `priority` untouched and consistent with the P* mapping.
- No extra top-level fields added.

---

**End of AGENTS.md**
