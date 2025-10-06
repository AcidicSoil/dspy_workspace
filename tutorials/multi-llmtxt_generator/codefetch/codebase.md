Project Structure:
├── README.md
├── __pycache__
│   ├── repo_helpers.cpython-312.pyc
│   ├── repo_helpers.cpython-313.pyc
│   ├── repository_analyzer.cpython-312.pyc
│   ├── repository_analyzer.cpython-313.pyc
│   ├── signatures.cpython-312.pyc
│   └── signatures.cpython-313.pyc
├── codefetch
│   └── codebase.md
├── generate_llms.py
├── interactive_generate_llms_py_dynamic_names_owner_repo_dirs.py
├── repo_helpers.py
├── repository_analyzer.py
└── signatures.py


generate_llms.py
```
1 | # generate_llms.py
2 | 
3 | from dotenv import load_dotenv
4 | import dspy
5 | from repository_analyzer import RepositoryAnalyzer
6 | from repo_helpers import gather_repository_info
7 | 
8 | load_dotenv()
9 | 
10 | def generate_llms_txt_for_dspy(
11 |     repo_url="https://github.com/openai/openai-agents-python",
12 | ):
13 |     # Correct Ollama LM initialization
14 |     lm = dspy.LM(
15 |         "ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS",
16 |         api_base="http://localhost:11434",  # Local Ollama server URL
17 |         api_key="",  # Usually empty for local Ollama; remove if you do not have a key
18 |         streaming=False,
19 |         response_format={
20 |             "type": "json_schema",
21 |             "json_schema": {
22 |                 "schema": {
23 |                     "type": "object",
24 |                     "properties": {
25 |                         "project": {
26 |                             "type": "object",
27 |                             "properties": {
28 |                                 "name": {"type": "string"},
29 |                                 "description": {"type": "string"},
30 |                             },
31 |                             "required": ["name", "description"],
32 |                         },
33 |                         "key_concepts": {
34 |                             "type": "array",
35 |                             "items": {"type": "string"},
36 |                             "minItems": 1,
37 |                         },
38 |                         "architecture_overview": {"type": "string"},
39 |                         "important_directories": {
40 |                             "type": "array",
41 |                             "items": {"type": "string"},
42 |                             "minItems": 1,
43 |                         },
44 |                         "entry_points": {
45 |                             "type": "array",
46 |                             "items": {"type": "string"},
47 |                             "minItems": 1,
48 |                         },
49 |                         "development_info": {
50 |                             "type": "object",
51 |                             "properties": {
52 |                                 "test_dependencies": {
53 |                                     "type": "array",
54 |                                     "items": {"type": "string"},
55 |                                     "minItems": 1,
56 |                                 },
57 |                                 "linting_tools": {
58 |                                     "type": "array",
59 |                                     "items": {"type": "string"},
60 |                                     "minItems": 1,
61 |                                 },
62 |                                 "optional_dependencies": {
63 |                                     "type": "array",
64 |                                     "items": {"type": "string"},
65 |                                 },
66 |                             },
67 |                             "required": ["test_dependencies", "linting_tools"],
68 |                         },
69 |                         "usage_examples": {
70 |                             "type": "array",
71 |                             "items": {"type": "string"},
72 |                             "minItems": 1,
73 |                         },
74 |                     },
75 |                     "required": [
76 |                         "project",
77 |                         "key_concepts",
78 |                         "architecture_overview",
79 |                         "important_directories",
80 |                         "entry_points",
81 |                         "development_info",
82 |                         "usage_examples",
83 |                     ],
84 |                 }
85 |             },
86 |         },
87 |     )
88 |     dspy.configure(lm=lm)
89 | 
90 |     analyzer = RepositoryAnalyzer()
91 | 
92 | #    repo_url = "https://github.com/stanfordnlp/dspy"
93 |     file_tree, readme_content, package_files = gather_repository_info(repo_url)
94 | 
95 |     result = analyzer(
96 |         repo_url=repo_url,
97 |         file_tree=file_tree,
98 |         readme_content=readme_content,
99 |         package_files=package_files,
100 |     )
101 | 
102 |     return result
103 | 
104 | 
105 | if __name__ == "__main__":
106 |     result = generate_llms_txt_for_dspy()
107 |     with open("llms.txt", "w") as f:
108 |         f.write(result.llms_txt_content)
109 |     print("Generated llms.txt file!")
110 |     print("\nPreview:")
111 |     print(result.llms_txt_content[:500] + "...")
```

