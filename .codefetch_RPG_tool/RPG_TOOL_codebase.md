Project Structure:
├── AGENTS.md
├── GEMINI.md
├── README.md
├── RPG_REPOSITORY_PLANNING_GRAPH-parsed.json
├── RPG_REPOSITORY_PLANNING_GRAPH.pdf
├── RPG_build_guide.md
├── codefetch.config.mjs
├── docs
│   ├── PROJECT_SPEC.example.md
│   ├── PROJECT_SPEC.template.md
│   ├── featureTreeSeed.local.json
│   └── propCandidates.v1.json
├── execution-order.md
├── quick-reference-execution-guide.md
├── rpg-vector-index
│   ├── README.md
│   ├── sql
│   │   └── pgvector_schema.sql
│   └── tests
│       ├── test_faiss_index.py
│       └── test_schema_mapping.py
└── templates
    └── RPG-prompt-tool_templates.md


.browser-echo-mcp.json
```
1 | {"url":"http://127.0.0.1:44571","route":"/__client-logs","timestamp":1759353551411,"pid":823715}
```

AGENTS.md
```
1 | # AGENTS.md — {{primary_purpose}}
2 | 
3 | ## 1) Title & Scope
4 | 
5 | **Scope.** This playbook operationalizes the Repository Planning Graph (RPG) + ZeroRepo method to **plan → build → validate** complete software repositories using a persistent graph that unifies proposal- and implementation-level planning, and graph-guided TDD.
6 | **Assumptions.** {{environment}} provides access to <VECTOR_DB>, <GRAPH_STORE>, <RUNTIME>, <CI>, and <ARTIFACT_STORE>.
7 | **Non-goals.** Provider-specific APIs, model choices, or benchmark replication beyond KPIs defined in {{kpis}}.
8 | 
9 | ---
10 | 
11 | ## 2) System Overview
12 | 
13 | - **Operating Model.** **Observe → Plan → Act → Verify → Report → (Escalate/Iterate)**.
14 |   RPG encodes capabilities, folders/files, interfaces, and data/data-flow edges; code is generated **in topological order** with **test-driven development** (unit → regression → integration).
15 | - **Autonomy.** {{autonomy}} with HITL gates specified below.
16 | - **Environment.** {{environment}} (repos, data sources, deployment targets).
17 | 
18 | ---
19 | 
20 | ## 3) Agent Roster
21 | 
22 | For each agent: **Name • Role • Primary Goals • Inputs • Outputs • Success Signals**
23 | 
24 | 1. **Planner** • planning
25 | 
26 |    - **Goals:** Convert {{primary_purpose}} into an **RPG L0** functionality graph using explore–exploit retrieval from a global Feature Tree; refactor into cohesive modules.
27 |    - **Inputs:** <GOAL_SPEC>, <CONSTRAINTS>, <FEATURE_TREE>, <VECTOR_DB>
28 |    - **Outputs:** <RPG_L0.json> (modules, capabilities), <RISK_LOG>
29 |    - **Success:** Coverage of required functional categories ≥ <COVERAGE_TARGET>.
30 | 
31 | 2. **Implementer** (Executor) • implementation design
32 | 
33 |    - **Goals:** Map L0 to **folders/files (L1/L2)**; encode **typed inter-module data flows** and **intra-module file ordering**; define leaf interfaces (func/class).
34 |    - **Inputs:** <RPG_L0.json>
35 |    - **Outputs:** <RPG_FULL.json> (folders/files, edges, interfaces), <SKELETON_REPO>
36 |    - **Success:** DAG validation passes; interface docs complete.
37 | 
38 | 3. **Builder** (Executor) • code generation
39 | 
40 |    - **Goals:** Topologically traverse RPG; **derive tests first**, then implement to green; run selective regression; add integration tests per subgraph.
41 |    - **Inputs:** <RPG_FULL.json>, <TEST_PROMPTS>
42 |    - **Outputs:** <SRC_CODE>, <UNIT_TESTS>, <INTEG_TESTS>
43 |    - **Success:** Pass rate ≥ <PASS_RATE_TARGET>; no broken dependents.
44 | 
45 | 4. **Verifier** • validation & metrics
46 | 
47 |    - **Goals:** Majority-vote semantic checks for algorithm presence; attribute failures (impl vs test/env); compute Coverage/Novelty/Pass/Voting/LOC/Files/Tokens.
48 |    - **Inputs:** <SRC_CODE>, <TEST_RESULTS>, <TASK_SET>
49 |    - **Outputs:** <EVAL_REPORT>, <METRICS.json>, <DIAGNOSIS_LOG>
50 |    - **Success:** Voting agreement ≥ <VOTE_RATE_TARGET>; metrics computed as spec.
51 | 
52 | 5. **Orchestrator** • coordination
53 | 
54 |    - **Goals:** Schedule DAG execution, enforce budgets/timeouts, trigger escalations/HITL.
55 |    - **Inputs:** All artifacts above
56 |    - **Outputs:** <RUN_LOG>, <ALERTS>
57 |    - **Success:** SLA conformance: latency ≤ <SLA_LATENCY>, cost ≤ <SLA_BUDGET>.
58 | 
59 | 6. *(Optional)* **Retriever** • knowledge grounding
60 | 
61 |    - **Goals:** Manage Feature Tree search, diversity-aware exploration, LLM filtering and merge.
62 | 
63 | 7. *(Optional)* **Localizer** • graph-guided search/edit
64 | 
65 |    - **Goals:** Locate target code via functionality → repository navigation; support graph-guided edits.
66 | 
67 | ---
68 | 
69 | ## 4) Tooling & Permissions
70 | 
71 | ### Tool Catalog
72 | 
73 | *(Provider-agnostic; replace with {{tools}} where available.)*
74 | 
75 | 1. **vector_db.search**
76 | 
77 | - **Intent:** Retrieve top-k feature paths (exploit).
78 | - **Input Schema:** `{"query":"<TEXT>","k":<INT>,"filters":{}}`
79 | - **Output Schema:** `{"paths":[{"path":"a/b/c","score":<FLOAT>}]}`
80 | - **Side Effects:** none; reads <VECTOR_DB>
81 | - **Limits/Costs:** <QPS_LIMIT>, <BUDGET_PATH_SEARCH>
82 | - **Failure Modes:** skewed recall, latency spikes
83 | - **Example:** `vector_db.search({"query": "<GOAL_SPEC>", "k": 50})`
84 | - **Source:** Proposal retrieval.
85 | 
86 | 2. **feature_tree.sample_reject**
87 | 
88 | - **Intent:** Diversity-aware exploration with overlap threshold ρ and retries.
89 | - **Input:** `{"root":"<NODE>","rho":<FLOAT>,"tmax":<INT>}`
90 | - **Output:** `{"paths":[...]}`
91 | - **Side Effects:** none
92 | - **Failure:** insufficient diversity
93 | - **Example:** `feature_tree.sample_reject({"root":"root","rho":0.2,"tmax":10})`
94 | - **Source:** Rejection sampling algorithm.
95 | 
96 | 3. **llm.filter_merge**
97 | 
98 | - **Intent:** Filter, rank, dedupe candidates; propose missing features; batch self-check.
99 | - **Input:** `{"candidates":[...],"context":{"tree":"<JSON>"}}`
100 | - **Output:** `{"accepted":[...],"rationales":[...]}`
101 | - **Side Effects:** audit log
102 | - **Failure:** drift/inconsistency
103 | - **Example:** `llm.filter_merge({...})`
104 | - **Source:** LLM filtering + self-check.
105 | 
106 | 4. **graph_store.persist**
107 | 
108 | - **Intent:** Versioned save of RPG L0/L1/L2/full.
109 | - **Input:** `{"graph":"<RPG_JSON>","version":"<RPG_VER>"}`
110 | - **Output:** `{"checksum":"<HEX>","uri":"<URI>"}`
111 | - **Side Effects:** writes <GRAPH_STORE>
112 | - **Failure:** schema mismatch
113 | - **Example:** `graph_store.persist({...})`
114 | - **Source:** Persistent representation.
115 | 
116 | 5. **graph.validate_dag**
117 | 
118 | - **Intent:** Enforce acyclicity; check inter-/intra-module constraints.
119 | - **Input:** `{"graph":"<RPG_JSON>"}`
120 | - **Output:** `{"ok":true,"errors":[]}`
121 | - **Side Effects:** CI gate
122 | - **Failure:** cycles/contradictions
123 | - **Example:** `graph.validate_dag({...})`
124 | - **Source:** Typed flows & topological order.
125 | 
126 | 6. **repo.scaffold**
127 | 
128 | - **Intent:** Map modules→folders; features→files; generate skeleton.
129 | - **Input:** `{"graph":"<RPG_L1/L2>","root":"<PATH>"}`
130 | - **Output:** `{"paths":[...]}`
131 | - **Side Effects:** writes <SKELETON_REPO>
132 | - **Failure:** over-nesting
133 | - **Source:** File/folder encoding.
134 | 
135 | 7. **tests.unit.generate**
136 | 
137 | - **Intent:** Derive unit test from interface/spec docstring.
138 | - **Input:** `{"interface":"<FQN>","spec":"<DOC>"}`
139 | - **Output:** `{"test_file":"<PATH>","code":"<STR>"}`
140 | - **Side Effects:** writes tests
141 | - **Failure:** weak coverage
142 | - **Source:** TDD at leaf nodes.
143 | 
144 | 8. **tests.run**
145 | 
146 | - **Intent:** Execute unit/regression/integration suite; selective by graph impact.
147 | - **Input:** `{"scope":["unit|regression|integration"],"targets":[...],"impact_from_graph":true}`
148 | - **Output:** `{"pass":<BOOL>,"log":"<URI>","failures":[...]}`
149 | - **Side Effects:** CI status
150 | - **Failure:** env flakiness
151 | - **Source:** Regression & integration gates.
152 | 
153 | 9. **evaluator.vote**
154 | 
155 | - **Intent:** Majority-vote semantic validation (n=5; 2 rounds).
156 | - **Input:** `{"candidate":"<CODE_URI>","task":"<DESC>"}`
157 | - **Output:** `{"votes":5,"agree":<INT>,"confidence":<FLOAT>}`
158 | - **Side Effects:** cost tokens
159 | - **Failure:** judge variance
160 | - **Source:** Majority-vote validation.
161 | 
162 | 10. **metrics.compute**
163 | 
164 | - **Intent:** Coverage, Novelty, Pass Rate, Voting Rate, Files, LOC, Tokens (per D.3.1).
165 | - **Input:** `{"repo_uri":"<URI>","taxonomy":"<REF>"}`
166 | - **Output:** `{"coverage":...,"novelty":...,"pass":...,"voting":...,"files":...,"loc":...,"tokens":...}`
167 | - **Side Effects:** writes <METRICS_STORE>
168 | - **Failure:** category drift
169 | - **Source:** Metrics definitions.
170 | 
171 | 11. **rpg.localize / repo.view / dep.trace**
172 | 
173 | - **Intent:** Graph-guided localization (functionality→code), interface view, dependency trace.
174 | - **Schemas:** simple `{ "query":"<TEXT|FEATURE_PATH>" }` → list of FQNs/paths.
175 | - **Source:** Localization toolset.
176 | 
177 | 12. **governance.scan**
178 | 
179 | - **Intent:** SBOM, licenses, secrets scan.
180 | - **Source:** Governance risk mitigation (derived).
181 | 
182 | ### Permission Matrix (excerpt)
183 | 
184 | | Agent \ Tool | vector_db.search | feature_tree.sample_reject | graph_store.persist | tests.run | evaluator.vote | governance.scan |
185 | | ------------ | ---------------: | -------------------------: | ------------------: | --------: | -------------: | --------------: |
186 | | Planner      |            ✅read |                      ✅read |                   ⛔ |         ⛔ |              ⛔ |               ⛔ |
187 | | Implementer  |                ⛔ |                          ⛔ |              ✅write |         ⛔ |              ⛔ |               ⛔ |
188 | | Builder      |                ⛔ |                          ⛔ |                   ⛔ |     ✅exec |              ⛔ |               ⛔ |
189 | | Verifier     |                ⛔ |                          ⛔ |                   ⛔ |     ✅exec |          ✅exec |           ✅exec |
190 | | Orchestrator |           ✅audit |                     ✅audit |            ✅approve |  ✅approve |       ✅approve |        ✅approve |
191 | 
192 | Sensitive ops (**write/exec/approve**) require HITL if <RISK_LEVEL> ≥ <HITL_THRESHOLD>.
193 | 
194 | ---
195 | 
196 | ## 5) Task Graph & Protocols
197 | 
198 | ### Goal Decomposition (ASCII DAG)
199 | 
200 | ```
201 | [Observe Spec]
202 |    ↓
203 | [Planner: RPG L0 (exploit+explore)]  --> [HITL-Approve?] -->
204 |    ↓
205 | [Implementer: Folders/Files + DataFlows + Interfaces → RPG Full]
206 |    ↓
207 | [Builder: Topo Build Queue → (Unit Test → Implement → Regression) → Integration Tests]
208 |    ↓
209 | [Verifier: Vote + Metrics + Diagnosis]
210 |    ↓
211 | [Report/Release or Iterate/Escalate]
212 | ```
213 | 
214 | **Source:** Three-stage pipeline + topo traversal + testing.
215 | 
216 | ### Message Contracts
217 | 
218 | - **Request (agent→agent):** `{id, from, to, intent, content, constraints[], artifacts[], deadline, budget}`
219 | - **Response:** `{id, in_reply_to, status, summary, artifacts[], metrics{}, notes}`
220 | 
221 | - **Error:** `{id, in_reply_to, error_code, error_class, evidence_uri}`
222 | 
223 | ### Scheduling
224 | 
225 | - **Concurrency:** Max parallelism = min(<CPU_CORES>, <MAX_PARALLEL_NODES>), **respect DAG order**.
226 | - **Retries/Backoff:** Tool-call retries: 2 with exponential backoff (1×, 2×).
227 | - **Time bounds:** <MAX_STAGE_LATENCY> per stage; **stop** on budget/latency breach.
228 | 
229 | ---
230 | 
231 | ## 6) Standard Operating Procedures (SOPs)
232 | 
233 | ### SOP: **Plan** — task breakdown & risk scan
234 | 
235 | - **WHEN:** <GOAL_SPEC> received.
236 | - **DO:**
237 | 
238 |   1. Retrieve top-k exploit paths from <VECTOR_DB>.
239 |   2. Sample explore paths via diversity-aware rejection (ρ).
240 |   3. LLM filter/merge; propose missing features; batch self-check; log rationales.
241 |   4. Refactor to cohesive modules (maximize cohesion/minimize coupling).
242 |   5. Persist as **RPG L0** (versioned).
243 | - **CHECK:** `<COVERAGE> ≥ <COVERAGE_TARGET>`; modules non-overlapping; rationale log present.
244 | - **IF FAIL:** Increase k/ρ; expand synonyms; induce missing features; re-run 1–4.
245 | - **ARTIFACTS:** <RPG_L0.json>, <PLAN_LOG>
246 | - **SOURCE:** ¶3.2/Alg.2 “exploit–explore + filter/merge”; ¶3.1 dual-semantics note.
247 | 
248 | ### SOP: **Gather** — retrieval, freshness, provenance
249 | 
250 | - **WHEN:** Planner requests grounding.
251 | - **DO:**
252 | 
253 |   1. Ensure Feature Tree embeddings loaded with paths/meta.
254 |   2. Run vector_db.search and sample_reject; attach scores/overlap stats.
255 |   3. Record provenance (source tree node IDs, timestamps).
256 | - **CHECK:** Query latency ≤ <EMBED_QPS>; provenance complete.
257 | - **IF FAIL:** Rebuild embeddings; partition index; cache hot queries.
258 | - **ARTIFACTS:** <RETRIEVAL_LOG>, <PROVENANCE_CSV>
259 | - **SOURCE:** Feature Tree embeddings + metadata.
260 | 
261 | ### SOP: **Build/Execute** — implementation & graph-guided TDD
262 | 
263 | - **WHEN:** RPG L0 approved.
264 | - **DO:**
265 | 
266 |   1. Map modules→folders; features→files; create skeleton.
267 |   2. Encode typed inter-module data flows and intra-module file ordering; validate DAG.
268 |   3. Design leaf interfaces (func/class) with docstrings; no bodies.
269 |   4. **Topologically** sort RPG into <BUILD_QUEUE>.
270 |   5. For each leaf: **generate unit test → implement → run → commit only on green**.
271 |   6. On edits: run **selective regression** (impacted parents/children).
272 |   7. For completed subgraphs: add **integration tests**.
273 | - **CHECK:** DAG passes; unit pass ≥ <UNIT_PASS_TARGET>; coverage ≥ <MIN_COV>.
274 | - **IF FAIL:** Localize via rpg.localize/repo.view/dep.trace; patch; rerun tests.
275 | - **ARTIFACTS:** <RPG_FULL.json>, <SRC_CODE>, <TESTS>, <CI_REPORT>
276 | - **SOURCE:** §3.3, §4 (topo + TDD + regression/integration).
277 | 
278 | #### Testing Pitfalls & Guardrails
279 | 
280 | ##### Common pitfalls
281 | 
282 | - Writing tests that are tied to implementation details (fragile).
283 | - Over-specifying: testing how instead of what.
284 | - Giant steps: skipping the tiny loop, leading to long failing streaks.
285 | - Mocking everything: lose real behavior; mock only true boundaries.
286 | 
287 | ##### Guardrails that make it work
288 | 
289 | - Keep acceptance tests few and slow but critical; keep unit tests many and fast.
290 | - Contracts are versioned (backward-compatible by default); breaking changes require a contract test update first.
291 | - Make failures actionable: test names read like requirements, outputs diff JSON bodies/schemas, not logs.
292 | 
293 | ### SOP: **Validate** — metrics & policy checks
294 | 
295 | - **WHEN:** Build completes for milestone/subgraph.
296 | - **DO:**
297 | 
298 |   1. Majority-vote semantic check (5 votes; 2 rounds) per task.
299 |   2. Attribute failures: **impl vs test/env**; auto-remediate latter.
300 |   3. Compute **Coverage, Novelty, Pass, Voting, Files, LOC, Tokens** as D.3.1.
301 |   4. Run license/secret scan; generate SBOM.
302 | - **CHECK:** `<PASS_RATE> ≥ <PASS_RATE_TARGET>`, `<VOTING_RATE> ≥ <VOTE_RATE_TARGET>`, no license/sec violations.
303 | - **IF FAIL:** Escalate with evidence bundle; increase retries for env/test up to <N_REMEDIATIONS>.
304 | - **ARTIFACTS:** <EVAL_REPORT>, <METRICS.json>, <SBOM>, <GOV_REPORT>
305 | - **SOURCE:** §5/§D.3.1 metrics; validation pipeline.
306 | 
307 | ### SOP: **Deliver/Report** — release & handoff
308 | 
309 | - **WHEN:** Metrics hit thresholds or HITL approves.
310 | - **DO:**
311 | 
312 |   1. Emit release notes: scope, build hash, metrics deltas, known issues.
313 |   2. Publish artifacts to <ARTIFACT_STORE>; tag <RPG_VER>.
314 |   3. Schedule next iteration if coverage gap or backlog exists.
315 | - **CHECK:** Artifacts present; checksums match; dashboards updated.
316 | - **IF FAIL:** Rollback to previous green tag; notify stakeholders.
317 | - **ARTIFACTS:** <RELEASE_NOTES>, <ARTIFACT_MANIFEST>
318 | - **SOURCE:** Persistent RPG & staged iteration.
319 | 
320 | ### SOP: **Monitor** — drift & review cadence
321 | 
322 | - **WHEN:** Post-release or nightly.
323 | - **DO:**
324 | 
325 |   1. Enforce DAG/schema validation on every RPG change via CI.
326 |   2. Track near-linear scaling of features/LOC; alert on plateau.
327 |   3. Log localization/tool calls for audit; redact PII.
328 | - **CHECK:** CI clean; slope ≥ <MIN_SLOPE>; audit logs ≥ <MIN_LOG_FIELDS>.
329 | - **IF FAIL:** Quarantine change; root-cause; schedule fix.
330 | - **ARTIFACTS:** <CI_LOGS>, <SCALING_DASHBOARD>, <AUDIT_LOG>
331 | - **SOURCE:** Topological CI; scalability analyses; logging examples.
332 | 
333 | ---
334 | 
335 | ## 7) Decision Policies & Guardrails
336 | 
337 | - **Quality Gates:**
338 | 
339 |   - `<PASS_RATE> ≥ <PASS_RATE_TARGET>`; `<VOTING_RATE> ≥ <VOTE_RATE_TARGET>`; `<COVERAGE> ≥ <COVERAGE_TARGET>`; `<NOVELTY> ≤ <NOVELTY_MAX>` unless explicitly allowed.
340 | - **Safety Checks:**
341 | 
342 |   - Enforce license policy; secrets = 0; SBOM emitted; PII redaction in logs.
343 | - **Cost/Time Budgets:**
344 | 
345 |   - `<MAX_TOOL_CALLS>`, `<MAX_TOKENS>`, `<MAX_WALLTIME>` per stage; **terminate** on breach with evidence bundle.
346 | - **Escalation Matrix:**
347 | 
348 |   - *What:* DAG cycles, persistent test/env failures, metric shortfall > <DELTA_THRESHOLD>.
349 |   - *To whom:* {{human_roles}} (PM/Eng/QA/Legal/SME).
350 |   - *Bundle:* `{context, diffs, failing tests, votes, logs, metrics_delta}`.
351 | - **Termination Conditions:**
352 | 
353 |   - All gates green **or** budget exhausted **or** HITL stop; handoff includes <RPG_FULL.json>, code, tests, metrics.
354 | 
355 | ---
356 | 
357 | ## 8) Collaboration Playbooks
358 | 
359 | - **Multi-Agent Pattern:** `Planner → Implementer → Builder → Verifier` loop until gates pass; max <N_LOOPS>.
360 | - **Consensus/Critique:** Verifier may trigger 1 critique round with <N_CRITICS>; if unresolved → HITL.
361 | - **HITL Interfaces:** Approval prompts include `{summary, changes, risks, budgets, diffs, metrics}`; “request changes” restarts from affected stage only.
362 | - **Communication Etiquette:** Keep messages ≤ <512 tokens>; include `id, intent, constraints, artifacts`.
363 | 
364 | ---
365 | 
366 | ## 9) Observability & Artifacts
367 | 
368 | - **Logging Fields:** `ts, run_id, agent, tool, input_hash, output_hash, duration_ms, cost, redactions[]`.
369 | - **Redaction Policy:** Strip PII/secrets; hash examples; store raw only in quarantined vault.
370 | - **Artifacts:**
371 | 
372 |   - Naming: `<proj>-<stage>-<yyyymmdd>-<hash>.<ext>`; store in `<ARTIFACT_STORE>/<stage>/`.
373 | - **Dashboards/Reviews:**
374 | 
375 |   - Charts: Coverage, Pass/Vote, LOC growth (expect near-linear under RPG), failure classes; weekly review.
376 | 
377 | ---
378 | 
379 | ## 10) Error Handling & Recovery
380 | 
381 | - **Error Classes:** `validation`, `quota`, `tool`, `network`, `policy`.
382 | - **Playbooks:**
383 | 
384 |   - `validation`: localize→fix→rerun tests.
385 |   - `quota`: backoff, reduce k/ρ, compress context.
386 |   - `tool`: retry (2), alternate endpoint, stub.
387 |   - `network`: retry with jitter; cache results.
388 |   - `policy`: quarantine, notify Legal, redact & re-run.
389 | - **Rollback:** Revert to last **green** tag (<RPG_VER_prev>); lock write ops until RCA complete.
390 | 
391 | ---
392 | 
393 | ## 11) Configuration Templates
394 | 
395 | ### Agent Spec (YAML)
396 | 
397 | ```yaml
398 | agents:
399 |   - name: Planner
400 |     role: planning
401 |     inputs: [<GOAL_SPEC>, <CONSTRAINTS>]
402 |     outputs: [<RPG_L0.json>, <RISKS>]
403 |     permissions: [read.vector_db, plan, write.plan_log]
404 |   - name: Implementer
405 |     role: implementation
406 |     inputs: [<RPG_L0.json>]
407 |     outputs: [<RPG_FULL.json>, <SKELETON_REPO>]
408 |     permissions: [write.graph, write.repo, validate.dag]
409 |   - name: Builder
410 |     role: build
411 |     inputs: [<RPG_FULL.json>]
412 |     outputs: [<SRC_CODE>, <TESTS>]
413 |     permissions: [exec.tests, write.code]
414 |   - name: Verifier
415 |     role: verify
416 |     inputs: [<SRC_CODE>, <TEST_RESULTS>, <TASK_SET>]
417 |     outputs: [<EVAL_REPORT>, <METRICS.json>]
418 |     permissions: [exec.vote, exec.metrics, exec.governance]
419 | tools:
420 |   - name: vector_db.search
421 |     intent: retrieve exploit paths
422 |     input_schema: {query: <TEXT>, k: <INT>}
423 |     output_schema: {paths: [<PATH_OBJ>]}
424 |     limits: {rate: <N/min>, budget: <$MAX>}
425 | policies:
426 |   quality_gates:
427 |     - metric: pass_rate
428 |       threshold: <PASS_RATE_TARGET>
429 |     - metric: coverage
430 |       threshold: <COVERAGE_TARGET>
431 | ```
432 | 
433 | ### Message Contract (JSON)
434 | 
435 | ```json
436 | {
437 |   "id": "<UUID>",
438 |   "from": "<AGENT>",
439 |   "to": "<AGENT|HUMAN>",
440 |   "intent": "<PLAN|EXECUTE|VERIFY|ESCALATE>",
441 |   "content": "<BRIEF>",
442 |   "constraints": ["<RULE1>", "<RULE2>"],
443 |   "artifacts": ["<URI1>", "<URI2>"]
444 | }
445 | ```
446 | 
447 | ---
448 | 
449 | ## 12) Examples (Few-Shot)
450 | 
451 | **Example A — Planner → Builder handoff**
452 | 
453 | - **Planner output (abridged):**
454 |   `RPG_L0.json` with modules `{algorithms, evaluation, data_loading}` and candidate paths (k=50 exploit + explore set), refactored into cohesive modules. *(Source: proposal-level construction)*
455 | - **Implementer:** maps to `src/algos`, `src/eval`, `src/data_load`; assigns files; encodes flows `data_load → algos → eval`; defines interfaces `DataLoader`, `LinearModels`.
456 | - **Builder:** topo queue then (unit test → implement → commit on green).
457 | 
458 | **Example B — Verifier blocks & escalates**
459 | 
460 | - Voting confirms presence (4/5) but **execution fails**; diagnosis labels **test/env** → auto remediation; if still failing, **escalate** with logs, diffs, and metrics to QA.
461 | 
462 | ---
463 | 
464 | ## 13) Traceability
465 | 
466 | Below are key sources used; each SOP/policy/tool above includes an inline **SOURCE** with paragraph cue.
467 | 
468 | - **RPG Structure & Dual Semantics; Inter-/Intra- edges; Topological Order.** §3.1 (“nodes specify… files/classes/functions… edges encode data flows/order”).
469 | - **Proposal-Level Construction:** Feature Tree embeddings; exploit–explore; LLM filter/merge; refactor by cohesion/coupling; Algorithm 2.
470 | - **Implementation-Level Construction:** Folder/file encoding; typed flows; adaptive interfaces (func vs class).
471 | - **Graph-Guided Generation:** Topological traversal; **TDD**; regression & integration testing.
472 | - **Localization & Editing Tools:** rpg-guided search, repo view, dependency exploration.
473 | - **Validation Pipeline:** Majority-vote semantic check; failure attribution; remediation loops.
474 | - **Metrics:** Coverage, Novelty, Pass, Voting, Files/LOC/Tokens (Appendix D.3.1).
475 | - **Governance Additions (SBOM, licenses, secrets):** operational risk mitigation derived in build guide.
476 | - **Scalability & Monitoring:** Near-linear growth expectations; CI DAG validation; logging exemplars.
477 | 
478 | ---
479 | 
480 | ## 14) Temporary Priority Dual-Labeling (Taskmaster + RPG)
481 | 
482 | **Goal:** Use Taskmaster’s priority for scheduling while making the RPG priority explicit—without changing Taskmaster’s schema.
483 | 
484 | **Authoritative field (unchanged):** `priority` ∈ `{high, medium, low}`
485 | **RPG mapping:** `P0→high`, `P1→medium`, `P2→low`
486 | 
487 | ### What to do (apply to every task and subtask)
488 | 
489 | 1. **Prefix the title (visible)**
490 | 
491 |    - Format: `[P*] <Title>`
492 |    - Optional ID: `[P*|<RPG_ID>] <Title>`
493 |    - Examples: `[P0] Initialize repo`, `[P1|DSC-001] Define project spec`
494 | 
495 | 2. **Stamp the details (machine-friendly)**
496 | 
497 |    - Insert as the **first line** of `details`:
498 | 
499 |      - `RPG_PRIORITY=P*`
500 |      - Optional: `RPG_ID=<RPG_ID>` on the next line
501 |    - Preserve the rest of `details` as-is after a blank line.
502 | 
503 | ### Do / Don’t
504 | 
505 | - ✅ **Do** keep `priority` exactly `high|medium|low`.
506 | - ✅ **Do** dual-label with `[P*]` in `title` **and** `RPG_PRIORITY=P*` in `details`.
507 | - ✅ **Do** let subtasks inherit the parent’s P* if their own `priority` is missing.
508 | - ❌ **Don’t** add new top-level fields (e.g., `rpg_priority`) or wrappers.
509 | - ❌ **Don’t** rename or re-case Taskmaster’s `priority` values.
510 | 
511 | ### Quick reference
512 | 
513 | | RPG | Taskmaster `priority` | Title Prefix | Details Stamp     |
514 | | --- | --------------------- | ------------ | ----------------- |
515 | | P0  | high                  | `[P0]`       | `RPG_PRIORITY=P0` |
516 | | P1  | medium                | `[P1]`       | `RPG_PRIORITY=P1` |
517 | | P2  | low                   | `[P2]`       | `RPG_PRIORITY=P2` |
518 | 
519 | ### Example (before → after)
520 | 
521 | **Before**
522 | 
523 | ```json
524 | {
525 |   "title": "Initialize repository",
526 |   "priority": "high",
527 |   "details": "Create repo, add README.",
528 |   "subtasks": [
529 |     { "title": "Add CI", "priority": "medium", "details": "Set up basic workflow." }
530 |   ]
531 | }
532 | ```
533 | 
534 | **After**
535 | 
536 | ```json
537 | {
538 |   "title": "[P0] Initialize repository",
539 |   "priority": "high",
540 |   "details": "RPG_PRIORITY=P0\n\nCreate repo, add README.",
541 |   "subtasks": [
542 |     {
543 |       "title": "[P1] Add CI",
544 |       "priority": "medium",
545 |       "details": "RPG_PRIORITY=P1\n\nSet up basic workflow."
546 |     }
547 |   ]
548 | }
549 | ```
550 | 
551 | **Validation checklist (agents):**
552 | 
553 | - Title starts with `[P0]`, `[P1]`, or `[P2]`.
554 | - `details` first line is `RPG_PRIORITY=P*`.
555 | - Taskmaster `priority` untouched and consistent with the P* mapping.
556 | - No extra top-level fields added.
557 | 
558 | ---
559 | 
560 | **End of AGENTS.md**
```

