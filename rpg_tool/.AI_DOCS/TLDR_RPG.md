# 1) TL;DR (2–3 sentences)

The paper introduces the **Repository Planning Graph (RPG)**—a persistent graph that unifies proposal-level and implementation-level plans for generating full software repositories—and **ZeroRepo**, a graph-driven system that traverses the RPG in topological order with test-driven development. On the **RepoCraft** benchmark (six real-world Python projects, 1,052 tasks), ZeroRepo reports **81.5% functional coverage**, **69.7% test pass rate**, and repositories averaging **36K LOC**, substantially outperforming natural-language–based multi-agent and workflow baselines.

---

# 2) Executive Summary (5–10 bullets)

- **Purpose & scope:** Replace ambiguous natural-language planning with a **structured, persistent representation** (RPG) that encodes capabilities, files, classes/functions, and **data-flow edges**, enabling coherent **long-horizon** repository generation.
- **System:** **ZeroRepo** constructs an RPG in two stages (proposal-level, then implementation-level refinement) and then performs **graph-guided, TDD-based code generation** in topological order with localization and editing tools.
- **Benchmark:** **RepoCraft** evaluates end-to-end repository synthesis across **scikit-learn, pandas, sympy, statsmodels, requests, django** (names paraphrased to reduce leakage), comprising **1,052 tasks**.
- **Headline results:** ZeroRepo achieves **81.5% coverage**, **69.7% pass rate**, **36K LOC / 445K tokens**; ≈**3.9×** the code size of Claude Code and ≈**64×** other baselines; +**27.3** and +**35.8** percentage-point gains in coverage and pass rate over Claude Code.
- **Scaling:** RPG supports **near-linear growth** in features and LOC across iterations; natural-language baselines stagnate.
- **Mechanisms:** A **1.5M-node Feature Tree** grounds functionality selection via explore–exploit retrieval; interfaces and data flows impose **topological order** and **contract consistency** across modules.
- **Evaluation method:** Multi-stage pipeline—localization, LLM majority-vote semantic checks, then **execution of adapted tests**—measures both **presence** and **correctness**; auxiliary metrics cover **novelty** and **code scale**.
- **Implications:** RPG provides a **global, functionality-oriented map** that improves **reasoning consistency**, accelerates **bug localization** (30–50% fewer steps), and yields repositories closer to “gold” projects.

---

# 3) Detailed Narrative

## Context & motivation

Authors (Microsoft, Tsinghua, UC San Diego; dated **September 24, 2025**) argue that LLMs are strong at **function/file-level** code generation but struggle to create **complete repositories** because natural-language plans are **ambiguous, unstructured, and brittle** over long horizons. This causes unstable proposal-level scope and fragmented implementation plans in multi-file codebases.

## Approach

**Repository Planning Graph (RPG):** Nodes encode hierarchical **capabilities → files → classes/functions**; edges encode **inter-module data flows** and **intra-module orderings**, enforcing a **topological order** that aligns execution semantics with code organization.

**ZeroRepo pipeline (3 stages):**

1. **Proposal-level construction:** Ground user goals in a **large Feature Tree (≈1.5M nodes)**; use an **explore–exploit** strategy to form a repo-aligned subtree; refactor into a **modular functionality graph**.
2. **Implementation-level refinement:** Add **folder/file layout**, **data-flow constraints**, **shared abstractions** (e.g., base classes), and **adaptive interface design** (grouping features into functions/classes).
3. **Graph-guided code generation:** Traverse the RPG in **topological order**; at each leaf, perform **TDD** (derive tests, implement, iterate until pass). Include **graph-guided localization/editing** tools and staged **unit/regression/integration** validation.

## Results & evidence

**Benchmark:** **RepoCraft** compiles **1,052 tasks** from six widely used Python projects (paraphrased), with tasks derived from curated test suites and organized hierarchically; evaluation measures **coverage**, **novelty**, **accuracy** (pass & voting rates), and **code scale**.

**Quantitative outcomes:**

- **Coverage:** **81.5%** (ZeroRepo), **+27.3 pp** over Claude Code; **Novelty:** **~11–13%** with **100+** new features.
- **Correctness:** **69.7% pass rate** (o3-mini backbone), **+35.8 pp** over Claude Code; localization and validation pipeline ceiling on human gold projects: **81.0% pass**, **92.0% voting agreement**.
- **Scale:** **36K LOC**, **445K tokens** for ZeroRepo (Qwen3-Coder), ≈**3.9×** Claude Code, ≈**64×** others. **Near-linear growth** in features and LOC over 30 iterations; baselines plateau at **3–4K LOC** (Claude/Gemini) or **<1K LOC** (Codex).
- **Efficiency:** Graph guidance reduces localization steps by **30–50%** across integration testing, incremental development, and debugging.