interactive_generate_llms_py_dynamic_names_owner_repo_dirs.py
```
1 | # interactive_generate_llms.py — prompt user for a valid GitHub URL
2 | # Timestamp comments are optional and added only if --stamp is passed.
3 | 
4 | import argparse
5 | import os
6 | import re
7 | import subprocess
8 | from datetime import datetime, timezone
9 | 
10 | import dspy
11 | from dotenv import load_dotenv
12 | from repository_analyzer import RepositoryAnalyzer
13 | from repo_helpers import gather_repository_info
14 | 
15 | load_dotenv()
16 | 
17 | HTTPS_RE = re.compile(
18 |     r"^https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/.*)?$", re.IGNORECASE
19 | )
20 | SSH_RE = re.compile(r"^git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$", re.IGNORECASE)
21 | MODEL_NAME = "hf.co/Mungert/osmosis-mcp-4b-GGUF:Q4_K_M"
22 | 
23 | 
24 | def normalize_repo_url(url: str) -> str:
25 |     """Accept common GitHub URL forms and normalize to https form.
26 |     Valid examples:
27 |       - https://github.com/owner/repo
28 |       - https://github.com/owner/repo.git
29 |       - git@github.com:owner/repo.git
30 |     Returns: https://github.com/<owner>/<repo>
31 |     Raises: ValueError if not a recognizable GitHub URL.
32 |     """
33 |     if not url or not isinstance(url, str):
34 |         raise ValueError("URL cannot be empty.")
35 |     url = url.strip()
36 |     m = HTTPS_RE.match(url)
37 |     if m:
38 |         owner, repo = m.group(1), m.group(2)
39 |         return f"https://github.com/{owner}/{repo}"
40 |     m = SSH_RE.match(url)
41 |     if m:
42 |         owner, repo = m.group(1), m.group(2)
43 |         return f"https://github.com/{owner}/{repo}"
44 |     raise ValueError(
45 |         "Invalid GitHub URL. Expected https://github.com/<owner>/<repo> "
46 |         "or git@github.com:owner/repo.git"
47 |     )
48 | 
49 | 
50 | def split_owner_repo(normalized_https_url: str) -> tuple[str, str]:
51 |     m = HTTPS_RE.match(normalized_https_url)
52 |     if not m:
53 |         raise ValueError("Unexpected URL format after normalization.")
54 |     return m.group(1), m.group(2)
55 | 
56 | 
57 | def prompt_for_repo_url() -> str:
58 |     while True:
59 |         try:
60 |             raw = input(
61 |                 "Enter GitHub repo URL (e.g., https://github.com/<owner>/<repo>): "
62 |             ).strip()
63 |             normalized = normalize_repo_url(raw)
64 |             return normalized
65 |         except ValueError as e:
66 |             print(f"\n{e}\nPlease try again.\n")
67 |         except KeyboardInterrupt:
68 |             print("\nCanceled by user.")
69 |             raise SystemExit(1) from None
70 | 
71 | 
72 | def generate_llms_txt_for_dspy(repo_url: str):
73 |     # Correct Ollama LM initialization
74 |     lm = dspy.LM(
75 |         f"ollama_chat/{MODEL_NAME}",
76 |         api_base="http://localhost:11434",
77 |         api_key="",
78 |         streaming=False,
79 |         cache=False,
80 |     )
81 |     dspy.configure(lm=lm)
82 | 
83 |     file_tree, readme_content, package_files = gather_repository_info(repo_url)
84 |     from repository_analyzer import (
85 |         # Local import so script still works without analyzer until used
86 |         RepositoryAnalyzer,
87 |     )
88 | 
89 |     analyzer = RepositoryAnalyzer()
90 |     result = analyzer(
91 |         repo_url=repo_url,
92 |         file_tree=file_tree,
93 |         readme_content=readme_content,
94 |         package_files=package_files,
95 |     )
96 |     return result
97 | 
98 | 
99 | def stop_ollama_model(model_name: str) -> None:
100 |     """Stop the specified Ollama model to free server resources."""
101 |     try:
102 |         subprocess.run(
103 |             ["ollama", "stop", model_name],
104 |             check=True,
105 |             capture_output=True,
106 |         )
107 |     except subprocess.CalledProcessError as exc:  # pragma: no cover - log warning only
108 |         print(f"Warning: Failed to stop model {model_name}: {exc}")
109 | 
110 | 
111 | def ensure_dir(path: str) -> None:
112 |     os.makedirs(path, exist_ok=True)
113 | 
114 | 
115 | def timestamp_comment(prefix: str = "# Generated", tzname: str | None = None) -> str:
116 |     # Use UTC by default to avoid local ambiguity. User requested comment only.
117 |     now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
118 |     tz_note = f" ({tzname})" if tzname else ""
119 |     return f"{prefix}: {now} UTC{tz_note}"
120 | 
121 | 
122 | def write_text(path: str, content: str, add_stamp: bool) -> None:
123 |     if add_stamp:
124 |         content = content.rstrip() + "\n\n" + timestamp_comment()
125 |     with open(path, "w", encoding="utf-8") as f:
126 |         f.write(content)
127 | 
128 | 
129 | if __name__ == "__main__":
130 |     parser = argparse.ArgumentParser(
131 |         description=(
132 |             "Generate llms.txt for a GitHub repo with organized owner/repo output"
133 |         )
134 |     )
135 |     parser.add_argument(
136 |         "--repo", help="GitHub repo URL (https://github.com/<owner>/<repo>)"
137 |     )
138 |     parser.add_argument(
139 |         "--outdir",
140 |         default="artifacts",
141 |         help="Base directory to save outputs (default: ./artifacts)",
142 |     )
143 |     parser.add_argument(
144 |         "--stamp",
145 |         action="store_true",
146 |         help="Append a timestamp as a trailing comment in each text file",
147 |     )
148 |     args = parser.parse_args()
149 | 
150 |     repo_url = None
151 |     if args.repo:
152 |         try:
153 |             repo_url = normalize_repo_url(args.repo)
154 |         except ValueError as e:
155 |             print(f"{e}\nFalling back to interactive prompt...\n")
156 | 
157 |     if not repo_url:
158 |         repo_url = prompt_for_repo_url()
159 | 
160 |     owner, repo = split_owner_repo(repo_url)
161 | 
162 |     # Output directory: <outdir>/<owner>/<repo>
163 |     repo_root = os.path.join(args.outdir, owner, repo)
164 |     ensure_dir(repo_root)
165 | 
166 |     # Base names derived from repo for clarity; filenames avoid timestamps
167 |     base = repo.lower()
168 |     llms_path = os.path.join(repo_root, f"{base}-llms.txt")
169 | 
170 |     # Run analysis
171 |     result = generate_llms_txt_for_dspy(repo_url=repo_url)
172 | 
173 |     # Keep a pristine in-memory copy for parsers (avoid stamping issues)
174 |     txt = result.llms_txt_content
175 | 
176 |     # Write llms.txt-like artifact
177 |     write_text(llms_path, result.llms_txt_content, add_stamp=args.stamp)
178 | 
179 |     # Prefer the canonical API, but fall back if needed
180 |     try:
181 |         from llms_txt import create_ctx
182 |     except ImportError:
183 |         from llm_ctx.core import create_ctx
184 |     # Create contexts from the pristine in-memory text (no stamp inside parser input)
185 | 
186 |     ctx = create_ctx(txt, optional=False)
187 |     ctx_full = create_ctx(txt, optional=True)
188 | 
189 |     ctx_path = os.path.join(repo_root, f"{base}-llms-ctx.txt")
190 |     ctx_full_path = os.path.join(repo_root, f"{base}-llms-ctx-full.txt")
191 | 
192 |     write_text(ctx_path, ctx, add_stamp=args.stamp)
193 |     write_text(ctx_full_path, ctx_full, add_stamp=args.stamp)
194 | 
195 |     print("Artifacts written:")
196 |     print(f" - {llms_path}")
197 |     print(f" - {ctx_path}")
198 |     print(f" - {ctx_full_path}")
199 | 
200 |     # Show preview
201 |     preview = (result.llms_txt_content or "").strip()
202 |     head = preview[:500] + ("..." if len(preview) > 500 else "")
203 |     print("\nPreview of llms content:\n")
204 |     print(head)
205 | 
206 |     stop_ollama_model(MODEL_NAME)
```