RPG_build_guide.md
```
1 | RPG_REPOSITORY_PLANNING_GRAPH.pdf
2 | 
3 | A) Human-readable Plan (Markdown)
4 | =================================
5 | 
6 | **Overview.** This plan turns the _RPG: Repository Planning Graph_ whitepaper into a deduplicated, provider-agnostic, step-by-step build guide. It covers: (1) defining the RPG schema; (2) proposal- and implementation-level graph construction; (3) graph-guided, test-driven code generation; and (4) evaluation/monitoring (RepoCraft-style). Assumptions: Python repos, any LLM, any vector DB/graph DB, any CI. RPG_REPOSITORY_PLANNING_GRAPH
7 | 
8 | **Primary Purpose assumed:** _Operationalize RPG/ZeroRepo to generate full repositories from scratch using a unified planning graph and graph-guided TDD._ RPG_REPOSITORY_PLANNING_GRAPH
9 | 
10 | **Audience/Actors assumed:** Research Engineer, Software Architect, QA/Testing, PM, DevOps.
11 | **Constraints assumed:** provider-agnostic, offline-friendly, reproducible, acyclic data-flows, test-gated commits, license-safe inputs.
12 | **Preferred Taxonomy used:** **Discover → Design → Build → Validate → Benchmark → Monitor**.
13 | **Priority Policy:** P0 blocker (must), P1 important, P2 nice-to-have.
14 | 
15 | * * *
16 | 
17 | Instruction List (grouped by taxonomy)
18 | --------------------------------------
19 | 
20 | ### Discover
21 | 
22 | - **ID:** DSC-001
23 |     **Topic:** Discover
24 |     **Instruction:** Define <PROJECT\_SPEC> with goals, scope, constraints, and acceptance metrics.
25 |     **Acceptance Criteria:** Doc includes <GOALS>, <NON\_GOALS>, <CONSTRAINTS>, <METRICS>; reviewed by <STAKEHOLDERS>.
26 |     **Dependencies:** —
27 |     **Priority:** P0
28 |     **Risks & Mitigations:** Ambiguity → add examples and anti-requirements.
29 |     **Source:** ¶2 — “generating complete repositories… demands coherent… planning.” RPG_REPOSITORY_PLANNING_GRAPH
30 |     **Tool Suggestions:** markdown repo template
31 | 
32 | - **ID:** DSC-002
33 |     **Topic:** Discover
34 |     **Instruction:** Specify RPG schema with <NODE\_TYPES>, <EDGE\_TYPES>, required fields, and DAG constraint.
35 |     **Acceptance Criteria:** JSON Schema covers nodes {capability, folder, file, class, function} and edges {hierarchy, data\_flow, order}; validates acyclicity.
36 |     **Dependencies:** DSC-001
37 |     **Priority:** P0
38 |     **Risks & Mitigations:** Over-generalization → start minimal; iterate.
39 |     **Source:** ¶6 — “nodes specify… files, classes, and functions… edges encode… data flows… order.” RPG_REPOSITORY_PLANNING_GRAPH
40 |     **Tool Suggestions:** generic schema validator; graph DB
41 | 
42 | - **ID:** DSC-003
43 |     **Topic:** Discover
44 |     **Instruction:** Assemble <FEATURE\_TREE\_SOURCE> and embed nodes into <VECTOR\_DB>.
45 |     **Acceptance Criteria:** ≥1M features loaded or configured; embeddings stored with path metadata; latency < <EMBED\_QPS>.
46 |     **Dependencies:** DSC-001
47 |     **Priority:** P0
48 |     **Risks & Mitigations:** Bias/skew → record level distribution; add sampling.
49 |     **Source:** ¶7 — “Feature Tree… 1.5M capabilities… embedded… vector database.” RPG_REPOSITORY_PLANNING_GRAPH
50 |     **Tool Suggestions:** any embedding model; FAISS/pgvector/milvus
51 | 
52 | 
53 | * * *
54 | 
55 | ### Design (Proposal-level)
56 | 
57 | - **ID:** PROP-001
58 |     **Topic:** Proposal Design
59 |     **Instruction:** Retrieve top-k feature paths for <PROJECT\_SPEC> into <CANDIDATES\_EXPLOIT>.
60 |     **Acceptance Criteria:** Query returns k paths with similarity scores and full hierarchical paths.
61 |     **Dependencies:** DSC-003
62 |     **Priority:** P0
63 |     **Risks & Mitigations:** Narrow recall → expand synonyms.
64 |     **Source:** ¶8 — “retrieve top-k feature paths… aligned with the user goal.” RPG_REPOSITORY_PLANNING_GRAPH
65 |     **Tool Suggestions:** vector search
66 | 
67 | - **ID:** PROP-002
68 |     **Topic:** Proposal Design
69 |     **Instruction:** Sample unvisited ontology regions into <CANDIDATES\_EXPLORE>.
70 |     **Acceptance Criteria:** At least <N\_EXPL> diverse paths not overlapping existing subtree (> <RHO> threshold).
71 |     **Dependencies:** DSC-003
72 |     **Priority:** P0
73 |     **Risks & Mitigations:** Irrelevance → diversity-aware rejection sampling.
74 |     **Source:** ¶8/¶21 — “exploration ensures diversity… rejection mechanism.” RPG_REPOSITORY_PLANNING_GRAPH
75 |     **Tool Suggestions:** weighted sampler
76 | 
77 | - **ID:** PROP-003
78 |     **Topic:** Proposal Design
79 |     **Instruction:** Filter, rank, and merge candidates using <LLM\_FILTER\_PROMPT>.
80 |     **Acceptance Criteria:** Merged set deduped; rationale captured per path; audit log stored.
81 |     **Dependencies:** PROP-001, PROP-002
82 |     **Priority:** P0
83 |     **Risks & Mitigations:** LLM drift → batch self-check.
84 |     **Source:** ¶8/Algorithm 2 — “LLM… filter… self-checks… insert paths.” RPG_REPOSITORY_PLANNING_GRAPH
85 |     **Tool Suggestions:** any LLM; prompt templatizer
86 | 
87 | - **ID:** PROP-004
88 |     **Topic:** Proposal Design
89 |     **Instruction:** Refactor subtree into modules maximizing cohesion, minimizing coupling.
90 |     **Acceptance Criteria:** Modules have clear boundaries; taxonomy justification per move recorded.
91 |     **Dependencies:** PROP-003
92 |     **Priority:** P0
93 |     **Risks & Mitigations:** Over-fragmentation → merge pass.
94 |     **Source:** ¶9 — “partitions… into cohesive modules… cohesion and coupling.” RPG_REPOSITORY_PLANNING_GRAPH
95 |     **Tool Suggestions:** graph partitioner
96 | 
97 | - **ID:** PROP-005
98 |     **Topic:** Proposal Design
99 |     **Instruction:** Persist the functionality graph as RPG layer L0 with version <RPG\_VER>.
100 |     **Acceptance Criteria:** L0 saved; checksum; diffable; CI loads without errors.
101 |     **Dependencies:** PROP-004
102 |     **Priority:** P0
103 |     **Risks & Mitigations:** Schema drift → add migration script.
104 |     **Source:** ¶4 — “persistent and evolvable representation.” RPG_REPOSITORY_PLANNING_GRAPH
105 |     **Tool Suggestions:** git LFS; graph DB
106 | 
107 | 
108 | * * *
109 | 
110 | ### Design (Implementation-level)
111 | 
112 | - **ID:** IMPL-001
113 |     **Topic:** Implementation Design
114 |     **Instruction:** Map L0 modules to folder layout under <ROOT\_DIR>/src as L1 folder nodes.
115 |     **Acceptance Criteria:** Each module ↔ one folder; mapping table with subtree names; path lint passes.
116 |     **Dependencies:** PROP-005
117 |     **Priority:** P0
118 |     **Risks & Mitigations:** Over-nesting → cap depth.
119 |     **Source:** ¶10 — “assigning each subgraph a dedicated directory namespace.” RPG_REPOSITORY_PLANNING_GRAPH
120 |     **Tool Suggestions:** code scaffolder
121 | 
122 | - **ID:** IMPL-002
123 |     **Topic:** Implementation Design
124 |     **Instruction:** Group intermediate nodes into files; create L2 file nodes.
125 |     **Acceptance Criteria:** Files contain cohesive features; naming per PEP8; ≤ <MAX\_FILES\_PER\_DIR> unless subfolders added.
126 |     **Dependencies:** IMPL-001
127 |     **Priority:** P0
128 |     **Risks & Mitigations:** Cross-file coupling → regroup.
129 |     **Source:** ¶11 — “assigning files to intermediate nodes… preserve semantic cohesion.” RPG_REPOSITORY_PLANNING_GRAPH
130 |     **Tool Suggestions:** file planner
131 | 
132 | - **ID:** IMPL-003
133 |     **Topic:** Implementation Design
134 |     **Instruction:** Encode inter-module data-flow edges with typed I/O; ensure DAG.
135 |     **Acceptance Criteria:** Edges include {from,to,data\_id,data\_type,transformation}; cycle check passes.
136 |     **Dependencies:** IMPL-001
137 |     **Priority:** P0
138 |     **Risks & Mitigations:** Hidden cycles → topological check in CI.
139 |     **Source:** ¶12 — “typed input–output flows… impose a topological order.” RPG_REPOSITORY_PLANNING_GRAPH
140 |     **Tool Suggestions:** DAG/graph validator
141 | 
142 | - **ID:** IMPL-004
143 |     **Topic:** Implementation Design
144 |     **Instruction:** Define intra-module file order edges for build/load constraints.
145 |     **Acceptance Criteria:** Order edges exist for each module; no contradictions; linter validates.
146 |     **Dependencies:** IMPL-002
147 |     **Priority:** P1
148 |     **Risks & Mitigations:** Brittle imports → lazy load.
149 |     **Source:** ¶6/¶12 — “intra-module file ordering… precedes…” RPG_REPOSITORY_PLANNING_GRAPH
150 |     **Tool Suggestions:** import graph analyzer
151 | 
152 | - **ID:** IMPL-005
153 |     **Topic:** Implementation Design
154 |     **Instruction:** Abstract shared patterns into <BASE\_CLASSES> and shared data structures.
155 |     **Acceptance Criteria:** Base types defined only for recurring patterns; adoption rate ≥ <ADOPTION\_RATE>.
156 |     **Dependencies:** IMPL-003
157 |     **Priority:** P1
158 |     **Risks & Mitigations:** Premature abstraction → justify with usage.
159 |     **Source:** ¶13 — “abstract… base classes… enforce interface consistency.” RPG_REPOSITORY_PLANNING_GRAPH
160 |     **Tool Suggestions:** UML generator
161 | 
162 | - **ID:** IMPL-006
163 |     **Topic:** Implementation Design
164 |     **Instruction:** For each leaf feature, design exactly one interface (func or class) with docstring.
165 |     **Acceptance Criteria:** One interface/leaf; docstrings include args/returns; no bodies (pass).
166 |     **Dependencies:** IMPL-002, IMPL-003, IMPL-005
167 |     **Priority:** P0
168 |     **Risks & Mitigations:** Over-classing → prefer functions for stateless ops.
169 |     **Source:** ¶14 & Appendix B.1 — “adaptive mapping… functions vs classes; prompt template.” RPG_REPOSITORY_PLANNING_GRAPH
170 |     **Tool Suggestions:** interface generator
171 | 
172 | 
173 | * * *
174 | 
175 | ### Build (Graph-guided TDD)
176 | 
177 | - **ID:** GEN-001
178 |     **Topic:** Build
179 |     **Instruction:** Topologically sort RPG and plan build queue <BUILD\_QUEUE>.
180 |     **Acceptance Criteria:** Queue respects all edges; snapshot stored; reproducible order.
181 |     **Dependencies:** IMPL-003, IMPL-004
182 |     **Priority:** P0
183 |     **Risks & Mitigations:** Nondeterminism → seed & persist order.
184 |     **Source:** ¶15 — “traverses the RPG in topological order.” RPG_REPOSITORY_PLANNING_GRAPH
185 |     **Tool Suggestions:** topo-sort lib
186 | 
187 | - **ID:** GEN-002
188 |     **Topic:** Build
189 |     **Instruction:** For each leaf, auto-derive a unit test from its interface/spec.
190 |     **Acceptance Criteria:** Test covers normal & edge inputs; executable via <TEST\_RUNNER>.
191 |     **Dependencies:** IMPL-006
192 |     **Priority:** P0
193 |     **Risks & Mitigations:** Weak tests → mutation testing.
194 |     **Source:** ¶15 — “test-driven development… test is derived… validated.” RPG_REPOSITORY_PLANNING_GRAPH
195 |     **Tool Suggestions:** test generator
196 | 
197 | - **ID:** GEN-003
198 |     **Topic:** Build
199 |     **Instruction:** Implement code to pass the unit test; commit only on green.
200 |     **Acceptance Criteria:** Test passes locally and in CI; code style OK; coverage ≥ <MIN\_COV>.
201 |     **Dependencies:** GEN-002
202 |     **Priority:** P0
203 |     **Risks & Mitigations:** Flaky tests → rerun policy.
204 |     **Source:** ¶15 — “Only functions that pass all tests are committed.” RPG_REPOSITORY_PLANNING_GRAPH
205 |     **Tool Suggestions:** CI runner
206 | 
207 | - **ID:** GEN-004
208 |     **Topic:** Build
209 |     **Instruction:** On edits, run regression tests for impacted nodes and parents.
210 |     **Acceptance Criteria:** Impact set derived from RPG edges; all prior tests green.
211 |     **Dependencies:** GEN-003
212 |     **Priority:** P0
213 |     **Risks & Mitigations:** Large blast radius → selective test.
214 |     **Source:** ¶17 — “Validated components trigger regression tests upon modification.” RPG_REPOSITORY_PLANNING_GRAPH
215 |     **Tool Suggestions:** test impact analyzer
216 | 
217 | - **ID:** GEN-005
218 |     **Topic:** Build
219 |     **Instruction:** Create integration tests for completed subgraphs before release.
220 |     **Acceptance Criteria:** Data-flows executed; contract checks pass; artifacts persisted.
221 |     **Dependencies:** GEN-003
222 |     **Priority:** P1
223 |     **Risks & Mitigations:** Orchestration failures → synthetic fixtures.
224 |     **Source:** ¶17 — “completed subgraphs undergo integration tests.” RPG_REPOSITORY_PLANNING_GRAPH
225 |     **Tool Suggestions:** integration harness
226 | 
227 | 
228 | * * *
229 | 
230 | ### Validate
231 | 
232 | - **ID:** VAL-001
233 |     **Topic:** Validation
234 |     **Instruction:** Add LLM majority-vote semantic validator for algorithm presence.
235 |     **Acceptance Criteria:** 5-vote majority result logged; confidence ≥ <VOTE\_THRESHOLD>.
236 |     **Dependencies:** GEN-003
237 |     **Priority:** P1
238 |     **Risks & Mitigations:** Judge variance → temperature 0 & tie-break rules.
239 |     **Source:** ¶17 & D.3 — “majority-vote checking… two rounds/5 votes.” RPG_REPOSITORY_PLANNING_GRAPH
240 |     **Tool Suggestions:** evaluator LLM
241 | 
242 | - **ID:** VAL-002
243 |     **Topic:** Validation
244 |     **Instruction:** Implement failure attribution: implementation vs test/env; auto-remediate latter.
245 |     **Acceptance Criteria:** Errors labeled; env/test issues retried ≤ <N\_REMEDIATIONS>; logs kept.
246 |     **Dependencies:** GEN-003
247 |     **Priority:** P1
248 |     **Risks & Mitigations:** Mislabeling → add heuristics & review.
249 |     **Source:** ¶17 — “majority-vote diagnosis… handle environment or test issues.” RPG_REPOSITORY_PLANNING_GRAPH
250 |     **Tool Suggestions:** log analyzer
251 | 
252 | - **ID:** VAL-003
253 |     **Topic:** Validation
254 |     **Instruction:** Compute Coverage, Novelty, Pass Rate, Voting Rate, Files, LOC, Tokens.
255 |     **Acceptance Criteria:** Metrics computed per formulas (D.3.1); stored in <METRICS\_STORE>.
256 |     **Dependencies:** PROP-005, GEN-003
257 |     **Priority:** P0
258 |     **Risks & Mitigations:** Category drift → fixed centroids + human audit.
259 |     **Source:** ¶19 & D.3.1 — “Coverage… Novelty… Pass/Voting… Code-level statistics.” RPG_REPOSITORY_PLANNING_GRAPH
260 |     **Tool Suggestions:** metrics job
261 | 
262 | 
263 | * * *
264 | 
265 | ### Benchmark
266 | 
267 | - **ID:** BMR-001
268 |     **Topic:** Benchmark
269 |     **Instruction:** Build task set by parsing reference tests into <TASKS> with NL descriptions.
270 |     **Acceptance Criteria:** > <N\_TASKS> tasks with input/outputs; trivial cases filtered.
271 |     **Dependencies:** DSC-001
272 |     **Priority:** P1
273 |     **Risks & Mitigations:** Leakage → anonymize names.
274 |     **Source:** ¶18 & D.2 — “derive tasks from reference repositories… filter trivial.” RPG_REPOSITORY_PLANNING_GRAPH
275 |     **Tool Suggestions:** test parser
276 | 
277 | - **ID:** BMR-002
278 |     **Topic:** Benchmark
279 |     **Instruction:** Run localization → validation → execution loop per task.
280 |     **Acceptance Criteria:** For each task: candidate found or absence recorded; test adapted; result stored.
281 |     **Dependencies:** BMR-001, VAL-001
282 |     **Priority:** P1
283 |     **Risks & Mitigations:** False negatives → retry budget.
284 |     **Source:** D.3 — “Stage 1 localization… Stage 2 voting… Stage 3 execution.” RPG_REPOSITORY_PLANNING_GRAPH
285 |     **Tool Suggestions:** harness runner
286 | 
287 | 
288 | * * *
289 | 
290 | ### Monitor & Operate
291 | 
292 | - **ID:** MON-001
293 |     **Topic:** Monitor
294 |     **Instruction:** Enforce DAG acyclicity and schema validation in CI on every RPG change.
295 |     **Acceptance Criteria:** CI blocks cycles/schema violations; report lists offending edges/nodes.
296 |     **Dependencies:** DSC-002, IMPL-003
297 |     **Priority:** P0
298 |     **Risks & Mitigations:** Slow checks → cache results.
299 |     **Source:** ¶12 — “impose a topological order… DAG.” RPG_REPOSITORY_PLANNING_GRAPH
300 |     **Tool Suggestions:** CI job
301 | 
302 | - **ID:** MON-002
303 |     **Topic:** Monitor
304 |     **Instruction:** Log localization steps and tool calls for auditability.
305 |     **Acceptance Criteria:** Each step recorded with inputs/outputs; PII scrubbed; replayable.
306 |     **Dependencies:** GEN-001
307 |     **Priority:** P2
308 |     **Risks & Mitigations:** Verbose logs → sampling.
309 |     **Source:** C.3 — “representative logs… tool invocations… termination results.” RPG_REPOSITORY_PLANNING_GRAPH
310 |     **Tool Suggestions:** structured logging
311 | 
312 | - **ID:** MON-003
313 |     **Topic:** Governance
314 |     **Instruction:** Add license and security checks for generated code and dependencies.
315 |     **Acceptance Criteria:** SBOM created; license policy enforced; secrets scan clean.
316 |     **Dependencies:** GEN-003
317 |     **Priority:** P0
318 |     **Risks & Mitigations:** False positives → allowlist with review.
319 |     **Source:** (general compliance risk implied by large-scale gen) RPG_REPOSITORY_PLANNING_GRAPH
320 |     **Tool Suggestions:** SBOM, license scanner
321 | 
322 | - **ID:** MON-004
323 |     **Topic:** Monitor
324 |     **Instruction:** Track scaling metrics over iterations (features, LOC) to detect stagnation.
325 |     **Acceptance Criteria:** Plots show near-linear growth or flag plateau; regression alerts.
326 |     **Dependencies:** VAL-003
327 |     **Priority:** P2
328 |     **Risks & Mitigations:** Metric gaming → cross-check with pass rate.
329 |     **Source:** ¶7.1/7.2 — “near-linear growth of functionalities and LOC.” RPG_REPOSITORY_PLANNING_GRAPH
330 |     **Tool Suggestions:** metrics dashboard
331 | 
332 | 
333 | * * *
334 | 
335 | Trace Matrix (Source Paragraph → Instruction IDs)
336 | -------------------------------------------------
337 | 
338 | - **¶2** → DSC-001
339 | 
340 | - **¶4** → PROP-005
341 | 
342 | - **¶6** → DSC-002, IMPL-004
343 | 
344 | - **¶7** → DSC-003
345 | 
346 | - **¶8** → PROP-001, PROP-002, PROP-003
347 | 
348 | - **¶9** → PROP-004
349 | 
350 | - **¶10** → IMPL-001
351 | 
352 | - **¶11** → IMPL-002
353 | 
354 | - **¶12** → IMPL-003, MON-001
355 | 
356 | - **¶13** → IMPL-005
357 | 
358 | - **¶14** → IMPL-006
359 | 
360 | - **¶15** → GEN-001, GEN-002, GEN-003
361 | 
362 | - **¶17** → GEN-004, GEN-005, VAL-002
363 | 
364 | - **¶18** → BMR-001
365 | 
366 | - **¶19** → VAL-003
367 | 
368 | - **D.2/D.3** → BMR-001, BMR-002, VAL-001
369 | 
370 | - **C.3** → MON-002
371 | 
372 | - **7.1/7.2** → MON-004
373 | 
374 | 
375 | > Key phrases (quoted ≤20 words) appear under each instruction’s **Source** field.
376 | 
377 | * * *
378 | 
379 | B) Machine-readable JSON
380 | ========================
381 | 
382 |     {
383 |       "instruction_pack": {
384 |         "metadata": {
385 |           "primary_purpose": "Operationalize RPG/ZeroRepo for unified, scalable repository generation via a persistent planning graph and graph-guided TDD.",
386 |           "generated_at": "2025-09-30T00:00:00Z",
387 |           "language": "English",
388 |           "taxonomy_used": "Discover → Design → Build → Validate → Benchmark → Monitor"
389 |         },
390 |         "instructions": [
391 |           {
392 |             "id": "DSC-001",
393 |             "topic": "Discover",
394 |             "instruction": "Define <PROJECT_SPEC> with goals, scope, constraints, and acceptance metrics.",
395 |             "acceptance_criteria": [
396 |               "Doc includes <GOALS>, <NON_GOALS>, <CONSTRAINTS>, <METRICS>",
397 |               "Reviewed by <STAKEHOLDERS>"
398 |             ],
399 |             "dependencies": [],
400 |             "priority": "P0",
401 |             "risks": ["Ambiguity in scope"],
402 |             "mitigations": ["Add examples, anti-requirements"],
403 |             "tool_suggestions": ["markdown template"],
404 |             "source": {
405 |               "paragraph_indexes": [2],
406 |               "key_phrase": "generating complete repositories… demands coherent and reliable planning"
407 |             },
408 |             "tags": ["planning","inputs"]
409 |           },
410 |           {
411 |             "id": "DSC-002",
412 |             "topic": "Discover",
413 |             "instruction": "Specify RPG schema with <NODE_TYPES>, <EDGE_TYPES>, required fields, and DAG constraint.",
414 |             "acceptance_criteria": [
415 |               "JSON Schema validates nodes and edges",
416 |               "Acyclicity check available"
417 |             ],
418 |             "dependencies": ["DSC-001"],
419 |             "priority": "P0",
420 |             "risks": ["Over-general schema"],
421 |             "mitigations": ["Start minimal; iterate"],
422 |             "tool_suggestions": ["schema validator","graph DB"],
423 |             "source": {
424 |               "paragraph_indexes": [6],
425 |               "key_phrase": "nodes specify… files, classes… edges encode… data flows… ordering"
426 |             },
427 |             "tags": ["rpg","schema"]
428 |           },
429 |           {
430 |             "id": "DSC-003",
431 |             "topic": "Discover",
432 |             "instruction": "Assemble <FEATURE_TREE_SOURCE> and embed nodes into <VECTOR_DB>.",
433 |             "acceptance_criteria": [
434 |               "Embeddings stored with path metadata",
435 |               "Query latency < <EMBED_QPS>"
436 |             ],
437 |             "dependencies": ["DSC-001"],
438 |             "priority": "P0",
439 |             "risks": ["Ontology skew"],
440 |             "mitigations": ["Diversity-aware sampling"],
441 |             "tool_suggestions": ["embedding model","vector DB"],
442 |             "source": {
443 |               "paragraph_indexes": [7],
444 |               "key_phrase": "large-scale ontology… nodes embedded… vector database"
445 |             },
446 |             "tags": ["kb","retrieval"]
447 |           },
448 |           {
449 |             "id": "PROP-001",
450 |             "topic": "Proposal Design",
451 |             "instruction": "Retrieve top-k feature paths for <PROJECT_SPEC> into <CANDIDATES_EXPLOIT>.",
452 |             "acceptance_criteria": [
453 |               "k paths with scores and full hierarchical paths"
454 |             ],
455 |             "dependencies": ["DSC-003"],
456 |             "priority": "P0",
457 |             "risks": ["Narrow recall"],
458 |             "mitigations": ["Expand synonyms"],
459 |             "tool_suggestions": ["vector search"],
460 |             "source": {
461 |               "paragraph_indexes": [8],
462 |               "key_phrase": "retrieve top-k feature paths most aligned with the user goal"
463 |             },
464 |             "tags": ["retrieval","exploit"]
465 |           },
466 |           {
467 |             "id": "PROP-002",
468 |             "topic": "Proposal Design",
469 |             "instruction": "Sample unvisited ontology regions into <CANDIDATES_EXPLORE>.",
470 |             "acceptance_criteria": [
471 |               "≥ <N_EXPL> non-overlapping candidate paths"
472 |             ],
473 |             "dependencies": ["DSC-003"],
474 |             "priority": "P0",
475 |             "risks": ["Low precision"],
476 |             "mitigations": ["Diversity-aware rejection sampling"],
477 |             "tool_suggestions": ["sampler"],
478 |             "source": {
479 |               "paragraph_indexes": [8,21],
480 |               "key_phrase": "exploration ensures diversity… diversity-aware rejection mechanism"
481 |             },
482 |             "tags": ["retrieval","explore"]
483 |           },
484 |           {
485 |             "id": "PROP-003",
486 |             "topic": "Proposal Design",
487 |             "instruction": "Filter, rank, and merge candidates using <LLM_FILTER_PROMPT>.",
488 |             "acceptance_criteria": [
489 |               "Merged set deduped with rationales",
490 |               "Batch self-check logs stored"
491 |             ],
492 |             "dependencies": ["PROP-001","PROP-002"],
493 |             "priority": "P0",
494 |             "risks": ["LLM drift"],
495 |             "mitigations": ["Batch self-checks"],
496 |             "tool_suggestions": ["LLM"],
497 |             "source": {
498 |               "paragraph_indexes": [8],
499 |               "key_phrase": "LLM… filter candidates… self-check… insert paths"
500 |             },
501 |             "tags": ["filter","ranking"]
502 |           },
503 |           {
504 |             "id": "PROP-004",
505 |             "topic": "Proposal Design",
506 |             "instruction": "Refactor subtree into modules maximizing cohesion and minimizing coupling.",
507 |             "acceptance_criteria": [
508 |               "Modules have boundary definitions",
509 |               "Move/merge justifications recorded"
510 |             ],
511 |             "dependencies": ["PROP-003"],
512 |             "priority": "P0",
513 |             "risks": ["Over-fragmentation"],
514 |             "mitigations": ["Merge pass"],
515 |             "tool_suggestions": ["graph partitioner"],
516 |             "source": {
517 |               "paragraph_indexes": [9],
518 |               "key_phrase": "partitions functionalities into cohesive modules… cohesion and coupling"
519 |             },
520 |             "tags": ["modularity"]
521 |           },
522 |           {
523 |             "id": "PROP-005",
524 |             "topic": "Proposal Design",
525 |             "instruction": "Persist functionality graph as RPG layer L0 with version <RPG_VER>.",
526 |             "acceptance_criteria": [
527 |               "L0 saved and diffable",
528 |               "Checksum recorded"
529 |             ],
530 |             "dependencies": ["PROP-004"],
531 |             "priority": "P0",
532 |             "risks": ["Schema drift"],
533 |             "mitigations": ["Migration script"],
534 |             "tool_suggestions": ["git","graph DB"],
535 |             "source": {
536 |               "paragraph_indexes": [4],
537 |               "key_phrase": "persistent and evolvable representation that unifies planning"
538 |             },
539 |             "tags": ["versioning"]
540 |           },
541 |           {
542 |             "id": "IMPL-001",
543 |             "topic": "Implementation Design",
544 |             "instruction": "Map L0 modules to folder layout under <ROOT_DIR>/src as L1 folder nodes.",
545 |             "acceptance_criteria": [
546 |               "One folder per module",
547 |               "Mapping table created; lints pass"
548 |             ],
549 |             "dependencies": ["PROP-005"],
550 |             "priority": "P0",
551 |             "risks": ["Over-nesting"],
552 |             "mitigations": ["Cap depth"],
553 |             "tool_suggestions": ["scaffolder"],
554 |             "source": {
555 |               "paragraph_indexes": [10],
556 |               "key_phrase": "assign each subgraph a dedicated directory namespace"
557 |             },
558 |             "tags": ["folders"]
559 |           },
560 |           {
561 |             "id": "IMPL-002",
562 |             "topic": "Implementation Design",
563 |             "instruction": "Group intermediate nodes into files to create L2 file nodes.",
564 |             "acceptance_criteria": [
565 |               "Files are cohesive",
566 |               "PEP8 naming; directory size ≤ <MAX_FILES_PER_DIR>"
567 |             ],
568 |             "dependencies": ["IMPL-001"],
569 |             "priority": "P0",
570 |             "risks": ["Cross-file coupling"],
571 |             "mitigations": ["Regroup features"],
572 |             "tool_suggestions": ["file planner"],
573 |             "source": {
574 |               "paragraph_indexes": [11],
575 |               "key_phrase": "assigning files to intermediate nodes… preserve semantic cohesion"
576 |             },
577 |             "tags": ["files"]
578 |           },
579 |           {
580 |             "id": "IMPL-003",
581 |             "topic": "Implementation Design",
582 |             "instruction": "Encode inter-module data-flow edges with typed inputs and outputs.",
583 |             "acceptance_criteria": [
584 |               "Edges have from,to,data_id,data_type,transformation",
585 |               "DAG validation passes"
586 |             ],
587 |             "dependencies": ["IMPL-001"],
588 |             "priority": "P0",
589 |             "risks": ["Hidden cycles"],
590 |             "mitigations": ["Topological checks"],
591 |             "tool_suggestions": ["DAG validator"],
592 |             "source": {
593 |               "paragraph_indexes": [12],
594 |               "key_phrase": "typed input–output flows connect subgraph roots"
595 |             },
596 |             "tags": ["dataflow"]
597 |           },
598 |           {
599 |             "id": "IMPL-004",
600 |             "topic": "Implementation Design",
601 |             "instruction": "Define intra-module file ordering edges for build/load constraints.",
602 |             "acceptance_criteria": [
603 |               "Order edges exist and have no contradictions"
604 |             ],
605 |             "dependencies": ["IMPL-002"],
606 |             "priority": "P1",
607 |             "risks": ["Brittle imports"],
608 |             "mitigations": ["Lazy loading"],
609 |             "tool_suggestions": ["import graph analyzer"],
610 |             "source": {
611 |               "paragraph_indexes": [6,12],
612 |               "key_phrase": "intra-module file ordering… precedes… outputs propagated"
613 |             },
614 |             "tags": ["ordering"]
615 |           },
616 |           {
617 |             "id": "IMPL-005",
618 |             "topic": "Implementation Design",
619 |             "instruction": "Define <BASE_CLASSES> and shared data structures for recurring patterns.",
620 |             "acceptance_criteria": [
621 |               "Base types justified by reuse",
622 |               "Adoption rate ≥ <ADOPTION_RATE>"
623 |             ],
624 |             "dependencies": ["IMPL-003"],
625 |             "priority": "P1",
626 |             "risks": ["Premature abstraction"],
627 |             "mitigations": ["Usage-driven creation"],
628 |             "tool_suggestions": ["UML"],
629 |             "source": {
630 |               "paragraph_indexes": [13],
631 |               "key_phrase": "abstracted into common data structures or base classes"
632 |             },
633 |             "tags": ["abstractions"]
634 |           },
635 |           {
636 |             "id": "IMPL-006",
637 |             "topic": "Implementation Design",
638 |             "instruction": "Design one interface per leaf feature with docstring; choose func or class.",
639 |             "acceptance_criteria": [
640 |               "Exactly one interface/leaf",
641 |               "Docstring has purpose, args, returns"
642 |             ],
643 |             "dependencies": ["IMPL-002","IMPL-003","IMPL-005"],
644 |             "priority": "P0",
645 |             "risks": ["Over-classing"],
646 |             "mitigations": ["Prefer functions unless stateful"],
647 |             "tool_suggestions": ["interface generator"],
648 |             "source": {
649 |               "paragraph_indexes": [14],
650 |               "key_phrase": "independent features as functions… interdependent… shared classes"
651 |             },
652 |             "tags": ["interfaces"]
653 |           },
654 |           {
655 |             "id": "GEN-001",
656 |             "topic": "Build",
657 |             "instruction": "Topologically sort RPG and create reproducible <BUILD_QUEUE>.",
658 |             "acceptance_criteria": [
659 |               "Queue respects edges",
660 |               "Order persisted and reproducible"
661 |             ],
662 |             "dependencies": ["IMPL-003","IMPL-004"],
663 |             "priority": "P0",
664 |             "risks": ["Nondeterministic order"],
665 |             "mitigations": ["Seed and persist"],
666 |             "tool_suggestions": ["topo sort"],
667 |             "source": {
668 |               "paragraph_indexes": [15],
669 |               "key_phrase": "traverses the RPG in topological order"
670 |             },
671 |             "tags": ["build-plan"]
672 |           },
673 |           {
674 |             "id": "GEN-002",
675 |             "topic": "Build",
676 |             "instruction": "Auto-derive a unit test from each interface/spec before implementation.",
677 |             "acceptance_criteria": [
678 |               "Test executes in <TEST_RUNNER>",
679 |               "Covers normal and edge cases"
680 |             ],
681 |             "dependencies": ["IMPL-006"],
682 |             "priority": "P0",
683 |             "risks": ["Weak tests"],
684 |             "mitigations": ["Mutation testing"],
685 |             "tool_suggestions": ["test generator"],
686 |             "source": {
687 |               "paragraph_indexes": [15],
688 |               "key_phrase": "test-driven development… a test is derived"
689 |             },
690 |             "tags": ["tdd","tests"]
691 |           },
692 |           {
693 |             "id": "GEN-003",
694 |             "topic": "Build",
695 |             "instruction": "Implement code to pass the test; commit only on green.",
696 |             "acceptance_criteria": [
697 |               "Unit test green locally and in CI",
698 |               "Coverage ≥ <MIN_COV>"
699 |             ],
700 |             "dependencies": ["GEN-002"],
701 |             "priority": "P0",
702 |             "risks": ["Flaky tests"],
703 |             "mitigations": ["Rerun policy"],
704 |             "tool_suggestions": ["CI"],
705 |             "source": {
706 |               "paragraph_indexes": [15],
707 |               "key_phrase": "Only functions that pass all tests are committed"
708 |             },
709 |             "tags": ["tdd","commit-policy"]
710 |           },
711 |           {
712 |             "id": "GEN-004",
713 |             "topic": "Build",
714 |             "instruction": "Run regression tests for impacted nodes when code changes.",
715 |             "acceptance_criteria": [
716 |               "Impact set from graph edges",
717 |               "All prior tests green"
718 |             ],
719 |             "dependencies": ["GEN-003"],
720 |             "priority": "P0",
721 |             "risks": ["Large impact sets"],
722 |             "mitigations": ["Selective testing"],
723 |             "tool_suggestions": ["test impact analyzer"],
724 |             "source": {
725 |               "paragraph_indexes": [17],
726 |               "key_phrase": "Validated components trigger regression tests upon modification"
727 |             },
728 |             "tags": ["regression"]
729 |           },
730 |           {
731 |             "id": "GEN-005",
732 |             "topic": "Build",
733 |             "instruction": "Create integration tests per completed subgraph before release.",
734 |             "acceptance_criteria": [
735 |               "Data flows executed end-to-end",
736 |               "Contracts validated"
737 |             ],
738 |             "dependencies": ["GEN-003"],
739 |             "priority": "P1",
740 |             "risks": ["Complex orchestration"],
741 |             "mitigations": ["Synthetic fixtures"],
742 |             "tool_suggestions": ["integration harness"],
743 |             "source": {
744 |               "paragraph_indexes": [17],
745 |               "key_phrase": "completed subgraphs undergo integration tests"
746 |             },
747 |             "tags": ["integration"]
748 |           },
749 |           {
750 |             "id": "VAL-001",
751 |             "topic": "Validation",
752 |             "instruction": "Use majority-vote LLM to validate algorithm presence semantically.",
753 |             "acceptance_criteria": [
754 |               "5-vote majority with confidence ≥ <VOTE_THRESHOLD>"
755 |             ],
756 |             "dependencies": ["GEN-003"],
757 |             "priority": "P1",
758 |             "risks": ["Judge variance"],
759 |             "mitigations": ["Temp=0, tie-break"],
760 |             "tool_suggestions": ["LLM judge"],
761 |             "source": {
762 |               "paragraph_indexes": [17],
763 |               "key_phrase": "majority-vote checking is applied"
764 |             },
765 |             "tags": ["evaluation","semantics"]
766 |           },
767 |           {
768 |             "id": "VAL-002",
769 |             "topic": "Validation",
770 |             "instruction": "Attribute failures to code vs test/env; auto-remediate test/env cases.",
771 |             "acceptance_criteria": [
772 |               "Errors labeled; ≤ <N_REMEDIATIONS> auto fixes attempted"
773 |             ],
774 |             "dependencies": ["GEN-003"],
775 |             "priority": "P1",
776 |             "risks": ["Misattribution"],
777 |             "mitigations": ["Heuristics + review"],
778 |             "tool_suggestions": ["log analyzer"],
779 |             "source": {
780 |               "paragraph_indexes": [17],
781 |               "key_phrase": "distinguishes… and automatically handling the latter"
782 |             },
783 |             "tags": ["triage"]
784 |           },
785 |           {
786 |             "id": "VAL-003",
787 |             "topic": "Validation",
788 |             "instruction": "Compute Coverage, Novelty, Pass Rate, Voting Rate, Files, LOC, Tokens.",
789 |             "acceptance_criteria": [
790 |               "Formulas per spec implemented",
791 |               "Results in <METRICS_STORE>"
792 |             ],
793 |             "dependencies": ["PROP-005","GEN-003"],
794 |             "priority": "P0",
795 |             "risks": ["Category drift"],
796 |             "mitigations": ["Fixed centroids + audit"],
797 |             "tool_suggestions": ["metrics job"],
798 |             "source": {
799 |               "paragraph_indexes": [19],
800 |               "key_phrase": "Coverage… Novelty… Pass Rate… Voting Rate… code statistics"
801 |             },
802 |             "tags": ["metrics"]
803 |           },
804 |           {
805 |             "id": "BMR-001",
806 |             "topic": "Benchmark",
807 |             "instruction": "Parse reference tests into <TASKS> with NL descriptions; filter trivial.",
808 |             "acceptance_criteria": [
809 |               "> <N_TASKS> tasks with inputs/outputs",
810 |               "Non-algorithmic tests removed"
811 |             ],
812 |             "dependencies": ["DSC-001"],
813 |             "priority": "P1",
814 |             "risks": ["Leakage"],
815 |             "mitigations": ["Anonymize names"],
816 |             "tool_suggestions": ["test parser"],
817 |             "source": {
818 |               "paragraph_indexes": [18],
819 |               "key_phrase": "derive tasks from reference repositories… filter out trivial"
820 |             },
821 |             "tags": ["benchmark","tasks"]
822 |           },
823 |           {
824 |             "id": "BMR-002",
825 |             "topic": "Benchmark",
826 |             "instruction": "Run localization → validation → execution loop for each task.",
827 |             "acceptance_criteria": [
828 |               "Candidate localized or absence recorded",
829 |               "Adapted test executed and logged"
830 |             ],
831 |             "dependencies": ["BMR-001","VAL-001"],
832 |             "priority": "P1",
833 |             "risks": ["False negatives"],
834 |             "mitigations": ["Retry budget"],
835 |             "tool_suggestions": ["harness runner"],
836 |             "source": {
837 |               "paragraph_indexes": [18],
838 |               "key_phrase": "localization… validation… execution testing… verify correctness"
839 |             },
840 |             "tags": ["evaluation-loop"]
841 |           },
842 |           {
843 |             "id": "MON-001",
844 |             "topic": "Monitor",
845 |             "instruction": "Validate DAG acyclicity and schema in CI on every RPG change.",
846 |             "acceptance_criteria": [
847 |               "CI blocks cycles and schema violations",
848 |               "Error report lists offending edges"
849 |             ],
850 |             "dependencies": ["DSC-002","IMPL-003"],
851 |             "priority": "P0",
852 |             "risks": ["Slow checks"],
853 |             "mitigations": ["Caching"],
854 |             "tool_suggestions": ["CI job"],
855 |             "source": {
856 |               "paragraph_indexes": [12],
857 |               "key_phrase": "topological order… acyclic structure"
858 |             },
859 |             "tags": ["ci","governance"]
860 |           },
861 |           {
862 |             "id": "MON-002",
863 |             "topic": "Monitor",
864 |             "instruction": "Record localization tool steps and outcomes for audit.",
865 |             "acceptance_criteria": [
866 |               "Structured logs per step",
867 |               "PII scrubbed; replayable"
868 |             ],
869 |             "dependencies": ["GEN-001"],
870 |             "priority": "P2",
871 |             "risks": ["Excessive volume"],
872 |             "mitigations": ["Sampling"],
873 |             "tool_suggestions": ["structured logging"],
874 |             "source": {
875 |               "paragraph_indexes": [28],
876 |               "key_phrase": "logs… demonstrate the end-to-end process… tool invocations"
877 |             },
878 |             "tags": ["audit"]
879 |           },
880 |           {
881 |             "id": "MON-003",
882 |             "topic": "Governance",
883 |             "instruction": "Run license and security checks on generated code and dependencies.",
884 |             "acceptance_criteria": [
885 |               "SBOM created",
886 |               "Licenses compliant; no secrets"
887 |             ],
888 |             "dependencies": ["GEN-003"],
889 |             "priority": "P0",
890 |             "risks": ["False positives"],
891 |             "mitigations": ["Allowlist with review"],
892 |             "tool_suggestions": ["SBOM","license scanner","secret scanner"],
893 |             "source": {
894 |               "paragraph_indexes": [1],
895 |               "key_phrase": "scalable repository generation raises practical governance needs"
896 |             },
897 |             "tags": ["compliance","security"]
898 |           },
899 |           {
900 |             "id": "MON-004",
901 |             "topic": "Monitor",
902 |             "instruction": "Track feature and LOC scaling over iterations; alert on stagnation.",
903 |             "acceptance_criteria": [
904 |               "Dashboards for features and LOC",
905 |               "Alert when slope < <MIN_SLOPE>"
906 |             ],
907 |             "dependencies": ["VAL-003"],
908 |             "priority": "P2",
909 |             "risks": ["Metric gaming"],
910 |             "mitigations": ["Correlate with pass rate"],
911 |             "tool_suggestions": ["dashboard"],
912 |             "source": {
913 |               "paragraph_indexes": [29],
914 |               "key_phrase": "near-linear growth of functionalities and repository size"
915 |             },
916 |             "tags": ["scaling","monitoring"]
917 |           }
918 |         ],
919 |         "trace_matrix": [
920 |           { "paragraph_index": 1, "instruction_ids": ["MON-003"] },
921 |           { "paragraph_index": 2, "instruction_ids": ["DSC-001"] },
922 |           { "paragraph_index": 4, "instruction_ids": ["PROP-005"] },
923 |           { "paragraph_index": 6, "instruction_ids": ["DSC-002","IMPL-004"] },
924 |           { "paragraph_index": 7, "instruction_ids": ["DSC-003"] },
925 |           { "paragraph_index": 8, "instruction_ids": ["PROP-001","PROP-002","PROP-003"] },
926 |           { "paragraph_index": 9, "instruction_ids": ["PROP-004"] },
927 |           { "paragraph_index": 10, "instruction_ids": ["IMPL-001"] },
928 |           { "paragraph_index": 11, "instruction_ids": ["IMPL-002"] },
929 |           { "paragraph_index": 12, "instruction_ids": ["IMPL-003","MON-001"] },
930 |           { "paragraph_index": 13, "instruction_ids": ["IMPL-005"] },
931 |           { "paragraph_index": 14, "instruction_ids": ["IMPL-006"] },
932 |           { "paragraph_index": 15, "instruction_ids": ["GEN-001","GEN-002","GEN-003"] },
933 |           { "paragraph_index": 17, "instruction_ids": ["GEN-004","GEN-005","VAL-002"] },
934 |           { "paragraph_index": 18, "instruction_ids": ["BMR-001","BMR-002"] },
935 |           { "paragraph_index": 19, "instruction_ids": ["VAL-003"] },
936 |           { "paragraph_index": 28, "instruction_ids": ["MON-002"] },
937 |           { "paragraph_index": 29, "instruction_ids": ["MON-004"] }
938 |         ]
939 |       }
940 |     }
941 | 
942 | 
943 | _Notes:_ IDs are unique and single-action; placeholders use ASCII angle brackets; risks/mitigations and tool suggestions are provider-agnostic. All items trace back to whitepaper passages (paragraph indices with ≤20-word key phrases). RPG_REPOSITORY_PLANNING_GRAPH
944 | 
945 | ---
946 | 
```

