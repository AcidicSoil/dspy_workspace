# signatures.py - DSPy signatures focused on extracting teachings from a single file
from typing import List

import dspy


class FileOverview(dspy.Signature):
    """Summarize the file structure and core narrative."""

    file_path: str = dspy.InputField(desc="Path to the source file")
    file_content: str = dspy.InputField(desc="Full raw text of the file")

    overview: str = dspy.OutputField(desc="2-3 paragraph overview capturing the file's intent")
    section_notes: List[str] = dspy.OutputField(desc="Bullet list summarizing each major section")


class TeachingPoints(dspy.Signature):
    """Extract teachable concepts, workflows, and cautions."""

    file_content: str = dspy.InputField(desc="Full raw text of the file")

    key_concepts: List[str] = dspy.OutputField(desc="Essential ideas learners must retain")
    practical_steps: List[str] = dspy.OutputField(desc="Actionable steps or workflows described")
    pitfalls: List[str] = dspy.OutputField(desc="Warnings, gotchas, or misconceptions to avoid")
    references: List[str] = dspy.OutputField(desc="Follow-up links, exercises, or related material")


class TeachingReport(dspy.Signature):
    """Compose a concise but comprehensive markdown teaching brief."""

    file_path: str = dspy.InputField(desc="Original file path for context header")
    overview: str = dspy.InputField()
    section_notes: List[str] = dspy.InputField()
    key_concepts: List[str] = dspy.InputField()
    practical_steps: List[str] = dspy.InputField()
    pitfalls: List[str] = dspy.InputField()
    references: List[str] = dspy.InputField()

    report_markdown: str = dspy.OutputField(desc="Final markdown document capturing key teachings")