repo_helpers.py
```
1 | # repo_helpers.py
2 | 
3 | import requests
4 | from dotenv import load_dotenv
5 | import os
6 | 
7 | # os.environ["GITHUB_ACCESS_TOKEN"] = "<your_access_token>"
8 | # Load variables from .env file into environment
9 | load_dotenv()
10 | 
11 | def get_github_file_tree(repo_url):
12 |     token = os.getenv("GITHUB_ACCESS_TOKEN")
13 |     """Get repository file structure from GitHub API."""
14 |     parts = repo_url.rstrip("/").split("/")
15 |     owner, repo = parts[-2], parts[-1]
16 | 
17 |     api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
18 |     response = requests.get(
19 |         api_url,
20 |         headers={"Authorization": f"Bearer {token}"},
21 |     )
22 | 
23 |     if response.status_code == 200:
24 |         tree_data = response.json()
25 |         file_paths = [
26 |             item["path"] for item in tree_data["tree"] if item["type"] == "blob"
27 |         ]
28 |         return "\n".join(sorted(file_paths))
29 |     else:
30 |         raise Exception(f"Failed to fetch repository tree: {response.status_code}")
31 | 
32 | 
33 | def get_github_file_content(repo_url, file_path):
34 |     """Get specific file content from GitHub."""
35 |     token = os.getenv("GITHUB_ACCESS_TOKEN")
36 |     parts = repo_url.rstrip("/").split("/")
37 |     owner, repo = parts[-2], parts[-1]
38 | 
39 |     api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
40 |     response = requests.get(
41 |         api_url,
42 |         headers={"Authorization": f"Bearer {token}"},
43 |     )
44 | 
45 |     if response.status_code == 200:
46 |         import base64
47 | 
48 |         content = base64.b64decode(response.json()["content"]).decode("utf-8")
49 |         return content
50 |     else:
51 |         return f"Could not fetch {file_path}"
52 | 
53 | 
54 | def gather_repository_info(repo_url):
55 |     """Gather all necessary repository information."""
56 |     file_tree = get_github_file_tree(repo_url)
57 |     readme_content = get_github_file_content(repo_url, "README.md")
58 | 
59 |     package_files = []
60 |     for file_path in ["pyproject.toml", "setup.py", "requirements.txt", "package.json"]:
61 |         try:
62 |             content = get_github_file_content(repo_url, file_path)
63 |             if "Could not fetch" not in content:
64 |                 package_files.append(f"=== {file_path} ===\n{content}")
65 |         except:
66 |             continue
67 | 
68 |     package_files_content = "\n\n".join(package_files)
69 | 
70 |     return file_tree, readme_content, package_files_content
71 | 
72 | 
73 | # --- helpers for raw GitHub URLs ---
74 | 
75 | def owner_repo_from_url(repo_url: str):
76 |     """Extract (owner, repo) from https or SSH GitHub URLs."""
77 |     repo_url = repo_url.strip()
78 |     if repo_url.startswith("git@github.com:"):
79 |         rest = repo_url.split("git@github.com:", 1)[1]
80 |         owner, repo = rest.split("/", 1)
81 |         repo = repo.replace(".git", "").strip("/")
82 |         return owner, repo
83 |     if repo_url.startswith(("https://", "http://")):
84 |         from urllib.parse import urlparse
85 |         p = urlparse(repo_url)
86 |         parts = [x for x in p.path.strip("/").split("/") if x]
87 |         if len(parts) >= 2:
88 |             owner, repo = parts[0], parts[1].replace(".git", "")
89 |             return owner, repo
90 |     raise ValueError("Unrecognized GitHub URL")
91 | 
92 | def construct_raw_url(repo_url: str, path: str) -> str:
93 |     """Build a raw.githubusercontent.com URL for a file on the repo’s default branch."""
94 |     owner, repo = owner_repo_from_url(repo_url)
95 |     # Uses your existing get_default_branch(repo_url); falls back to 'main' if missing
96 |     ref = get_default_branch(repo_url) if "get_default_branch" in globals() else "main"
97 |     return f"https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}"
```