codefetch.config.mjs
```
1 | /** @type {import('codefetch').CodefetchConfig} */
2 | export default {
3 |   "projectTree": 2,
4 |   "tokenLimiter": "truncated",
5 |   "defaultPromptFile": "default.md",
6 |   "tokenLimiter": "truncated"
7 | };
```

execution-order.md
```
1 | Here’s the **execution order** that’s aligned to the RPG pipeline — **Discover → Design → Build → Validate → Benchmark → Monitor** — and consistent with the whitepaper’s sequence (implementation-level refinement before graph-guided topo build). Where a task’s minimal deps would allow earlier execution (e.g., GEN-001), I place it later so the build plan captures intra-module order and full constraints, which is the safer choice for stability. (Build Guide trace matrix; Whitepaper Fig. 1 “B1/B2 before C”. )
2 | 
3 | 1. **4 — [DSC-001] Develop Project Spec Parser**.
4 | 2. **1 — [DSC-002] Define Detailed RPG Schema**.
5 | 3. **2 — Extend Graph Service for Typed Nodes and Edges** (uses schema).
6 | 4. **6 — [DSC-003] Build Feature Tree Index** (spec → feature tree).
7 | 5. **7 — [PROP-001] Exploit Retrieval (top-k)**.
8 | 6. **8 — [PROP-002] Explore Sampling (diversity)**.
9 | 7. **9 — [PROP-003] LLM Filter & Merge**.
10 | 8. **10 — [PROP-004] Refactor into Cohesive Modules**.
11 | 9. **11 — [PROP-005] Persist L0 Functionality Graph**.
12 | 10. **5 — [IMPL-001] Map Nodes → Folders** (L0→L1).
13 | 11. **12 — [IMPL-002] Group Capabilities into Files** (L1→L2).
14 | 12. **13 — [IMPL-003] Encode Typed Data-Flows**.
15 | 13. **26 — [MON-001] CI Gate: DAG & Schema** (turn on guardrails now that data-flows exist).
16 | 14. **14 — [IMPL-004] Define Intra-Module File Order**.
17 | 15. **30 — [IMPL-004] Intra-Module Order Lints**.
18 | 16. **15 — [IMPL-005] Abstract Base Classes & Shared Types** (usage-driven).
19 | 17. **16 — [IMPL-006] One Interface per Leaf**.
20 | 18. **3 — [GEN-001] Topological Build Plan Generator** (placed **after** IMPL so order edges & data-flows are respected).
21 | 19. **27 — [MON-002] Audit Logging of Localization Steps** (depends on planner).
22 | 20. **17 — [GEN-002] Auto-Derive Unit Tests**.
23 | 21. **18 — [GEN-003] Implement-to-Green & Coverage Gate**.
24 | 22. **19 — [GEN-004] Selective Regression by Impact**.
25 | 23. **20 — [GEN-005] Integration Tests per Subgraph**.
26 | 24. **21 — [VAL-001] Majority-Vote Semantic Validator**.
27 | 25. **22 — [VAL-002] Failure Attribution & Auto-Remediation**.
28 | 26. **23 — [VAL-003] RepoCraft Metrics (Coverage/Novelty/Pass/Vote/Files/LOC/Tokens)**.
29 | 27. **24 — [BMR-001] Build Benchmark Task Set**.
30 | 28. **25 — [BMR-002] Evaluation Loop per Task**.
31 | 29. **28 — [MON-003] Governance: SBOM, Licenses, Secrets** (after core GEN loop exists).
32 | 30. **29 — [MON-004] Scaling Dashboards** (after metrics).
33 | 
34 | ### Machine-readable order
35 | 
36 | ```json
37 | {
38 |   "execution_order": [
39 |     {"id": 4, "title": "[DSC-001] Develop Project Spec Parser"},
40 |     {"id": 1, "title": "[DSC-002] Define Detailed RPG Schema"},
41 |     {"id": 2, "title": "Extend Graph Service for Typed Nodes and Edges"},
42 |     {"id": 6, "title": "[DSC-003] Build Feature Tree Index"},
43 |     {"id": 7, "title": "[PROP-001] Exploit Retrieval"},
44 |     {"id": 8, "title": "[PROP-002] Explore Sampling"},
45 |     {"id": 9, "title": "[PROP-003] LLM Filter & Merge"},
46 |     {"id": 10, "title": "[PROP-004] Refactor into Cohesive Modules"},
47 |     {"id": 11, "title": "[PROP-005] Persist L0 Functionality Graph"},
48 |     {"id": 5, "title": "[IMPL-001] Map Graph Nodes to File System Structure"},
49 |     {"id": 12, "title": "[IMPL-002] Group Capabilities into Files"},
50 |     {"id": 13, "title": "[IMPL-003] Encode Typed Data-Flows"},
51 |     {"id": 26, "title": "[MON-001] CI Gate: DAG & Schema"},
52 |     {"id": 14, "title": "[IMPL-004] Define Intra-Module File Order"},
53 |     {"id": 30, "title": "[IMPL-004] Intra-Module Order Lints"},
54 |     {"id": 15, "title": "[IMPL-005] Abstract Base Classes & Shared Types"},
55 |     {"id": 16, "title": "[IMPL-006] Define One Interface per Leaf"},
56 |     {"id": 3, "title": "[GEN-001] Topological Build Plan Generator"},
57 |     {"id": 27, "title": "[MON-002] Audit Logging of Localization Steps"},
58 |     {"id": 17, "title": "[GEN-002] Auto-Derive Unit Tests"},
59 |     {"id": 18, "title": "[GEN-003] Implement to Green & Gate Commits"},
60 |     {"id": 19, "title": "[GEN-004] Selective Regression by Impact"},
61 |     {"id": 20, "title": "[GEN-005] Add Integration Tests per Subgraph"},
62 |     {"id": 21, "title": "[VAL-001] Majority-Vote Semantic Validator"},
63 |     {"id": 22, "title": "[VAL-002] Failure Attribution & Auto-Remediation"},
64 |     {"id": 23, "title": "[VAL-003] RepoCraft Metrics"},
65 |     {"id": 24, "title": "[BMR-001] Build Benchmark Task Set"},
66 |     {"id": 25, "title": "[BMR-002] Evaluation Loop per Task"},
67 |     {"id": 28, "title": "[MON-003] Governance: SBOM, Licenses, Secrets"},
68 |     {"id": 29, "title": "[MON-004] Scaling Dashboards"}
69 |   ]
70 | }
71 | ```
72 | 
73 | **Why this order:** It respects all declared deps in your task list while enforcing the paper/guide’s staging: proposal & implementation refinement precede topo build and codegen, which then feed validation, benchmarking, and monitoring. This avoids unstable plans and ensures the build queue is constrained by both inter-module data-flows and intra-module order. (Whitepaper Fig. 1; Build Guide §Trace Matrix IMPL→GEN→VAL→BMR→MON).
```

