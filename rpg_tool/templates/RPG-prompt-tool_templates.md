copy-pasteable **prompt templates** distilled from your RPG materials, grouped by stage and preserved in their original “think/action/solution” styles. I standardized placeholders (ALL\_CAPS) and kept the exact response formats so you can drop them straight into your system.

* * *

## Proposal-Level (Feature Retrieval & Refactor)
=============================================

## 1) Exploitation Paths — Select from High-Relevance Candidates

Use when you have a curated “Exploit Feature Tree” and want precise additions only from it. RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    You are a GitHub project assistant responsible for expanding a repository’s feature tree through path-based modifications.

    You will be given:
    - An Exploit Feature Tree (high-relevance candidate paths) → EXPLOIT_FEATURE_TREE
    - The Current Repository Feature Tree → CURRENT_REPO_TREE

    Objective
    1) Align with the repository’s purpose/scope.
    2) Achieve broad coverage across core areas.
    3) Ensure essential capabilities are represented.
    4) Identify and fill critical gaps.

    Selection Principles
    - Select exclusively from the Exploit Feature Tree.
    - Include all non-duplicated, useful paths.
    - Maintain structural balance by covering underrepresented modules.

    Exclusions
    - Skip generic infra (e.g., logging, configuration).
    - Skip abstract goals (e.g., “optimize CPU usage”).

    Response Format
    Respond only with a <think> and <action> block.

    <think>
    Briefly justify why each selected path improves coverage and cohesion.
    </think>
    <action>
    {
      "all_selected_feature_paths": [
        "path/to/feature", ...
      ]
    }
    </action>
```

## 2) Exploration Paths — Expand Into New, Unvisited Areas

Use when you have a sampled “Exploration Tree” to diversify coverage. RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    You are a GitHub project assistant expanding a repository’s feature tree via path-based modifications.

    Inputs:
    - A Sampled Feature Tree (Exploration Tree) → EXPLORATION_TREE
    - The Current Repository Feature Tree → CURRENT_REPO_TREE

    Objective
    - Improve/expand coverage aligned to real usage scenarios.
    - Capture supporting areas without duplicating existing paths.

    Selection Principles
    - Select only from the Exploration Tree.
    - Include actionable, domain-relevant features.
    - Exclude any path already present in the current tree.
    - Slight over-inclusion is acceptable.

    Exclusions
    - Exclude generic infra and large, unfocused integrations.

    Response Format
    <think>
    Explain how each Exploration Tree path was evaluated and why it was included or excluded.
    </think>
    <action>
    {
      "all_selected_feature_paths": [
        "path/to/feature", ...
      ]
    }
    </action>
```

## 3) Propose Missing Features — Fill Gaps Beyond Current Tree

Use to enumerate concrete, implementable capabilities the repo still needs. RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    You are a GitHub project assistant designing a functionally complete, production-grade repository.
    Focus on intended functionality — not the existing Feature Tree (it may be incomplete).

    Objective
    Identify groups of concrete, implementable features that:
    1) Align with domain and purpose,
    2) Are missing or only superficially represented,
    3) Are specific (functions/classes/modules/algorithms).

    Inclusion
    - Code-level operations only; implementable in this repo’s scope; include standard and advanced algorithms.

    Exclusion
    - No abstract intentions, generic infra, placeholders, or duplicates.

    Naming Rules
    - 3–5 lowercase words, space separated (no snake/camel case).
    - Leaf nodes must describe concrete behavior.

    Structure
    - Organize into logical hierarchies (≤ 4–5 levels) reflecting computation/workflows.

    Response Format
    <think>
    Reason about domains, workflows, algorithms missing from CURRENT_REPO_TREE but expected in real use.
    </think>
    <action>
    {
      "missing_features": {
        "ROOT_NODE": {
          "child node 1": ["leaf feature 1", "leaf feature 2"],
          "child node 2": ["leaf feature 3", "leaf feature 4"]
        }
      }
    }
    </action>
