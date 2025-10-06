# AGENTS.md — Tool Selection (Python)

When you need to call tools from the shell, use this rubric:

## File & Text

- Find files by file name: `fd`
- Find files with path name: `fd -p <file-path>`
- List files in a directory: `fd . <directory>`
- Find files with extension and pattern: `fd -e <extension> <pattern>`
- Find Text: `rg` (ripgrep)
- Find Code Structure: `ast-grep`
  - Common languages:
    - Python → `ast-grep --lang python -p '<pattern>'`
    - TypeScript → `ast-grep --lang ts -p '<pattern>'`
    - Bash → `ast-grep --lang bash -p '<pattern>'`
    - TSX (React) → `ast-grep --lang tsx -p '<pattern>'`
    - JavaScript → `ast-grep --lang js -p '<pattern>'`
    - Rust → `ast-grep --lang rust -p '<pattern>'`
    - JSON → `ast-grep --lang json -p '<pattern>'`
  - Prefer `ast-grep` over ripgrep/grep unless a plain-text search is explicitly requested.
- Select among matches: pipe to `fzf`

## Data

- JSON: `jq`
- YAML/XML: `yq`

## Python Tooling

- Package Management & Virtual Envs: `uv`
  (fast replacement for pip/pip-tools/virtualenv; use `uv pip install ...`, `uv run ...`)
- Linting & Formatting: `ruff`
  (linter + formatter; use `ruff check .`, `ruff format .`)
- Static Typing: `mypy`
  (type checking; use `mypy .`)
- Security: `bandit`
  (Python security linter; use `bandit -r .`)
- Testing: `pytest`
  (test runner; use `pytest -q`, `pytest -k <pattern>` to filter tests)
- Logging: `loguru`
  (runtime logging utility; import in code:

  ```python
  from loguru import logger
  logger.info("message")
  ```)

## Notes

- Prefer uv for Python dependency and environment management instead of pip/venv/poetry/pip-tools.

## MCP_SERVERS

Use the dspy_Docs mcp server to get latest docs for DSPy usage.

## Rules for Best-Practice

<file_length_and_structure>

- Prefer maintainability signals over fixed line caps.
- Split when cognitive complexity > 15, cohesion drops, or fan-in/out spikes.
- Group by feature. Keep a file to one capability plus its close helpers.
- Use clear folder names and consistent naming.

</file_length_and_structure>

<paradigm_and_style>

- Use OOP, functional, or data-oriented styles as idiomatic for the language.
- Favor composition. In OOP, model behavior behind small interfaces or protocols.
- Prefer pure functions and algebraic data types where natural.

</paradigm_and_style>

<single_responsibility_principle>

- Aim for one capability and its close helpers. Avoid micro-files.
- Enforce through module boundaries and public APIs, not line counts.

</single_responsibility_principle>

<modular_design>

- Design modules to be interchangeable, testable, and isolated.
- Keep public surfaces small. Inject dependencies. Avoid tight coupling.
- Optimize for replaceability and test seams over premature reuse.

</modular_design>

<roles_by_platform>

- UI stacks: ViewModel for UI logic, Manager for business logic, Coordinator for navigation and state flow.
- Backend and CLI: Service, Handler, Repository, Job, Workflow.
- Do not mix view code with business logic.

</roles_by_platform>

<function_and_class_size>

- Size by behavior, not lines.
- Functions ≤ 20–30 cognitive steps.
- Split a class when it owns more than one lifecycle or more than one external dependency graph.

</function_and_class_size>

<naming_and_readability>

- Use intention revealing names.
- Allow domain terms with qualifiers, for example UserData, BillingInfo.
- Forbid empty suffixes like Helper or Utils unless tightly scoped.

</naming_and_readability>

<scalability_mindset>

- Build for extension points from day one, such as interfaces, protocols, and constructor injection.
- Prefer local duplication over unstable abstractions.
- Document contracts at module seams.

</scalability_mindset>

<avoid_god_classes>

- Do not centralize everything in one file or class.
- Split into UI, State, Handlers, Networking, and other focused parts.

</avoid_god_classes>

<dependency_injection>

- Backends: prefer constructor injection. Keep containers optional.
- Swift, Kotlin, TypeScript: use protocols or interfaces. Inject by initializer or factory.
- Limit global singletons. Provide test doubles at seams.

</dependency_injection>

<testing>

- Require deterministic seams.
- Add contract tests for modules and layers.
- Use snapshot or golden tests for UI and renderers.

</testing>

<architecture_boundaries>

- Feature oriented packaging with clear dependency direction: UI → app → domain → infra.
- Stabilize domain modules. Keep infra replaceable.
- Enforce imports with rules or module maps.

</architecture_boundaries>