quick-reference-execution-guide.md
```
1 | Here’s a quick-reference you can use to jump to the right place in our two sources for **each step of the execution order**. For each item I list the **Build Guide instruction (procedural)** and the **Whitepaper anchor (concept/conceptual)** as recorded in the guide’s Trace Matrix/“Source” fields.
2 | 
3 | - **4 — DSC-001 · Develop Project Spec Parser** → **Build Guide:** DSC-001 (Discover). **Whitepaper:** ¶2.
4 | - **1 — DSC-002 · Define RPG Schema** → **Build Guide:** DSC-002. **Whitepaper:** ¶6.
5 | - **2 — Extend Graph Service (typed nodes/edges)** → **Build Guide:** under DSC-002 (schema adoption) and IMPL-003 (typed data_flow semantics). **Whitepaper:** ¶6/¶12 (nodes/edges, DAG).
6 | - **6 — DSC-003 · Feature Tree Index** → **Build Guide:** DSC-003. **Whitepaper:** ¶7 (global feature tree).
7 | - **7 — PROP-001 · Exploit Retrieval (top-k)** → **Build Guide:** PROP-001. **Whitepaper:** ¶8 (proposal-stage retrieval).
8 | - **8 — PROP-002 · Explore Sampling (diversity)** → **Build Guide:** PROP-002. **Whitepaper:** ¶8.
9 | - **9 — PROP-003 · LLM Filter & Merge** → **Build Guide:** PROP-003. **Whitepaper:** ¶8 (batch self-check).
10 | - **10 — PROP-004 · Refactor into Cohesive Modules** → **Build Guide:** PROP-004. **Whitepaper:** ¶9 (reorganization into functionality graph).
11 | - **11 — PROP-005 · Persist L0 Functionality Graph** → **Build Guide:** PROP-005. **Whitepaper:** ¶4 (persistence/versioning motivation).
12 | - **5 — IMPL-001 · Map nodes→folders (L0→L1)** → **Build Guide:** IMPL-001. **Whitepaper:** ¶10.
13 | - **12 — IMPL-002 · Group capabilities into files (L1→L2)** → **Build Guide:** IMPL-002. **Whitepaper:** ¶11.
14 | - **13 — IMPL-003 · Encode typed data-flows** → **Build Guide:** IMPL-003. **Whitepaper:** ¶12 (DAG/acyclicity).
15 | - **26 — MON-001 · CI gate: DAG & schema** → **Build Guide:** MON-001. **Whitepaper:** ¶12.
16 | - **14 — IMPL-004 · Intra-module file order (define)** → **Build Guide:** IMPL-004. **Whitepaper:** ¶6 (order edges).
17 | - **30 — IMPL-004 · Intra-module order lints** → **Build Guide:** IMPL-004 (linting follow-on). **Whitepaper:** ¶6.
18 | - **15 — IMPL-005 · Abstract base classes & shared types** → **Build Guide:** IMPL-005. **Whitepaper:** ¶13.
19 | - **16 — IMPL-006 · One interface per leaf** → **Build Guide:** IMPL-006. **Whitepaper:** ¶14.
20 | - **3 — GEN-001 · Topological build plan** → **Build Guide:** GEN-001. **Whitepaper:** ¶15 (graph-guided TDD/topo).
21 | - **27 — MON-002 · Audit logging of localization steps** → **Build Guide:** MON-002. **Whitepaper:** C.3 (audit logs/tool calls).
22 | - **17 — GEN-002 · Auto-derive unit tests** → **Build Guide:** GEN-002. **Whitepaper:** ¶15.
23 | - **18 — GEN-003 · Implement-to-green & coverage gate** → **Build Guide:** GEN-003. **Whitepaper:** ¶15.
24 | - **19 — GEN-004 · Selective regression by impact** → **Build Guide:** GEN-004. **Whitepaper:** ¶17 (staged testing/regression).
25 | - **20 — GEN-005 · Integration tests per subgraph** → **Build Guide:** GEN-005. **Whitepaper:** ¶17.
26 | - **21 — VAL-001 · Majority-vote semantic validator** → **Build Guide:** Validation list; mapped via Trace Matrix. **Whitepaper:** D.3/D.3.1 (vote-based judging).
27 | - **22 — VAL-002 · Failure attribution & auto-remediation** → **Build Guide:** VAL-002. **Whitepaper:** ¶17 (diagnosis in staged loop).
28 | - **23 — VAL-003 · RepoCraft metrics (Coverage/Novelty/Pass/Vote/Files/LOC/Tokens)** → **Build Guide:** VAL-003. **Whitepaper:** ¶19 (metrics), §5/Appendix D references in checklist.
29 | - **24 — BMR-001 · Build benchmark task set** → **Build Guide:** BMR-001. **Whitepaper:** D.2 (task harvesting).
30 | - **25 — BMR-002 · Evaluation loop per task** → **Build Guide:** BMR-002. **Whitepaper:** D.3 (localize → vote → execute).
31 | - **28 — MON-003 · Governance: SBOM, licenses, secrets** → **Build Guide:** MON-003 (governance). **Whitepaper:** (policy/gov motivation noted; no specific section call-out).
32 | - **29 — MON-004 · Scaling dashboards** → **Build Guide:** MON-004. **Whitepaper:** §7.1/§7.2 (near-linear growth & scaling).
```