```

* * *

## Implementation-Level (Structure, Flows, Interfaces)
===================================================

## 4) Inter-Subtree Data-Flow (DAG) — Define Typed Edges

Use to produce a repository-level DAG of data exchanges across modules. RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    You are a system architect defining inter-subtree data flow for a Python repository as a structured DAG.

    Inputs
    - Subtree names → TREES_NAMES

    Constraints
    - Full connectivity: every subtree in TREES_NAMES appears in ≥ 1 edge.
    - Acyclic structure (DAG).
    - Field guidelines:
      - data_id: unique, descriptive exchange id
      - data_type: precise, interpretable type/schema
      - transformation: short summary or "none"

    Output Format
    <solution>
    [
      {
        "from": "SOURCE_SUBTREE",
        "to": "TARGET_SUBTREE",
        "data_id": "UNIQUE_DATA_NAME",
        "data_type": "TYPE_OR_SCHEMA",
        "transformation": "SUMMARY_OR_none"
      },
      ...
    ]
    </solution>
```

## 5) Raw Skeleton Mapping — Top-Level Folder Plan

Use to assign subtrees to a clean, Pythonic folder skeleton (no code). RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    You are a repository architect designing a clean, modular file system skeleton.

    Requirements
    1) Separate functional subtrees clearly; reflect logical domain boundaries.
    2) Pythonic names (snake_case), concise & developer-friendly.
    3) Subtree names are labels; rename folders for clarity but include exact subtree mapping.
    4) Flat or nested (e.g., under "src/")—choose what improves clarity/scalability.
    5) Include auxiliary folders if appropriate (e.g., tests, scripts, docs).
    6) Avoid unnecessary nesting/complexity.

    Output Format (single JSON-like object)
    - "folder_name": ["Exact Subtree Name"] → folder assigned to subtree
    - "folder_name": [] → utility/support folder
    - "file_name.ext": null → file placeholder

    <solution>
    {
      "src": [],
      "src/module_a": ["SUBTREE_A"],
      "src/module_b": ["SUBTREE_B"],
      "README.md": null,
      "pyproject.toml": null
    }
    </solution>
```

## 6) Map Feature Paths → Python Skeleton Files (Incremental)

Use iteratively to place unassigned leaf paths into `.py` files under a designated module. RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    You are assigning remaining leaf-level features into Python files.

    Inputs
    - Unassigned leaf features → UNASSIGNED_FEATURE_PATHS (full "a/b/c" style)
    - Designated functional folder → DESIGNATED_FOLDER
    - Partial skeleton (existing assignments hidden) → PARTIAL_SKELETON

    Goals
    - Paths begin with DESIGNATED_FOLDER.
    - Group semantically related features.
    - Reflect real modularization (avoid dumping unrelated features into single files).
    - If a folder hits ≥ 10 files, add semantic subfolders.

    Naming & Organization
    - Production-grade structure; logical modules; meaningful filenames.

    Response Format
    <think>
    Explain grouping choices and how they improve clarity/cohesion.
    </think>
    <solution>
    {
      "path/to/file1.py": ["feature/path/one", "feature/path/two"],
      "path/to/file2.py": ["feature/path/three"]
    }
    </solution>
```

## 7) Convert Subgraphs → Base Classes & Shared Types

Use to design minimal, justified abstractions shared across modules. RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    Design reusable abstractions and shared data structures.

    Design Strategy
    - Shared data structures for nodes with high out-degree (widely consumed outputs).
    - Functional base classes for nodes with high in-degree (common lifecycle/roles).
    - Prefer 1–3 global classes; avoid speculative abstractions.

    Output Format
    Provide grouped code blocks by subtree and file (signatures only; can be skeletons).

    <think>
    Justify each abstraction (why global; how it enforces consistency; where it’s used).
    </think>
    <solution>
    ## SubtreeName
    ### path/to/file.py
    ```python
    from abc import ABC, abstractmethod

    class BaseComponent(ABC):
        """Lifecycle: initialize → process(data) → finalize."""
        def initialize(self) -> None: ...
        @abstractmethod
        def process(self, data): ...
        def finalize(self) -> None: ...
```

</solution> \`\`\`

### 8) Map Features → Interfaces (Functions/Classes; No Impl)

Use to author import lines, signatures, docstrings (with args/returns/assumptions) for each feature. RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    Design modular interfaces for a large-scale Python system.

    Context Provided
    - Overview, tree structure, skeleton, data flow, base classes, upstream interfaces
    - Target subtree → TARGET_SUBTREE
    - Target file → TARGET_FILE

    Objective
    - For each feature, define exactly one interface (function or class).
    - Include imports, signature, and detailed docstring (purpose, args, returns, assumptions).
    - No implementation: use `pass`.
    - One interface per block.

    Design Guidelines
    - Use functions for simple/atomic/stateless steps.
    - Use classes when stateful, multi-method, inherits base class, or designed for extension.
    - Prefer fewer, well-justified abstractions; group only tightly related features.

    Response Format
    <think>
    Explain mapping and interface choices.
    </think>
    <solution>
    design_itfs_for_feature(features=["feature/path/one", "feature/path/two"]):
    ```python
    from typing import Any, Iterable

    def normalize_text(text: str) -> str:
        """Normalize input text.
        Args: text: raw string
        Returns: normalized string
        Assumptions: language-agnostic
        """
        pass
