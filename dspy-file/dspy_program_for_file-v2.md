# Writing a dspy program for file inference

Based on the DSPy documentation and tutorials, I'll show you how to create a DSPy program that performs inference on a single file instead of processing an entire repository. The key is to structure your program with appropriate signatures and modules that take file content as input.

Here's a complete example of a DSPy program that analyzes a single file and performs inference on it:

```python
import dspy
import os
from typing import List, Optional

# Configure DSPy with your preferred language model
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"  # Replace with your actual key
lm = dspy.LM(model="openai/gpt-4o-mini")
dspy.settings.configure(lm=lm)

# Define signatures for different aspects of file analysis
class FileAnalysis(dspy.Signature):
    """Analyze the structure and content of a code file."""
    file_path: str = dspy.InputField(desc="Path to the file being analyzed")
    file_content: str = dspy.InputField(desc="Complete content of the file")
    file_extension: str = dspy.InputField(desc="File extension (e.g., .py, .js, .md)")

    file_type: str = dspy.OutputField(desc="Type of file (code, documentation, config, etc.)")
    main_purpose: str = dspy.OutputField(desc="Primary purpose or function of this file")
    key_components: List[str] = dspy.OutputField(desc="Main components, classes, or functions")
    dependencies: List[str] = dspy.OutputField(desc="External dependencies or imports")

class CodeQualityAssessment(dspy.Signature):
    """Assess code quality and provide recommendations."""
    file_content: str = dspy.InputField(desc="The code content to analyze")
    file_type: str = dspy.InputField(desc="Type of file being analyzed")
    language: str = dspy.InputField(desc="Programming language")

    quality_score: int = dspy.OutputField(desc="Quality score from 1-10")
    strengths: List[str] = dspy.OutputField(desc="What the code does well")
    issues: List[str] = dspy.OutputField(desc="Potential issues or improvements")
    recommendations: List[str] = dspy.OutputField(desc="Specific recommendations for improvement")

class DocumentationSummary(dspy.Signature):
    """Generate a summary of what the file does."""
    file_path: str = dspy.InputField(desc="File path")
    analysis: str = dspy.InputField(desc="Analysis results from file analysis")
    quality_assessment: str = dspy.InputField(desc="Quality assessment results")

    summary: str = dspy.OutputField(desc="Concise summary of the file's purpose and functionality")
    usage_examples: List[str] = dspy.OutputField(desc="Example usage patterns if applicable")

# Create the main DSPy module
class FileAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.file_analysis = dspy.ChainOfThought(FileAnalysis)
        self.quality_assessment = dspy.ChainOfThought(CodeQualityAssessment)
        self.documentation = dspy.ChainOfThought(DocumentationSummary)

    def forward(self, file_path: str, file_content: str):
        # Extract file extension for context
        file_extension = os.path.splitext(file_path)[1].lower()

        # Determine language based on extension
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.md': 'Markdown',
            '.txt': 'Plain Text',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML'
        }
        language = language_map.get(file_extension, 'Unknown')

        # Step 1: Analyze file structure and content
        analysis = self.file_analysis(
            file_path=file_path,
            file_content=file_content,
            file_extension=file_extension
        )

        # Step 2: Assess code quality (skip for non-code files)
        if analysis.file_type in ['code', 'script', 'module']:
            quality = self.quality_assessment(
                file_content=file_content,
                file_type=analysis.file_type,
                language=language
            )
        else:
            quality = dspy.Prediction(
                quality_score=0,
                strengths=["Not applicable for non-code files"],
                issues=[],
                recommendations=[]
            )

        # Step 3: Generate documentation summary
        summary = self.documentation(
            file_path=file_path,
            analysis=f"Type: {analysis.file_type}\nPurpose: {analysis.main_purpose}\nComponents: {', '.join(analysis.key_components)}\nDependencies: {', '.join(analysis.dependencies)}",
            quality_assessment=f"Score: {quality.quality_score}/10\nStrengths: {', '.join(quality.strengths)}\nIssues: {', '.join(quality.issues)}"
        )

        return dspy.Prediction(
            file_analysis=analysis,
            quality_assessment=quality,
            documentation=summary
        )

# Helper function to read a file
def read_file_content(file_path: str) -> str:
    """Read the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Main function to analyze a single file
def analyze_file(file_path: str):
    """
    Analyze a single file using DSPy inference.

    Args:
        file_path (str): Path to the file to analyze
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Read file content
    file_content = read_file_content(file_path)

    if file_content.startswith("Error reading file:"):
        print(file_content)
        return

    # Initialize the analyzer
    analyzer = FileAnalyzer()

    print(f"Analyzing file: {file_path}")
    print("=" * 50)

    try:
        # Run the analysis
        result = analyzer(file_path=file_path, file_content=file_content)

        # Display results
        print("📁 FILE ANALYSIS:")
        print(f"Type: {result.file_analysis.file_type}")
        print(f"Purpose: {result.file_analysis.main_purpose}")
        print(f"Key Components: {', '.join(result.file_analysis.key_components)}")
        print(f"Dependencies: {', '.join(result.file_analysis.dependencies)}")

        if result.quality_assessment.quality_score > 0:
            print("
⭐ QUALITY ASSESSMENT:"            print(f"Score: {result.quality_assessment.quality_score}/10")
            print(f"Strengths: {', '.join(result.quality_assessment.strengths)}")
            print(f"Issues: {', '.join(result.quality_assessment.issues)}")
            print(f"Recommendations: {', '.join(result.quality_assessment.recommendations)}")

        print("
📝 SUMMARY:"        print(result.documentation.summary)

        if result.documentation.usage_examples:
            print("
💡 USAGE EXAMPLES:"            for i, example in enumerate(result.documentation.usage_examples, 1):
                print(f"{i}. {example}")

    except Exception as e:
        print(f"Error during analysis: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Analyze the current file itself as an example
    analyze_file(__file__)

    # You can also analyze other files:
    # analyze_file("path/to/your/file.py")
    # analyze_file("README.md")
    # analyze_file("config.json")
```