.codex/AGENTS.md
```
1 | # AGENTS.md — Tool Selection (Python)
2 | 
3 | When you need to call tools from the shell, use this rubric:
4 | 
5 | ## File & Text
6 | 
7 | - Find files by file name: `fd`
8 | - Find files with path name: `fd -p <file-path>`
9 | - List files in a directory: `fd . <directory>`
10 | - Find files with extension and pattern: `fd -e <extension> <pattern>`
11 | - Find Text: `rg` (ripgrep)
12 | - Find Code Structure: `ast-grep`
13 |   - Common languages:
14 |     - Python → `ast-grep --lang python -p '<pattern>'`
15 |     - TypeScript → `ast-grep --lang ts -p '<pattern>'`
16 |     - Bash → `ast-grep --lang bash -p '<pattern>'`
17 |     - TSX (React) → `ast-grep --lang tsx -p '<pattern>'`
18 |     - JavaScript → `ast-grep --lang js -p '<pattern>'`
19 |     - Rust → `ast-grep --lang rust -p '<pattern>'`
20 |     - JSON → `ast-grep --lang json -p '<pattern>'`
21 |   - Prefer `ast-grep` over ripgrep/grep unless a plain-text search is explicitly requested.
22 | - Select among matches: pipe to `fzf`
23 | 
24 | ## Data
25 | 
26 | - JSON: `jq`
27 | - YAML/XML: `yq`
28 | 
29 | ## Python Tooling
30 | 
31 | - Package Management & Virtual Envs: `uv`
32 |   (fast replacement for pip/pip-tools/virtualenv; use `uv pip install ...`, `uv run ...`)
33 | - Linting & Formatting: `ruff`
34 |   (linter + formatter; use `ruff check .`, `ruff format .`)
35 | - Static Typing: `mypy`
36 |   (type checking; use `mypy .`)
37 | - Security: `bandit`
38 |   (Python security linter; use `bandit -r .`)
39 | - Testing: `pytest`
40 |   (test runner; use `pytest -q`, `pytest -k <pattern>` to filter tests)
41 | - Logging: `loguru`
42 |   (runtime logging utility; import in code:
43 | 
44 |   ```python
45 |   from loguru import logger
46 |   logger.info("message")
47 |   ```)
48 | 
49 | ## Notes
50 | 
51 | - Prefer uv for Python dependency and environment management instead of pip/venv/poetry/pip-tools.
52 | 
53 | 
54 | You are **RPG Assistant**, an expert grounded in two attached documents that are your **only sources of truth**: (1) the official whitepaper *“RPG: A Repository Planning Graph for Unified and Scalable Codebase Generation”*  and (2) the operational *“RPG build guide.md”* . Answer the user’s questions **strictly by citing these docs**—prefer the whitepaper for concepts/definitions and the build guide for procedures. If they conflict, state both briefly, then adopt the whitepaper’s definition and the build guide’s implementation steps.
55 | 
56 | ### What to do
57 | 
58 | 1. **Identify intent & scope** of the user’s query (conceptual vs. how-to vs. troubleshooting vs. evaluation).
59 | 2. **Locate** the relevant sections:
60 | 
61 |    - Concepts, pipeline, metrics, RepoCraft, RPG structure/topology → **whitepaper** (e.g., RPG nodes/edges, proposal/implementation stages, graph-guided TDD, coverage/novelty metrics).
62 |    - Step-by-step actions, IDs, acceptance criteria, tooling, CI rules → **build guide** (e.g., DSC-001, PROP-001..005, IMPL-001..006, GEN-001..005, VAL/BMR/MON).
63 | 3. **Answer with evidence** (short quotes ≤20 words only when necessary) and **inline citations** to the exact doc you used.
64 | 4. **If info is missing** from both docs, say so plainly, list the exact missing pieces, and suggest the nearest doc-backed alternative—not external facts.
65 | 5. **Never speculate** or introduce outside material unless the user explicitly asks you to broaden beyond these docs.
66 | 
67 | ### How to format every answer
68 | 
69 | - **Answer:** A crisp, user-level response (bullets or short paragraphs).
70 | - **RPG mapping:** Name the relevant RPG stage(s) or build-guide step IDs (e.g., “IMPL-003 data-flow DAG”).
71 | - **Steps / Checklist (if procedural):** Ordered actions referencing build-guide IDs with one-line acceptance criteria.
72 | - **Citations:** Inline after the sentence(s) they support; cite the specific source (whitepaper vs build guide).
73 | - **Assumptions (if any):** Keep to one short line, and only if unavoidable.
74 | 
75 | ### Style & guardrails
76 | 
77 | - Be precise and actionable; keep replies focused and brief.
78 | - Do not expose chain-of-thought; use concise rationales instead.
79 | - Use the build-guide taxonomy when proposing work (**Discover → Design → Build → Validate → Benchmark → Monitor**).
80 | - Use whitepaper terminology for RPG semantics (nodes: capability/folder/file/class/function; edges: hierarchy/data-flow/order; DAG/topological traversal).
81 | - For metrics, report Coverage, Novelty, Pass/Vote rates, Files/LOC/Tokens exactly as defined.
82 | 
83 | ### Examples of acceptable references in your prose
84 | 
85 | - “Encode inter-module typed I/O and ensure a DAG (IMPL-003).”
86 | - “Traverse RPG in topological order with graph-guided TDD.”
87 | 
88 | **Important:** All factual claims must be backed by one of the two sources above, with inline citations. If the user asks for comparisons, outside tooling, or unrelated frameworks, politely state that such content is outside the current knowledge bank and ask whether they want to broaden scope.
```

.github/pull_request_tempate.md
```
1 | <!-- path: .github/pull_request_template.md -->
2 | # PR Checklist — DSC‑001 Gate
3 | 
4 | 
5 | **Purpose:** Ensure the project spec meets DSC‑001 before merging.
6 | 
7 | 
8 | - [ ] Spec lives at `docs/PROJECT_SPEC.md` (or uses the template name).
9 | - [ ] Sections present & non‑empty: **Goals · Non‑Goals · Constraints · Acceptance Metrics**.
10 | - [ ] Stakeholders listed and marked **approved**.
11 | - [ ] (If changed) `tools/validate_project_spec` run locally and in CI.
12 | 
13 | 
14 | > Paste the validator output here (OK / errors):
```

docs/PROJECT_SPEC.example.md
```
1 | <!-- path: docs/PROJECT_SPEC.example.md -->
2 | # RPG‑Build‑Assistant — Project Spec (Example)
3 | 
4 | 
5 | ## Goals
6 | 
7 | - Parse a markdown **Project Spec** into JSON `{goals[], non_goals[], constraints[], metrics[]}`.
8 | - Fail CI when any required section is missing/empty.
9 | 
10 | 
11 | ## Non-Goals
12 | 
13 | - Build the full RPG schema.
14 | - Generate code from the spec.
15 | 
16 | 
17 | ## Constraints
18 | 
19 | - Python 3.11; no external deps.
20 | - Runs in CI in < 5s.
21 | 
22 | 
23 | ## Acceptance Metrics
24 | 
25 | - Validator returns **OK** for `docs/PROJECT_SPEC.example.md`.
26 | - CI job fails on malformed specs.
27 | 
28 | 
29 | ### Stakeholders & Review
30 | 
31 | - **Owner:** Repo Maintainer
32 | - **Stakeholders:** PM, Tech Lead
33 | - **Review Status:** approved
34 | 
35 | 
36 | ### Context
37 | 
38 | - Downstream task will use this JSON as input.
```

docs/PROJECT_SPEC.template.md
```
1 | <!-- path: docs/PROJECT_SPEC.template.md -->
2 | # <PROJECT_NAME> — Project Spec
3 | 
4 | 
5 | > Fill the four mandatory sections. Keep each bullet concise (one idea per line). Use **Non‑Goals** to prevent scope creep.
6 | 
7 | 
8 | ## Goals
9 | 
10 | - <what outcomes we want>
11 | - <primary user problems we solve>
12 | 
13 | 
14 | ## Non-Goals
15 | 
16 | - <explicitly out of scope>
17 | - <things we won’t do>
18 | 
19 | 
20 | ## Constraints
21 | 
22 | - <technical or policy constraints>
23 | - <time/cost/platform limits>
24 | 
25 | 
26 | ## Acceptance Metrics
27 | 
28 | - <measurable success criteria (e.g., pass rate ≥ X%, coverage ≥ Y%)>
29 | - <launch gates or SLOs>
30 | 
31 | 
32 | ---
33 | 
34 | 
35 | ### Stakeholders & Review
36 | 
37 | - **Owner:** <name>
38 | - **Stakeholders:** <name1>, <name2>
39 | - **Review Status:** <pending | approved>
40 | 
41 | 
42 | ### Context (Optional)
43 | 
44 | - Link to docs, tickets, or prior art.
45 | 
46 | 
47 | ### Changelog (Optional)
48 | 
49 | - YYYY‑MM‑DD — <note>
```

