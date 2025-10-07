Project Structure:
├── codeGeneration_for_unfamilar_libraries
│   ├── README.md
│   ├── __pycache__
│   │   ├── main.cpython-312.pyc
│   │   └── repo_helpers.cpython-312.pyc
│   ├── generate_examples.py
│   ├── interactive_learning.py
│   ├── learn_library.py
│   ├── main.py
│   └── repo_helpers.py
├── ollama-llm_config
│   ├── README.md
│   ├── __pycache__
│   │   ├── main.cpython-312.pyc
│   │   └── repo_helpers.cpython-312.pyc
│   ├── generate_examples.py
│   ├── interactive_learning.py
│   ├── learn_library.py
│   ├── litellm_learning.json
│   ├── main.py
│   ├── repo_helpers.py
│   └── vllm_learning.json
└── vllm-llm_config
    ├── README.md
    ├── __pycache__
    │   ├── main.cpython-312.pyc
    │   └── repo_helpers.cpython-312.pyc
    ├── generate_examples.py
    ├── interactive_learning.py
    ├── learn_library.py
    ├── litellm_learning.json
    ├── main.py
    └── repo_helpers.py


codeGeneration_for_unfamilar_libraries/generate_examples.py
```
1 | # generate_examples.py
2 | # Purpose: Generate code examples for any learned library
3 | 
4 | from learn_library import fastapi_info, streamlit_info, agent
5 | 
6 | 
7 | def generate_examples_for_library(library_info: dict, library_name: str):
8 |     """Generate code examples for any library based on its documentation."""
9 | 
10 |     # Define generic use cases that can apply to most libraries
11 |     use_cases = [
12 |         {
13 |             "name": "Basic Setup and Hello World",
14 |             "description": f"Create a minimal working example with {library_name}",
15 |             "requirements": "Include installation, imports, and basic usage",
16 |         },
17 |         {
18 |             "name": "Common Operations",
19 |             "description": f"Demonstrate the most common {library_name} operations",
20 |             "requirements": "Show typical workflow and best practices",
21 |         },
22 |         {
23 |             "name": "Advanced Usage",
24 |             "description": f"Create a more complex example showcasing {library_name} capabilities",
25 |             "requirements": "Include error handling and optimization",
26 |         },
27 |     ]
28 | 
29 |     generated_examples = []
30 | 
31 |     print(f"\n🔧 Generating examples for {library_name}...")
32 | 
33 |     for use_case in use_cases:
34 |         print(f"\n📝 {use_case['name']}")
35 |         print(f"Description: {use_case['description']}")
36 | 
37 |         example = agent.generate_example(
38 |             library_info=library_info,
39 |             use_case=use_case["description"],
40 |             requirements=use_case["requirements"],
41 |         )
42 | 
43 |         print("\n💻 Generated Code:")
44 |         print("```python")
45 |         print(example["code"])
46 |         print("```")
47 | 
48 |         print("\n📦 Required Imports:")
49 |         for imp in example["imports"]:
50 |             print(f"  • {imp}")
51 | 
52 |         print("\n📝 Explanation:")
53 |         print(example["explanation"])
54 | 
55 |         print("\n✅ Best Practices:")
56 |         for practice in example["best_practices"]:
57 |             print(f"  • {practice}")
58 | 
59 |         generated_examples.append(
60 |             {
61 |                 "use_case": use_case["name"],
62 |                 "code": example["code"],
63 |                 "imports": example["imports"],
64 |                 "explanation": example["explanation"],
65 |                 "best_practices": example["best_practices"],
66 |             }
67 |         )
68 | 
69 |         print("-" * 80)
70 | 
71 |     return generated_examples
72 | 
73 | 
74 | # Generate examples for both libraries
75 | print("🎯 Generating FastAPI Examples:")
76 | fastapi_examples = generate_examples_for_library(fastapi_info, "FastAPI")
77 | 
78 | print("\n\n🎯 Generating Streamlit Examples:")
79 | streamlit_examples = generate_examples_for_library(streamlit_info, "Streamlit")
```

codeGeneration_for_unfamilar_libraries/interactive_learning.py
```
1 | # interactive_learning.py
2 | # Purpose: Run a full interactive session for learning any Python library from docs
3 | 
4 | from main import agent
5 | from typing import Dict
6 | 
7 | 
8 | def learn_any_library(
9 |     library_name: str, documentation_urls: list[str], use_cases: list[str] = None
10 | ):
11 |     """Learn any library from its documentation and generate examples."""
12 | 
13 |     if use_cases is None:
14 |         use_cases = [
15 |             "Basic setup and hello world example",
16 |             "Common operations and workflows",
17 |             "Advanced usage with best practices",
18 |         ]
19 | 
20 |     print(f"🚀 Starting automated learning for {library_name}...")
21 |     print(f"Documentation sources: {len(documentation_urls)} URLs")
22 | 
23 |     try:
24 |         # Step 1: Learn from documentation
25 |         library_info = agent.learn_from_urls(library_name, documentation_urls)
26 | 
27 |         # Step 2: Generate examples for each use case
28 |         all_examples = []
29 | 
30 |         for i, use_case in enumerate(use_cases, 1):
31 |             print(f"\n📝 Generating example {i}/{len(use_cases)}: {use_case}")
32 | 
33 |             example = agent.generate_example(
34 |                 library_info=library_info,
35 |                 use_case=use_case,
36 |                 requirements="Include error handling, comments, and follow best practices",
37 |             )
38 | 
39 |             all_examples.append(
40 |                 {
41 |                     "use_case": use_case,
42 |                     "code": example["code"],
43 |                     "imports": example["imports"],
44 |                     "explanation": example["explanation"],
45 |                     "best_practices": example["best_practices"],
46 |                 }
47 |             )
48 | 
49 |         return {"library_info": library_info, "examples": all_examples}
50 | 
51 |     except Exception as e:
52 |         print(f"❌ Error learning {library_name}: {e}")
53 |         return None
54 | 
55 | 
56 | def interactive_learning_session():
57 |     """Interactive session for learning libraries with user input."""
58 | 
59 |     print("🎯 Welcome to the Interactive Library Learning System!")
60 |     print(
61 |         "This system will help you learn any Python library from its documentation.\n"
62 |     )
63 | 
64 |     learned_libraries = {}
65 | 
66 |     while True:
67 |         print("\n" + "=" * 60)
68 |         print("🚀 LIBRARY LEARNING SESSION")
69 |         print("=" * 60)
70 | 
71 |         # Get library name from user
72 |         library_name = input(
73 |             "\n📚 Enter the library name you want to learn (or 'quit' to exit): "
74 |         ).strip()
75 | 
76 |         if library_name.lower() in ["quit", "exit", "q"]:
77 |             print("\n👋 Thanks for using the Interactive Library Learning System!")
78 |             break
79 | 
80 |         if not library_name:
81 |             print("❌ Please enter a valid library name.")
82 |             continue
83 | 
84 |         # Get documentation URLs
85 |         print(
86 |             f"\n🔗 Enter documentation URLs for {library_name} (one per line, empty line to finish):"
87 |         )
88 |         urls = []
89 |         while True:
90 |             url = input("  URL: ").strip()
91 |             if not url:
92 |                 break
93 |             if not url.startswith(("http://", "https://")):
94 |                 print(
95 |                     "    ⚠️  Please enter a valid URL starting with http:// or https://"
96 |                 )
97 |                 continue
98 |             urls.append(url)
99 | 
100 |         if not urls:
101 |             print("❌ No valid URLs provided. Skipping this library.")
102 |             continue
103 | 
104 |         # Get custom use cases from user
105 |         print(
106 |             f"\n🎯 Define use cases for {library_name} (optional, press Enter for defaults):"
107 |         )
108 |         print(
109 |             "   Default use cases will be: Basic setup, Common operations, Advanced usage"
110 |         )
111 | 
112 |         user_wants_custom = (
113 |             input("   Do you want to define custom use cases? (y/n): ").strip().lower()
114 |         )
115 | 
116 |         use_cases = None
117 |         if user_wants_custom in ["y", "yes"]:
118 |             print("   Enter your use cases (one per line, empty line to finish):")
119 |             use_cases = []
120 |             while True:
121 |                 use_case = input("     Use case: ").strip()
122 |                 if not use_case:
123 |                     break
124 |                 use_cases.append(use_case)
125 | 
126 |             if not use_cases:
127 |                 print("   No custom use cases provided, using defaults.")
128 |                 use_cases = None
129 | 
130 |         # Learn the library
131 |         print(f"\n🚀 Starting learning process for {library_name}...")
132 |         result = learn_any_library(library_name, urls, use_cases)
133 | 
134 |         if result:
135 |             learned_libraries[library_name] = result
136 |             print(f"\n✅ Successfully learned {library_name}!")
137 | 
138 |             # Show summary
139 |             print(f"\n📊 Learning Summary for {library_name}:")
140 |             print(
141 |                 f"   • Core concepts: {len(result['library_info']['core_concepts'])} identified"
142 |             )
143 |             print(
144 |                 f"   • Common patterns: {len(result['library_info']['patterns'])} found"
145 |             )
146 |             print(f"   • Examples generated: {len(result['examples'])}")
147 | 
148 |             # Ask if user wants to see examples
149 |             show_examples = (
150 |                 input(
151 |                     f"\n👀 Do you want to see the generated examples for {library_name}? (y/n): "
152 |                 )
153 |                 .strip()
154 |                 .lower()
155 |             )
156 | 
157 |             if show_examples in ["y", "yes"]:
158 |                 for i, example in enumerate(result["examples"], 1):
159 |                     print(f"\n{'─' * 50}")
160 |                     print(f"📝 Example {i}: {example['use_case']}")
161 |                     print(f"{'─' * 50}")
162 | 
163 |                     print("\n💻 Generated Code:")
164 |                     print("```python")
165 |                     print(example["code"])
166 |                     print("```")
167 | 
168 |                     print(f"\n📦 Required Imports:")
169 |                     for imp in example["imports"]:
170 |                         print(f"  • {imp}")
171 | 
172 |                     print(f"\n📝 Explanation:")
173 |                     print(example["explanation"])
174 | 
175 |                     print(f"\n✅ Best Practices:")
176 |                     for practice in example["best_practices"]:
177 |                         print(f"  • {practice}")
178 | 
179 |                     # Ask if user wants to see the next example
180 |                     if i < len(result["examples"]):
181 |                         continue_viewing = (
182 |                             input(f"\nContinue to next example? (y/n): ")
183 |                             .strip()
184 |                             .lower()
185 |                         )
186 |                         if continue_viewing not in ["y", "yes"]:
187 |                             break
188 | 
189 |             # Offer to save results
190 |             save_results = (
191 |                 input(f"\n💾 Save learning results for {library_name} to file? (y/n): ")
192 |                 .strip()
193 |                 .lower()
194 |             )
195 | 
196 |             if save_results in ["y", "yes"]:
197 |                 filename = input(
198 |                     f"   Enter filename (default: {library_name.lower()}_learning.json): "
199 |                 ).strip()
200 |                 if not filename:
201 |                     filename = f"{library_name.lower()}_learning.json"
202 | 
203 |                 try:
204 |                     import json
205 | 
206 |                     with open(filename, "w") as f:
207 |                         json.dump(result, f, indent=2, default=str)
208 |                     print(f"   ✅ Results saved to {filename}")
209 |                 except Exception as e:
210 |                     print(f"   ❌ Error saving file: {e}")
211 | 
212 |         else:
213 |             print(f"❌ Failed to learn {library_name}")
214 | 
215 |         # Ask if user wants to learn another library
216 |         print(f"\n📚 Libraries learned so far: {list(learned_libraries.keys())}")
217 |         continue_learning = (
218 |             input("\n🔄 Do you want to learn another library? (y/n): ").strip().lower()
219 |         )
220 | 
221 |         if continue_learning not in ["y", "yes"]:
222 |             break
223 | 
224 |     # Final summary
225 |     if learned_libraries:
226 |         print(f"\n🎉 Session Summary:")
227 |         print(f"Successfully learned {len(learned_libraries)} libraries:")
228 |         for lib_name, info in learned_libraries.items():
229 |             print(f"  • {lib_name}: {len(info['examples'])} examples generated")
230 | 
231 |     return learned_libraries
232 | 
233 | 
234 | # Example: Run interactive learning session
235 | if __name__ == "__main__":
236 |     # Run interactive session
237 |     learned_libraries = interactive_learning_session()
```

codeGeneration_for_unfamilar_libraries/learn_library.py
```
1 | # learn_library.py
2 | # Purpose: Utility to learn any library from a set of documentation URLs using the agent
3 | 
4 | from main import agent  # Import the previously defined agent
5 | from typing import Dict
6 | 
7 | 
8 | def learn_library_from_urls(library_name: str, documentation_urls: list[str]) -> Dict:
9 |     """Learn about any library from its documentation URLs."""
10 | 
11 |     try:
12 |         library_info = agent.learn_from_urls(library_name, documentation_urls)
13 | 
14 |         print(f"\n🔍 Library Analysis Results for {library_name}:")
15 |         print(f"Sources: {len(library_info['source_urls'])} successful fetches")
16 |         print(f"Core Concepts: {library_info['core_concepts']}")
17 |         print(f"Common Patterns: {library_info['patterns']}")
18 |         print(f"Key Methods: {library_info['methods']}")
19 |         print(f"Installation: {library_info['installation']}")
20 |         print(f"Found {len(library_info['examples'])} code examples")
21 | 
22 |         return library_info
23 | 
24 |     except Exception as e:
25 |         print(f"❌ Error learning library: {e}")
26 |         raise
27 | 
28 | 
29 | # Example 1: Learn FastAPI from official documentation
30 | fastapi_urls = [
31 |     "https://fastapi.tiangolo.com/",
32 |     "https://fastapi.tiangolo.com/tutorial/first-steps/",
33 |     "https://fastapi.tiangolo.com/tutorial/path-params/",
34 |     "https://fastapi.tiangolo.com/tutorial/query-params/",
35 | ]
36 | 
37 | print("🚀 Learning FastAPI from official documentation...")
38 | fastapi_info = learn_library_from_urls("FastAPI", fastapi_urls)
39 | 
40 | # Example 2: Learn a different library (you can replace with any library)
41 | streamlit_urls = [
42 |     "https://docs.streamlit.io/",
43 |     "https://docs.streamlit.io/get-started",
44 |     "https://docs.streamlit.io/develop/api-reference",
45 | ]
46 | 
47 | print("\n\n📊 Learning Streamlit from official documentation...")
48 | streamlit_info = learn_library_from_urls("Streamlit", streamlit_urls)
```

codeGeneration_for_unfamilar_libraries/main.py
```
1 | # main.py
2 | # Purpose: Automated documentation-powered code generation pipeline using DSPy.
3 | # Now with integrated GitHub repository analysis.
4 | 
5 | import dspy
6 | import requests
7 | from bs4 import BeautifulSoup
8 | import html2text
9 | from typing import List, Dict, Any
10 | import json
11 | import time
12 | 
13 | # Import the GitHub helper functions
14 | from repo_helpers import gather_repository_info
15 | 
16 | # --- DSPy Configuration ---
17 | # Replace with your actual LM provider if not using a local one
18 |     # For models like Llama
19 | lm = dspy.LM(
20 |         "ollama_chat/hf.co/Mungert/osmosis-mcp-4b-GGUF:Q4_K_M",
21 |         api_base="http://localhost:11434",  # Local Ollama server URL
22 |         api_key="EMPTY",  # Usually empty for local Ollama; remove if you do not have a key
23 |         streaming=False,
24 |         response_format={
25 |             "type": "json_schema",
26 |             "json_schema": {
27 |                 "schema": {
28 |                     "type": "object",
29 |                     "properties": {
30 |                         "project": {
31 |                             "type": "object",
32 |                             "properties": {
33 |                                 "name": {"type": "string"},
34 |                                 "description": {"type": "string"},
35 |                             },
36 |                             "required": ["name", "description"],
37 |                         },
38 |                         "key_concepts": {
39 |                             "type": "array",
40 |                             "items": {"type": "string"},
41 |                             "minItems": 1,
42 |                         },
43 |                         "architecture_overview": {"type": "string"},
44 |                         "important_directories": {
45 |                             "type": "array",
46 |                             "items": {"type": "string"},
47 |                             "minItems": 1,
48 |                         },
49 |                         "entry_points": {
50 |                             "type": "array",
51 |                             "items": {"type": "string"},
52 |                             "minItems": 1,
53 |                         },
54 |                         "development_info": {
55 |                             "type": "object",
56 |                             "properties": {
57 |                                 "test_dependencies": {
58 |                                     "type": "array",
59 |                                     "items": {"type": "string"},
60 |                                     "minItems": 1,
61 |                                 },
62 |                                 "linting_tools": {
63 |                                     "type": "array",
64 |                                     "items": {"type": "string"},
65 |                                     "minItems": 1,
66 |                                 },
67 |                                 "optional_dependencies": {
68 |                                     "type": "array",
69 |                                     "items": {"type": "string"},
70 |                                 },
71 |                             },
72 |                             "required": ["test_dependencies", "linting_tools"],
73 |                         },
74 |                         "usage_examples": {
75 |                             "type": "array",
76 |                             "items": {"type": "string"},
77 |                             "minItems": 1,
78 |                         },
79 |                     },
80 |                     "required": [
81 |                         "project",
82 |                         "key_concepts",
83 |                         "architecture_overview",
84 |                         "important_directories",
85 |                         "entry_points",
86 |                         "development_info",
87 |                         "usage_examples",
88 |                     ],
89 |                 }
90 |             },
91 |         },
92 |     )
93 | dspy.configure(lm=lm)
94 | 
95 | 
96 | # --- Data Fetching Classes ---
97 | 
98 | 
99 | class DocumentationFetcher:
100 |     """
101 |     Fetches and processes documentation from both standard URLs and GitHub repositories.
102 |     """
103 | 
104 |     def __init__(self, max_retries=3, delay=1):
105 |         self.session = requests.Session()
106 |         self.session.headers.update(
107 |             {
108 |                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
109 |             }
110 |         )
111 |         self.max_retries = max_retries
112 |         self.delay = delay
113 |         self.html_converter = html2text.HTML2Text()
114 |         self.html_converter.ignore_links = False
115 |         self.html_converter.ignore_images = True
116 | 
117 |     def fetch_website_url(self, url: str) -> dict:
118 |         """Fetches and cleans content from a standard website URL."""
119 |         for attempt in range(self.max_retries):
120 |             try:
121 |                 print(f"📡 Fetching Website: {url} (attempt {attempt + 1})")
122 |                 response = self.session.get(url, timeout=15)
123 |                 response.raise_for_status()
124 |                 soup = BeautifulSoup(response.content, "html.parser")
125 |                 for script in soup(["script", "style", "nav", "footer", "header"]):
126 |                     script.decompose()
127 |                 markdown_content = self.html_converter.handle(str(soup))
128 |                 return {
129 |                     "url": url,
130 |                     "title": soup.title.string if soup.title else "No title",
131 |                     "content": markdown_content,
132 |                     "success": True,
133 |                 }
134 |             except Exception as e:
135 |                 print(f"❌ Error fetching {url}: {e}")
136 |                 if attempt < self.max_retries - 1:
137 |                     time.sleep(self.delay)
138 |         return {"url": url, "title": "Failed to fetch", "content": "", "success": False}
139 | 
140 |     def fetch_github_repo(self, url: str) -> dict:
141 |         """Fetches and consolidates content from a GitHub repository."""
142 |         print(f"📦 Fetching GitHub Repo: {url}")
143 |         try:
144 |             # Use the helper function to get README and example files
145 |             combined_content, details = gather_repository_info(url)
146 |             if "Could not access" in combined_content:
147 |                 return {
148 |                     "url": url,
149 |                     "title": "Failed to fetch repo",
150 |                     "content": "",
151 |                     "success": False,
152 |                 }
153 | 
154 |             return {
155 |                 "url": url,
156 |                 "title": f"GitHub Repo: {url.split('/')[-1]}",
157 |                 "content": combined_content,
158 |                 "success": True,
159 |                 "details": details,
160 |             }
161 |         except Exception as e:
162 |             print(f"❌ Error fetching GitHub repo {url}: {e}")
163 |             return {
164 |                 "url": url,
165 |                 "title": "Failed to fetch repo",
166 |                 "content": f"Error: {e}",
167 |                 "success": False,
168 |             }
169 | 
170 |     def fetch_documentation(self, urls: list[str]) -> list[dict]:
171 |         """
172 |         Fetches documentation from a list of URLs, routing to the correct
173 |         fetcher (website or GitHub) based on the URL.
174 |         """
175 |         results = []
176 |         for url in urls:
177 |             if "github.com" in url:
178 |                 result = self.fetch_github_repo(url)
179 |             else:
180 |                 result = self.fetch_website_url(url)
181 | 
182 |             results.append(result)
183 |             time.sleep(self.delay)  # Be respectful to servers
184 |         return results
185 | 
186 | 
187 | # --- DSPy Signatures and Modules ---
188 | 
189 | 
190 | class LibraryAnalyzer(dspy.Signature):
191 |     """Analyze library documentation to understand core concepts, patterns, and examples."""
192 | 
193 |     library_name: str = dspy.InputField(desc="Name of the library to analyze")
194 |     documentation_content: str = dspy.InputField(
195 |         desc="Combined documentation from websites, READMEs, and code examples"
196 |     )
197 | 
198 |     core_concepts: list[str] = dspy.OutputField(
199 |         desc="Main concepts, classes, and components of the library."
200 |     )
201 |     common_patterns: list[str] = dspy.OutputField(
202 |         desc="Common usage patterns or workflows."
203 |     )
204 |     key_methods: list[str] = dspy.OutputField(
205 |         desc="List of important methods or functions and their purpose."
206 |     )
207 |     installation_info: str = dspy.OutputField(
208 |         desc="How to install the library (e.g., 'pip install ...')."
209 |     )
210 |     code_examples: list[str] = dspy.OutputField(
211 |         desc="Key code snippets found in the documentation."
212 |     )
213 | 
214 | 
215 | class CodeGenerator(dspy.Signature):
216 |     """Generate a complete, working code example for a specific use case."""
217 | 
218 |     library_info: str = dspy.InputField(
219 |         desc="Summary of the library's concepts, patterns, and methods."
220 |     )
221 |     use_case: str = dspy.InputField(
222 |         desc="The specific task to accomplish with the code."
223 |     )
224 |     requirements: str = dspy.InputField(
225 |         desc="Additional requirements or constraints for the code."
226 |     )
227 | 
228 |     code_example: str = dspy.OutputField(
229 |         desc="A single, complete, and runnable code block."
230 |     )
231 |     explanation: str = dspy.OutputField(
232 |         desc="A step-by-step explanation of the generated code."
233 |     )
234 |     best_practices: list[str] = dspy.OutputField(
235 |         desc="Tips and best practices for using the library."
236 |     )
237 |     imports_needed: list[str] = dspy.OutputField(
238 |         desc="A list of necessary import statements."
239 |     )
240 | 
241 | 
242 | class DocumentationLearningAgent(dspy.Module):
243 |     """Agent that learns from documentation and generates code."""
244 | 
245 |     def __init__(self):
246 |         super().__init__()
247 |         self.fetcher = DocumentationFetcher()
248 |         self.analyze_docs = dspy.ChainOfThought(LibraryAnalyzer)
249 |         self.generate_code = dspy.ChainOfThought(CodeGenerator)
250 | 
251 |     def learn_from_urls(self, library_name: str, doc_urls: list[str]) -> Dict:
252 |         """Learns about a library from documentation URLs and GitHub repos."""
253 |         print(f"📚 Learning about {library_name} from {len(doc_urls)} sources...")
254 |         docs = self.fetcher.fetch_documentation(doc_urls)
255 | 
256 |         combined_content = "\n\n---\n\n".join(
257 |             [
258 |                 f"SOURCE: {doc['url']}\n\n{doc['content']}"
259 |                 for doc in docs
260 |                 if doc["success"]
261 |             ]
262 |         )
263 | 
264 |         if not combined_content:
265 |             raise ValueError("No documentation could be fetched successfully.")
266 | 
267 |         analysis = self.analyze_docs(
268 |             library_name=library_name, documentation_content=combined_content
269 |         )
270 | 
271 |         return {
272 |             "library": library_name,
273 |             "source_urls": [doc["url"] for doc in docs if doc["success"]],
274 |             "core_concepts": analysis.core_concepts,
275 |             "patterns": analysis.common_patterns,
276 |             "methods": analysis.key_methods,
277 |             "installation": analysis.installation_info,
278 |             "examples": analysis.code_examples,
279 |         }
280 | 
281 |     def generate_example(
282 |         self, library_info: Dict, use_case: str, requirements: str = ""
283 |     ) -> Dict:
284 |         """Generates a code example for a specific use case."""
285 |         info_text = f"""
286 |         Library: {library_info["library"]}
287 |         Core Concepts: {", ".join(library_info["core_concepts"])}
288 |         Common Patterns: {", ".join(library_info["patterns"])}
289 |         Key Methods: {", ".join(library_info["methods"])}
290 |         Installation: {library_info["installation"]}
291 |         """
292 | 
293 |         code_result = self.generate_code(
294 |             library_info=info_text, use_case=use_case, requirements=requirements
295 |         )
296 | 
297 |         return {
298 |             "code": code_result.code_example,
299 |             "explanation": code_result.explanation,
300 |             "best_practices": code_result.best_practices,
301 |             "imports": code_result.imports_needed,
302 |         }
303 | 
304 | 
305 | # --- Interactive Session Logic ---
306 | 
307 | 
308 | def interactive_learning_session():
309 |     """Main interactive session for the library learning system."""
310 |     print("🎯 Welcome to the Interactive Library Learning System!")
311 |     print("This system now supports learning from websites AND GitHub repositories.\n")
312 | 
313 |     agent = DocumentationLearningAgent()
314 |     learned_libraries = {}
315 | 
316 |     while True:
317 |         print("\n" + "=" * 60)
318 |         library_name = input(
319 |             "\n📚 Enter the library name (or 'quit' to exit): "
320 |         ).strip()
321 |         if library_name.lower() in ["quit", "exit", "q"]:
322 |             break
323 | 
324 |         print(
325 |             f"\n🔗 Enter documentation URLs or a GitHub repo URL for {library_name} (one per line, empty line to finish):"
326 |         )
327 |         urls = []
328 |         while True:
329 |             url = input("  URL: ").strip()
330 |             if not url:
331 |                 break
332 |             urls.append(url)
333 | 
334 |         if not urls:
335 |             continue
336 | 
337 |         try:
338 |             # Step 1: Learn about the library from the provided sources
339 |             library_info = agent.learn_from_urls(library_name, urls)
340 |             print(f"\n✅ Successfully learned {library_name}!")
341 |             print(f"   - Core Concepts: {library_info.get('core_concepts', 'N/A')}")
342 |             print(f"   - Installation: {library_info.get('installation', 'N/A')}")
343 | 
344 |             # Step 2: Get all use cases from the user upfront
345 |             print(
346 |                 f"\n🎯 Define use cases for {library_name} (one per line, empty line to finish):"
347 |             )
348 |             use_cases = []
349 |             while True:
350 |                 use_case = input("     Use case: ").strip()
351 |                 if not use_case:
352 |                     break
353 |                 use_cases.append(use_case)
354 | 
355 |             if not use_cases:
356 |                 print("No use cases provided. Moving on.")
357 |                 continue
358 | 
359 |             # Step 3: Generate and display all examples
360 |             print(f"\n🔧 Generating {len(use_cases)} examples for {library_name}...")
361 |             all_examples = []
362 |             for i, use_case in enumerate(use_cases, 1):
363 |                 print(f"\n--- EXAMPLE {i}/{len(use_cases)}: {use_case} ---")
364 | 
365 |                 example = agent.generate_example(library_info, use_case)
366 |                 all_examples.append({"use_case": use_case, **example})
367 | 
368 |                 print("\n💻 Code Example:")
369 |                 print(f"```python\n{example['code']}\n```")
370 | 
371 |                 print("\n📦 Required Imports:")
372 |                 print("\n".join([f"  • {imp}" for imp in example["imports"]]))
373 | 
374 |                 print("\n📝 Explanation:")
375 |                 print(example["explanation"])
376 | 
377 |                 print("\n✅ Best Practices:")
378 |                 print("\n".join([f"  • {bp}" for bp in example["best_practices"]]))
379 |                 print("--- END OF EXAMPLE ---")
380 | 
381 |             # Store the complete results
382 |             learned_libraries[library_name] = {
383 |                 "library_info": library_info,
384 |                 "examples": all_examples,
385 |             }
386 | 
387 |             # Step 4: Offer to save the results to a file
388 |             save_results = (
389 |                 input(f"\n💾 Save learning results for {library_name} to file? (y/n): ")
390 |                 .strip()
391 |                 .lower()
392 |             )
393 |             if save_results in ["y", "yes"]:
394 |                 filename = input(
395 |                     f"   Enter filename (default: {library_name.lower()}_learning.json): "
396 |                 ).strip()
397 |                 if not filename:
398 |                     filename = f"{library_name.lower()}_learning.json"
399 | 
400 |                 try:
401 |                     with open(filename, "w", encoding="utf-8") as f:
402 |                         json.dump(
403 |                             learned_libraries[library_name], f, indent=2, default=str
404 |                         )
405 |                     print(f"   ✅ Results saved to {filename}")
406 |                 except Exception as e:
407 |                     print(f"   ❌ Error saving file: {e}")
408 | 
409 |         except Exception as e:
410 |             print(f"❌ An error occurred while learning {library_name}: {e}")
411 | 
412 |     print("\n👋 Thanks for using the Interactive Library Learning System!")
413 |     if learned_libraries:
414 |         print(f"\n🎉 Session Summary:")
415 |         print(
416 |             f"Successfully learned {len(learned_libraries)} libraries: {list(learned_libraries.keys())}"
417 |         )
418 | 
419 | 
420 | if __name__ == "__main__":
421 |     interactive_learning_session()
```

codeGeneration_for_unfamilar_libraries/repo_helpers.py
```
1 | # repo_helpers.py
2 | # Contains functions for interacting with the GitHub API.
3 | 
4 | import requests
5 | from dotenv import load_dotenv
6 | import os
7 | import base64
8 | 
9 | # Load environment variables from a .env file
10 | load_dotenv()
11 | 
12 | 
13 | def get_github_file_tree(repo_url):
14 |     """Get repository file structure from the GitHub API."""
15 |     token = os.getenv("GITHUB_ACCESS_TOKEN")
16 |     parts = repo_url.strip("/").split("/")
17 |     owner, repo = parts[-2], parts[-1]
18 | 
19 |     api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
20 |     headers = {"Authorization": f"Bearer {token}"} if token else {}
21 | 
22 |     print(f"🌳 Fetching file tree for {owner}/{repo}...")
23 |     response = requests.get(api_url, headers=headers)
24 | 
25 |     if response.status_code == 200:
26 |         tree_data = response.json()
27 |         # Filter for files (blobs) only
28 |         file_paths = [
29 |             item["path"] for item in tree_data.get("tree", []) if item["type"] == "blob"
30 |         ]
31 |         return "\n".join(sorted(file_paths))
32 |     else:
33 |         print(
34 |             f"⚠️  Could not fetch repository tree (Status: {response.status_code}): {response.text}"
35 |         )
36 |         return "Could not fetch repository file tree."
37 | 
38 | 
39 | def get_github_file_content(repo_url, file_path):
40 |     """Get specific file content from a GitHub repository."""
41 |     token = os.getenv("GITHUB_ACCESS_TOKEN")
42 |     parts = repo_url.strip("/").split("/")
43 |     owner, repo = parts[-2], parts[-1]
44 | 
45 |     api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
46 |     headers = {"Authorization": f"Bearer {token}"} if token else {}
47 | 
48 |     response = requests.get(api_url, headers=headers)
49 | 
50 |     if response.status_code == 200:
51 |         content = base64.b64decode(response.json()["content"]).decode("utf-8")
52 |         return content
53 |     else:
54 |         return f"Could not fetch {file_path}"
55 | 
56 | 
57 | def gather_repository_info(repo_url):
58 |     """
59 |     Gathers the file tree, README, and example files from a repository.
60 |     Focuses on README for overview and Python/Jupyter files for examples.
61 |     """
62 |     print(f"🔍 Gathering information from repository: {repo_url}")
63 |     file_tree_str = get_github_file_tree(repo_url)
64 | 
65 |     if "Could not fetch" in file_tree_str:
66 |         return "Could not access repository.", {}
67 | 
68 |     readme_content = get_github_file_content(repo_url, "README.md")
69 | 
70 |     # --- Find and fetch example files ---
71 |     example_files = {}
72 |     file_paths = file_tree_str.split("\n")
73 | 
74 |     # Look for common example directories or files
75 |     example_keywords = ["examples", "example", "docs", "samples", "tutorial"]
76 |     py_files = [p for p in file_paths if p.endswith(".py")]
77 |     ipynb_files = [p for p in file_paths if p.endswith(".ipynb")]
78 | 
79 |     # Prioritize files in example-related directories
80 |     potential_examples = [
81 |         p
82 |         for p in py_files + ipynb_files
83 |         if any(keyword in p.lower() for keyword in example_keywords)
84 |     ]
85 | 
86 |     # If not enough found, take a few from the root
87 |     if len(potential_examples) < 5:
88 |         potential_examples.extend(
89 |             [p for p in py_files if "/" not in p][:5]
90 |         )  # Top-level python files
91 | 
92 |     # Fetch content for a limited number of examples to avoid being overwhelming
93 |     for i, file_path in enumerate(
94 |         list(set(potential_examples))[:5]
95 |     ):  # Limit to 5 unique examples
96 |         print(f"📄 Fetching example file: {file_path}")
97 |         content = get_github_file_content(repo_url, file_path)
98 |         if "Could not fetch" not in content:
99 |             example_files[file_path] = content
100 | 
101 |     # --- Combine all info into a single string for the LLM ---
102 |     combined_content = f"# REPOSITORY OVERVIEW: {repo_url}\n\n"
103 |     combined_content += "## README.md\n\n" + readme_content + "\n\n---\n\n"
104 | 
105 |     if example_files:
106 |         combined_content += "## CODE EXAMPLES\n\n"
107 |         for path, code in example_files.items():
108 |             combined_content += f"### File: {path}\n\n```python\n{code}\n```\n\n"
109 | 
110 |     return combined_content, {"file_tree": file_tree_str, **example_files}
```

ollama-llm_config/generate_examples.py
```
1 | # generate_examples.py
2 | # Purpose: Generate code examples for any learned library
3 | 
4 | from learn_library import fastapi_info, streamlit_info, agent
5 | 
6 | 
7 | def generate_examples_for_library(library_info: dict, library_name: str):
8 |     """Generate code examples for any library based on its documentation."""
9 | 
10 |     # Define generic use cases that can apply to most libraries
11 |     use_cases = [
12 |         {
13 |             "name": "Basic Setup and Hello World",
14 |             "description": f"Create a minimal working example with {library_name}",
15 |             "requirements": "Include installation, imports, and basic usage",
16 |         },
17 |         {
18 |             "name": "Common Operations",
19 |             "description": f"Demonstrate the most common {library_name} operations",
20 |             "requirements": "Show typical workflow and best practices",
21 |         },
22 |         {
23 |             "name": "Advanced Usage",
24 |             "description": f"Create a more complex example showcasing {library_name} capabilities",
25 |             "requirements": "Include error handling and optimization",
26 |         },
27 |     ]
28 | 
29 |     generated_examples = []
30 | 
31 |     print(f"\n🔧 Generating examples for {library_name}...")
32 | 
33 |     for use_case in use_cases:
34 |         print(f"\n📝 {use_case['name']}")
35 |         print(f"Description: {use_case['description']}")
36 | 
37 |         example = agent.generate_example(
38 |             library_info=library_info,
39 |             use_case=use_case["description"],
40 |             requirements=use_case["requirements"],
41 |         )
42 | 
43 |         print("\n💻 Generated Code:")
44 |         print("```python")
45 |         print(example["code"])
46 |         print("```")
47 | 
48 |         print("\n📦 Required Imports:")
49 |         for imp in example["imports"]:
50 |             print(f"  • {imp}")
51 | 
52 |         print("\n📝 Explanation:")
53 |         print(example["explanation"])
54 | 
55 |         print("\n✅ Best Practices:")
56 |         for practice in example["best_practices"]:
57 |             print(f"  • {practice}")
58 | 
59 |         generated_examples.append(
60 |             {
61 |                 "use_case": use_case["name"],
62 |                 "code": example["code"],
63 |                 "imports": example["imports"],
64 |                 "explanation": example["explanation"],
65 |                 "best_practices": example["best_practices"],
66 |             }
67 |         )
68 | 
69 |         print("-" * 80)
70 | 
71 |     return generated_examples
72 | 
73 | 
74 | # Generate examples for both libraries
75 | print("🎯 Generating FastAPI Examples:")
76 | fastapi_examples = generate_examples_for_library(fastapi_info, "FastAPI")
77 | 
78 | print("\n\n🎯 Generating Streamlit Examples:")
79 | streamlit_examples = generate_examples_for_library(streamlit_info, "Streamlit")
```

ollama-llm_config/interactive_learning.py
```
1 | # interactive_learning.py
2 | # Purpose: Run a full interactive session for learning any Python library from docs
3 | 
4 | from main import agent
5 | from typing import Dict
6 | 
7 | 
8 | def learn_any_library(
9 |     library_name: str, documentation_urls: list[str], use_cases: list[str] = None
10 | ):
11 |     """Learn any library from its documentation and generate examples."""
12 | 
13 |     if use_cases is None:
14 |         use_cases = [
15 |             "Basic setup and hello world example",
16 |             "Common operations and workflows",
17 |             "Advanced usage with best practices",
18 |         ]
19 | 
20 |     print(f"🚀 Starting automated learning for {library_name}...")
21 |     print(f"Documentation sources: {len(documentation_urls)} URLs")
22 | 
23 |     try:
24 |         # Step 1: Learn from documentation
25 |         library_info = agent.learn_from_urls(library_name, documentation_urls)
26 | 
27 |         # Step 2: Generate examples for each use case
28 |         all_examples = []
29 | 
30 |         for i, use_case in enumerate(use_cases, 1):
31 |             print(f"\n📝 Generating example {i}/{len(use_cases)}: {use_case}")
32 | 
33 |             example = agent.generate_example(
34 |                 library_info=library_info,
35 |                 use_case=use_case,
36 |                 requirements="Include error handling, comments, and follow best practices",
37 |             )
38 | 
39 |             all_examples.append(
40 |                 {
41 |                     "use_case": use_case,
42 |                     "code": example["code"],
43 |                     "imports": example["imports"],
44 |                     "explanation": example["explanation"],
45 |                     "best_practices": example["best_practices"],
46 |                 }
47 |             )
48 | 
49 |         return {"library_info": library_info, "examples": all_examples}
50 | 
51 |     except Exception as e:
52 |         print(f"❌ Error learning {library_name}: {e}")
53 |         return None
54 | 
55 | 
56 | def interactive_learning_session():
57 |     """Interactive session for learning libraries with user input."""
58 | 
59 |     print("🎯 Welcome to the Interactive Library Learning System!")
60 |     print(
61 |         "This system will help you learn any Python library from its documentation.\n"
62 |     )
63 | 
64 |     learned_libraries = {}
65 | 
66 |     while True:
67 |         print("\n" + "=" * 60)
68 |         print("🚀 LIBRARY LEARNING SESSION")
69 |         print("=" * 60)
70 | 
71 |         # Get library name from user
72 |         library_name = input(
73 |             "\n📚 Enter the library name you want to learn (or 'quit' to exit): "
74 |         ).strip()
75 | 
76 |         if library_name.lower() in ["quit", "exit", "q"]:
77 |             print("\n👋 Thanks for using the Interactive Library Learning System!")
78 |             break
79 | 
80 |         if not library_name:
81 |             print("❌ Please enter a valid library name.")
82 |             continue
83 | 
84 |         # Get documentation URLs
85 |         print(
86 |             f"\n🔗 Enter documentation URLs for {library_name} (one per line, empty line to finish):"
87 |         )
88 |         urls = []
89 |         while True:
90 |             url = input("  URL: ").strip()
91 |             if not url:
92 |                 break
93 |             if not url.startswith(("http://", "https://")):
94 |                 print(
95 |                     "    ⚠️  Please enter a valid URL starting with http:// or https://"
96 |                 )
97 |                 continue
98 |             urls.append(url)
99 | 
100 |         if not urls:
101 |             print("❌ No valid URLs provided. Skipping this library.")
102 |             continue
103 | 
104 |         # Get custom use cases from user
105 |         print(
106 |             f"\n🎯 Define use cases for {library_name} (optional, press Enter for defaults):"
107 |         )
108 |         print(
109 |             "   Default use cases will be: Basic setup, Common operations, Advanced usage"
110 |         )
111 | 
112 |         user_wants_custom = (
113 |             input("   Do you want to define custom use cases? (y/n): ").strip().lower()
114 |         )
115 | 
116 |         use_cases = None
117 |         if user_wants_custom in ["y", "yes"]:
118 |             print("   Enter your use cases (one per line, empty line to finish):")
119 |             use_cases = []
120 |             while True:
121 |                 use_case = input("     Use case: ").strip()
122 |                 if not use_case:
123 |                     break
124 |                 use_cases.append(use_case)
125 | 
126 |             if not use_cases:
127 |                 print("   No custom use cases provided, using defaults.")
128 |                 use_cases = None
129 | 
130 |         # Learn the library
131 |         print(f"\n🚀 Starting learning process for {library_name}...")
132 |         result = learn_any_library(library_name, urls, use_cases)
133 | 
134 |         if result:
135 |             learned_libraries[library_name] = result
136 |             print(f"\n✅ Successfully learned {library_name}!")
137 | 
138 |             # Show summary
139 |             print(f"\n📊 Learning Summary for {library_name}:")
140 |             print(
141 |                 f"   • Core concepts: {len(result['library_info']['core_concepts'])} identified"
142 |             )
143 |             print(
144 |                 f"   • Common patterns: {len(result['library_info']['patterns'])} found"
145 |             )
146 |             print(f"   • Examples generated: {len(result['examples'])}")
147 | 
148 |             # Ask if user wants to see examples
149 |             show_examples = (
150 |                 input(
151 |                     f"\n👀 Do you want to see the generated examples for {library_name}? (y/n): "
152 |                 )
153 |                 .strip()
154 |                 .lower()
155 |             )
156 | 
157 |             if show_examples in ["y", "yes"]:
158 |                 for i, example in enumerate(result["examples"], 1):
159 |                     print(f"\n{'─' * 50}")
160 |                     print(f"📝 Example {i}: {example['use_case']}")
161 |                     print(f"{'─' * 50}")
162 | 
163 |                     print("\n💻 Generated Code:")
164 |                     print("```python")
165 |                     print(example["code"])
166 |                     print("```")
167 | 
168 |                     print(f"\n📦 Required Imports:")
169 |                     for imp in example["imports"]:
170 |                         print(f"  • {imp}")
171 | 
172 |                     print(f"\n📝 Explanation:")
173 |                     print(example["explanation"])
174 | 
175 |                     print(f"\n✅ Best Practices:")
176 |                     for practice in example["best_practices"]:
177 |                         print(f"  • {practice}")
178 | 
179 |                     # Ask if user wants to see the next example
180 |                     if i < len(result["examples"]):
181 |                         continue_viewing = (
182 |                             input(f"\nContinue to next example? (y/n): ")
183 |                             .strip()
184 |                             .lower()
185 |                         )
186 |                         if continue_viewing not in ["y", "yes"]:
187 |                             break
188 | 
189 |             # Offer to save results
190 |             save_results = (
191 |                 input(f"\n💾 Save learning results for {library_name} to file? (y/n): ")
192 |                 .strip()
193 |                 .lower()
194 |             )
195 | 
196 |             if save_results in ["y", "yes"]:
197 |                 filename = input(
198 |                     f"   Enter filename (default: {library_name.lower()}_learning.json): "
199 |                 ).strip()
200 |                 if not filename:
201 |                     filename = f"{library_name.lower()}_learning.json"
202 | 
203 |                 try:
204 |                     import json
205 | 
206 |                     with open(filename, "w") as f:
207 |                         json.dump(result, f, indent=2, default=str)
208 |                     print(f"   ✅ Results saved to {filename}")
209 |                 except Exception as e:
210 |                     print(f"   ❌ Error saving file: {e}")
211 | 
212 |         else:
213 |             print(f"❌ Failed to learn {library_name}")
214 | 
215 |         # Ask if user wants to learn another library
216 |         print(f"\n📚 Libraries learned so far: {list(learned_libraries.keys())}")
217 |         continue_learning = (
218 |             input("\n🔄 Do you want to learn another library? (y/n): ").strip().lower()
219 |         )
220 | 
221 |         if continue_learning not in ["y", "yes"]:
222 |             break
223 | 
224 |     # Final summary
225 |     if learned_libraries:
226 |         print(f"\n🎉 Session Summary:")
227 |         print(f"Successfully learned {len(learned_libraries)} libraries:")
228 |         for lib_name, info in learned_libraries.items():
229 |             print(f"  • {lib_name}: {len(info['examples'])} examples generated")
230 | 
231 |     return learned_libraries
232 | 
233 | 
234 | # Example: Run interactive learning session
235 | if __name__ == "__main__":
236 |     # Run interactive session
237 |     learned_libraries = interactive_learning_session()
```

ollama-llm_config/learn_library.py
```
1 | # learn_library.py
2 | # Purpose: Utility to learn any library from a set of documentation URLs using the agent
3 | 
4 | from main import agent  # Import the previously defined agent
5 | from typing import Dict
6 | 
7 | 
8 | def learn_library_from_urls(library_name: str, documentation_urls: list[str]) -> Dict:
9 |     """Learn about any library from its documentation URLs."""
10 | 
11 |     try:
12 |         library_info = agent.learn_from_urls(library_name, documentation_urls)
13 | 
14 |         print(f"\n🔍 Library Analysis Results for {library_name}:")
15 |         print(f"Sources: {len(library_info['source_urls'])} successful fetches")
16 |         print(f"Core Concepts: {library_info['core_concepts']}")
17 |         print(f"Common Patterns: {library_info['patterns']}")
18 |         print(f"Key Methods: {library_info['methods']}")
19 |         print(f"Installation: {library_info['installation']}")
20 |         print(f"Found {len(library_info['examples'])} code examples")
21 | 
22 |         return library_info
23 | 
24 |     except Exception as e:
25 |         print(f"❌ Error learning library: {e}")
26 |         raise
27 | 
28 | 
29 | # Example 1: Learn FastAPI from official documentation
30 | fastapi_urls = [
31 |     "https://fastapi.tiangolo.com/",
32 |     "https://fastapi.tiangolo.com/tutorial/first-steps/",
33 |     "https://fastapi.tiangolo.com/tutorial/path-params/",
34 |     "https://fastapi.tiangolo.com/tutorial/query-params/",
35 | ]
36 | 
37 | print("🚀 Learning FastAPI from official documentation...")
38 | fastapi_info = learn_library_from_urls("FastAPI", fastapi_urls)
39 | 
40 | # Example 2: Learn a different library (you can replace with any library)
41 | streamlit_urls = [
42 |     "https://docs.streamlit.io/",
43 |     "https://docs.streamlit.io/get-started",
44 |     "https://docs.streamlit.io/develop/api-reference",
45 | ]
46 | 
47 | print("\n\n📊 Learning Streamlit from official documentation...")
48 | streamlit_info = learn_library_from_urls("Streamlit", streamlit_urls)
```

ollama-llm_config/litellm_learning.json
```
1 | {
2 |   "library_info": {
3 |     "library": "litellm",
4 |     "source_urls": [
5 |       "https://github.com/BerriAI/litellm"
6 |     ],
7 |     "core_concepts": [
8 |       "Unified interface for multiple LLM providers",
9 |       "Model abstraction layer that hides provider-specific details",
10 |       "Support for various model types (chat, text generation)",
11 |       "Integration with LangChain for complex workflows",
12 |       "VertexAI configuration requirements (project ID, location)"
13 |     ],
14 |     "patterns": [
15 |       "Using litellm.completion() for model inference",
16 |       "Setting provider-specific configurations",
17 |       "Handling model responses in standardized format",
18 |       "Configuring VertexAI with vertex_project and vertex_location",
19 |       "Managing multiple LLM providers in a single application"
20 |     ],
21 |     "methods": [
22 |       "litellm.completion() - Main method for model inference",
23 |       "litellm.vertex_project - Set Google Cloud Project ID",
24 |       "litellm.vertex_location - Set Vertex AI region",
25 |       "litellm.get_model_info() - Get information about supported models",
26 |       "litellm.set_verbose() - Enable detailed logging"
27 |     ],
28 |     "installation": "To use these examples, install the required packages:\n\n```bash\npip install litellm==0.1.388\npip install langchain\n```\n\nFor VertexAI integration, also ensure:\n- Application Default Credentials are configured via `gcloud auth application-default login`\n- Google Cloud Project ID and region are set in the code",
29 |     "examples": [
30 |       "from litellm import completion\nresponse = completion(model='gpt-4', messages=[{'role': 'user', 'content': 'Hello'}])",
31 |       "litellm.vertex_project = 'your-project-id'\nlitellm.vertex_location = 'us-central1'\nresponse = completion(model='chat-bison', messages=[{'role': 'user', 'content': 'What is liteLLM?'}])",
32 |       "from langchain.llms import LlamaCpp\nfrom langchain import PromptTemplate, LLMChain\nllm = LlamaCpp(model_path='/path/to/model')\nllm_chain = LLMChain(prompt=prompt, llm=llm)",
33 |       "import litellm\nresponse = completion(model='azure/gpt-4', messages=[{'role': 'user', 'content': 'Hello'}], api_key='your-key', api_base='your-endpoint')",
34 |       "from litellm import completion\nresponse = completion(model='text-bison@001', messages=[{'role': 'user', 'content': 'What is liteLLM?'}], temperature=0.4, top_k=10)"
35 |     ]
36 |   },
37 |   "examples": [
38 |     {
39 |       "use_case": "Route OpenAI-compatible API requests to different LLM providers using LiteLLM.",
40 |       "code": "import litellm\nfrom typing import Dict, Any\n\nclass LLMRouter:\n    def __init__(self):\n        # Configure providers with their specific settings\n        self.providers = {\n            'openai': {\n                'model': 'gpt-4',\n                'api_key': 'your-openai-api-key'\n            },\n            'azure': {\n                'model': 'gpt-4',\n                'api_key': 'your-azure-api-key',\n                'api_version': '2023-07-01-preview',\n                'api_base': 'https://your-resource.azure.com'\n            },\n            'vertexai': {\n                'model': 'chat-bison',\n                'project_id': 'your-project-id',\n                'location': 'us-central1'\n            }\n        }\n\n    def route_request(self, provider: str, messages: list, **kwargs) -> Dict[str, Any]:\n        \"\"\"\n        Route request to appropriate provider based on provider name\n        \"\"\"\n        if provider not in self.providers:\n            raise ValueError(f'Unsupported provider: {provider}')\n\n        # Prepare the configuration for the specific provider\n        config = self.providers[provider].copy()\n        \n        # Add or override with any additional parameters\n        config.update(kwargs)\n        \n        try:\n            # Make the completion request using litellm\n            response = litellm.completion(\n                model=config['model'],\n                messages=messages,\n                **{k: v for k, v in config.items() if k != 'model'}\n            )\n            return {\n                'provider': provider,\n                'response': response\n            }\n        except Exception as e:\n            return {\n                'error': str(e)\n            }\n\n# Example usage\nif __name__ == '__main__':\n    router = LLMRouter()\n    \n    # Sample messages for the request\n    messages = [\n        {'role': 'user', 'content': 'What is the capital of France?'}\n    ]\n    \n    # Route to different providers\n    print('Routing to OpenAI:')\n    result = router.route_request('openai', messages)\n    print(result)\n    \n    print('\\nRouting to Azure:')\n    result = router.route_request('azure', messages)\n    print(result)\n    \n    print('\\nRouting to VertexAI:')\n    result = router.route_request('vertexai', messages)\n    print(result)",
41 |       "explanation": "This code example demonstrates how to route OpenAI-compatible API requests to different LLM providers using LiteLLM. The implementation includes: 1) A LLMRouter class that manages configurations for multiple providers (OpenAI, Azure, VertexAI), 2) A route_request method that selects the appropriate provider based on input parameters, 3) Proper configuration handling for each provider type, 4) Error handling for failed requests, and 5) Example usage showing how to route requests to different providers. The code abstracts away provider-specific details through LiteLLM's unified interface while allowing customization of model parameters for each provider.",
42 |       "best_practices": [
43 |         "Always validate provider names before routing requests",
44 |         "Handle exceptions gracefully when making API calls",
45 |         "Store sensitive information like API keys securely (not in code)",
46 |         "Use environment variables for configuration values",
47 |         "Implement logging to track request routing and performance",
48 |         "Test with different model types and providers before production use"
49 |       ],
50 |       "imports": [
51 |         "litellm",
52 |         "typing.Dict",
53 |         "typing.Any"
54 |       ]
55 |     }
56 |   ]
57 | }
```

ollama-llm_config/main.py
```
1 | # main.py
2 | # Purpose: Automated documentation-powered code generation pipeline using DSPy.
3 | # Now with integrated GitHub repository analysis.
4 | 
5 | import dspy
6 | import requests
7 | from bs4 import BeautifulSoup
8 | import html2text
9 | from typing import List, Dict, Any
10 | import json
11 | import time
12 | 
13 | # Import the GitHub helper functions
14 | from repo_helpers import gather_repository_info
15 | 
16 | # --- DSPy Configuration ---
17 | # Replace with your actual LM provider if not using a local one
18 |     # For models like Llama
19 | lm = dspy.LM(
20 |      #"ollama_chat/acidic/Qwen3-Coder-IQ2_XXS:latest",
21 |     "ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:IQ2_XXS",
22 |     api_base="http://localhost:11434",  # Local Ollama server URL
23 |     api_key="EMPTY",  # Usually empty for local Ollama; remove if you do not have a key
24 |     streaming=False,
25 |     response_format={
26 |         "type": "json_schema",
27 |         "json_schema": {
28 |             "schema": {
29 |                 "type": "object",
30 |                 "properties": {
31 |                     "project": {
32 |                         "type": "object",
33 |                         "properties": {
34 |                             "name": {"type": "string"},
35 |                             "description": {"type": "string"},
36 |                         },
37 |                         "required": ["name", "description"],
38 |                     },
39 |                     "key_concepts": {
40 |                         "type": "array",
41 |                         "items": {"type": "string"},
42 |                         "minItems": 1,
43 |                     },
44 |                     "architecture_overview": {"type": "string"},
45 |                     "important_directories": {
46 |                         "type": "array",
47 |                         "items": {"type": "string"},
48 |                         "minItems": 1,
49 |                     },
50 |                     "entry_points": {
51 |                         "type": "array",
52 |                         "items": {"type": "string"},
53 |                         "minItems": 1,
54 |                     },
55 |                     "development_info": {
56 |                         "type": "object",
57 |                         "properties": {
58 |                             "test_dependencies": {
59 |                                 "type": "array",
60 |                                 "items": {"type": "string"},
61 |                                 "minItems": 1,
62 |                             },
63 |                             "linting_tools": {
64 |                                 "type": "array",
65 |                                 "items": {"type": "string"},
66 |                                 "minItems": 1,
67 |                             },
68 |                             "optional_dependencies": {
69 |                                 "type": "array",
70 |                                 "items": {"type": "string"},
71 |                             },
72 |                         },
73 |                         "required": ["test_dependencies", "linting_tools"],
74 |                     },
75 |                     "usage_examples": {
76 |                         "type": "array",
77 |                         "items": {"type": "string"},
78 |                         "minItems": 1,
79 |                     },
80 |                 },
81 |                 "required": [
82 |                     "project",
83 |                     "key_concepts",
84 |                     "architecture_overview",
85 |                     "important_directories",
86 |                     "entry_points",
87 |                     "development_info",
88 |                     "usage_examples",
89 |                 ],
90 |             }
91 |         },
92 |     },
93 | )
94 | dspy.configure(lm=lm)
95 | 
96 | 
97 | # --- Data Fetching Classes ---
98 | 
99 | 
100 | class DocumentationFetcher:
101 |     """
102 |     Fetches and processes documentation from both standard URLs and GitHub repositories.
103 |     """
104 | 
105 |     def __init__(self, max_retries=3, delay=1):
106 |         self.session = requests.Session()
107 |         self.session.headers.update(
108 |             {
109 |                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
110 |             }
111 |         )
112 |         self.max_retries = max_retries
113 |         self.delay = delay
114 |         self.html_converter = html2text.HTML2Text()
115 |         self.html_converter.ignore_links = False
116 |         self.html_converter.ignore_images = True
117 | 
118 |     def fetch_website_url(self, url: str) -> dict:
119 |         """Fetches and cleans content from a standard website URL."""
120 |         for attempt in range(self.max_retries):
121 |             try:
122 |                 print(f"📡 Fetching Website: {url} (attempt {attempt + 1})")
123 |                 response = self.session.get(url, timeout=15)
124 |                 response.raise_for_status()
125 |                 soup = BeautifulSoup(response.content, "html.parser")
126 |                 for script in soup(["script", "style", "nav", "footer", "header"]):
127 |                     script.decompose()
128 |                 markdown_content = self.html_converter.handle(str(soup))
129 |                 return {
130 |                     "url": url,
131 |                     "title": soup.title.string if soup.title else "No title",
132 |                     "content": markdown_content,
133 |                     "success": True,
134 |                 }
135 |             except Exception as e:
136 |                 print(f"❌ Error fetching {url}: {e}")
137 |                 if attempt < self.max_retries - 1:
138 |                     time.sleep(self.delay)
139 |         return {"url": url, "title": "Failed to fetch", "content": "", "success": False}
140 | 
141 |     def fetch_github_repo(self, url: str) -> dict:
142 |         """Fetches and consolidates content from a GitHub repository."""
143 |         print(f"📦 Fetching GitHub Repo: {url}")
144 |         try:
145 |             # Use the helper function to get README and example files
146 |             combined_content, details = gather_repository_info(url)
147 |             if "Could not access" in combined_content:
148 |                 return {
149 |                     "url": url,
150 |                     "title": "Failed to fetch repo",
151 |                     "content": "",
152 |                     "success": False,
153 |                 }
154 | 
155 |             return {
156 |                 "url": url,
157 |                 "title": f"GitHub Repo: {url.split('/')[-1]}",
158 |                 "content": combined_content,
159 |                 "success": True,
160 |                 "details": details,
161 |             }
162 |         except Exception as e:
163 |             print(f"❌ Error fetching GitHub repo {url}: {e}")
164 |             return {
165 |                 "url": url,
166 |                 "title": "Failed to fetch repo",
167 |                 "content": f"Error: {e}",
168 |                 "success": False,
169 |             }
170 | 
171 |     def fetch_documentation(self, urls: list[str]) -> list[dict]:
172 |         """
173 |         Fetches documentation from a list of URLs, routing to the correct
174 |         fetcher (website or GitHub) based on the URL.
175 |         """
176 |         results = []
177 |         for url in urls:
178 |             if "github.com" in url:
179 |                 result = self.fetch_github_repo(url)
180 |             else:
181 |                 result = self.fetch_website_url(url)
182 | 
183 |             results.append(result)
184 |             time.sleep(self.delay)  # Be respectful to servers
185 |         return results
186 | 
187 | 
188 | # --- DSPy Signatures and Modules ---
189 | 
190 | 
191 | class LibraryAnalyzer(dspy.Signature):
192 |     """Analyze library documentation to understand core concepts, patterns, and examples."""
193 | 
194 |     library_name: str = dspy.InputField(desc="Name of the library to analyze")
195 |     documentation_content: str = dspy.InputField(
196 |         desc="Combined documentation from websites, READMEs, and code examples"
197 |     )
198 | 
199 |     core_concepts: list[str] = dspy.OutputField(
200 |         desc="Main concepts, classes, and components of the library."
201 |     )
202 |     common_patterns: list[str] = dspy.OutputField(
203 |         desc="Common usage patterns or workflows."
204 |     )
205 |     key_methods: list[str] = dspy.OutputField(
206 |         desc="List of important methods or functions and their purpose."
207 |     )
208 |     installation_info: str = dspy.OutputField(
209 |         desc="How to install the library (e.g., 'pip install ...')."
210 |     )
211 |     code_examples: list[str] = dspy.OutputField(
212 |         desc="Key code snippets found in the documentation."
213 |     )
214 | 
215 | 
216 | class CodeGenerator(dspy.Signature):
217 |     """Generate a complete, working code example for a specific use case."""
218 | 
219 |     library_info: str = dspy.InputField(
220 |         desc="Summary of the library's concepts, patterns, and methods."
221 |     )
222 |     use_case: str = dspy.InputField(
223 |         desc="The specific task to accomplish with the code."
224 |     )
225 |     requirements: str = dspy.InputField(
226 |         desc="Additional requirements or constraints for the code."
227 |     )
228 | 
229 |     code_example: str = dspy.OutputField(
230 |         desc="A single, complete, and runnable code block."
231 |     )
232 |     explanation: str = dspy.OutputField(
233 |         desc="A step-by-step explanation of the generated code."
234 |     )
235 |     best_practices: list[str] = dspy.OutputField(
236 |         desc="Tips and best practices for using the library."
237 |     )
238 |     imports_needed: list[str] = dspy.OutputField(
239 |         desc="A list of necessary import statements."
240 |     )
241 | 
242 | 
243 | class DocumentationLearningAgent(dspy.Module):
244 |     """Agent that learns from documentation and generates code."""
245 | 
246 |     def __init__(self):
247 |         super().__init__()
248 |         self.fetcher = DocumentationFetcher()
249 |         self.analyze_docs = dspy.ChainOfThought(LibraryAnalyzer)
250 |         self.generate_code = dspy.ChainOfThought(CodeGenerator)
251 | 
252 |     def learn_from_urls(self, library_name: str, doc_urls: list[str]) -> Dict:
253 |         """Learns about a library from documentation URLs and GitHub repos."""
254 |         print(f"📚 Learning about {library_name} from {len(doc_urls)} sources...")
255 |         docs = self.fetcher.fetch_documentation(doc_urls)
256 | 
257 |         combined_content = "\n\n---\n\n".join(
258 |             [
259 |                 f"SOURCE: {doc['url']}\n\n{doc['content']}"
260 |                 for doc in docs
261 |                 if doc["success"]
262 |             ]
263 |         )
264 | 
265 |         if not combined_content:
266 |             raise ValueError("No documentation could be fetched successfully.")
267 | 
268 |         analysis = self.analyze_docs(
269 |             library_name=library_name, documentation_content=combined_content
270 |         )
271 | 
272 |         return {
273 |             "library": library_name,
274 |             "source_urls": [doc["url"] for doc in docs if doc["success"]],
275 |             "core_concepts": analysis.core_concepts,
276 |             "patterns": analysis.common_patterns,
277 |             "methods": analysis.key_methods,
278 |             "installation": analysis.installation_info,
279 |             "examples": analysis.code_examples,
280 |         }
281 | 
282 |     def generate_example(
283 |         self, library_info: Dict, use_case: str, requirements: str = ""
284 |     ) -> Dict:
285 |         """Generates a code example for a specific use case."""
286 |         info_text = f"""
287 |         Library: {library_info["library"]}
288 |         Core Concepts: {", ".join(library_info["core_concepts"])}
289 |         Common Patterns: {", ".join(library_info["patterns"])}
290 |         Key Methods: {", ".join(library_info["methods"])}
291 |         Installation: {library_info["installation"]}
292 |         """
293 | 
294 |         code_result = self.generate_code(
295 |             library_info=info_text, use_case=use_case, requirements=requirements
296 |         )
297 | 
298 |         return {
299 |             "code": code_result.code_example,
300 |             "explanation": code_result.explanation,
301 |             "best_practices": code_result.best_practices,
302 |             "imports": code_result.imports_needed,
303 |         }
304 | 
305 | 
306 | # --- Interactive Session Logic ---
307 | 
308 | 
309 | def interactive_learning_session():
310 |     """Main interactive session for the library learning system."""
311 |     print("🎯 Welcome to the Interactive Library Learning System!")
312 |     print("This system now supports learning from websites AND GitHub repositories.\n")
313 | 
314 |     agent = DocumentationLearningAgent()
315 |     learned_libraries = {}
316 | 
317 |     while True:
318 |         print("\n" + "=" * 60)
319 |         library_name = input(
320 |             "\n📚 Enter the library name (or 'quit' to exit): "
321 |         ).strip()
322 |         if library_name.lower() in ["quit", "exit", "q"]:
323 |             break
324 | 
325 |         print(
326 |             f"\n🔗 Enter documentation URLs or a GitHub repo URL for {library_name} (one per line, empty line to finish):"
327 |         )
328 |         urls = []
329 |         while True:
330 |             url = input("  URL: ").strip()
331 |             if not url:
332 |                 break
333 |             urls.append(url)
334 | 
335 |         if not urls:
336 |             continue
337 | 
338 |         try:
339 |             # Step 1: Learn about the library from the provided sources
340 |             library_info = agent.learn_from_urls(library_name, urls)
341 |             print(f"\n✅ Successfully learned {library_name}!")
342 |             print(f"   - Core Concepts: {library_info.get('core_concepts', 'N/A')}")
343 |             print(f"   - Installation: {library_info.get('installation', 'N/A')}")
344 | 
345 |             # Step 2: Get all use cases from the user upfront
346 |             print(
347 |                 f"\n🎯 Define use cases for {library_name} (one per line, empty line to finish):"
348 |             )
349 |             use_cases = []
350 |             while True:
351 |                 use_case = input("     Use case: ").strip()
352 |                 if not use_case:
353 |                     break
354 |                 use_cases.append(use_case)
355 | 
356 |             if not use_cases:
357 |                 print("No use cases provided. Moving on.")
358 |                 continue
359 | 
360 |             # Step 3: Generate and display all examples
361 |             print(f"\n🔧 Generating {len(use_cases)} examples for {library_name}...")
362 |             all_examples = []
363 |             for i, use_case in enumerate(use_cases, 1):
364 |                 print(f"\n--- EXAMPLE {i}/{len(use_cases)}: {use_case} ---")
365 | 
366 |                 example = agent.generate_example(library_info, use_case)
367 |                 all_examples.append({"use_case": use_case, **example})
368 | 
369 |                 print("\n💻 Code Example:")
370 |                 print(f"```python\n{example['code']}\n```")
371 | 
372 |                 print("\n📦 Required Imports:")
373 |                 print("\n".join([f"  • {imp}" for imp in example["imports"]]))
374 | 
375 |                 print("\n📝 Explanation:")
376 |                 print(example["explanation"])
377 | 
378 |                 print("\n✅ Best Practices:")
379 |                 print("\n".join([f"  • {bp}" for bp in example["best_practices"]]))
380 |                 print("--- END OF EXAMPLE ---")
381 | 
382 |             # Store the complete results
383 |             learned_libraries[library_name] = {
384 |                 "library_info": library_info,
385 |                 "examples": all_examples,
386 |             }
387 | 
388 |             # Step 4: Offer to save the results to a file
389 |             save_results = (
390 |                 input(f"\n💾 Save learning results for {library_name} to file? (y/n): ")
391 |                 .strip()
392 |                 .lower()
393 |             )
394 |             if save_results in ["y", "yes"]:
395 |                 filename = input(
396 |                     f"   Enter filename (default: {library_name.lower()}_learning.json): "
397 |                 ).strip()
398 |                 if not filename:
399 |                     filename = f"{library_name.lower()}_learning.json"
400 | 
401 |                 try:
402 |                     with open(filename, "w", encoding="utf-8") as f:
403 |                         json.dump(
404 |                             learned_libraries[library_name], f, indent=2, default=str
405 |                         )
406 |                     print(f"   ✅ Results saved to {filename}")
407 |                 except Exception as e:
408 |                     print(f"   ❌ Error saving file: {e}")
409 | 
410 |         except Exception as e:
411 |             print(f"❌ An error occurred while learning {library_name}: {e}")
412 | 
413 |     print("\n👋 Thanks for using the Interactive Library Learning System!")
414 |     if learned_libraries:
415 |         print(f"\n🎉 Session Summary:")
416 |         print(
417 |             f"Successfully learned {len(learned_libraries)} libraries: {list(learned_libraries.keys())}"
418 |         )
419 | 
420 | 
421 | if __name__ == "__main__":
422 |     interactive_learning_session()
```

ollama-llm_config/repo_helpers.py
```
1 | # repo_helpers.py
2 | # Contains functions for interacting with the GitHub API.
3 | 
4 | import requests
5 | from dotenv import load_dotenv
6 | import os
7 | import base64
8 | 
9 | # Load environment variables from a .env file
10 | load_dotenv()
11 | 
12 | 
13 | def get_github_file_tree(repo_url):
14 |     """Get repository file structure from the GitHub API."""
15 |     token = os.getenv("GITHUB_ACCESS_TOKEN")
16 |     parts = repo_url.strip("/").split("/")
17 |     owner, repo = parts[-2], parts[-1]
18 | 
19 |     api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
20 |     headers = {"Authorization": f"Bearer {token}"} if token else {}
21 | 
22 |     print(f"🌳 Fetching file tree for {owner}/{repo}...")
23 |     response = requests.get(api_url, headers=headers)
24 | 
25 |     if response.status_code == 200:
26 |         tree_data = response.json()
27 |         # Filter for files (blobs) only
28 |         file_paths = [
29 |             item["path"] for item in tree_data.get("tree", []) if item["type"] == "blob"
30 |         ]
31 |         return "\n".join(sorted(file_paths))
32 |     else:
33 |         print(
34 |             f"⚠️  Could not fetch repository tree (Status: {response.status_code}): {response.text}"
35 |         )
36 |         return "Could not fetch repository file tree."
37 | 
38 | 
39 | def get_github_file_content(repo_url, file_path):
40 |     """Get specific file content from a GitHub repository."""
41 |     token = os.getenv("GITHUB_ACCESS_TOKEN")
42 |     parts = repo_url.strip("/").split("/")
43 |     owner, repo = parts[-2], parts[-1]
44 | 
45 |     api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
46 |     headers = {"Authorization": f"Bearer {token}"} if token else {}
47 | 
48 |     response = requests.get(api_url, headers=headers)
49 | 
50 |     if response.status_code == 200:
51 |         content = base64.b64decode(response.json()["content"]).decode("utf-8")
52 |         return content
53 |     else:
54 |         return f"Could not fetch {file_path}"
55 | 
56 | 
57 | def gather_repository_info(repo_url):
58 |     """
59 |     Gathers the file tree, README, and example files from a repository.
60 |     Focuses on README for overview and Python/Jupyter files for examples.
61 |     """
62 |     print(f"🔍 Gathering information from repository: {repo_url}")
63 |     file_tree_str = get_github_file_tree(repo_url)
64 | 
65 |     if "Could not fetch" in file_tree_str:
66 |         return "Could not access repository.", {}
67 | 
68 |     readme_content = get_github_file_content(repo_url, "README.md")
69 | 
70 |     # --- Find and fetch example files ---
71 |     example_files = {}
72 |     file_paths = file_tree_str.split("\n")
73 | 
74 |     # Look for common example directories or files
75 |     example_keywords = ["examples", "example", "docs", "samples", "tutorial"]
76 |     py_files = [p for p in file_paths if p.endswith(".py")]
77 |     ipynb_files = [p for p in file_paths if p.endswith(".ipynb")]
78 | 
79 |     # Prioritize files in example-related directories
80 |     potential_examples = [
81 |         p
82 |         for p in py_files + ipynb_files
83 |         if any(keyword in p.lower() for keyword in example_keywords)
84 |     ]
85 | 
86 |     # If not enough found, take a few from the root
87 |     if len(potential_examples) < 5:
88 |         potential_examples.extend(
89 |             [p for p in py_files if "/" not in p][:5]
90 |         )  # Top-level python files
91 | 
92 |     # Fetch content for a limited number of examples to avoid being overwhelming
93 |     for i, file_path in enumerate(
94 |         list(set(potential_examples))[:5]
95 |     ):  # Limit to 5 unique examples
96 |         print(f"📄 Fetching example file: {file_path}")
97 |         content = get_github_file_content(repo_url, file_path)
98 |         if "Could not fetch" not in content:
99 |             example_files[file_path] = content
100 | 
101 |     # --- Combine all info into a single string for the LLM ---
102 |     combined_content = f"# REPOSITORY OVERVIEW: {repo_url}\n\n"
103 |     combined_content += "## README.md\n\n" + readme_content + "\n\n---\n\n"
104 | 
105 |     if example_files:
106 |         combined_content += "## CODE EXAMPLES\n\n"
107 |         for path, code in example_files.items():
108 |             combined_content += f"### File: {path}\n\n```python\n{code}\n```\n\n"
109 | 
110 |     return combined_content, {"file_tree": file_tree_str, **example_files}
```

ollama-llm_config/vllm_learning.json
```
1 | {
2 |   "library_info": {
3 |     "library": "vllm",
4 |     "source_urls": [
5 |       "https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html"
6 |     ],
7 |     "core_concepts": [
8 |       "vLLM engine",
9 |       "OpenAI-compatible HTTP API",
10 |       "Ray Serve LLM",
11 |       "Scalable model serving",
12 |       "Multi-modal inputs",
13 |       "Re-ranking and scoring"
14 |     ],
15 |     "patterns": [
16 |       "Using curl commands to send requests to endpoints",
17 |       "Support for both single and batch input processing",
18 |       "Integration with Hugging Face processors",
19 |       "Use of priority and activation flags in requests",
20 |       "Compatibility with Jina AI and Cohere APIs"
21 |     ],
22 |     "methods": [
23 |       "vllm serve",
24 |       "Ray Serve deployment",
25 |       "POST requests to /score or /rerank endpoints",
26 |       "Using mm_processor_kwargs for multi-modal inputs",
27 |       "Handling of document lists in reranking tasks"
28 |     ],
29 |     "installation": "To use the described features, one needs to have vLLM and Ray Serve installed. The example uses `vllm serve` command and Ray Serve LLM integration.",
30 |     "examples": [
31 |       "curl -X 'POST' 'http://localhost:8000/v1/rerank' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{\"model\": \"BAAI/bge-reranker-base\", \"query\": \"What is the capital of France?\", \"documents\": [\"The capital of Brazil is Brasilia.\", \"The capital of France is Paris.\", \"Horses and cows are both animals\"]}'",
32 |       "import requests\nresponse = requests.post(\"http://localhost:8000/v1/score\", json={\"model\": \"jinaai/jina-reranker-m0\", \"text_1\": \"slm markdown\", \"text_2\": {\"content\": [{\"type\": \"image_url\", \"image_url\": {\"url\": \"https://raw.githubusercontent.com/jina-ai/multimodal-reranker-test/main/handelsblatt-preview.png\"}}, {\"type\": \"image_url\", \"image_url\": {\"url\": \"https://raw.githubusercontent.com/jina-ai/multimodal-reranker-test/main/paper-11.png\"}}]}})\nresponse.raise_for_status()\nprint(response.json())"
33 |     ]
34 |   },
35 |   "examples": [
36 |     {
37 |       "use_case": "Deploy a local LLM with vLLM and serve it using the OpenAI-compatible API.",
38 |       "code": "import subprocess\nimport time\n\ndef deploy_local_llm():\n    # Start the vLLM server with a specific model\n    # This example uses the 'meta/llama3-8b' model\n    try:\n        # Run the vLLM serve command\n        process = subprocess.Popen([\n            'vllm', 'serve', \n            'meta/llama3-8b',\n            '--host', '0.0.0.0',\n            '--port', '8000',\n            '--dtype', 'bfloat16'\n        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)\n        \n        # Give the server time to start\n        time.sleep(5)\n        \n        print(f\"vLLM server started with PID: {process.pid}\")\n        print(\"Server is running at http://0.0.0.0:8000/v1/\")\n        \n        # For demonstration purposes, we'll just show the command that would be used\n        print(\"To test the API, use curl:\")\n        print(\"curl http://localhost:8000/v1/completions -H 'Content-Type: application/json' -d '{\\\"prompt\\\": \\\"Hello world\\\", \\\"max_tokens\\\": 10}'\")\n        \n        return process.pid\n    except Exception as e:\n        print(f\"Error starting vLLM server: {e}\")\n        return None\n\n# Deploy the local LLM\nif __name__ == \"__main__\":\n    deploy_local_llm()",
39 |       "explanation": "This code demonstrates how to deploy a local LLM using vLLM with an OpenAI-compatible API. The process involves:\n\n1. Using subprocess.Popen to run the 'vllm serve' command which starts the server\n2. Specifying the model to use ('meta/llama3-8b')\n3. Configuring the server to listen on all interfaces (0.0.0.0) and port 8000\n4. Setting the data type to bfloat16 for efficient inference\n5. Allowing time for the server to initialize before showing usage examples\n6. Providing a curl command example that demonstrates how to interact with the API\n\nThe server will be accessible at http://localhost:8000/v1/ and will support OpenAI-compatible endpoints like /completions.",
40 |       "best_practices": [
41 |         "Always specify the model explicitly when deploying with vLLM",
42 |         "Use appropriate data types (bfloat16, float16) to balance performance and accuracy",
43 |         "Configure the server to listen on specific interfaces for security purposes",
44 |         "Set appropriate timeouts and resource limits for production deployments",
45 |         "Test API endpoints after deployment using curl or similar tools",
46 |         "Monitor server logs for debugging and performance optimization"
47 |       ],
48 |       "imports": [
49 |         "subprocess",
50 |         "time"
51 |       ]
52 |     }
53 |   ]
54 | }
```

vllm-llm_config/generate_examples.py
```
1 | # generate_examples.py
2 | # Purpose: Generate code examples for any learned library
3 | 
4 | from learn_library import fastapi_info, streamlit_info, agent
5 | 
6 | 
7 | def generate_examples_for_library(library_info: dict, library_name: str):
8 |     """Generate code examples for any library based on its documentation."""
9 | 
10 |     # Define generic use cases that can apply to most libraries
11 |     use_cases = [
12 |         {
13 |             "name": "Basic Setup and Hello World",
14 |             "description": f"Create a minimal working example with {library_name}",
15 |             "requirements": "Include installation, imports, and basic usage",
16 |         },
17 |         {
18 |             "name": "Common Operations",
19 |             "description": f"Demonstrate the most common {library_name} operations",
20 |             "requirements": "Show typical workflow and best practices",
21 |         },
22 |         {
23 |             "name": "Advanced Usage",
24 |             "description": f"Create a more complex example showcasing {library_name} capabilities",
25 |             "requirements": "Include error handling and optimization",
26 |         },
27 |     ]
28 | 
29 |     generated_examples = []
30 | 
31 |     print(f"\n🔧 Generating examples for {library_name}...")
32 | 
33 |     for use_case in use_cases:
34 |         print(f"\n📝 {use_case['name']}")
35 |         print(f"Description: {use_case['description']}")
36 | 
37 |         example = agent.generate_example(
38 |             library_info=library_info,
39 |             use_case=use_case["description"],
40 |             requirements=use_case["requirements"],
41 |         )
42 | 
43 |         print("\n💻 Generated Code:")
44 |         print("```python")
45 |         print(example["code"])
46 |         print("```")
47 | 
48 |         print("\n📦 Required Imports:")
49 |         for imp in example["imports"]:
50 |             print(f"  • {imp}")
51 | 
52 |         print("\n📝 Explanation:")
53 |         print(example["explanation"])
54 | 
55 |         print("\n✅ Best Practices:")
56 |         for practice in example["best_practices"]:
57 |             print(f"  • {practice}")
58 | 
59 |         generated_examples.append(
60 |             {
61 |                 "use_case": use_case["name"],
62 |                 "code": example["code"],
63 |                 "imports": example["imports"],
64 |                 "explanation": example["explanation"],
65 |                 "best_practices": example["best_practices"],
66 |             }
67 |         )
68 | 
69 |         print("-" * 80)
70 | 
71 |     return generated_examples
72 | 
73 | 
74 | # Generate examples for both libraries
75 | print("🎯 Generating FastAPI Examples:")
76 | fastapi_examples = generate_examples_for_library(fastapi_info, "FastAPI")
77 | 
78 | print("\n\n🎯 Generating Streamlit Examples:")
79 | streamlit_examples = generate_examples_for_library(streamlit_info, "Streamlit")
```

vllm-llm_config/interactive_learning.py
```
1 | # interactive_learning.py
2 | # Purpose: Run a full interactive session for learning any Python library from docs
3 | 
4 | from main import agent
5 | from typing import Dict
6 | 
7 | 
8 | def learn_any_library(
9 |     library_name: str, documentation_urls: list[str], use_cases: list[str] = None
10 | ):
11 |     """Learn any library from its documentation and generate examples."""
12 | 
13 |     if use_cases is None:
14 |         use_cases = [
15 |             "Basic setup and hello world example",
16 |             "Common operations and workflows",
17 |             "Advanced usage with best practices",
18 |         ]
19 | 
20 |     print(f"🚀 Starting automated learning for {library_name}...")
21 |     print(f"Documentation sources: {len(documentation_urls)} URLs")
22 | 
23 |     try:
24 |         # Step 1: Learn from documentation
25 |         library_info = agent.learn_from_urls(library_name, documentation_urls)
26 | 
27 |         # Step 2: Generate examples for each use case
28 |         all_examples = []
29 | 
30 |         for i, use_case in enumerate(use_cases, 1):
31 |             print(f"\n📝 Generating example {i}/{len(use_cases)}: {use_case}")
32 | 
33 |             example = agent.generate_example(
34 |                 library_info=library_info,
35 |                 use_case=use_case,
36 |                 requirements="Include error handling, comments, and follow best practices",
37 |             )
38 | 
39 |             all_examples.append(
40 |                 {
41 |                     "use_case": use_case,
42 |                     "code": example["code"],
43 |                     "imports": example["imports"],
44 |                     "explanation": example["explanation"],
45 |                     "best_practices": example["best_practices"],
46 |                 }
47 |             )
48 | 
49 |         return {"library_info": library_info, "examples": all_examples}
50 | 
51 |     except Exception as e:
52 |         print(f"❌ Error learning {library_name}: {e}")
53 |         return None
54 | 
55 | 
56 | def interactive_learning_session():
57 |     """Interactive session for learning libraries with user input."""
58 | 
59 |     print("🎯 Welcome to the Interactive Library Learning System!")
60 |     print(
61 |         "This system will help you learn any Python library from its documentation.\n"
62 |     )
63 | 
64 |     learned_libraries = {}
65 | 
66 |     while True:
67 |         print("\n" + "=" * 60)
68 |         print("🚀 LIBRARY LEARNING SESSION")
69 |         print("=" * 60)
70 | 
71 |         # Get library name from user
72 |         library_name = input(
73 |             "\n📚 Enter the library name you want to learn (or 'quit' to exit): "
74 |         ).strip()
75 | 
76 |         if library_name.lower() in ["quit", "exit", "q"]:
77 |             print("\n👋 Thanks for using the Interactive Library Learning System!")
78 |             break
79 | 
80 |         if not library_name:
81 |             print("❌ Please enter a valid library name.")
82 |             continue
83 | 
84 |         # Get documentation URLs
85 |         print(
86 |             f"\n🔗 Enter documentation URLs for {library_name} (one per line, empty line to finish):"
87 |         )
88 |         urls = []
89 |         while True:
90 |             url = input("  URL: ").strip()
91 |             if not url:
92 |                 break
93 |             if not url.startswith(("http://", "https://")):
94 |                 print(
95 |                     "    ⚠️  Please enter a valid URL starting with http:// or https://"
96 |                 )
97 |                 continue
98 |             urls.append(url)
99 | 
100 |         if not urls:
101 |             print("❌ No valid URLs provided. Skipping this library.")
102 |             continue
103 | 
104 |         # Get custom use cases from user
105 |         print(
106 |             f"\n🎯 Define use cases for {library_name} (optional, press Enter for defaults):"
107 |         )
108 |         print(
109 |             "   Default use cases will be: Basic setup, Common operations, Advanced usage"
110 |         )
111 | 
112 |         user_wants_custom = (
113 |             input("   Do you want to define custom use cases? (y/n): ").strip().lower()
114 |         )
115 | 
116 |         use_cases = None
117 |         if user_wants_custom in ["y", "yes"]:
118 |             print("   Enter your use cases (one per line, empty line to finish):")
119 |             use_cases = []
120 |             while True:
121 |                 use_case = input("     Use case: ").strip()
122 |                 if not use_case:
123 |                     break
124 |                 use_cases.append(use_case)
125 | 
126 |             if not use_cases:
127 |                 print("   No custom use cases provided, using defaults.")
128 |                 use_cases = None
129 | 
130 |         # Learn the library
131 |         print(f"\n🚀 Starting learning process for {library_name}...")
132 |         result = learn_any_library(library_name, urls, use_cases)
133 | 
134 |         if result:
135 |             learned_libraries[library_name] = result
136 |             print(f"\n✅ Successfully learned {library_name}!")
137 | 
138 |             # Show summary
139 |             print(f"\n📊 Learning Summary for {library_name}:")
140 |             print(
141 |                 f"   • Core concepts: {len(result['library_info']['core_concepts'])} identified"
142 |             )
143 |             print(
144 |                 f"   • Common patterns: {len(result['library_info']['patterns'])} found"
145 |             )
146 |             print(f"   • Examples generated: {len(result['examples'])}")
147 | 
148 |             # Ask if user wants to see examples
149 |             show_examples = (
150 |                 input(
151 |                     f"\n👀 Do you want to see the generated examples for {library_name}? (y/n): "
152 |                 )
153 |                 .strip()
154 |                 .lower()
155 |             )
156 | 
157 |             if show_examples in ["y", "yes"]:
158 |                 for i, example in enumerate(result["examples"], 1):
159 |                     print(f"\n{'─' * 50}")
160 |                     print(f"📝 Example {i}: {example['use_case']}")
161 |                     print(f"{'─' * 50}")
162 | 
163 |                     print("\n💻 Generated Code:")
164 |                     print("```python")
165 |                     print(example["code"])
166 |                     print("```")
167 | 
168 |                     print(f"\n📦 Required Imports:")
169 |                     for imp in example["imports"]:
170 |                         print(f"  • {imp}")
171 | 
172 |                     print(f"\n📝 Explanation:")
173 |                     print(example["explanation"])
174 | 
175 |                     print(f"\n✅ Best Practices:")
176 |                     for practice in example["best_practices"]:
177 |                         print(f"  • {practice}")
178 | 
179 |                     # Ask if user wants to see the next example
180 |                     if i < len(result["examples"]):
181 |                         continue_viewing = (
182 |                             input(f"\nContinue to next example? (y/n): ")
183 |                             .strip()
184 |                             .lower()
185 |                         )
186 |                         if continue_viewing not in ["y", "yes"]:
187 |                             break
188 | 
189 |             # Offer to save results
190 |             save_results = (
191 |                 input(f"\n💾 Save learning results for {library_name} to file? (y/n): ")
192 |                 .strip()
193 |                 .lower()
194 |             )
195 | 
196 |             if save_results in ["y", "yes"]:
197 |                 filename = input(
198 |                     f"   Enter filename (default: {library_name.lower()}_learning.json): "
199 |                 ).strip()
200 |                 if not filename:
201 |                     filename = f"{library_name.lower()}_learning.json"
202 | 
203 |                 try:
204 |                     import json
205 | 
206 |                     with open(filename, "w") as f:
207 |                         json.dump(result, f, indent=2, default=str)
208 |                     print(f"   ✅ Results saved to {filename}")
209 |                 except Exception as e:
210 |                     print(f"   ❌ Error saving file: {e}")
211 | 
212 |         else:
213 |             print(f"❌ Failed to learn {library_name}")
214 | 
215 |         # Ask if user wants to learn another library
216 |         print(f"\n📚 Libraries learned so far: {list(learned_libraries.keys())}")
217 |         continue_learning = (
218 |             input("\n🔄 Do you want to learn another library? (y/n): ").strip().lower()
219 |         )
220 | 
221 |         if continue_learning not in ["y", "yes"]:
222 |             break
223 | 
224 |     # Final summary
225 |     if learned_libraries:
226 |         print(f"\n🎉 Session Summary:")
227 |         print(f"Successfully learned {len(learned_libraries)} libraries:")
228 |         for lib_name, info in learned_libraries.items():
229 |             print(f"  • {lib_name}: {len(info['examples'])} examples generated")
230 | 
231 |     return learned_libraries
232 | 
233 | 
234 | # Example: Run interactive learning session
235 | if __name__ == "__main__":
236 |     # Run interactive session
237 |     learned_libraries = interactive_learning_session()
```

vllm-llm_config/learn_library.py
```
1 | # learn_library.py
2 | # Purpose: Utility to learn any library from a set of documentation URLs using the agent
3 | 
4 | from main import agent  # Import the previously defined agent
5 | from typing import Dict
6 | 
7 | 
8 | def learn_library_from_urls(library_name: str, documentation_urls: list[str]) -> Dict:
9 |     """Learn about any library from its documentation URLs."""
10 | 
11 |     try:
12 |         library_info = agent.learn_from_urls(library_name, documentation_urls)
13 | 
14 |         print(f"\n🔍 Library Analysis Results for {library_name}:")
15 |         print(f"Sources: {len(library_info['source_urls'])} successful fetches")
16 |         print(f"Core Concepts: {library_info['core_concepts']}")
17 |         print(f"Common Patterns: {library_info['patterns']}")
18 |         print(f"Key Methods: {library_info['methods']}")
19 |         print(f"Installation: {library_info['installation']}")
20 |         print(f"Found {len(library_info['examples'])} code examples")
21 | 
22 |         return library_info
23 | 
24 |     except Exception as e:
25 |         print(f"❌ Error learning library: {e}")
26 |         raise
27 | 
28 | 
29 | # Example 1: Learn FastAPI from official documentation
30 | fastapi_urls = [
31 |     "https://fastapi.tiangolo.com/",
32 |     "https://fastapi.tiangolo.com/tutorial/first-steps/",
33 |     "https://fastapi.tiangolo.com/tutorial/path-params/",
34 |     "https://fastapi.tiangolo.com/tutorial/query-params/",
35 | ]
36 | 
37 | print("🚀 Learning FastAPI from official documentation...")
38 | fastapi_info = learn_library_from_urls("FastAPI", fastapi_urls)
39 | 
40 | # Example 2: Learn a different library (you can replace with any library)
41 | streamlit_urls = [
42 |     "https://docs.streamlit.io/",
43 |     "https://docs.streamlit.io/get-started",
44 |     "https://docs.streamlit.io/develop/api-reference",
45 | ]
46 | 
47 | print("\n\n📊 Learning Streamlit from official documentation...")
48 | streamlit_info = learn_library_from_urls("Streamlit", streamlit_urls)
```

vllm-llm_config/litellm_learning.json
```
1 | {
2 |   "library_info": {
3 |     "library": "litellm",
4 |     "source_urls": [
5 |       "https://github.com/BerriAI/litellm"
6 |     ],
7 |     "core_concepts": [
8 |       "LiteLLM Proxy",
9 |       "API Key Authentication",
10 |       "Custom Authentication",
11 |       "FastAPI FastAPI"
12 |     ],
13 |     "patterns": [
14 |       "Authentication using API keys",
15 |       "User-defined authentication logic",
16 |       "Asynchronous key generation decisions",
17 |       "Environment variable management"
18 |     ],
19 |     "methods": [
20 |       "user_api_key_auth",
21 |       "generate_key_fn"
22 |     ],
23 |     "installation": "The installation of litellm proxy example_config_yaml custom_auth.py is not directly related to the JSON object, as it's a Python file that contains authentication logic for LiteLLM Proxy.",
24 |     "examples": [
25 |       "async def user_api_key_auth(request: Request, api_key: str) -> UserAPIKeyAuth",
26 |       "async def generate_key_fn(data: GenerateKeyRequest)",
27 |       "async def make_completions():",
28 |       "async def custom_auth_example_usage()"
29 |     ]
30 |   },
31 |   "examples": [
32 |     {
33 |       "use_case": "Route OpenAI-compatible API requests to different LLM providers using LiteLLM.",
34 |       "code": "from fastapi import FastAPI, HTTPException\nimport litellm\nfrom litellm.proxy.auth import user_api_key_auth, generate_key_fn\nimport os\n\napp = FastAPI()\n\n@app.post(\"/auth\")\nasync def authenticate_user(api_key: str):\n    try:\n        response = await user_api_key_auth(api_key)\n        return response\n    except Exception as e:\n        raise HTTPException(status_code=401, detail=str(e))\n\n@app.post(\"/generate-key\")\nasync def generate_api_key():\n    key = await generate_key_fn()\n    return {\"api_key\": key}\n\n# Example endpoint for OpenAI-compatible requests\n@app.post(\"/openai/chat/completions\")\nasync def chat_completions(messages: list):\n    response = litellm.chat.completions.create(\n        model=\"gpt-4\",\n        messages=messages,\n        api_key=os.getenv(\"API_KEY\")\n    )\n    return response",
35 |       "explanation": "This code example demonstrates authentication using LiteLLM proxy methods. First, we import FastAPI and necessary authentication functions from litellm.proxy.auth. Then we define routes for user authentication (POST /auth) and API key generation (POST /generate-key). The authentication logic validates API keys against the proxy system, while generating API keys allows users to create secure access tokens. Finally, an OpenAI-compatible chat completion endpoint is defined that uses LiteLLM's chat functionality.",
36 |       "best_practices": [
37 |         "Use environment variables for API key management",
38 |         "Implement asynchronous authentication decisions",
39 |         "Validate user credentials before routing requests",
40 |         "Generate secure API keys with appropriate permissions"
41 |       ],
42 |       "imports": [
43 |         "fastapi",
44 |         "litellm.proxy.auth",
45 |         "os"
46 |       ]
47 |     }
48 |   ]
49 | }
```

vllm-llm_config/main.py
```
1 | # main.py
2 | # Purpose: Automated documentation-powered code generation pipeline using DSPy.
3 | # Now with integrated GitHub repository analysis.
4 | 
5 | import dspy
6 | import requests
7 | from bs4 import BeautifulSoup
8 | import html2text
9 | from typing import List, Dict, Any
10 | import json
11 | import time
12 | 
13 | # Import the GitHub helper functions
14 | from repo_helpers import gather_repository_info
15 | 
16 | # --- DSPy Configuration ---
17 | # Replace with your actual LM provider if not using a local one
18 |     # For models like Llama
19 | lm = dspy.LM(
20 |     "ollama_chat/hf.co/unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF:Q3_K_XL_XXS",
21 |     api_base="http://localhost:11434",  # Local Ollama server URL
22 |     api_key="EMPTY",  # Usually empty for local Ollama; remove if you do not have a key
23 |     streaming=False,
24 |     response_format={
25 |         "type": "json_schema",
26 |         "json_schema": {
27 |             "schema": {
28 |                 "type": "object",
29 |                 "properties": {
30 |                     "project": {
31 |                         "type": "object",
32 |                         "properties": {
33 |                             "name": {"type": "string"},
34 |                             "description": {"type": "string"},
35 |                         },
36 |                         "required": ["name", "description"],
37 |                     },
38 |                     "key_concepts": {
39 |                         "type": "array",
40 |                         "items": {"type": "string"},
41 |                         "minItems": 1,
42 |                     },
43 |                     "architecture_overview": {"type": "string"},
44 |                     "important_directories": {
45 |                         "type": "array",
46 |                         "items": {"type": "string"},
47 |                         "minItems": 1,
48 |                     },
49 |                     "entry_points": {
50 |                         "type": "array",
51 |                         "items": {"type": "string"},
52 |                         "minItems": 1,
53 |                     },
54 |                     "development_info": {
55 |                         "type": "object",
56 |                         "properties": {
57 |                             "test_dependencies": {
58 |                                 "type": "array",
59 |                                 "items": {"type": "string"},
60 |                                 "minItems": 1,
61 |                             },
62 |                             "linting_tools": {
63 |                                 "type": "array",
64 |                                 "items": {"type": "string"},
65 |                                 "minItems": 1,
66 |                             },
67 |                             "optional_dependencies": {
68 |                                 "type": "array",
69 |                                 "items": {"type": "string"},
70 |                             },
71 |                         },
72 |                         "required": ["test_dependencies", "linting_tools"],
73 |                     },
74 |                     "usage_examples": {
75 |                         "type": "array",
76 |                         "items": {"type": "string"},
77 |                         "minItems": 1,
78 |                     },
79 |                 },
80 |                 "required": [
81 |                     "project",
82 |                     "key_concepts",
83 |                     "architecture_overview",
84 |                     "important_directories",
85 |                     "entry_points",
86 |                     "development_info",
87 |                     "usage_examples",
88 |                 ],
89 |             }
90 |         },
91 |     },
92 | )
93 | dspy.configure(lm=lm)
94 | 
95 | 
96 | # --- Data Fetching Classes ---
97 | 
98 | 
99 | class DocumentationFetcher:
100 |     """
101 |     Fetches and processes documentation from both standard URLs and GitHub repositories.
102 |     """
103 | 
104 |     def __init__(self, max_retries=3, delay=1):
105 |         self.session = requests.Session()
106 |         self.session.headers.update(
107 |             {
108 |                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
109 |             }
110 |         )
111 |         self.max_retries = max_retries
112 |         self.delay = delay
113 |         self.html_converter = html2text.HTML2Text()
114 |         self.html_converter.ignore_links = False
115 |         self.html_converter.ignore_images = True
116 | 
117 |     def fetch_website_url(self, url: str) -> dict:
118 |         """Fetches and cleans content from a standard website URL."""
119 |         for attempt in range(self.max_retries):
120 |             try:
121 |                 print(f"📡 Fetching Website: {url} (attempt {attempt + 1})")
122 |                 response = self.session.get(url, timeout=15)
123 |                 response.raise_for_status()
124 |                 soup = BeautifulSoup(response.content, "html.parser")
125 |                 for script in soup(["script", "style", "nav", "footer", "header"]):
126 |                     script.decompose()
127 |                 markdown_content = self.html_converter.handle(str(soup))
128 |                 return {
129 |                     "url": url,
130 |                     "title": soup.title.string if soup.title else "No title",
131 |                     "content": markdown_content,
132 |                     "success": True,
133 |                 }
134 |             except Exception as e:
135 |                 print(f"❌ Error fetching {url}: {e}")
136 |                 if attempt < self.max_retries - 1:
137 |                     time.sleep(self.delay)
138 |         return {"url": url, "title": "Failed to fetch", "content": "", "success": False}
139 | 
140 |     def fetch_github_repo(self, url: str) -> dict:
141 |         """Fetches and consolidates content from a GitHub repository."""
142 |         print(f"📦 Fetching GitHub Repo: {url}")
143 |         try:
144 |             # Use the helper function to get README and example files
145 |             combined_content, details = gather_repository_info(url)
146 |             if "Could not access" in combined_content:
147 |                 return {
148 |                     "url": url,
149 |                     "title": "Failed to fetch repo",
150 |                     "content": "",
151 |                     "success": False,
152 |                 }
153 | 
154 |             return {
155 |                 "url": url,
156 |                 "title": f"GitHub Repo: {url.split('/')[-1]}",
157 |                 "content": combined_content,
158 |                 "success": True,
159 |                 "details": details,
160 |             }
161 |         except Exception as e:
162 |             print(f"❌ Error fetching GitHub repo {url}: {e}")
163 |             return {
164 |                 "url": url,
165 |                 "title": "Failed to fetch repo",
166 |                 "content": f"Error: {e}",
167 |                 "success": False,
168 |             }
169 | 
170 |     def fetch_documentation(self, urls: list[str]) -> list[dict]:
171 |         """
172 |         Fetches documentation from a list of URLs, routing to the correct
173 |         fetcher (website or GitHub) based on the URL.
174 |         """
175 |         results = []
176 |         for url in urls:
177 |             if "github.com" in url:
178 |                 result = self.fetch_github_repo(url)
179 |             else:
180 |                 result = self.fetch_website_url(url)
181 | 
182 |             results.append(result)
183 |             time.sleep(self.delay)  # Be respectful to servers
184 |         return results
185 | 
186 | 
187 | # --- DSPy Signatures and Modules ---
188 | 
189 | 
190 | class LibraryAnalyzer(dspy.Signature):
191 |     """Analyze library documentation to understand core concepts, patterns, and examples."""
192 | 
193 |     library_name: str = dspy.InputField(desc="Name of the library to analyze")
194 |     documentation_content: str = dspy.InputField(
195 |         desc="Combined documentation from websites, READMEs, and code examples"
196 |     )
197 | 
198 |     core_concepts: list[str] = dspy.OutputField(
199 |         desc="Main concepts, classes, and components of the library."
200 |     )
201 |     common_patterns: list[str] = dspy.OutputField(
202 |         desc="Common usage patterns or workflows."
203 |     )
204 |     key_methods: list[str] = dspy.OutputField(
205 |         desc="List of important methods or functions and their purpose."
206 |     )
207 |     installation_info: str = dspy.OutputField(
208 |         desc="How to install the library (e.g., 'pip install ...')."
209 |     )
210 |     code_examples: list[str] = dspy.OutputField(
211 |         desc="Key code snippets found in the documentation."
212 |     )
213 | 
214 | 
215 | class CodeGenerator(dspy.Signature):
216 |     """Generate a complete, working code example for a specific use case."""
217 | 
218 |     library_info: str = dspy.InputField(
219 |         desc="Summary of the library's concepts, patterns, and methods."
220 |     )
221 |     use_case: str = dspy.InputField(
222 |         desc="The specific task to accomplish with the code."
223 |     )
224 |     requirements: str = dspy.InputField(
225 |         desc="Additional requirements or constraints for the code."
226 |     )
227 | 
228 |     code_example: str = dspy.OutputField(
229 |         desc="A single, complete, and runnable code block."
230 |     )
231 |     explanation: str = dspy.OutputField(
232 |         desc="A step-by-step explanation of the generated code."
233 |     )
234 |     best_practices: list[str] = dspy.OutputField(
235 |         desc="Tips and best practices for using the library."
236 |     )
237 |     imports_needed: list[str] = dspy.OutputField(
238 |         desc="A list of necessary import statements."
239 |     )
240 | 
241 | 
242 | class DocumentationLearningAgent(dspy.Module):
243 |     """Agent that learns from documentation and generates code."""
244 | 
245 |     def __init__(self):
246 |         super().__init__()
247 |         self.fetcher = DocumentationFetcher()
248 |         self.analyze_docs = dspy.ChainOfThought(LibraryAnalyzer)
249 |         self.generate_code = dspy.ChainOfThought(CodeGenerator)
250 | 
251 |     def learn_from_urls(self, library_name: str, doc_urls: list[str]) -> Dict:
252 |         """Learns about a library from documentation URLs and GitHub repos."""
253 |         print(f"📚 Learning about {library_name} from {len(doc_urls)} sources...")
254 |         docs = self.fetcher.fetch_documentation(doc_urls)
255 | 
256 |         combined_content = "\n\n---\n\n".join(
257 |             [
258 |                 f"SOURCE: {doc['url']}\n\n{doc['content']}"
259 |                 for doc in docs
260 |                 if doc["success"]
261 |             ]
262 |         )
263 | 
264 |         if not combined_content:
265 |             raise ValueError("No documentation could be fetched successfully.")
266 | 
267 |         analysis = self.analyze_docs(
268 |             library_name=library_name, documentation_content=combined_content
269 |         )
270 | 
271 |         return {
272 |             "library": library_name,
273 |             "source_urls": [doc["url"] for doc in docs if doc["success"]],
274 |             "core_concepts": analysis.core_concepts,
275 |             "patterns": analysis.common_patterns,
276 |             "methods": analysis.key_methods,
277 |             "installation": analysis.installation_info,
278 |             "examples": analysis.code_examples,
279 |         }
280 | 
281 |     def generate_example(
282 |         self, library_info: Dict, use_case: str, requirements: str = ""
283 |     ) -> Dict:
284 |         """Generates a code example for a specific use case."""
285 |         info_text = f"""
286 |         Library: {library_info["library"]}
287 |         Core Concepts: {", ".join(library_info["core_concepts"])}
288 |         Common Patterns: {", ".join(library_info["patterns"])}
289 |         Key Methods: {", ".join(library_info["methods"])}
290 |         Installation: {library_info["installation"]}
291 |         """
292 | 
293 |         code_result = self.generate_code(
294 |             library_info=info_text, use_case=use_case, requirements=requirements
295 |         )
296 | 
297 |         return {
298 |             "code": code_result.code_example,
299 |             "explanation": code_result.explanation,
300 |             "best_practices": code_result.best_practices,
301 |             "imports": code_result.imports_needed,
302 |         }
303 | 
304 | 
305 | # --- Interactive Session Logic ---
306 | 
307 | 
308 | def interactive_learning_session():
309 |     """Main interactive session for the library learning system."""
310 |     print("🎯 Welcome to the Interactive Library Learning System!")
311 |     print("This system now supports learning from websites AND GitHub repositories.\n")
312 | 
313 |     agent = DocumentationLearningAgent()
314 |     learned_libraries = {}
315 | 
316 |     while True:
317 |         print("\n" + "=" * 60)
318 |         library_name = input(
319 |             "\n📚 Enter the library name (or 'quit' to exit): "
320 |         ).strip()
321 |         if library_name.lower() in ["quit", "exit", "q"]:
322 |             break
323 | 
324 |         print(
325 |             f"\n🔗 Enter documentation URLs or a GitHub repo URL for {library_name} (one per line, empty line to finish):"
326 |         )
327 |         urls = []
328 |         while True:
329 |             url = input("  URL: ").strip()
330 |             if not url:
331 |                 break
332 |             urls.append(url)
333 | 
334 |         if not urls:
335 |             continue
336 | 
337 |         try:
338 |             # Step 1: Learn about the library from the provided sources
339 |             library_info = agent.learn_from_urls(library_name, urls)
340 |             print(f"\n✅ Successfully learned {library_name}!")
341 |             print(f"   - Core Concepts: {library_info.get('core_concepts', 'N/A')}")
342 |             print(f"   - Installation: {library_info.get('installation', 'N/A')}")
343 | 
344 |             # Step 2: Get all use cases from the user upfront
345 |             print(
346 |                 f"\n🎯 Define use cases for {library_name} (one per line, empty line to finish):"
347 |             )
348 |             use_cases = []
349 |             while True:
350 |                 use_case = input("     Use case: ").strip()
351 |                 if not use_case:
352 |                     break
353 |                 use_cases.append(use_case)
354 | 
355 |             if not use_cases:
356 |                 print("No use cases provided. Moving on.")
357 |                 continue
358 | 
359 |             # Step 3: Generate and display all examples
360 |             print(f"\n🔧 Generating {len(use_cases)} examples for {library_name}...")
361 |             all_examples = []
362 |             for i, use_case in enumerate(use_cases, 1):
363 |                 print(f"\n--- EXAMPLE {i}/{len(use_cases)}: {use_case} ---")
364 | 
365 |                 example = agent.generate_example(library_info, use_case)
366 |                 all_examples.append({"use_case": use_case, **example})
367 | 
368 |                 print("\n💻 Code Example:")
369 |                 print(f"```python\n{example['code']}\n```")
370 | 
371 |                 print("\n📦 Required Imports:")
372 |                 print("\n".join([f"  • {imp}" for imp in example["imports"]]))
373 | 
374 |                 print("\n📝 Explanation:")
375 |                 print(example["explanation"])
376 | 
377 |                 print("\n✅ Best Practices:")
378 |                 print("\n".join([f"  • {bp}" for bp in example["best_practices"]]))
379 |                 print("--- END OF EXAMPLE ---")
380 | 
381 |             # Store the complete results
382 |             learned_libraries[library_name] = {
383 |                 "library_info": library_info,
384 |                 "examples": all_examples,
385 |             }
386 | 
387 |             # Step 4: Offer to save the results to a file
388 |             save_results = (
389 |                 input(f"\n💾 Save learning results for {library_name} to file? (y/n): ")
390 |                 .strip()
391 |                 .lower()
392 |             )
393 |             if save_results in ["y", "yes"]:
394 |                 filename = input(
395 |                     f"   Enter filename (default: {library_name.lower()}_learning.json): "
396 |                 ).strip()
397 |                 if not filename:
398 |                     filename = f"{library_name.lower()}_learning.json"
399 | 
400 |                 try:
401 |                     with open(filename, "w", encoding="utf-8") as f:
402 |                         json.dump(
403 |                             learned_libraries[library_name], f, indent=2, default=str
404 |                         )
405 |                     print(f"   ✅ Results saved to {filename}")
406 |                 except Exception as e:
407 |                     print(f"   ❌ Error saving file: {e}")
408 | 
409 |         except Exception as e:
410 |             print(f"❌ An error occurred while learning {library_name}: {e}")
411 | 
412 |     print("\n👋 Thanks for using the Interactive Library Learning System!")
413 |     if learned_libraries:
414 |         print(f"\n🎉 Session Summary:")
415 |         print(
416 |             f"Successfully learned {len(learned_libraries)} libraries: {list(learned_libraries.keys())}"
417 |         )
418 | 
419 | 
420 | if __name__ == "__main__":
421 |     interactive_learning_session()
```

vllm-llm_config/repo_helpers.py
```
1 | # repo_helpers.py
2 | # Contains functions for interacting with the GitHub API.
3 | 
4 | import requests
5 | from dotenv import load_dotenv
6 | import os
7 | import base64
8 | 
9 | # Load environment variables from a .env file
10 | load_dotenv()
11 | 
12 | 
13 | def get_github_file_tree(repo_url):
14 |     """Get repository file structure from the GitHub API."""
15 |     token = os.getenv("GITHUB_ACCESS_TOKEN")
16 |     parts = repo_url.strip("/").split("/")
17 |     owner, repo = parts[-2], parts[-1]
18 | 
19 |     api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
20 |     headers = {"Authorization": f"Bearer {token}"} if token else {}
21 | 
22 |     print(f"🌳 Fetching file tree for {owner}/{repo}...")
23 |     response = requests.get(api_url, headers=headers)
24 | 
25 |     if response.status_code == 200:
26 |         tree_data = response.json()
27 |         # Filter for files (blobs) only
28 |         file_paths = [
29 |             item["path"] for item in tree_data.get("tree", []) if item["type"] == "blob"
30 |         ]
31 |         return "\n".join(sorted(file_paths))
32 |     else:
33 |         print(
34 |             f"⚠️  Could not fetch repository tree (Status: {response.status_code}): {response.text}"
35 |         )
36 |         return "Could not fetch repository file tree."
37 | 
38 | 
39 | def get_github_file_content(repo_url, file_path):
40 |     """Get specific file content from a GitHub repository."""
41 |     token = os.getenv("GITHUB_ACCESS_TOKEN")
42 |     parts = repo_url.strip("/").split("/")
43 |     owner, repo = parts[-2], parts[-1]
44 | 
45 |     api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
46 |     headers = {"Authorization": f"Bearer {token}"} if token else {}
47 | 
48 |     response = requests.get(api_url, headers=headers)
49 | 
50 |     if response.status_code == 200:
51 |         content = base64.b64decode(response.json()["content"]).decode("utf-8")
52 |         return content
53 |     else:
54 |         return f"Could not fetch {file_path}"
55 | 
56 | 
57 | def gather_repository_info(repo_url):
58 |     """
59 |     Gathers the file tree, README, and example files from a repository.
60 |     Focuses on README for overview and Python/Jupyter files for examples.
61 |     """
62 |     print(f"🔍 Gathering information from repository: {repo_url}")
63 |     file_tree_str = get_github_file_tree(repo_url)
64 | 
65 |     if "Could not fetch" in file_tree_str:
66 |         return "Could not access repository.", {}
67 | 
68 |     readme_content = get_github_file_content(repo_url, "README.md")
69 | 
70 |     # --- Find and fetch example files ---
71 |     example_files = {}
72 |     file_paths = file_tree_str.split("\n")
73 | 
74 |     # Look for common example directories or files
75 |     example_keywords = ["examples", "example", "docs", "samples", "tutorial"]
76 |     py_files = [p for p in file_paths if p.endswith(".py")]
77 |     ipynb_files = [p for p in file_paths if p.endswith(".ipynb")]
78 | 
79 |     # Prioritize files in example-related directories
80 |     potential_examples = [
81 |         p
82 |         for p in py_files + ipynb_files
83 |         if any(keyword in p.lower() for keyword in example_keywords)
84 |     ]
85 | 
86 |     # If not enough found, take a few from the root
87 |     if len(potential_examples) < 5:
88 |         potential_examples.extend(
89 |             [p for p in py_files if "/" not in p][:5]
90 |         )  # Top-level python files
91 | 
92 |     # Fetch content for a limited number of examples to avoid being overwhelming
93 |     for i, file_path in enumerate(
94 |         list(set(potential_examples))[:5]
95 |     ):  # Limit to 5 unique examples
96 |         print(f"📄 Fetching example file: {file_path}")
97 |         content = get_github_file_content(repo_url, file_path)
98 |         if "Could not fetch" not in content:
99 |             example_files[file_path] = content
100 | 
101 |     # --- Combine all info into a single string for the LLM ---
102 |     combined_content = f"# REPOSITORY OVERVIEW: {repo_url}\n\n"
103 |     combined_content += "## README.md\n\n" + readme_content + "\n\n---\n\n"
104 | 
105 |     if example_files:
106 |         combined_content += "## CODE EXAMPLES\n\n"
107 |         for path, code in example_files.items():
108 |             combined_content += f"### File: {path}\n\n```python\n{code}\n```\n\n"
109 | 
110 |     return combined_content, {"file_tree": file_tree_str, **example_files}
```