repository_analyzer.py
```
1 | # repository_analyzer.py — deterministic llms.txt builder (ctx-compatible)
2 | import re
3 | import dspy
4 | from signatures import (
5 |     AnalyzeRepository,
6 |     AnalyzeCodeStructure,
7 |     GenerateUsageExamples,
8 |     GenerateLLMsTxt,
9 | )
10 | from typing import List, Tuple
11 | 
12 | 
13 | def _nicify_title(name: str) -> str:
14 |     base = name.rsplit("/", 1)[-1]
15 |     base = re.sub(r"\.(md|rst|txt|py|ipynb|js|ts)$", "", base, flags=re.I)
16 |     base = base.replace("-", " ").replace("_", " ")
17 |     return base.strip().title() or name
18 | 
19 | 
20 | def _select_paths(file_tree: str, patterns: List[str]) -> List[str]:
21 |     paths = [p.strip() for p in file_tree.splitlines() if p.strip()]
22 |     out = []
23 |     for p in paths:
24 |         for pat in patterns:
25 |             if re.search(pat, p, flags=re.I):
26 |                 out.append(p)
27 |                 break
28 |     # de-dup preserving order
29 |     seen = set(); uniq = []
30 |     for p in out:
31 |         if p not in seen:
32 |             uniq.append(p); seen.add(p)
33 |     return uniq
34 | 
35 | 
36 | def _build_links(repo_url: str, file_tree: str) -> Tuple[List[Tuple[str, str, str]], List[Tuple[str, str, str]], List[Tuple[str, str, str]]]:
37 |     from repo_helpers import construct_raw_url
38 | 
39 |     # Priority picks
40 |     readme_first = _select_paths(file_tree, [r"(^|/)README\.md$"])
41 |     docs_md = _select_paths(file_tree, [r"(^|/)(docs?|documentation)/.*\.md$"])
42 |     root_md = _select_paths(file_tree, [r"^[^/]+\.md$"])
43 | 
44 |     examples = _select_paths(file_tree, [
45 |         r"(^|/)(examples?|demos?|tutorials?)/.*\.(md|py|ipynb|js|ts)$"
46 |     ])
47 | 
48 |     optional = _select_paths(file_tree, [
49 |         r"(^|/)CONTRIBUTING\.md$",
50 |         r"(^|/)CHANGELOG\.md$",
51 |         r"(^|/)HISTORY\.md$",
52 |         r"(^|/)BENCHMARKS?\.md$",
53 |         r"(^|/)LICENSE(\.|$)",
54 |         r"(^|/)SECURITY\.md$",
55 |     ])
56 | 
57 |     # Build at most N links for each section
58 |     def to_links(paths, note_hint):
59 |         links = []
60 |         for p in paths:
61 |             url = construct_raw_url(repo_url, p)
62 |             title = "README" if re.search(r"(^|/)README\.md$", p, flags=re.I) else _nicify_title(p)
63 |             note = note_hint(p)
64 |             links.append((title, url, note))
65 |         return links
66 | 
67 |     docs_links = []
68 |     docs_links += to_links(readme_first[:1], lambda p: "overview and usage.")
69 |     # Prefer a handful of docs pages
70 |     docs_links += to_links(docs_md[:6], lambda p: "docs page.")
71 |     # Then a couple of root .mds (skipping README which we already added)
72 |     root_md_filtered = [p for p in root_md if not re.search(r"(^|/)README\.md$", p, flags=re.I)]
73 |     docs_links += to_links(root_md_filtered[:4], lambda p: "reference page.")
74 |     docs_links = docs_links[:8]
75 | 
76 |     example_links = to_links(examples[:6], lambda p: "worked example.")
77 | 
78 |     optional_links = to_links(optional[:8], lambda p: "optional reading.")
79 | 
80 |     # If nothing found at all, at least link README (raw) as Docs
81 |     if not docs_links and readme_first:
82 |         p = readme_first[0]
83 |         url = construct_raw_url(repo_url, p)
84 |         docs_links.append(("README", url, "overview and usage."))
85 | 
86 |     return docs_links, example_links, optional_links
87 | 
88 | 
89 | def _render_llms_markdown(project_name: str, project_purpose: str, remember_bullets: List[str], docs_links, example_links, optional_links) -> str:
90 |     # constrain remember bullets 3–6 items
91 |     rb = [str(b).strip().rstrip(".") for b in remember_bullets if str(b).strip()]
92 |     rb = rb[:6] or ["Key concepts and usage patterns", "Common pitfalls and best practices", "Consult Docs and Examples links below"]
93 |     if len(rb) < 3:
94 |         rb += ["Follow the docs for setup", "Use examples as starting points"][: 3 - len(rb)]
95 | 
96 |     def fmt_links(links):
97 |         return "\n".join([f"- [{title}]({url}): {note}" for (title, url, note) in links]) or "- [README](https://example.com): overview."
98 | 
99 |     md = f"""# {project_name}
100 | 
101 | > {project_purpose.strip().replace('\n', ' ')}
102 | 
103 | **Remember:**
104 | """ + "\n".join([f"- {b}" for b in rb]) + """
105 | 
106 | ## Docs
107 | """ + fmt_links(docs_links) + """
108 | 
109 | ## Examples
110 | """ + fmt_links(example_links) + """
111 | 
112 | ## Optional
113 | """ + fmt_links(optional_links) + "\n"
114 | 
115 |     return md
116 | 
117 | 
118 | class RepositoryAnalyzer(dspy.Module):
119 |     def __init__(self, final_lm=None):
120 |         super().__init__()
121 |         self.analyze_repo = dspy.ChainOfThought(AnalyzeRepository)
122 |         self.analyze_structure = dspy.ChainOfThought(AnalyzeCodeStructure)
123 |         self.generate_examples = dspy.ChainOfThought(GenerateUsageExamples)
124 |         self.generate_llms_txt = dspy.ChainOfThought(GenerateLLMsTxt)  # kept for compatibility if needed
125 |         self.final_lm = final_lm  # set to a plain-text LM
126 | 
127 |     def forward(self, repo_url, file_tree, readme_content, package_files):
128 |         repo_analysis = self.analyze_repo(
129 |             repo_url=repo_url,
130 |             file_tree=file_tree,
131 |             readme_content=readme_content,
132 |         )
133 |         structure_analysis = self.analyze_structure(
134 |             file_tree=file_tree,
135 |             package_files=package_files,
136 |         )
137 |         usage_examples = self.generate_examples(
138 |             repo_info=(
139 |                 f"Purpose: {repo_analysis.project_purpose}\n\n"
140 |                 f"Concepts: {', '.join(repo_analysis.key_concepts or [])}\n\n"
141 |                 f"Entry points: {', '.join(structure_analysis.entry_points or [])}\n"
142 |             )
143 |         )
144 | 
145 |         # Derive a friendly project name
146 |         try:
147 |             from repo_helpers import owner_repo_from_url
148 |             owner, repo = owner_repo_from_url(repo_url)
149 |             project_name = repo.replace('-', ' ').replace('_', ' ').title()
150 |         except Exception:
151 |             project_name = "Project"
152 | 
153 |         docs_links, example_links, optional_links = _build_links(repo_url, file_tree)
154 | 
155 |         llms_txt_content = _render_llms_markdown(
156 |             project_name=project_name,
157 |             project_purpose=repo_analysis.project_purpose or "Project overview unavailable.",
158 |             remember_bullets=repo_analysis.key_concepts or [],
159 |             docs_links=docs_links,
160 |             example_links=example_links,
161 |             optional_links=optional_links,
162 |         )
163 | 
164 |         return dspy.Prediction(
165 |             llms_txt_content=llms_txt_content,
166 |             analysis=repo_analysis,
167 |             structure=structure_analysis,
168 |         )
```