**Mechanistic insights:** RPG induces **layered dependencies**, supports **design anchors** (shared structures like base estimators), and maintains **interface consistency** across modules—improving planning stability and repository coherence as features scale.

## Discussion & implications

Replacing free-form plans with a **persistent graph** improves **coverage**, **correctness**, and **scalability**, and shapes more systematic agent behavior (coarse search → content inspection → global exploration). The Feature Tree mitigates enumerative bias, while the RPG’s topology aligns design and execution, supporting **long-horizon** development.

## Conclusion

RPG + ZeroRepo constitute a **graph-first paradigm** for repository generation, achieving **state-of-the-art** results on RepoCraft and providing a structured basis for future large-scale, multi-module software synthesis.

---

# 4) Key Concepts & Entities (glossary bullets)

- **Repository Planning Graph (RPG):** A persistent graph where nodes are capabilities/files/classes/functions and edges encode data flows and orderings; enforces topological build and execution consistency.
- **ZeroRepo:** System that builds an RPG (proposal → implementation) and generates code via topological traversal and TDD, with graph-guided localization and editing.
- **Feature Tree (≈1.5M nodes):** Large ontology of software capabilities used to ground functionality selection via retrieval and explore–exploit expansion.
- **RepoCraft:** Benchmark of six Python repositories with 1,052 tasks to evaluate coverage, novelty, correctness, and code scale for end-to-end repo generation.
- **Coverage / Novelty / Pass rate / Voting rate:** Metrics for breadth, originality, and correctness (execution and semantic agreement).

---

# 5) Notable Quantitative Facts

- **1,052 tasks** across **six** real-world Python projects (paraphrased).
- **Coverage:** **81.5%** (ZeroRepo) vs **54.2%** (Claude Code) → **+27.3 pp**.
- **Pass rate:** **69.7%** (ZeroRepo) vs **33.9%** (Claude Code) → **+35.8 pp**.
- **Repository size:** **36K LOC**, **445K tokens** (ZeroRepo with Qwen3-Coder); ≈**3.9×** Claude Code, ≈**64×** others.
- **Localization effort:** **30–50%** fewer steps with graph guidance.
- **Upper bound check:** On human “gold” projects, pipeline **81.0%** pass, **92.0%** voting agreement.

---

# 6) Limitations & Assumptions

- **Evaluation mediation by LLMs:** Semantic validation uses **majority-vote LLM judgments**, introducing potential model bias despite safeguards.
- **Leakage mitigation but not elimination:** Repository names/descriptions are paraphrased; still, residual pretraining overlap cannot be fully ruled out.
- **Feature Tree skew:** The global ontology is **long-tailed** (data-processing heavy); requires substantial filtering/reorganization to match domains.
- **Test generation limits:** Even with higher code success, **test coverage** remains moderate and tends to decline as code length increases, highlighting a bottleneck in automated testing.
- **Backbone sensitivity:** Some reported numbers are tied to backbones (e.g., o3-mini, Qwen3-Coder) and specific iteration budgets.

---

# 7) Open Questions & Next Steps

- **Generalization across languages/stacks:** How well do RPG and ZeroRepo transfer beyond Python and the six benchmarked domains?
- **Richer contracts:** Can RPG encode **resource, latency, or security** constraints (not just I/O types) to guide non-functional requirements?
- **Human-in-the-loop planning:** What interfaces best let engineers **edit the RPG** and propagate changes safely through code and tests?
- **Testing robustness:** How to improve **automatic test generation** and **coverage** as repositories scale, reducing reliance on LLM adjudication?
- **Ontology governance:** Methods to **debias and update** the Feature Tree continuously as ecosystems evolve.

---

# 8) Provenance Notes (lightweight)

- **Authorship & date:** Jane Luo, Xin Zhang, Steven Liu, Jie Wu, Yiming Huang, Yangyu Huang, Chengyu Yin, Ying Xin, Jianfeng Liu, Yuefeng Zhan, Hao Sun, Qi Chen, Scarlett Li, Mao Yang; **Microsoft, Tsinghua University, UC San Diego; September 24, 2025.**
- **Figure/appendix cues:** The text references **Figure 1–2** (RPG structure and pipeline), **Figures 5–6** (near-linear scaling), and multiple **appendices** (A–E) for algorithms, statistics, and tool details; exact page numbers are not explicitly visible in the provided text.

---

*Prepared from the provided document text only; phrasing and numbers follow the source precisely where stated.*
