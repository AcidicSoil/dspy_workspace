**Stakeholder & Audience Brief**

**Alignment:** Maps to background doc sections 0–1 (Scope, Inputs) and 6 (Interfaces). Stakeholder roles correspond to Planner/Implementer/Builder/Verifier/Orchestrator agents, ensuring consistent ownership across artifacts.

**Primary stakeholder groups**

- **Platform Engineering Leads**: Sponsor accelerator adoption, own budgets, prioritize ROI and integration into existing ML platforms.
- **DSPy Enablement Team**: Curate tutorials, maintain module catalog, enforce quality standards for reusable assets.
- **Applied ML Squads**: Build domain-specific agents and workflows, deliver end-user functionality, provide feedback on usability and coverage.
- **ZeroRepo / RPG Operability Owners**: Govern repository planning practices, ensure graph schemas stay consistent, operate tooling pipelines.

**Audience definition**

- Core audience: technical leads and senior engineers using RPG to plan new DSPy-based repositories.
- Secondary audience: product managers and solution architects who review planning artifacts and measure delivery risk.

**Objectives by stakeholder**

- Platform Engineering Leads: reduce time-to-production for new AI services by ≥40%, maintain compliance and observability baselines.
- DSPy Enablement Team: raise tutorial reuse rate ≥5 per project, keep catalog synchronized with RPG capability taxonomy.
- Applied ML Squads: achieve ≥70% repo generation pass rate within two optimizer iterations, minimize manual graph edits.
- ZeroRepo / RPG Owners: maintain DAG validity and coverage ≥90%, ensure localization tooling accelerates post-generation edits.

**Decision checkpoints and templates**

- Requirements intake template: capture capability scope, constraints, data sources, and KPIs (owner: product manager, reviewer: platform lead).
- RPG capability mapping review: validate capability-to-module binding, check edge cases, confirm coverage (owner: DSPy enablement, reviewer: RPG owner).
- Execution readiness review: sign off on optimizer budget, observability setup, HITL gates prior to topological build (owner: applied ML lead, reviewer: platform lead).