docs/featureTreeSeed.local.json
```
1 | {
2 |   "metadata": {
3 |     "name": "RPG Global Feature Tree — Local Seed",
4 |     "version": "0.1.0",
5 |     "generated_at": "2025-10-01T00:00:00Z",
6 |     "rpg_alignment": {
7 |       "build_guide_ids": ["DSC-003"],
8 |       "whitepaper_sections": ["§3.2", "Appx A.2"]
9 |     },
10 |     "description": "Bootstrapped, self-contained feature tree seed with hierarchical nodes and a minimal retrieval index to ground proposal-level planning locally.",
11 |     "levels": 4,
12 |     "stats": { "node_count": 44 }
13 |   },
14 |   "schema": {
15 |     "node": {
16 |       "id": "string",
17 |       "path": "string (slash-delimited hierarchy)",
18 |       "name": "string",
19 |       "level": "integer (1=root … n=leaf)",
20 |       "ancestors": "string[]",
21 |       "description": "string",
22 |       "tags": "string[]",
23 |       "aliases": "string[]"
24 |     },
25 |     "hierarchy_edges": { "parent": "node.id", "child": "node.id" },
26 |     "retrieval": {
27 |       "embedding_method": "feature_hashing_bigrams",
28 |       "dims": 8,
29 |       "vectors": { "node.id": "float[dims] for leaf nodes" },
30 |       "inverted_index": { "token": "node.id[]" }
31 |     }
32 |   },
33 |   "nodes": [
34 |     {
35 |       "id": "FT-0001",
36 |       "path": "ml",
37 |       "name": "Machine Learning",
38 |       "level": 1,
39 |       "ancestors": [],
40 |       "description": "ML-related functionality root.",
41 |       "tags": ["ml"],
42 |       "aliases": []
43 |     },
44 |     {
45 |       "id": "FT-0002",
46 |       "path": "data",
47 |       "name": "Data",
48 |       "level": 1,
49 |       "ancestors": [],
50 |       "description": "Data ingestion and preprocessing.",
51 |       "tags": ["data"],
52 |       "aliases": []
53 |     },
54 |     {
55 |       "id": "FT-0003",
56 |       "path": "evaluation",
57 |       "name": "Evaluation",
58 |       "level": 1,
59 |       "ancestors": [],
60 |       "description": "Metrics and validation.",
61 |       "tags": ["eval"],
62 |       "aliases": []
63 |     },
64 |     {
65 |       "id": "FT-0004",
66 |       "path": "io",
67 |       "name": "I/O",
68 |       "level": 1,
69 |       "ancestors": [],
70 |       "description": "Serialization and persistence.",
71 |       "tags": ["io"],
72 |       "aliases": []
73 |     },
74 | 
75 |     {
76 |       "id": "FT-0101",
77 |       "path": "ml/algorithms",
78 |       "name": "Algorithms",
79 |       "level": 2,
80 |       "ancestors": ["ml"],
81 |       "description": "Learning algorithms.",
82 |       "tags": ["ml"],
83 |       "aliases": []
84 |     },
85 |     {
86 |       "id": "FT-0102",
87 |       "path": "ml/model_selection",
88 |       "name": "Model Selection",
89 |       "level": 2,
90 |       "ancestors": ["ml"],
91 |       "description": "Hyperparameter tuning and selection.",
92 |       "tags": ["ml", "selection"],
93 |       "aliases": []
94 |     },
95 | 
96 |     {
97 |       "id": "FT-0201",
98 |       "path": "data/loading",
99 |       "name": "Loading",
100 |       "level": 2,
101 |       "ancestors": ["data"],
102 |       "description": "Read data from files.",
103 |       "tags": ["io", "data"],
104 |       "aliases": []
105 |     },
106 |     {
107 |       "id": "FT-0202",
108 |       "path": "data/preprocessing",
109 |       "name": "Preprocessing",
110 |       "level": 2,
111 |       "ancestors": ["data"],
112 |       "description": "Transform raw data.",
113 |       "tags": ["prep"],
114 |       "aliases": []
115 |     },
116 | 
117 |     {
118 |       "id": "FT-0301",
119 |       "path": "evaluation/metrics",
120 |       "name": "Metrics",
121 |       "level": 2,
122 |       "ancestors": ["evaluation"],
123 |       "description": "Quality measures.",
124 |       "tags": ["metrics"],
125 |       "aliases": []
126 |     },
127 |     {
128 |       "id": "FT-0302",
129 |       "path": "evaluation/validation",
130 |       "name": "Validation",
131 |       "level": 2,
132 |       "ancestors": ["evaluation"],
133 |       "description": "Train/test protocols.",
134 |       "tags": ["validation"],
135 |       "aliases": []
136 |     },
137 | 
138 |     {
139 |       "id": "FT-0401",
140 |       "path": "io/persistence",
141 |       "name": "Persistence",
142 |       "level": 2,
143 |       "ancestors": ["io"],
144 |       "description": "Save/load models.",
145 |       "tags": ["persistence"],
146 |       "aliases": []
147 |     },
148 |     {
149 |       "id": "FT-0402",
150 |       "path": "io/serialization",
151 |       "name": "Serialization",
152 |       "level": 2,
153 |       "ancestors": ["io"],
154 |       "description": "Object serialization.",
155 |       "tags": ["serialization"],
156 |       "aliases": []
157 |     },
158 | 
159 |     {
160 |       "id": "FT-0111",
161 |       "path": "ml/algorithms/regression",
162 |       "name": "Regression",
163 |       "level": 3,
164 |       "ancestors": ["ml", "algorithms"],
165 |       "description": "Continuous target prediction.",
166 |       "tags": ["regression"],
167 |       "aliases": []
168 |     },
169 |     {
170 |       "id": "FT-0112",
171 |       "path": "ml/algorithms/classification",
172 |       "name": "Classification",
173 |       "level": 3,
174 |       "ancestors": ["ml", "algorithms"],
175 |       "description": "Discrete label prediction.",
176 |       "tags": ["classification"],
177 |       "aliases": []
178 |     },
179 |     {
180 |       "id": "FT-0113",
181 |       "path": "ml/algorithms/clustering",
182 |       "name": "Clustering",
183 |       "level": 3,
184 |       "ancestors": ["ml", "algorithms"],
185 |       "description": "Unsupervised grouping.",
186 |       "tags": ["clustering"],
187 |       "aliases": []
188 |     },
189 | 
190 |     {
191 |       "id": "FT-0211",
192 |       "path": "data/loading/csv",
193 |       "name": "CSV",
194 |       "level": 3,
195 |       "ancestors": ["data", "loading"],
196 |       "description": "Comma-separated values.",
197 |       "tags": ["csv"],
198 |       "aliases": []
199 |     },
200 |     {
201 |       "id": "FT-0212",
202 |       "path": "data/loading/json",
203 |       "name": "JSON",
204 |       "level": 3,
205 |       "ancestors": ["data", "loading"],
206 |       "description": "JavaScript Object Notation.",
207 |       "tags": ["json"],
208 |       "aliases": []
209 |     },
210 | 
211 |     {
212 |       "id": "FT-0221",
213 |       "path": "data/preprocessing/scaling",
214 |       "name": "Scaling",
215 |       "level": 3,
216 |       "ancestors": ["data", "preprocessing"],
217 |       "description": "Feature scaling.",
218 |       "tags": ["scaling"],
219 |       "aliases": []
220 |     },
221 |     {
222 |       "id": "FT-0222",
223 |       "path": "data/preprocessing/imputation",
224 |       "name": "Imputation",
225 |       "level": 3,
226 |       "ancestors": ["data", "preprocessing"],
227 |       "description": "Missing value handling.",
228 |       "tags": ["impute"],
229 |       "aliases": []
230 |     },
231 |     {
232 |       "id": "FT-0223",
233 |       "path": "data/preprocessing/encoding",
234 |       "name": "Encoding",
235 |       "level": 3,
236 |       "ancestors": ["data", "preprocessing"],
237 |       "description": "Categorical encoders.",
238 |       "tags": ["encoding"],
239 |       "aliases": []
240 |     },
241 | 
242 |     {
243 |       "id": "FT-0311",
244 |       "path": "evaluation/metrics/classification",
245 |       "name": "Classification Metrics",
246 |       "level": 3,
247 |       "ancestors": ["evaluation", "metrics"],
248 |       "description": "Metrics for classifiers.",
249 |       "tags": ["metrics", "classification"],
250 |       "aliases": []
251 |     },
252 |     {
253 |       "id": "FT-0312",
254 |       "path": "evaluation/metrics/regression",
255 |       "name": "Regression Metrics",
256 |       "level": 3,
257 |       "ancestors": ["evaluation", "metrics"],
258 |       "description": "Metrics for regressors.",
259 |       "tags": ["metrics", "regression"],
260 |       "aliases": []
261 |     },
262 |     {
263 |       "id": "FT-0313",
264 |       "path": "evaluation/metrics/clustering",
265 |       "name": "Clustering Metrics",
266 |       "level": 3,
267 |       "ancestors": ["evaluation", "metrics"],
268 |       "description": "Metrics for clustering.",
269 |       "tags": ["metrics", "clustering"],
270 |       "aliases": []
271 |     },
272 | 
273 |     {
274 |       "id": "FT-0321",
275 |       "path": "evaluation/validation/cross_validation",
276 |       "name": "Cross-Validation",
277 |       "level": 3,
278 |       "ancestors": ["evaluation", "validation"],
279 |       "description": "K-fold, etc.",
280 |       "tags": ["cv"],
281 |       "aliases": []
282 |     },
283 |     {
284 |       "id": "FT-0322",
285 |       "path": "evaluation/validation/train_test_split",
286 |       "name": "Train/Test Split",
287 |       "level": 3,
288 |       "ancestors": ["evaluation", "validation"],
289 |       "description": "Holdout split.",
290 |       "tags": ["split"],
291 |       "aliases": []
292 |     },
293 | 
294 |     {
295 |       "id": "FT-0411",
296 |       "path": "io/persistence/save_model",
297 |       "name": "Save Model",
298 |       "level": 3,
299 |       "ancestors": ["io", "persistence"],
300 |       "description": "Persist models.",
301 |       "tags": ["save"],
302 |       "aliases": []
303 |     },
304 |     {
305 |       "id": "FT-0412",
306 |       "path": "io/persistence/load_model",
307 |       "name": "Load Model",
308 |       "level": 3,
309 |       "ancestors": ["io", "persistence"],
310 |       "description": "Restore models.",
311 |       "tags": ["load"],
312 |       "aliases": []
313 |     },
314 |     {
315 |       "id": "FT-0421",
316 |       "path": "io/serialization/to_json",
317 |       "name": "To JSON",
318 |       "level": 3,
319 |       "ancestors": ["io", "serialization"],
320 |       "description": "Serialize to JSON.",
321 |       "tags": ["json"],
322 |       "aliases": []
323 |     },
324 |     {
325 |       "id": "FT-0422",
326 |       "path": "io/serialization/to_pickle",
327 |       "name": "To Pickle",
328 |       "level": 3,
329 |       "ancestors": ["io", "serialization"],
330 |       "description": "Serialize to pickle.",
331 |       "tags": ["pickle"],
332 |       "aliases": []
333 |     },
334 | 
335 |     {
336 |       "id": "FT-1001",
337 |       "path": "ml/algorithms/regression/linear_regression",
338 |       "name": "Linear Regression",
339 |       "level": 4,
340 |       "ancestors": ["ml", "algorithms", "regression"],
341 |       "description": "Ordinary least squares.",
342 |       "tags": ["ols", "regression"],
343 |       "aliases": ["OLS"]
344 |     },
345 |     {
346 |       "id": "FT-1002",
347 |       "path": "ml/algorithms/regression/ridge",
348 |       "name": "Ridge Regression",
349 |       "level": 4,
350 |       "ancestors": ["ml", "algorithms", "regression"],
351 |       "description": "L2-regularized regression.",
352 |       "tags": ["ridge", "l2"],
353 |       "aliases": []
354 |     },
355 |     {
356 |       "id": "FT-1003",
357 |       "path": "ml/algorithms/regression/lasso",
358 |       "name": "Lasso Regression",
359 |       "level": 4,
360 |       "ancestors": ["ml", "algorithms", "regression"],
361 |       "description": "L1-regularized regression.",
362 |       "tags": ["lasso", "l1"],
363 |       "aliases": []
364 |     },
365 | 
366 |     {
367 |       "id": "FT-1101",
368 |       "path": "ml/algorithms/classification/logistic_regression",
369 |       "name": "Logistic Regression",
370 |       "level": 4,
371 |       "ancestors": ["ml", "algorithms", "classification"],
372 |       "description": "Binary/multiclass logistic model.",
373 |       "tags": ["logistic", "classification"],
374 |       "aliases": []
375 |     },
376 |     {
377 |       "id": "FT-1102",
378 |       "path": "ml/algorithms/classification/svm_classifier",
379 |       "name": "SVM Classifier",
380 |       "level": 4,
381 |       "ancestors": ["ml", "algorithms", "classification"],
382 |       "description": "Support Vector Machine (C-SVC).",
383 |       "tags": ["svm", "classification"],
384 |       "aliases": ["SVC"]
385 |     },
386 |     {
387 |       "id": "FT-1103",
388 |       "path": "ml/algorithms/classification/decision_tree_classifier",
389 |       "name": "Decision Tree Classifier",
390 |       "level": 4,
391 |       "ancestors": ["ml", "algorithms", "classification"],
392 |       "description": "CART decision tree for classification.",
393 |       "tags": ["tree", "classification"],
394 |       "aliases": []
395 |     },
396 | 
397 |     {
398 |       "id": "FT-1201",
399 |       "path": "ml/algorithms/clustering/kmeans",
400 |       "name": "K-Means",
401 |       "level": 4,
402 |       "ancestors": ["ml", "algorithms", "clustering"],
403 |       "description": "Partition into k clusters via Lloyd's algorithm.",
404 |       "tags": ["kmeans", "clustering"],
405 |       "aliases": []
406 |     },
407 |     {
408 |       "id": "FT-1202",
409 |       "path": "ml/algorithms/clustering/kmedoids",
410 |       "name": "K-Medoids",
411 |       "level": 4,
412 |       "ancestors": ["ml", "algorithms", "clustering"],
413 |       "description": "Partitioning Around Medoids.",
414 |       "tags": ["kmedoids", "clustering"],
415 |       "aliases": []
416 |     },
417 |     {
418 |       "id": "FT-1203",
419 |       "path": "ml/algorithms/clustering/dbscan",
420 |       "name": "DBSCAN",
421 |       "level": 4,
422 |       "ancestors": ["ml", "algorithms", "clustering"],
423 |       "description": "Density-based clustering.",
424 |       "tags": ["dbscan", "clustering"],
425 |       "aliases": []
426 |     },
427 | 
428 |     {
429 |       "id": "FT-2001",
430 |       "path": "data/loading/csv/read_csv",
431 |       "name": "Read CSV",
432 |       "level": 4,
433 |       "ancestors": ["data", "loading", "csv"],
434 |       "description": "Read tabular data from CSV.",
435 |       "tags": ["csv", "io"],
436 |       "aliases": []
437 |     },
438 |     {
439 |       "id": "FT-2002",
440 |       "path": "data/loading/json/read_json",
441 |       "name": "Read JSON",
442 |       "level": 4,
443 |       "ancestors": ["data", "loading", "json"],
444 |       "description": "Read data from JSON.",
445 |       "tags": ["json", "io"],
446 |       "aliases": []
447 |     },
448 | 
449 |     {
450 |       "id": "FT-2101",
451 |       "path": "data/preprocessing/scaling/standard_scaler",
452 |       "name": "Standard Scaler",
453 |       "level": 4,
454 |       "ancestors": ["data", "preprocessing", "scaling"],
455 |       "description": "Z-score standardization.",
456 |       "tags": ["scaling", "standardize"],
457 |       "aliases": []
458 |     },
459 |     {
460 |       "id": "FT-2102",
461 |       "path": "data/preprocessing/scaling/minmax_scaler",
462 |       "name": "MinMax Scaler",
463 |       "level": 4,
464 |       "ancestors": ["data", "preprocessing", "scaling"],
465 |       "description": "Scale features to [0,1].",
466 |       "tags": ["scaling", "minmax"],
467 |       "aliases": []
468 |     },
469 |     {
470 |       "id": "FT-2201",
471 |       "path": "data/preprocessing/imputation/mean_imputer",
472 |       "name": "Mean Imputer",
473 |       "level": 4,
474 |       "ancestors": ["data", "preprocessing", "imputation"],
475 |       "description": "Replace NaNs with column means.",
476 |       "tags": ["impute", "mean"],
477 |       "aliases": []
478 |     },
479 |     {
480 |       "id": "FT-2202",
481 |       "path": "data/preprocessing/imputation/median_imputer",
482 |       "name": "Median Imputer",
483 |       "level": 4,
484 |       "ancestors": ["data", "preprocessing", "imputation"],
485 |       "description": "Replace NaNs with medians.",
486 |       "tags": ["impute", "median"],
487 |       "aliases": []
488 |     },
489 |     {
490 |       "id": "FT-2301",
491 |       "path": "data/preprocessing/encoding/one_hot_encoder",
492 |       "name": "One-Hot Encoder",
493 |       "level": 4,
494 |       "ancestors": ["data", "preprocessing", "encoding"],
495 |       "description": "One-hot encode categoricals.",
496 |       "tags": ["encoding", "onehot"],
497 |       "aliases": []
498 |     },
499 |     {
500 |       "id": "FT-2302",
501 |       "path": "data/preprocessing/encoding/label_encoder",
502 |       "name": "Label Encoder",
503 |       "level": 4,
504 |       "ancestors": ["data", "preprocessing", "encoding"],
505 |       "description": "Ordinal label encoding.",
506 |       "tags": ["encoding", "label"],
507 |       "aliases": []
508 |     },
509 | 
510 |     {
511 |       "id": "FT-3001",
512 |       "path": "evaluation/metrics/classification/accuracy_score",
513 |       "name": "Accuracy Score",
514 |       "level": 4,
515 |       "ancestors": ["evaluation", "metrics", "classification"],
516 |       "description": "Fraction of correct predictions.",
517 |       "tags": ["accuracy", "classification"],
518 |       "aliases": []
519 |     },
520 |     {
521 |       "id": "FT-3002",
522 |       "path": "evaluation/metrics/classification/f1_score",
523 |       "name": "F1 Score",
524 |       "level": 4,
525 |       "ancestors": ["evaluation", "metrics", "classification"],
526 |       "description": "Harmonic mean of precision and recall.",
527 |       "tags": ["f1", "classification"],
528 |       "aliases": []
529 |     },
530 |     {
531 |       "id": "FT-3003",
532 |       "path": "evaluation/metrics/classification/roc_auc_score",
533 |       "name": "ROC AUC",
534 |       "level": 4,
535 |       "ancestors": ["evaluation", "metrics", "classification"],
536 |       "description": "Area under ROC curve.",
537 |       "tags": ["roc", "auc"],
538 |       "aliases": []
539 |     },
540 |     {
541 |       "id": "FT-3101",
542 |       "path": "evaluation/metrics/regression/mean_squared_error",
543 |       "name": "Mean Squared Error",
544 |       "level": 4,
545 |       "ancestors": ["evaluation", "metrics", "regression"],
546 |       "description": "Average squared residuals.",
547 |       "tags": ["mse", "regression"],
548 |       "aliases": []
549 |     },
550 |     {
551 |       "id": "FT-3102",
552 |       "path": "evaluation/metrics/regression/r2_score",
553 |       "name": "R2 Score",
554 |       "level": 4,
555 |       "ancestors": ["evaluation", "metrics", "regression"],
556 |       "description": "Coefficient of determination.",
557 |       "tags": ["r2", "regression"],
558 |       "aliases": []
559 |     },
560 |     {
561 |       "id": "FT-3201",
562 |       "path": "evaluation/metrics/clustering/silhouette_score",
563 |       "name": "Silhouette Score",
564 |       "level": 4,
565 |       "ancestors": ["evaluation", "metrics", "clustering"],
566 |       "description": "Mean silhouette coefficient.",
567 |       "tags": ["silhouette", "clustering"],
568 |       "aliases": []
569 |     },
570 | 
571 |     {
572 |       "id": "FT-3301",
573 |       "path": "evaluation/validation/cross_validation/k_fold",
574 |       "name": "K-Fold Split",
575 |       "level": 4,
576 |       "ancestors": ["evaluation", "validation", "cross_validation"],
577 |       "description": "K-fold cross validation.",
578 |       "tags": ["cv", "kfold"],
579 |       "aliases": []
580 |     },
581 |     {
582 |       "id": "FT-3302",
583 |       "path": "evaluation/validation/train_test_split/train_test_split",
584 |       "name": "Train/Test Split",
585 |       "level": 4,
586 |       "ancestors": ["evaluation", "validation", "train_test_split"],
587 |       "description": "Holdout set split.",
588 |       "tags": ["split", "holdout"],
589 |       "aliases": []
590 |     },
591 | 
592 |     {
593 |       "id": "FT-4001",
594 |       "path": "io/persistence/save_model/save_model_joblib",
595 |       "name": "Save Model (joblib)",
596 |       "level": 4,
597 |       "ancestors": ["io", "persistence", "save_model"],
598 |       "description": "Persist model via joblib.",
599 |       "tags": ["save", "joblib"],
600 |       "aliases": []
601 |     },
602 |     {
603 |       "id": "FT-4002",
604 |       "path": "io/persistence/load_model/load_model_joblib",
605 |       "name": "Load Model (joblib)",
606 |       "level": 4,
607 |       "ancestors": ["io", "persistence", "load_model"],
608 |       "description": "Load model via joblib.",
609 |       "tags": ["load", "joblib"],
610 |       "aliases": []
611 |     },
612 |     {
613 |       "id": "FT-4101",
614 |       "path": "io/serialization/to_json/model_to_json",
615 |       "name": "Model → JSON",
616 |       "level": 4,
617 |       "ancestors": ["io", "serialization", "to_json"],
618 |       "description": "Serialize model to JSON.",
619 |       "tags": ["json", "serialize"],
620 |       "aliases": []
621 |     },
622 |     {
623 |       "id": "FT-4102",
624 |       "path": "io/serialization/to_pickle/model_to_pickle",
625 |       "name": "Model → Pickle",
626 |       "level": 4,
627 |       "ancestors": ["io", "serialization", "to_pickle"],
628 |       "description": "Serialize model to pickle.",
629 |       "tags": ["pickle", "serialize"],
630 |       "aliases": []
631 |     }
632 |   ],
633 | 
634 |   "hierarchy_edges": [
635 |     { "parent": "FT-0001", "child": "FT-0101" },
636 |     { "parent": "FT-0001", "child": "FT-0102" },
637 |     { "parent": "FT-0002", "child": "FT-0201" },
638 |     { "parent": "FT-0002", "child": "FT-0202" },
639 |     { "parent": "FT-0003", "child": "FT-0301" },
640 |     { "parent": "FT-0003", "child": "FT-0302" },
641 |     { "parent": "FT-0004", "child": "FT-0401" },
642 |     { "parent": "FT-0004", "child": "FT-0402" },
643 | 
644 |     { "parent": "FT-0101", "child": "FT-0111" },
645 |     { "parent": "FT-0101", "child": "FT-0112" },
646 |     { "parent": "FT-0101", "child": "FT-0113" },
647 |     { "parent": "FT-0201", "child": "FT-0211" },
648 |     { "parent": "FT-0201", "child": "FT-0212" },
649 |     { "parent": "FT-0202", "child": "FT-0221" },
650 |     { "parent": "FT-0202", "child": "FT-0222" },
651 |     { "parent": "FT-0202", "child": "FT-0223" },
652 |     { "parent": "FT-0301", "child": "FT-0311" },
653 |     { "parent": "FT-0301", "child": "FT-0312" },
654 |     { "parent": "FT-0301", "child": "FT-0313" },
655 |     { "parent": "FT-0302", "child": "FT-0321" },
656 |     { "parent": "FT-0302", "child": "FT-0322" },
657 |     { "parent": "FT-0401", "child": "FT-0411" },
658 |     { "parent": "FT-0401", "child": "FT-0412" },
659 |     { "parent": "FT-0402", "child": "FT-0421" },
660 |     { "parent": "FT-0402", "child": "FT-0422" },
661 | 
662 |     { "parent": "FT-0111", "child": "FT-1001" },
663 |     { "parent": "FT-0111", "child": "FT-1002" },
664 |     { "parent": "FT-0111", "child": "FT-1003" },
665 |     { "parent": "FT-0112", "child": "FT-1101" },
666 |     { "parent": "FT-0112", "child": "FT-1102" },
667 |     { "parent": "FT-0112", "child": "FT-1103" },
668 |     { "parent": "FT-0113", "child": "FT-1201" },
669 |     { "parent": "FT-0113", "child": "FT-1202" },
670 |     { "parent": "FT-0113", "child": "FT-1203" },
671 | 
672 |     { "parent": "FT-0211", "child": "FT-2001" },
673 |     { "parent": "FT-0212", "child": "FT-2002" },
674 | 
675 |     { "parent": "FT-0221", "child": "FT-2101" },
676 |     { "parent": "FT-0221", "child": "FT-2102" },
677 |     { "parent": "FT-0222", "child": "FT-2201" },
678 |     { "parent": "FT-0222", "child": "FT-2202" },
679 |     { "parent": "FT-0223", "child": "FT-2301" },
680 |     { "parent": "FT-0223", "child": "FT-2302" },
681 | 
682 |     { "parent": "FT-0311", "child": "FT-3001" },
683 |     { "parent": "FT-0311", "child": "FT-3002" },
684 |     { "parent": "FT-0311", "child": "FT-3003" },
685 |     { "parent": "FT-0312", "child": "FT-3101" },
686 |     { "parent": "FT-0312", "child": "FT-3102" },
687 |     { "parent": "FT-0313", "child": "FT-3201" },
688 | 
689 |     { "parent": "FT-0321", "child": "FT-3301" },
690 |     { "parent": "FT-0322", "child": "FT-3302" },
691 | 
692 |     { "parent": "FT-0411", "child": "FT-4001" },
693 |     { "parent": "FT-0412", "child": "FT-4002" },
694 |     { "parent": "FT-0421", "child": "FT-4101" },
695 |     { "parent": "FT-0422", "child": "FT-4102" }
696 |   ],
697 | 
698 |   "retrieval": {
699 |     "embedding_method": "feature_hashing_bigrams",
700 |     "dims": 8,
701 |     "vectors": {
702 |       "FT-1001": [0.9, 0.1, 0.0, 0.2, 0.3, 0.0, 0.1, 0.0],
703 |       "FT-1002": [0.9, 0.1, 0.0, 0.2, 0.35, 0.05, 0.1, 0.0],
704 |       "FT-1003": [0.92, 0.08, 0.02, 0.18, 0.28, 0.02, 0.12, 0.0],
705 | 
706 |       "FT-1101": [0.8, 0.2, 0.1, 0.1, 0.4, 0.0, 0.1, 0.1],
707 |       "FT-1102": [0.82, 0.18, 0.1, 0.12, 0.38, 0.02, 0.08, 0.1],
708 |       "FT-1103": [0.78, 0.22, 0.1, 0.1, 0.42, 0.0, 0.12, 0.08],
709 | 
710 |       "FT-1201": [0.7, 0.0, 0.3, 0.1, 0.2, 0.2, 0.0, 0.1],
711 |       "FT-1202": [0.7, 0.02, 0.28, 0.1, 0.22, 0.22, 0.0, 0.1],
712 |       "FT-1203": [0.68, 0.0, 0.32, 0.12, 0.18, 0.18, 0.02, 0.1],
713 | 
714 |       "FT-2001": [0.1, 0.9, 0.0, 0.0, 0.2, 0.1, 0.1, 0.0],
715 |       "FT-2002": [0.12, 0.88, 0.0, 0.02, 0.18, 0.12, 0.08, 0.0],
716 | 
717 |       "FT-2101": [0.1, 0.8, 0.1, 0.0, 0.3, 0.1, 0.0, 0.0],
718 |       "FT-2102": [0.12, 0.78, 0.12, 0.0, 0.28, 0.12, 0.0, 0.0],
719 |       "FT-2201": [0.1, 0.7, 0.2, 0.1, 0.2, 0.1, 0.0, 0.0],
720 |       "FT-2202": [0.12, 0.68, 0.22, 0.08, 0.22, 0.1, 0.0, 0.0],
721 |       "FT-2301": [0.1, 0.6, 0.1, 0.2, 0.1, 0.1, 0.1, 0.0],
722 |       "FT-2302": [0.12, 0.58, 0.12, 0.22, 0.12, 0.08, 0.1, 0.0],
723 | 
724 |       "FT-3001": [0.2, 0.1, 0.8, 0.1, 0.2, 0.1, 0.0, 0.1],
725 |       "FT-3002": [0.2, 0.1, 0.82, 0.08, 0.22, 0.1, 0.0, 0.1],
726 |       "FT-3003": [0.22, 0.08, 0.78, 0.12, 0.18, 0.12, 0.0, 0.1],
727 |       "FT-3101": [0.2, 0.1, 0.7, 0.2, 0.1, 0.1, 0.0, 0.1],
728 |       "FT-3102": [0.22, 0.08, 0.68, 0.22, 0.12, 0.1, 0.0, 0.1],
729 |       "FT-3201": [0.2, 0.1, 0.6, 0.3, 0.1, 0.1, 0.0, 0.1],
730 | 
731 |       "FT-3301": [0.2, 0.2, 0.6, 0.1, 0.1, 0.1, 0.1, 0.0],
732 |       "FT-3302": [0.22, 0.18, 0.58, 0.12, 0.12, 0.1, 0.1, 0.0],
733 | 
734 |       "FT-4001": [0.0, 0.1, 0.1, 0.9, 0.0, 0.0, 0.2, 0.1],
735 |       "FT-4002": [0.0, 0.12, 0.12, 0.88, 0.02, 0.0, 0.2, 0.1],
736 |       "FT-4101": [0.0, 0.1, 0.1, 0.8, 0.1, 0.0, 0.1, 0.2],
737 |       "FT-4102": [0.02, 0.08, 0.12, 0.78, 0.12, 0.02, 0.1, 0.2]
738 |     },
739 |     "inverted_index": {
740 |       "linear": ["FT-1001"],
741 |       "ridge": ["FT-1002"],
742 |       "lasso": ["FT-1003"],
743 |       "logistic": ["FT-1101"],
744 |       "svm": ["FT-1102"],
745 |       "tree": ["FT-1103"],
746 |       "kmeans": ["FT-1201"],
747 |       "kmedoids": ["FT-1202"],
748 |       "dbscan": ["FT-1203"],
749 |       "read_csv": ["FT-2001"],
750 |       "read_json": ["FT-2002"],
751 |       "standard_scaler": ["FT-2101"],
752 |       "minmax_scaler": ["FT-2102"],
753 |       "mean_imputer": ["FT-2201"],
754 |       "median_imputer": ["FT-2202"],
755 |       "one_hot": ["FT-2301"],
756 |       "label_encoder": ["FT-2302"],
757 |       "accuracy": ["FT-3001"],
758 |       "f1": ["FT-3002"],
759 |       "roc_auc": ["FT-3003"],
760 |       "mse": ["FT-3101"],
761 |       "r2": ["FT-3102"],
762 |       "silhouette": ["FT-3201"],
763 |       "k_fold": ["FT-3301"],
764 |       "train_test_split": ["FT-3302"],
765 |       "save_model": ["FT-4001"],
766 |       "load_model": ["FT-4002"],
767 |       "to_json": ["FT-4101"],
768 |       "to_pickle": ["FT-4102"]
769 |     }
770 |   }
771 | }
```

