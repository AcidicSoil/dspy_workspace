# file_analyzer.py - DSPy module deriving a learning brief from a single file
from __future__ import annotations

from dataclasses import dataclass

import dspy

from .signatures import FileOverview, TeachingPoints, TeachingReport


@dataclass
class TeachingConfig:
    section_bullet_prefix: str = "- "


def _fallback_list(message: str) -> list[str]:
    return [message]


class FileTeachingAnalyzer(dspy.Module):
    """Generate a teaching-focused summary using DSPy chains of thought."""

    def __init__(self, config: TeachingConfig | None = None) -> None:
        super().__init__()
        self.config = config or TeachingConfig()
        self.overview = dspy.ChainOfThought(FileOverview)
        self.teachings = dspy.ChainOfThought(TeachingPoints)
        self.report = dspy.ChainOfThought(TeachingReport)

    def forward(self, *, file_path: str, file_content: str) -> dspy.Prediction:
        overview_pred = self.overview(
            file_path=file_path,
            file_content=file_content,
        )

        teaching_pred = self.teachings(
            file_content=file_content,
        )

        section_notes = overview_pred.section_notes or _fallback_list(
            "Section-level breakdown unavailable."
        )

        key_concepts = teaching_pred.key_concepts or _fallback_list(
            "Clarify core concepts manually."
        )

        practical_steps = teaching_pred.practical_steps or _fallback_list(
            "Document workflow steps explicitly."
        )

        pitfalls = teaching_pred.pitfalls or [
            "No pitfalls identified; review source for potential caveats."
        ]

        references = teaching_pred.references or []

        report_pred = self.report(
            file_path=file_path,
            overview=overview_pred.overview,
            section_notes=section_notes,
            key_concepts=key_concepts,
            practical_steps=practical_steps,
            pitfalls=pitfalls,
            references=references,
        )

        return dspy.Prediction(
            overview=overview_pred,
            teachings=teaching_pred,
            report=report_pred,
        )