## Key Differences from Repository-Based Programs

1. **Input Focus**: Instead of processing multiple files or a repository structure, this program takes a single file path and its content as input.

2. **Signatures**: The signatures are designed around file-level analysis rather than repository-level analysis:
   - `FileAnalysis`: Analyzes the structure and purpose of a single file
   - `CodeQualityAssessment`: Evaluates code quality for programming files
   - `DocumentationSummary`: Generates a summary of what the file does

3. **Modular Processing**: The program processes one file at a time, making it suitable for targeted analysis rather than bulk repository processing.

4. **File Type Handling**: The program intelligently handles different file types (code, documentation, config, etc.) and adjusts its analysis approach accordingly.

## How to Use This Program

1. **Set up your API key**: Replace `"your-openai-api-key-here"` with your actual OpenAI API key.

2. **Run the analysis**:

   ```python
   # Analyze a Python file
   analyze_file("my_script.py")

   # Analyze a README
   analyze_file("README.md")

   # Analyze a config file
   analyze_file("config.json")
   ```

3. **Adapt for your needs**: Modify the signatures and analysis logic to focus on the specific type of inference you want to perform on files (code review, documentation generation, security analysis, etc.).

This approach gives you the flexibility to perform sophisticated AI-powered analysis on individual files while maintaining the structured, modular nature of DSPy programs.