docs/propCandidates.v1.json
```
1 | {
2 |   "metadata": {
3 |     "artifact": "RPG PROP-001/PROP-002 Candidate Functionality Set",
4 |     "version": "1.0.0",
5 |     "generated_at": "2025-10-01T00:00:00Z",
6 |     "source_tree": "Feature Tree Seed v0.1.0",
7 |     "rpg_alignment": {
8 |       "build_guide_ids": ["PROP-001", "PROP-002", "PROP-003"],
9 |       "whitepaper_sections": ["§3.2", "Alg. 2"],
10 |       "notes": "Exploit: token+path semantic; Explore: branch/level stratified with overlap threshold 0.5; Filter/Merge: simple dedupe + rationale."
11 |     }
12 |   },
13 |   "retrieval_request": {
14 |     "query_summary": "Build a classification pipeline on CSV data with scaling and one-hot encoding, train Logistic Regression, evaluate with Accuracy and F1 (optionally ROC AUC), split data via train/test (optionally K-fold), and save the model.",
15 |     "query_tokens": [
16 |       "read_csv",
17 |       "standard_scaler",
18 |       "logistic",
19 |       "accuracy",
20 |       "f1",
21 |       "train_test_split",
22 |       "save_model"
23 |     ],
24 |     "filters": {
25 |       "levels": [4],
26 |       "branches": ["data", "ml", "evaluation", "io"]
27 |     },
28 |     "k": 8,
29 |     "overlap_threshold": 0.5
30 |   },
31 |   "exploit_hits": [
32 |     {
33 |       "rank": 1,
34 |       "id": "FT-1101",
35 |       "path": "ml/algorithms/classification/logistic_regression",
36 |       "score": 0.95,
37 |       "reason": "exact token match (logistic) + classification path proximity"
38 |     },
39 |     {
40 |       "rank": 2,
41 |       "id": "FT-2001",
42 |       "path": "data/loading/csv/read_csv",
43 |       "score": 0.92,
44 |       "reason": "exact token match (read_csv)"
45 |     },
46 |     {
47 |       "rank": 3,
48 |       "id": "FT-2101",
49 |       "path": "data/preprocessing/scaling/standard_scaler",
50 |       "score": 0.9,
51 |       "reason": "exact token match (standard_scaler)"
52 |     },
53 |     {
54 |       "rank": 4,
55 |       "id": "FT-3302",
56 |       "path": "evaluation/validation/train_test_split/train_test_split",
57 |       "score": 0.88,
58 |       "reason": "exact token match (train_test_split)"
59 |     },
60 |     {
61 |       "rank": 5,
62 |       "id": "FT-3002",
63 |       "path": "evaluation/metrics/classification/f1_score",
64 |       "score": 0.87,
65 |       "reason": "exact token match (f1) + classification metrics proximity"
66 |     },
67 |     {
68 |       "rank": 6,
69 |       "id": "FT-3001",
70 |       "path": "evaluation/metrics/classification/accuracy_score",
71 |       "score": 0.86,
72 |       "reason": "exact token match (accuracy) + classification metrics proximity"
73 |     },
74 |     {
75 |       "rank": 7,
76 |       "id": "FT-4001",
77 |       "path": "io/persistence/save_model/save_model_joblib",
78 |       "score": 0.84,
79 |       "reason": "exact token match (save_model)"
80 |     },
81 |     {
82 |       "rank": 8,
83 |       "id": "FT-2301",
84 |       "path": "data/preprocessing/encoding/one_hot_encoder",
85 |       "score": 0.83,
86 |       "reason": "derived from spec need for categoricals (one-hot)"
87 |     }
88 |   ],
89 |   "explore_candidates": [
90 |     {
91 |       "id": "FT-1102",
92 |       "path": "ml/algorithms/classification/svm_classifier",
93 |       "score": 0.72,
94 |       "reason": "alternative classifier for robustness; different margin properties"
95 |     },
96 |     {
97 |       "id": "FT-1103",
98 |       "path": "ml/algorithms/classification/decision_tree_classifier",
99 |       "score": 0.7,
100 |       "reason": "alternative with different bias/variance profile"
101 |     },
102 |     {
103 |       "id": "FT-3301",
104 |       "path": "evaluation/validation/cross_validation/k_fold",
105 |       "score": 0.69,
106 |       "reason": "more stable validation than single holdout"
107 |     },
108 |     {
109 |       "id": "FT-3003",
110 |       "path": "evaluation/metrics/classification/roc_auc_score",
111 |       "score": 0.68,
112 |       "reason": "metric robust to class imbalance"
113 |     },
114 |     {
115 |       "id": "FT-2102",
116 |       "path": "data/preprocessing/scaling/minmax_scaler",
117 |       "score": 0.65,
118 |       "reason": "alternative scaling depending on model sensitivity"
119 |     },
120 |     {
121 |       "id": "FT-2201",
122 |       "path": "data/preprocessing/imputation/mean_imputer",
123 |       "score": 0.64,
124 |       "reason": "handle missing numeric values"
125 |     },
126 |     {
127 |       "id": "FT-2202",
128 |       "path": "data/preprocessing/imputation/median_imputer",
129 |       "score": 0.63,
130 |       "reason": "robust imputation for skewed data"
131 |     },
132 |     {
133 |       "id": "FT-4101",
134 |       "path": "io/serialization/to_json/model_to_json",
135 |       "score": 0.6,
136 |       "reason": "alternate serialization format"
137 |     }
138 |   ],
139 |   "filter_merge": {
140 |     "kept": [
141 |       {
142 |         "id": "FT-1101",
143 |         "path": "ml/algorithms/classification/logistic_regression",
144 |         "source": "exploit"
145 |       },
146 |       {
147 |         "id": "FT-2001",
148 |         "path": "data/loading/csv/read_csv",
149 |         "source": "exploit"
150 |       },
151 |       {
152 |         "id": "FT-2301",
153 |         "path": "data/preprocessing/encoding/one_hot_encoder",
154 |         "source": "exploit"
155 |       },
156 |       {
157 |         "id": "FT-2201",
158 |         "path": "data/preprocessing/imputation/mean_imputer",
159 |         "source": "explore"
160 |       },
161 |       {
162 |         "id": "FT-2101",
163 |         "path": "data/preprocessing/scaling/standard_scaler",
164 |         "source": "exploit"
165 |       },
166 |       {
167 |         "id": "FT-3302",
168 |         "path": "evaluation/validation/train_test_split/train_test_split",
169 |         "source": "exploit"
170 |       },
171 |       {
172 |         "id": "FT-3301",
173 |         "path": "evaluation/validation/cross_validation/k_fold",
174 |         "source": "explore"
175 |       },
176 |       {
177 |         "id": "FT-3001",
178 |         "path": "evaluation/metrics/classification/accuracy_score",
179 |         "source": "exploit"
180 |       },
181 |       {
182 |         "id": "FT-3002",
183 |         "path": "evaluation/metrics/classification/f1_score",
184 |         "source": "exploit"
185 |       },
186 |       {
187 |         "id": "FT-3003",
188 |         "path": "evaluation/metrics/classification/roc_auc_score",
189 |         "source": "explore"
190 |       },
191 |       {
192 |         "id": "FT-4001",
193 |         "path": "io/persistence/save_model/save_model_joblib",
194 |         "source": "exploit"
195 |       },
196 |       {
197 |         "id": "FT-1102",
198 |         "path": "ml/algorithms/classification/svm_classifier",
199 |         "source": "explore"
200 |       },
201 |       {
202 |         "id": "FT-1103",
203 |         "path": "ml/algorithms/classification/decision_tree_classifier",
204 |         "source": "explore"
205 |       }
206 |     ],
207 |     "dropped": [
208 |       {
209 |         "id": "FT-2102",
210 |         "path": "data/preprocessing/scaling/minmax_scaler",
211 |         "reason": "redundant with standard scaler for baseline"
212 |       },
213 |       {
214 |         "id": "FT-2202",
215 |         "path": "data/preprocessing/imputation/median_imputer",
216 |         "reason": "choose one default imputer to reduce overlap"
217 |       },
218 |       {
219 |         "id": "FT-4101",
220 |         "path": "io/serialization/to_json/model_to_json",
221 |         "reason": "persistence already covered by save_model"
222 |       }
223 |     ]
224 |   },
225 |   "final_candidate_set": [
226 |     {
227 |       "order": 1,
228 |       "id": "FT-2001",
229 |       "path": "data/loading/csv/read_csv",
230 |       "role": "ingest"
231 |     },
232 |     {
233 |       "order": 2,
234 |       "id": "FT-2301",
235 |       "path": "data/preprocessing/encoding/one_hot_encoder",
236 |       "role": "preprocess"
237 |     },
238 |     {
239 |       "order": 3,
240 |       "id": "FT-2201",
241 |       "path": "data/preprocessing/imputation/mean_imputer",
242 |       "role": "preprocess"
243 |     },
244 |     {
245 |       "order": 4,
246 |       "id": "FT-2101",
247 |       "path": "data/preprocessing/scaling/standard_scaler",
248 |       "role": "preprocess"
249 |     },
250 |     {
251 |       "order": 5,
252 |       "id": "FT-1101",
253 |       "path": "ml/algorithms/classification/logistic_regression",
254 |       "role": "fit"
255 |     },
256 |     {
257 |       "order": 6,
258 |       "id": "FT-3302",
259 |       "path": "evaluation/validation/train_test_split/train_test_split",
260 |       "role": "validate"
261 |     },
262 |     {
263 |       "order": 7,
264 |       "id": "FT-3001",
265 |       "path": "evaluation/metrics/classification/accuracy_score",
266 |       "role": "metric"
267 |     },
268 |     {
269 |       "order": 8,
270 |       "id": "FT-3002",
271 |       "path": "evaluation/metrics/classification/f1_score",
272 |       "role": "metric"
273 |     },
274 |     {
275 |       "order": 9,
276 |       "id": "FT-3003",
277 |       "path": "evaluation/metrics/classification/roc_auc_score",
278 |       "role": "metric-optional"
279 |     },
280 |     {
281 |       "order": 10,
282 |       "id": "FT-4001",
283 |       "path": "io/persistence/save_model/save_model_joblib",
284 |       "role": "persist"
285 |     },
286 |     {
287 |       "order": 11,
288 |       "id": "FT-1102",
289 |       "path": "ml/algorithms/classification/svm_classifier",
290 |       "role": "alternative"
291 |     },
292 |     {
293 |       "order": 12,
294 |       "id": "FT-1103",
295 |       "path": "ml/algorithms/classification/decision_tree_classifier",
296 |       "role": "alternative"
297 |     },
298 |     {
299 |       "order": 13,
300 |       "id": "FT-3301",
301 |       "path": "evaluation/validation/cross_validation/k_fold",
302 |       "role": "validate-optional"
303 |     }
304 |   ]
305 | }
```