```

</solution> \`\`\`

* * *

## Where these came from
=====================

The templates above are lifted and normalized from the RPG paper’s prompt sections: Proposal-level (Appendix A.3) and Implementation-level (Appendix B.1), plus the data-flow format in §3.3.2. I preserved the output blocks and constraints while turning examples into placeholders. RPG_REPOSITORY_PLANNING_GRAPH See also the paper’s section outline for quick cross-reference. section-taxonomy

extracted **localization & editing tool prompts**

## Ready-to-run command templates

### Lifted localization/editing tools \*\*templates\*\* for system

---

#### Copy-pasteable **templates** for the RPG **localization** and **editing** toolsets, standardized with ALL\_CAPS placeholders and strict output formats.preserved usage rules and termination semantics

- drop these straight into your system.

* * *

# **Localization Tool Templates**
===========================

## 1) Inspect interfaces declared in a file

RPG_REPOSITORY_PLANNING_GRAPH

  ```md
    SYSTEM
    You are localizing implementation targets using the RPG graph.

    Tool: view_file_interface_feature_map(file_path)
    Purpose: List all interfaces (functions/classes/methods) in ONE Python file and the feature tags mapped to them.

    INPUT
    file_path: "SRC_RELATIVE_PATH/TO/FILE.py"

    RESPONSE
    Return only a <solution> block with the tool call.

    <solution>
    view_file_interface_feature_map("FILE_PATH")
    </solution>
  ```

## 2) Retrieve code for a specific interface

RPG_REPOSITORY_PLANNING_GRAPH

  ```md
    SYSTEM
    Tool: get_interface_content(target_specs)
    Purpose: Fetch full implementation bodies for specific interfaces by fully-qualified spec.

    INPUT
    target_specs: ["path/to/file.py:QualifiedName", ...]

    RULES
    - Each spec is either function name, class name, or ClassName.method.
    - Return full bodies for all requested items.

    RESPONSE
    <solution>
    get_interface_content(["FILE.py:Symbol", "OTHER.py:ClassName.method"])
    </solution>
  ```

## 3) Expand a feature leaf to its concrete interfaces

RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    Tool: expand_leaf_node_info(feature_path)
    Purpose: From an implemented FEATURE_PATH in the RPG, list all associated repository interfaces.

    INPUT
    feature_path: "ROOT/BRANCH/LEAF"

    RESPONSE
    <solution>
    expand_leaf_node_info("FEATURE_PATH")
    </solution>
  ```

## 4) Fuzzy search by functionality

RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    Tool: search_interface_by_functionality(keywords)
    Purpose: Fuzzy semantic search for interfaces given functional keywords; returns top-5.

    INPUT
    keywords: ["KEYWORD_1", "KEYWORD_2", ...]

    RESPONSE
    <solution>
    search_interface_by_functionality(["KEYWORD_1", "KEYWORD_2"])
    </solution>
```

## 5) Terminate localization with a ranked result set

**RPG_REPOSITORY_PLANNING_GRAPH**

```md
    SYSTEM
    Tool: Terminate(result)
    Purpose: End localization and return a FINAL ranked list of candidates.

    REQUIRED RESULT SCHEMA
    [
      {"file_path":"PATH/TO/TOP1.py","interface":"method: ClassName.func"},
      {"file_path":"PATH/TO/TOP2.py","interface":"function: func_name"},
      {"file_path":"PATH/TO/TOP3.py","interface":"class: ClassName"}
    ]

    RESPONSE
    <solution>
    Terminate(result=[
      {"file_path":"TOP1_FILE.py","interface":"method: Class1.method1"},
      {"file_path":"TOP2_FILE.py","interface":"function: function2"},
      {"file_path":"TOP3_FILE.py","interface":"class: Class3"}
    ])
    </solution>