```python
import dspy
import os
from typing import List, Optional

# Configure DSPy with your preferred language model
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"  # Replace with your actual key
lm = dspy.LM(model="openai/gpt-4o-mini")
dspy.settings.configure(lm=lm)

# Define signatures for different aspects of file analysis
class FileAnalysis(dspy.Signature):
    """Analyze the structure and content of a code file."""
    file_path: str = dspy.InputField(desc="Path to the file being analyzed")
    file_content: str = dspy.InputField(desc="Complete content of the file")
    file_extension: str = dspy.InputField(desc="File extension (e.g., .py, .js, .md)")

    file_type: str = dspy.OutputField(desc="Type of file (code, documentation, config, etc.)")
    main_purpose: str = dspy.OutputField(desc="Primary purpose or function of this file")
    key_components: List[str] = dspy.OutputField(desc="Main components, classes, or functions")
    dependencies: List[str] = dspy.OutputField(desc="External dependencies or imports")

class CodeQualityAssessment(dspy.Signature):
    """Assess code quality and provide recommendations."""
    file_content: str = dspy.InputField(desc="The code content to analyze")
    file_type: str = dspy.InputField(desc="Type of file being analyzed")
    language: str = dspy.InputField(desc="Programming language")

    quality_score: int = dspy.OutputField(desc="Quality score from 1-10")
    strengths: List[str] = dspy.OutputField(desc="What the code does well")
    issues: List[str] = dspy.OutputField(desc="Potential issues or improvements")
    recommendations: List[str] = dspy.OutputField(desc="Specific recommendations for improvement")

class DocumentationSummary(dspy.Signature):
    """Generate a summary of what the file does."""
    file_path: str = dspy.InputField(desc="File path")
    analysis: str = dspy.InputField(desc="Analysis results from file analysis")
    quality_assessment: str = dspy.InputField(desc="Quality assessment results")

    summary: str = dspy.OutputField(desc="Concise summary of the file's purpose and functionality")
    usage_examples: List[str] = dspy.OutputField(desc="Example usage patterns if applicable")

# Create the main DSPy module
class FileAnalyzer(dspy.Module):
    def __init__(self):
        super().__init__()
        self.file_analysis = dspy.ChainOfThought(FileAnalysis)
        self.quality_assessment = dspy.ChainOfThought(CodeQualityAssessment)
        self.documentation = dspy.ChainOfThought(DocumentationSummary)

    def forward(self, file_path: str, file_content: str):
        # Extract file extension for context
        file_extension = os.path.splitext(file_path)[1].lower()

        # Determine language based on extension
        language_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.php': 'PHP',
            '.rb': 'Ruby',
            '.md': 'Markdown',
            '.txt': 'Plain Text',
            '.json': 'JSON',
            '.yaml': 'YAML',
            '.yml': 'YAML'
        }
        language = language_map.get(file_extension, 'Unknown')

        # Step 1: Analyze file structure and content
        analysis = self.file_analysis(
            file_path=file_path,
            file_content=file_content,
            file_extension=file_extension
        )

        # Step 2: Assess code quality (skip for non-code files)
        if analysis.file_type in ['code', 'script', 'module']:
            quality = self.quality_assessment(
                file_content=file_content,
                file_type=analysis.file_type,
                language=language
            )
        else:
            quality = dspy.Prediction(
                quality_score=0,
                strengths=["Not applicable for non-code files"],
                issues=[],
                recommendations=[]
            )

        # Step 3: Generate documentation summary
        summary = self.documentation(
            file_path=file_path,
            analysis=f"Type: {analysis.file_type}\nPurpose: {analysis.main_purpose}\nComponents: {', '.join(analysis.key_components)}\nDependencies: {', '.join(analysis.dependencies)}",
            quality_assessment=f"Score: {quality.quality_score}/10\nStrengths: {', '.join(quality.strengths)}\nIssues: {', '.join(quality.issues)}"
        )

        return dspy.Prediction(
            file_analysis=analysis,
            quality_assessment=quality,
            documentation=summary
        )

# Helper function to read a file
def read_file_content(file_path: str) -> str:
    """Read the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Main function to analyze a single file
def analyze_file(file_path: str):
    """
    Analyze a single file using DSPy inference.

    Args:
        file_path (str): Path to the file to analyze
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Read file content
    file_content = read_file_content(file_path)

    if file_content.startswith("Error reading file:"):
        print(file_content)
        return

    # Initialize the analyzer
    analyzer = FileAnalyzer()

    print(f"Analyzing file: {file_path}")
    print("=" * 50)

    try:
        # Run the analysis
        result = analyzer(file_path=file_path, file_content=file_content)

        # Display results
        print("📁 FILE ANALYSIS:")
        print(f"Type: {result.file_analysis.file_type}")
        print(f"Purpose: {result.file_analysis.main_purpose}")
        print(f"Key Components: {', '.join(result.file_analysis.key_components)}")
        print(f"Dependencies: {', '.join(result.file_analysis.dependencies)}")

        if result.quality_assessment.quality_score > 0:
            print("
⭐ QUALITY ASSESSMENT:"            print(f"Score: {result.quality_assessment.quality_score}/10")
            print(f"Strengths: {', '.join(result.quality_assessment.strengths)}")
            print(f"Issues: {', '.join(result.quality_assessment.issues)}")
            print(f"Recommendations: {', '.join(result.quality_assessment.recommendations)}")

        print("
📝 SUMMARY:"        print(result.documentation.summary)

        if result.documentation.usage_examples:
            print("
💡 USAGE EXAMPLES:"            for i, example in enumerate(result.documentation.usage_examples, 1):
                print(f"{i}. {example}")

    except Exception as e:
        print(f"Error during analysis: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Analyze the current file itself as an example
    analyze_file(__file__)

    # You can also analyze other files:
    # analyze_file("path/to/your/file.py")
    # analyze_file("README.md")
    # analyze_file("config.json")
```

```python
   # Analyze a Python file
   analyze_file("my_script.py")

   # Analyze a README
   analyze_file("README.md")

   # Analyze a config file
   analyze_file("config.json")
   ```

3. **Adapt for your needs**: Modify the signatures and analysis logic to focus on the specific type of inference you want to perform on files (code review, documentation generation, security analysis, etc.).

This approach gives you the flexibility to perform sophisticated AI-powered analysis on individual files while maintaining the structured, modular nature of DSPy programs.

```