templates/RPG-prompt-tool_templates.md
```
1 | copy-pasteable **prompt templates** distilled from your RPG materials, grouped by stage and preserved in their original “think/action/solution” styles. I standardized placeholders (ALL\_CAPS) and kept the exact response formats so you can drop them straight into your system.
2 | 
3 | * * *
4 | 
5 | ## Proposal-Level (Feature Retrieval & Refactor)
6 | =============================================
7 | 
8 | ## 1) Exploitation Paths — Select from High-Relevance Candidates
9 | 
10 | Use when you have a curated “Exploit Feature Tree” and want precise additions only from it. RPG_REPOSITORY_PLANNING_GRAPH
11 | 
12 | ```md
13 |     SYSTEM
14 |     You are a GitHub project assistant responsible for expanding a repository’s feature tree through path-based modifications.
15 | 
16 |     You will be given:
17 |     - An Exploit Feature Tree (high-relevance candidate paths) → EXPLOIT_FEATURE_TREE
18 |     - The Current Repository Feature Tree → CURRENT_REPO_TREE
19 | 
20 |     Objective
21 |     1) Align with the repository’s purpose/scope.
22 |     2) Achieve broad coverage across core areas.
23 |     3) Ensure essential capabilities are represented.
24 |     4) Identify and fill critical gaps.
25 | 
26 |     Selection Principles
27 |     - Select exclusively from the Exploit Feature Tree.
28 |     - Include all non-duplicated, useful paths.
29 |     - Maintain structural balance by covering underrepresented modules.
30 | 
31 |     Exclusions
32 |     - Skip generic infra (e.g., logging, configuration).
33 |     - Skip abstract goals (e.g., “optimize CPU usage”).
34 | 
35 |     Response Format
36 |     Respond only with a <think> and <action> block.
37 | 
38 |     <think>
39 |     Briefly justify why each selected path improves coverage and cohesion.
40 |     </think>
41 |     <action>
42 |     {
43 |       "all_selected_feature_paths": [
44 |         "path/to/feature", ...
45 |       ]
46 |     }
47 |     </action>
48 | ```
49 | 
50 | ## 2) Exploration Paths — Expand Into New, Unvisited Areas
51 | 
52 | Use when you have a sampled “Exploration Tree” to diversify coverage. RPG_REPOSITORY_PLANNING_GRAPH
53 | 
54 | ```md
55 |     SYSTEM
56 |     You are a GitHub project assistant expanding a repository’s feature tree via path-based modifications.
57 | 
58 |     Inputs:
59 |     - A Sampled Feature Tree (Exploration Tree) → EXPLORATION_TREE
60 |     - The Current Repository Feature Tree → CURRENT_REPO_TREE
61 | 
62 |     Objective
63 |     - Improve/expand coverage aligned to real usage scenarios.
64 |     - Capture supporting areas without duplicating existing paths.
65 | 
66 |     Selection Principles
67 |     - Select only from the Exploration Tree.
68 |     - Include actionable, domain-relevant features.
69 |     - Exclude any path already present in the current tree.
70 |     - Slight over-inclusion is acceptable.
71 | 
72 |     Exclusions
73 |     - Exclude generic infra and large, unfocused integrations.
74 | 
75 |     Response Format
76 |     <think>
77 |     Explain how each Exploration Tree path was evaluated and why it was included or excluded.
78 |     </think>
79 |     <action>
80 |     {
81 |       "all_selected_feature_paths": [
82 |         "path/to/feature", ...
83 |       ]
84 |     }
85 |     </action>
86 | ```
87 | 
88 | ## 3) Propose Missing Features — Fill Gaps Beyond Current Tree
89 | 
90 | Use to enumerate concrete, implementable capabilities the repo still needs. RPG_REPOSITORY_PLANNING_GRAPH
91 | 
92 | ```md
93 |     SYSTEM
94 |     You are a GitHub project assistant designing a functionally complete, production-grade repository.
95 |     Focus on intended functionality — not the existing Feature Tree (it may be incomplete).
96 | 
97 |     Objective
98 |     Identify groups of concrete, implementable features that:
99 |     1) Align with domain and purpose,
100 |     2) Are missing or only superficially represented,
101 |     3) Are specific (functions/classes/modules/algorithms).
102 | 
103 |     Inclusion
104 |     - Code-level operations only; implementable in this repo’s scope; include standard and advanced algorithms.
105 | 
106 |     Exclusion
107 |     - No abstract intentions, generic infra, placeholders, or duplicates.
108 | 
109 |     Naming Rules
110 |     - 3–5 lowercase words, space separated (no snake/camel case).
111 |     - Leaf nodes must describe concrete behavior.
112 | 
113 |     Structure
114 |     - Organize into logical hierarchies (≤ 4–5 levels) reflecting computation/workflows.
115 | 
116 |     Response Format
117 |     <think>
118 |     Reason about domains, workflows, algorithms missing from CURRENT_REPO_TREE but expected in real use.
119 |     </think>
120 |     <action>
121 |     {
122 |       "missing_features": {
123 |         "ROOT_NODE": {
124 |           "child node 1": ["leaf feature 1", "leaf feature 2"],
125 |           "child node 2": ["leaf feature 3", "leaf feature 4"]
126 |         }
127 |       }
128 |     }
129 |     </action>
130 | ```
131 | 
132 | * * *
133 | 
134 | ## Implementation-Level (Structure, Flows, Interfaces)
135 | ===================================================
136 | 
137 | ## 4) Inter-Subtree Data-Flow (DAG) — Define Typed Edges
138 | 
139 | Use to produce a repository-level DAG of data exchanges across modules. RPG_REPOSITORY_PLANNING_GRAPH
140 | 
141 | ```md
142 |     SYSTEM
143 |     You are a system architect defining inter-subtree data flow for a Python repository as a structured DAG.
144 | 
145 |     Inputs
146 |     - Subtree names → TREES_NAMES
147 | 
148 |     Constraints
149 |     - Full connectivity: every subtree in TREES_NAMES appears in ≥ 1 edge.
150 |     - Acyclic structure (DAG).
151 |     - Field guidelines:
152 |       - data_id: unique, descriptive exchange id
153 |       - data_type: precise, interpretable type/schema
154 |       - transformation: short summary or "none"
155 | 
156 |     Output Format
157 |     <solution>
158 |     [
159 |       {
160 |         "from": "SOURCE_SUBTREE",
161 |         "to": "TARGET_SUBTREE",
162 |         "data_id": "UNIQUE_DATA_NAME",
163 |         "data_type": "TYPE_OR_SCHEMA",
164 |         "transformation": "SUMMARY_OR_none"
165 |       },
166 |       ...
167 |     ]
168 |     </solution>
169 | ```
170 | 
171 | ## 5) Raw Skeleton Mapping — Top-Level Folder Plan
172 | 
173 | Use to assign subtrees to a clean, Pythonic folder skeleton (no code). RPG_REPOSITORY_PLANNING_GRAPH
174 | 
175 | ```md
176 |     SYSTEM
177 |     You are a repository architect designing a clean, modular file system skeleton.
178 | 
179 |     Requirements
180 |     1) Separate functional subtrees clearly; reflect logical domain boundaries.
181 |     2) Pythonic names (snake_case), concise & developer-friendly.
182 |     3) Subtree names are labels; rename folders for clarity but include exact subtree mapping.
183 |     4) Flat or nested (e.g., under "src/")—choose what improves clarity/scalability.
184 |     5) Include auxiliary folders if appropriate (e.g., tests, scripts, docs).
185 |     6) Avoid unnecessary nesting/complexity.
186 | 
187 |     Output Format (single JSON-like object)
188 |     - "folder_name": ["Exact Subtree Name"] → folder assigned to subtree
189 |     - "folder_name": [] → utility/support folder
190 |     - "file_name.ext": null → file placeholder
191 | 
192 |     <solution>
193 |     {
194 |       "src": [],
195 |       "src/module_a": ["SUBTREE_A"],
196 |       "src/module_b": ["SUBTREE_B"],
197 |       "README.md": null,
198 |       "pyproject.toml": null
199 |     }
200 |     </solution>
201 | ```
202 | 
203 | ## 6) Map Feature Paths → Python Skeleton Files (Incremental)
204 | 
205 | Use iteratively to place unassigned leaf paths into `.py` files under a designated module. RPG_REPOSITORY_PLANNING_GRAPH
206 | 
207 | ```md
208 |     SYSTEM
209 |     You are assigning remaining leaf-level features into Python files.
210 | 
211 |     Inputs
212 |     - Unassigned leaf features → UNASSIGNED_FEATURE_PATHS (full "a/b/c" style)
213 |     - Designated functional folder → DESIGNATED_FOLDER
214 |     - Partial skeleton (existing assignments hidden) → PARTIAL_SKELETON
215 | 
216 |     Goals
217 |     - Paths begin with DESIGNATED_FOLDER.
218 |     - Group semantically related features.
219 |     - Reflect real modularization (avoid dumping unrelated features into single files).
220 |     - If a folder hits ≥ 10 files, add semantic subfolders.
221 | 
222 |     Naming & Organization
223 |     - Production-grade structure; logical modules; meaningful filenames.
224 | 
225 |     Response Format
226 |     <think>
227 |     Explain grouping choices and how they improve clarity/cohesion.
228 |     </think>
229 |     <solution>
230 |     {
231 |       "path/to/file1.py": ["feature/path/one", "feature/path/two"],
232 |       "path/to/file2.py": ["feature/path/three"]
233 |     }
234 |     </solution>
235 | ```
236 | 
237 | ## 7) Convert Subgraphs → Base Classes & Shared Types
238 | 
239 | Use to design minimal, justified abstractions shared across modules. RPG_REPOSITORY_PLANNING_GRAPH
240 | 
241 | ```md
242 |     SYSTEM
243 |     Design reusable abstractions and shared data structures.
244 | 
245 |     Design Strategy
246 |     - Shared data structures for nodes with high out-degree (widely consumed outputs).
247 |     - Functional base classes for nodes with high in-degree (common lifecycle/roles).
248 |     - Prefer 1–3 global classes; avoid speculative abstractions.
249 | 
250 |     Output Format
251 |     Provide grouped code blocks by subtree and file (signatures only; can be skeletons).
252 | 
253 |     <think>
254 |     Justify each abstraction (why global; how it enforces consistency; where it’s used).
255 |     </think>
256 |     <solution>
257 |     ## SubtreeName
258 |     ### path/to/file.py
259 |     ```python
260 |     from abc import ABC, abstractmethod
261 | 
262 |     class BaseComponent(ABC):
263 |         """Lifecycle: initialize → process(data) → finalize."""
264 |         def initialize(self) -> None: ...
265 |         @abstractmethod
266 |         def process(self, data): ...
267 |         def finalize(self) -> None: ...
268 | ```
269 | 
270 | </solution> \`\`\`
271 | 
272 | ### 8) Map Features → Interfaces (Functions/Classes; No Impl)
273 | 
274 | Use to author import lines, signatures, docstrings (with args/returns/assumptions) for each feature. RPG_REPOSITORY_PLANNING_GRAPH
275 | 
276 | ```md
277 |     SYSTEM
278 |     Design modular interfaces for a large-scale Python system.
279 | 
280 |     Context Provided
281 |     - Overview, tree structure, skeleton, data flow, base classes, upstream interfaces
282 |     - Target subtree → TARGET_SUBTREE
283 |     - Target file → TARGET_FILE
284 | 
285 |     Objective
286 |     - For each feature, define exactly one interface (function or class).
287 |     - Include imports, signature, and detailed docstring (purpose, args, returns, assumptions).
288 |     - No implementation: use `pass`.
289 |     - One interface per block.
290 | 
291 |     Design Guidelines
292 |     - Use functions for simple/atomic/stateless steps.
293 |     - Use classes when stateful, multi-method, inherits base class, or designed for extension.
294 |     - Prefer fewer, well-justified abstractions; group only tightly related features.
295 | 
296 |     Response Format
297 |     <think>
298 |     Explain mapping and interface choices.
299 |     </think>
300 |     <solution>
301 |     design_itfs_for_feature(features=["feature/path/one", "feature/path/two"]):
302 |     ```python
303 |     from typing import Any, Iterable
304 | 
305 |     def normalize_text(text: str) -> str:
306 |         """Normalize input text.
307 |         Args: text: raw string
308 |         Returns: normalized string
309 |         Assumptions: language-agnostic
310 |         """
311 |         pass
312 | ```
313 | 
314 | </solution> \`\`\`
315 | 
316 | * * *
317 | 
318 | ## Where these came from
319 | =====================
320 | 
321 | The templates above are lifted and normalized from the RPG paper’s prompt sections: Proposal-level (Appendix A.3) and Implementation-level (Appendix B.1), plus the data-flow format in §3.3.2. I preserved the output blocks and constraints while turning examples into placeholders. RPG_REPOSITORY_PLANNING_GRAPH See also the paper’s section outline for quick cross-reference. section-taxonomy
322 | 
323 | extracted **localization & editing tool prompts**
324 | 
325 | ## Ready-to-run command templates
326 | 
327 | ### Lifted localization/editing tools \*\*templates\*\* for system
328 | 
329 | ---
330 | 
331 | #### Copy-pasteable **templates** for the RPG **localization** and **editing** toolsets, standardized with ALL\_CAPS placeholders and strict output formats.preserved usage rules and termination semantics
332 | 
333 | - drop these straight into your system.
334 | 
335 | * * *
336 | 
337 | # **Localization Tool Templates**
338 | ===========================
339 | 
340 | ## 1) Inspect interfaces declared in a file
341 | 
342 | RPG_REPOSITORY_PLANNING_GRAPH
343 | 
344 |   ```md
345 |     SYSTEM
346 |     You are localizing implementation targets using the RPG graph.
347 | 
348 |     Tool: view_file_interface_feature_map(file_path)
349 |     Purpose: List all interfaces (functions/classes/methods) in ONE Python file and the feature tags mapped to them.
350 | 
351 |     INPUT
352 |     file_path: "SRC_RELATIVE_PATH/TO/FILE.py"
353 | 
354 |     RESPONSE
355 |     Return only a <solution> block with the tool call.
356 | 
357 |     <solution>
358 |     view_file_interface_feature_map("FILE_PATH")
359 |     </solution>
360 |   ```
361 | 
362 | ## 2) Retrieve code for a specific interface
363 | 
364 | RPG_REPOSITORY_PLANNING_GRAPH
365 | 
366 |   ```md
367 |     SYSTEM
368 |     Tool: get_interface_content(target_specs)
369 |     Purpose: Fetch full implementation bodies for specific interfaces by fully-qualified spec.
370 | 
371 |     INPUT
372 |     target_specs: ["path/to/file.py:QualifiedName", ...]
373 | 
374 |     RULES
375 |     - Each spec is either function name, class name, or ClassName.method.
376 |     - Return full bodies for all requested items.
377 | 
378 |     RESPONSE
379 |     <solution>
380 |     get_interface_content(["FILE.py:Symbol", "OTHER.py:ClassName.method"])
381 |     </solution>
382 |   ```
383 | 
384 | ## 3) Expand a feature leaf to its concrete interfaces
385 | 
386 | RPG_REPOSITORY_PLANNING_GRAPH
387 | 
388 | ```md
389 |     SYSTEM
390 |     Tool: expand_leaf_node_info(feature_path)
391 |     Purpose: From an implemented FEATURE_PATH in the RPG, list all associated repository interfaces.
392 | 
393 |     INPUT
394 |     feature_path: "ROOT/BRANCH/LEAF"
395 | 
396 |     RESPONSE
397 |     <solution>
398 |     expand_leaf_node_info("FEATURE_PATH")
399 |     </solution>
400 |   ```
401 | 
402 | ## 4) Fuzzy search by functionality
403 | 
404 | RPG_REPOSITORY_PLANNING_GRAPH
405 | 
406 | ```md
407 |     SYSTEM
408 |     Tool: search_interface_by_functionality(keywords)
409 |     Purpose: Fuzzy semantic search for interfaces given functional keywords; returns top-5.
410 | 
411 |     INPUT
412 |     keywords: ["KEYWORD_1", "KEYWORD_2", ...]
413 | 
414 |     RESPONSE
415 |     <solution>
416 |     search_interface_by_functionality(["KEYWORD_1", "KEYWORD_2"])
417 |     </solution>
418 | ```
419 | 
420 | ## 5) Terminate localization with a ranked result set
421 | 
422 | **RPG_REPOSITORY_PLANNING_GRAPH**
423 | 
424 | ```md
425 |     SYSTEM
426 |     Tool: Terminate(result)
427 |     Purpose: End localization and return a FINAL ranked list of candidates.
428 | 
429 |     REQUIRED RESULT SCHEMA
430 |     [
431 |       {"file_path":"PATH/TO/TOP1.py","interface":"method: ClassName.func"},
432 |       {"file_path":"PATH/TO/TOP2.py","interface":"function: func_name"},
433 |       {"file_path":"PATH/TO/TOP3.py","interface":"class: ClassName"}
434 |     ]
435 | 
436 |     RESPONSE
437 |     <solution>
438 |     Terminate(result=[
439 |       {"file_path":"TOP1_FILE.py","interface":"method: Class1.method1"},
440 |       {"file_path":"TOP2_FILE.py","interface":"function: function2"},
441 |       {"file_path":"TOP3_FILE.py","interface":"class: Class3"}
442 |     ])
443 |     </solution>
444 | ```
445 | 
446 | ### (Optional) Behavioral macro for search flow (CCG pattern)
447 | 
448 | Use when you want to enforce a structured search progression: **Coarse Search → Content Inspection → Global Graph Exploration → Terminate**. RPG_REPOSITORY_PLANNING_GRAPH
449 | 
450 | ```md
451 |     SYSTEM
452 |     Adopt a staged localization routine:
453 |     1) Coarse search (expand_leaf_node_info or functionality search)
454 |     2) Content inspection (view_file_interface_feature_map, then get_interface_content)
455 |     3) Graph exploration (iterate dependencies/related files per RPG links)
456 |     4) Terminate with ranked candidates
457 | 
458 |     RESPONSE
459 |     Use only the tool calls in <solution> blocks at each step; finish with Terminate(...).
460 | ```
461 | 
462 | * * *
463 | 
464 | ## Editing (Coding) Tool Templates
465 | ===============================
466 | 
467 | ## A) Edit an entire class (all methods + docstring)
468 | 
469 | **RPG_REPOSITORY_PLANNING_GRAPH**
470 | 
471 | ```md
472 |     SYSTEM
473 |     Tool: edit_whole_class_in_file(file_path, class_name)
474 |     Use when: The whole class definition must be replaced/edited.
475 | 
476 |     INPUT
477 |     file_path: "SRC_RELATIVE_PATH/TO/FILE.py"
478 |     class_name: "ClassName"
479 | 
480 |     OUTPUT REQUIREMENTS
481 |     - Return the FULL class definition (signature, ALL methods, docstring).
482 | 
483 |     RESPONSE
484 |     <solution>
485 |     edit_whole_class_in_file("FILE_PATH", "CLASS_NAME")
486 |     </solution>
487 | ```
488 | 
489 | ## B) Edit a single method inside a class
490 | 
491 | **RPG_REPOSITORY_PLANNING_GRAPH**
492 | 
493 | ```md
494 |     SYSTEM
495 |     Tool: edit_method_of_class_in_file(file_path, class_name, method_name)
496 |     Use when: Only one method in the class needs editing.
497 | 
498 |     RULES
499 |     - Return the full `class ClassName:` block containing ONLY the target method.
500 |     - Exclude unrelated methods.
501 |     - Do NOT return the method alone.
502 | 
503 |     INPUT
504 |     file_path: "SRC_RELATIVE_PATH/TO/FILE.py"
505 |     class_name: "ClassName"
506 |     method_name: "method_name"
507 | 
508 |     RESPONSE
509 |     <solution>
510 |     edit_method_of_class_in_file("FILE_PATH", "CLASS_NAME", "METHOD_NAME")
511 |     </solution>
512 |   ```
513 | 
514 | ## C) Edit a top-level function
515 | 
516 | **RPG_REPOSITORY_PLANNING_GRAPH**
517 | 
518 | ```md
519 |     SYSTEM
520 |     Tool: edit_function_in_file(file_path, function_name)
521 |     Use when: A standalone module-level function must be edited.
522 | 
523 |     INPUT
524 |     file_path: "SRC_RELATIVE_PATH/TO/FILE.py"
525 |     function_name: "function_name"
526 | 
527 |     OUTPUT REQUIREMENTS
528 |     - Full function (signature, logic, docstring).
529 | 
530 |     RESPONSE
531 |     <solution>
532 |     edit_function_in_file("FILE_PATH", "FUNCTION_NAME")
533 |     </solution>
534 | ```
535 | 
536 | ## D) Edit imports and top-level assignments only
537 | 
538 | **RPG_REPOSITORY_PLANNING_GRAPH**
539 | 
540 | ```md
541 |     SYSTEM
542 |     Tool: edit_imports_and_assignments_in_file(file_path)
543 |     Use when: Imports or module-level assignments need to be added/fixed.
544 | 
545 |     STRICT RULES
546 |     - Output ONLY imports and top-level assignments (no classes/functions).
547 |     - Import order: (1) standard library, (2) third-party, (3) local modules.
548 |     - Do NOT remove existing imports unless invalid/typo/non-existent.
549 |     - Retain “apparently unused” imports to preserve runtime deps.
550 | 
551 |     INPUT
552 |     file_path: "SRC_RELATIVE_PATH/TO/FILE.py"
553 | 
554 |     RESPONSE
555 |     <solution>
556 |     edit_imports_and_assignments_in_file("FILE_PATH")
557 |     </solution>
558 | ```
559 | 
560 | ## E) Terminate editing session
561 | 
562 | **RPG_REPOSITORY_PLANNING_GRAPH**
563 | 
564 | ```md
565 |     SYSTEM
566 |     Tool: Terminate()
567 |     Use when: All required edits are complete. Do not call prematurely.
568 | 
569 |     RESPONSE
570 |     <solution>
571 |     Terminate()
572 |     </solution>
573 | ```
574 | 
575 | ***
576 | 
577 | ## Notes you can embed in your system docs
578 | =======================================
579 | 
580 | ***
581 | 
582 | - These tools are part of the RPG **localization → editing** workflow: first find the exact interface(s) using the RPG and search tools, then apply the minimal, scoped edit tool, and finally **Terminate** when done. RPG_REPOSITORY_PLANNING_GRAPH
583 | 
584 | - The localization toolset is intentionally split into **file/interface inspection** and **feature-driven exploration**, and returns a **ranked, standardized** result at termination. RPG_REPOSITORY_PLANNING_GRAPH
585 | 
586 | - The editing tools enforce **narrow, auditable diffs** at class/method/function granularity and a **safe import policy** for reproducibility. RPG_REPOSITORY_PLANNING_GRAPH
587 | 
588 | ---
```

rpg-vector-index/sql/pgvector_schema.sql
```
1 | 
2 | \\ inferred\sql\pgvector_schema.sql
3 | ```sql
4 | -- path: sql/pgvector_schema.sql
5 | -- Requires: CREATE EXTENSION vector; (once per DB)
6 | -- Dimension is auto-detected by the loader, but this DDL uses a safe default of 8
7 | -- matching the seed. Change VECTOR(8) to your real embedding size when upgrading.
8 | 
9 | CREATE EXTENSION IF NOT EXISTS vector;
10 | 
11 | CREATE TABLE IF NOT EXISTS features (
12 |   id           TEXT PRIMARY KEY,
13 |   name         TEXT NOT NULL,
14 |   path_str     TEXT NOT NULL,
15 |   level        INT  NOT NULL,
16 |   l1_category  TEXT,
17 |   ancestors    TEXT[] NOT NULL,
18 |   description  TEXT,
19 |   tags         TEXT[] DEFAULT '{}',
20 |   aliases      TEXT[] DEFAULT '{}',
21 |   embedding    VECTOR(8)  -- set to your true dimension (e.g., 1536 or 3072)
22 | );
23 | 
24 | -- Helpful metadata indexes
25 | CREATE INDEX IF NOT EXISTS idx_features_path        ON features (path_str);
26 | CREATE INDEX IF NOT EXISTS idx_features_level       ON features (level);
27 | CREATE INDEX IF NOT EXISTS idx_features_l1_category ON features (l1_category);
28 | CREATE INDEX IF NOT EXISTS idx_features_tags        ON features USING GIN (tags);
29 | 
30 | -- Vector indexes (choose based on distance). HNSW prioritized; IVFFlat optional.
31 | -- HNSW: better speed/recall trade-off, slower to build, higher memory.
32 | CREATE INDEX IF NOT EXISTS features_embedding_hnsw_l2
33 |   ON features USING hnsw (embedding vector_l2_ops) WITH (m = 16, ef_construction = 64);
34 | -- Cosine
35 | -- CREATE INDEX IF NOT EXISTS features_embedding_hnsw_cos
36 | --   ON features USING hnsw (embedding vector_cosine_ops) WITH (m = 16, ef_construction = 64);
37 | -- Inner product
38 | -- CREATE INDEX IF NOT EXISTS features_embedding_hnsw_ip
39 | --   ON features USING hnsw (embedding vector_ip_ops) WITH (m = 16, ef_construction = 64);
40 | 
41 | -- Optional: IVFFlat (requires data present and a training step; tune lists accordingly)
42 | -- CREATE INDEX IF NOT EXISTS features_embedding_ivfflat_l2
43 | --   ON features USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
```

rpg-vector-index/tests/test_faiss_index.py
```
1 | # path: tests/test_faiss_index.py
2 | import json
3 | from pathlib import Path
4 | 
5 | import numpy as np
6 | import faiss
7 | 
8 | 
9 | def test_faiss_roundtrip(tmp_path: Path):
10 |     seed = Path(__file__).parents[1] / "feature_tree_seed.json"
11 |     data = json.loads(seed.read_text())
12 |     dim = int(data["retrieval"]["dims"])  # strict
13 |     vecs = data["retrieval"]["vectors"]
14 |     ids = sorted(vecs.keys())
15 |     mat = np.vstack([np.array(vecs[i], dtype="float32") for i in ids])
16 | 
17 |     faiss.normalize_L2(mat)
18 |     index = faiss.IndexHNSWFlat(dim, 16, faiss.METRIC_INNER_PRODUCT)
19 |     index.hnsw.efSearch = 32
20 |     index.add(mat)
21 | 
22 |     # nearest neighbor is itself
23 |     D, I = index.search(mat[:1], 1)
24 |     assert I[0][0] == 0
25 | 
26 |     # save/load
27 |     p = tmp_path / "idx.faiss"
28 |     faiss.write_index(index, str(p))
29 |     idx2 = faiss.read_index(str(p))
30 |     D2, I2 = idx2.search(mat[:1], 1)
31 |     assert I2[0][0] == 0
```

rpg-vector-index/tests/test_schema_mapping.py
```
1 | # path: tests/test_schema_mapping.py
2 | import json
3 | from pathlib import Path
4 | 
5 | from scripts.build_pgvector import FeatureNode
6 | 
7 | 
8 | def test_l1_category():
9 |     n = FeatureNode(
10 |         id="X",
11 |         name="X",
12 |         path="ml/algorithms/regression",
13 |         level=3,
14 |         ancestors=["ml", "algorithms"],
15 |         description=None,
16 |         tags=[],
17 |         aliases=[],
18 |     )
19 |     assert n.l1_category == "ml"
20 | 
21 | 
22 | def test_seed_loads_dim_matches():
23 |     seed = Path(__file__).parents[1] / "feature_tree_seed.json"
24 |     data = json.loads(seed.read_text())
25 |     dim = int(data["retrieval"]["dims"])  # fails if missing
26 |     assert dim > 0
```