signatures.py
```
1 | # signatures.py
2 | import dspy
3 | from typing import List
4 | 
5 | 
6 | class AnalyzeRepository(dspy.Signature):
7 |     """Analyze a repository and summarize its purpose and concepts."""
8 | 
9 |     repo_url: str = dspy.InputField(desc="GitHub repository URL")
10 |     file_tree: str = dspy.InputField(
11 |         desc="Repository file structure (one path per line)"
12 |     )
13 |     readme_content: str = dspy.InputField(desc="README.md content (raw)")
14 | 
15 |     project_purpose: str = dspy.OutputField(
16 |         desc="Main purpose and goals of the project (2–4 sentences)"
17 |     )
18 |     key_concepts: List[str] = dspy.OutputField(
19 |         desc="Important concepts and terminology (bullet list items)"
20 |     )
21 |     architecture_overview: str = dspy.OutputField(
22 |         desc="High-level architecture overview (1–2 paragraphs)"
23 |     )
24 | 
25 | 
26 | class AnalyzeCodeStructure(dspy.Signature):
27 |     """Identify important directories, entry points, and dev info."""
28 | 
29 |     file_tree: str = dspy.InputField()
30 |     package_files: str = dspy.InputField(
31 |         desc="Concatenated contents of pyproject/setup/requirements or package.json, etc."
32 |     )
33 | 
34 |     important_directories: List[str] = dspy.OutputField(
35 |         desc="Key directories with brief notes (e.g., src/, docs/, examples/)"
36 |     )
37 |     entry_points: List[str] = dspy.OutputField(
38 |         desc="Likely entry points or commands (e.g., cli.py, main.ts, npm scripts)"
39 |     )
40 |     development_info: str = dspy.OutputField(
41 |         desc="Development or build info (deps, scripts, tooling)"
42 |     )
43 | 
44 | 
45 | class GenerateUsageExamples(dspy.Signature):
46 |     """Produce a short section of common usage examples based on the repo analysis."""
47 | 
48 |     repo_info: str = dspy.InputField(
49 |         desc="Summary of the project's purpose and key concepts"
50 |     )
51 |     usage_examples: str = dspy.OutputField(
52 |         desc="Markdown examples (code fences) showing typical usage"
53 |     )
54 | 
55 | 
56 | class GenerateLLMsTxt(dspy.Signature):
57 |     """Generate a complete llms.txt (markdown index) for the project."""
58 | 
59 |     project_purpose: str = dspy.InputField()
60 |     key_concepts: List[str] = dspy.InputField()
61 |     architecture_overview: str = dspy.InputField()
62 |     important_directories: List[str] = dspy.InputField()
63 |     entry_points: List[str] = dspy.InputField()
64 |     development_info: str = dspy.InputField()
65 |     usage_examples: str = dspy.InputField(
66 |         desc="Common usage patterns and examples (markdown)"
67 |     )
68 | 
69 |     llms_txt_content: str = dspy.OutputField(
70 |         desc="Complete llms.txt content following the standard format"
71 |     )
```