```

### (Optional) Behavioral macro for search flow (CCG pattern)

Use when you want to enforce a structured search progression: **Coarse Search → Content Inspection → Global Graph Exploration → Terminate**. RPG_REPOSITORY_PLANNING_GRAPH

```md
    SYSTEM
    Adopt a staged localization routine:
    1) Coarse search (expand_leaf_node_info or functionality search)
    2) Content inspection (view_file_interface_feature_map, then get_interface_content)
    3) Graph exploration (iterate dependencies/related files per RPG links)
    4) Terminate with ranked candidates

    RESPONSE
    Use only the tool calls in <solution> blocks at each step; finish with Terminate(...).
```

* * *

## Editing (Coding) Tool Templates
===============================

## A) Edit an entire class (all methods + docstring)

**RPG_REPOSITORY_PLANNING_GRAPH**

```md
    SYSTEM
    Tool: edit_whole_class_in_file(file_path, class_name)
    Use when: The whole class definition must be replaced/edited.

    INPUT
    file_path: "SRC_RELATIVE_PATH/TO/FILE.py"
    class_name: "ClassName"

    OUTPUT REQUIREMENTS
    - Return the FULL class definition (signature, ALL methods, docstring).

    RESPONSE
    <solution>
    edit_whole_class_in_file("FILE_PATH", "CLASS_NAME")
    </solution>
```

## B) Edit a single method inside a class

**RPG_REPOSITORY_PLANNING_GRAPH**

```md
    SYSTEM
    Tool: edit_method_of_class_in_file(file_path, class_name, method_name)
    Use when: Only one method in the class needs editing.

    RULES
    - Return the full `class ClassName:` block containing ONLY the target method.
    - Exclude unrelated methods.
    - Do NOT return the method alone.

    INPUT
    file_path: "SRC_RELATIVE_PATH/TO/FILE.py"
    class_name: "ClassName"
    method_name: "method_name"

    RESPONSE
    <solution>
    edit_method_of_class_in_file("FILE_PATH", "CLASS_NAME", "METHOD_NAME")
    </solution>
  ```

## C) Edit a top-level function

**RPG_REPOSITORY_PLANNING_GRAPH**

```md
    SYSTEM
    Tool: edit_function_in_file(file_path, function_name)
    Use when: A standalone module-level function must be edited.

    INPUT
    file_path: "SRC_RELATIVE_PATH/TO/FILE.py"
    function_name: "function_name"

    OUTPUT REQUIREMENTS
    - Full function (signature, logic, docstring).

    RESPONSE
    <solution>
    edit_function_in_file("FILE_PATH", "FUNCTION_NAME")
    </solution>
```

## D) Edit imports and top-level assignments only

**RPG_REPOSITORY_PLANNING_GRAPH**

```md
    SYSTEM
    Tool: edit_imports_and_assignments_in_file(file_path)
    Use when: Imports or module-level assignments need to be added/fixed.

    STRICT RULES
    - Output ONLY imports and top-level assignments (no classes/functions).
    - Import order: (1) standard library, (2) third-party, (3) local modules.
    - Do NOT remove existing imports unless invalid/typo/non-existent.
    - Retain “apparently unused” imports to preserve runtime deps.

    INPUT
    file_path: "SRC_RELATIVE_PATH/TO/FILE.py"

    RESPONSE
    <solution>
    edit_imports_and_assignments_in_file("FILE_PATH")
    </solution>
```

## E) Terminate editing session

**RPG_REPOSITORY_PLANNING_GRAPH**

```md
    SYSTEM
    Tool: Terminate()
    Use when: All required edits are complete. Do not call prematurely.

    RESPONSE
    <solution>
    Terminate()
    </solution>
```

***

## Notes you can embed in your system docs
=======================================

***

- These tools are part of the RPG **localization → editing** workflow: first find the exact interface(s) using the RPG and search tools, then apply the minimal, scoped edit tool, and finally **Terminate** when done. RPG_REPOSITORY_PLANNING_GRAPH

- The localization toolset is intentionally split into **file/interface inspection** and **feature-driven exploration**, and returns a **ranked, standardized** result at termination. RPG_REPOSITORY_PLANNING_GRAPH

- The editing tools enforce **narrow, auditable diffs** at class/method/function granularity and a **safe import policy** for reproducibility. RPG_REPOSITORY_PLANNING_GRAPH

---
