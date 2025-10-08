Here’s the **execution order** that’s aligned to the RPG pipeline — **Discover → Design → Build → Validate → Benchmark → Monitor** — and consistent with the whitepaper’s sequence (implementation-level refinement before graph-guided topo build). Where a task’s minimal deps would allow earlier execution (e.g., GEN-001), I place it later so the build plan captures intra-module order and full constraints, which is the safer choice for stability. (Build Guide trace matrix; Whitepaper Fig. 1 “B1/B2 before C”. )

1. **4 — [DSC-001] Develop Project Spec Parser**.
2. **1 — [DSC-002] Define Detailed RPG Schema**.
3. **2 — Extend Graph Service for Typed Nodes and Edges** (uses schema).
4. **6 — [DSC-003] Build Feature Tree Index** (spec → feature tree).
5. **7 — [PROP-001] Exploit Retrieval (top-k)**.
6. **8 — [PROP-002] Explore Sampling (diversity)**.
7. **9 — [PROP-003] LLM Filter & Merge**.
8. **10 — [PROP-004] Refactor into Cohesive Modules**.
9. **11 — [PROP-005] Persist L0 Functionality Graph**.
10. **5 — [IMPL-001] Map Nodes → Folders** (L0→L1).
11. **12 — [IMPL-002] Group Capabilities into Files** (L1→L2).
12. **13 — [IMPL-003] Encode Typed Data-Flows**.
13. **26 — [MON-001] CI Gate: DAG & Schema** (turn on guardrails now that data-flows exist).
14. **14 — [IMPL-004] Define Intra-Module File Order**.
15. **30 — [IMPL-004] Intra-Module Order Lints**.
16. **15 — [IMPL-005] Abstract Base Classes & Shared Types** (usage-driven).
17. **16 — [IMPL-006] One Interface per Leaf**.
18. **3 — [GEN-001] Topological Build Plan Generator** (placed **after** IMPL so order edges & data-flows are respected).
19. **27 — [MON-002] Audit Logging of Localization Steps** (depends on planner).
20. **17 — [GEN-002] Auto-Derive Unit Tests**.
21. **18 — [GEN-003] Implement-to-Green & Coverage Gate**.
22. **19 — [GEN-004] Selective Regression by Impact**.
23. **20 — [GEN-005] Integration Tests per Subgraph**.
24. **21 — [VAL-001] Majority-Vote Semantic Validator**.
25. **22 — [VAL-002] Failure Attribution & Auto-Remediation**.
26. **23 — [VAL-003] RepoCraft Metrics (Coverage/Novelty/Pass/Vote/Files/LOC/Tokens)**.
27. **24 — [BMR-001] Build Benchmark Task Set**.
28. **25 — [BMR-002] Evaluation Loop per Task**.
29. **28 — [MON-003] Governance: SBOM, Licenses, Secrets** (after core GEN loop exists).
30. **29 — [MON-004] Scaling Dashboards** (after metrics).

### Machine-readable order

```json
{
  "execution_order": [
    {"id": 4, "title": "[DSC-001] Develop Project Spec Parser"},
    {"id": 1, "title": "[DSC-002] Define Detailed RPG Schema"},
    {"id": 2, "title": "Extend Graph Service for Typed Nodes and Edges"},
    {"id": 6, "title": "[DSC-003] Build Feature Tree Index"},
    {"id": 7, "title": "[PROP-001] Exploit Retrieval"},
    {"id": 8, "title": "[PROP-002] Explore Sampling"},
    {"id": 9, "title": "[PROP-003] LLM Filter & Merge"},
    {"id": 10, "title": "[PROP-004] Refactor into Cohesive Modules"},
    {"id": 11, "title": "[PROP-005] Persist L0 Functionality Graph"},
    {"id": 5, "title": "[IMPL-001] Map Graph Nodes to File System Structure"},
    {"id": 12, "title": "[IMPL-002] Group Capabilities into Files"},
    {"id": 13, "title": "[IMPL-003] Encode Typed Data-Flows"},
    {"id": 26, "title": "[MON-001] CI Gate: DAG & Schema"},
    {"id": 14, "title": "[IMPL-004] Define Intra-Module File Order"},
    {"id": 30, "title": "[IMPL-004] Intra-Module Order Lints"},
    {"id": 15, "title": "[IMPL-005] Abstract Base Classes & Shared Types"},
    {"id": 16, "title": "[IMPL-006] Define One Interface per Leaf"},
    {"id": 3, "title": "[GEN-001] Topological Build Plan Generator"},
    {"id": 27, "title": "[MON-002] Audit Logging of Localization Steps"},
    {"id": 17, "title": "[GEN-002] Auto-Derive Unit Tests"},
    {"id": 18, "title": "[GEN-003] Implement to Green & Gate Commits"},
    {"id": 19, "title": "[GEN-004] Selective Regression by Impact"},
    {"id": 20, "title": "[GEN-005] Add Integration Tests per Subgraph"},
    {"id": 21, "title": "[VAL-001] Majority-Vote Semantic Validator"},
    {"id": 22, "title": "[VAL-002] Failure Attribution & Auto-Remediation"},
    {"id": 23, "title": "[VAL-003] RepoCraft Metrics"},
    {"id": 24, "title": "[BMR-001] Build Benchmark Task Set"},
    {"id": 25, "title": "[BMR-002] Evaluation Loop per Task"},
    {"id": 28, "title": "[MON-003] Governance: SBOM, Licenses, Secrets"},
    {"id": 29, "title": "[MON-004] Scaling Dashboards"}
  ]
}
```

**Why this order:** It respects all declared deps in your task list while enforcing the paper/guide’s staging: proposal & implementation refinement precede topo build and codegen, which then feed validation, benchmarking, and monitoring. This avoids unstable plans and ensures the build queue is constrained by both inter-module data-flows and intra-module order. (Whitepaper Fig. 1; Build Guide §Trace Matrix IMPL→GEN→VAL→BMR→MON).
