# file_analyzer.py - DSPy module deriving a learning brief from a single file
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

import dspy

from .signatures import FileOverview, TeachingPoints, TeachingReport


@dataclass
class TeachingConfig:
    section_bullet_prefix: str = "- "
    overview_max_tokens: int = 2000
    teachings_max_tokens: int = 2000
    report_max_tokens: int = 2000
    temperature: float | None = 0.7
    top_p: float | None = None
    n_completions: int | None = None
    extra_lm_kwargs: dict[str, Any] = field(default_factory=dict)
    report_refine_attempts: int = 3
    report_reward_threshold: float = 0.8
    report_min_word_count: int = 400
    report_max_word_count: int = 2800
    report_target_ratio: float = 0.5
    report_soft_cap_ratio: float = 0.8

    def lm_args_for(self, scope: str) -> dict[str, Any]:
        """Return per-module LM kwargs without mutating shared config."""
        scope_tokens = {
            "overview": self.overview_max_tokens,
            "teachings": self.teachings_max_tokens,
            "report": self.report_max_tokens,
        }

        kwargs: dict[str, Any] = {**self.extra_lm_kwargs}
        kwargs["max_tokens"] = scope_tokens.get(scope, self.report_max_tokens)

        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        if self.top_p is not None:
            kwargs["top_p"] = self.top_p
        if self.n_completions is not None:
            kwargs["n"] = self.n_completions

        return kwargs


def _fallback_list(message: str) -> list[str]:
    return [message]


def _ensure_text(value: str | None, fallback: str) -> str:
    if value and value.strip():
        return value
    return fallback


def _ensure_list(
    values: Iterable[str] | None,
    fallback: str,
    *,
    strip_entries: bool = True,
) -> list[str]:
    if not values:
        return _fallback_list(fallback)

    cleaned: list[str] = []
    for entry in values:
        if entry is None:
            continue
        candidate = entry.rstrip() if not strip_entries else entry.strip()
        if candidate:
            cleaned.append(candidate)

    return cleaned or _fallback_list(fallback)


def _clean_list(values: Iterable[str] | None, *, strip_entries: bool = True) -> list[str]:
    if not values:
        return []

    cleaned: list[str] = []
    for entry in values:
        if entry is None:
            continue
        candidate = entry.rstrip() if not strip_entries else entry.strip()
        if candidate:
            cleaned.append(candidate)

    return cleaned


def _with_prefix(items: Iterable[str], prefix: str) -> list[str]:
    if not prefix:
        return [item for item in items if item.strip()]

    prefix_char = prefix.strip()[:1] if prefix.strip() else ""
    prefixed: list[str] = []

    for item in items:
        stripped = item.strip()
        if not stripped:
            continue
        if prefix_char and stripped.startswith(prefix_char):
            prefixed.append(stripped)
        else:
            prefixed.append(f"{prefix}{stripped}")

    return prefixed


def _word_count(text: str) -> int:
    return len(text.split())


class FileTeachingAnalyzer(dspy.Module):
    """Generate a teaching-focused summary using DSPy chains of thought."""

    def __init__(self, config: TeachingConfig | None = None) -> None:
        super().__init__()
        self.config = config or TeachingConfig()

        overview_signature = FileOverview.with_instructions(
            """
            Craft a thorough multi-section narrative that orients a senior learner.
            Describe the file's purpose, high-level architecture, main responsibilities,
            how data flows through each part, and any noteworthy patterns or dependencies.
            Aim for around five paragraphs that highlight why each section exists and
            how it contributes to the overall behavior.
            """
        )

        teachings_signature = TeachingPoints.with_instructions(
            """
            Extract every insight the learner would need for deep comprehension.
            Provide generous bullet lists (>=6 items when possible) covering concepts,
            workflows, pitfalls, integration guidance, and areas needing validation.
            When referencing identifiers, include the role they play.
            Prefer complete sentences that can stand alone in teaching materials.
            """
        )

        report_signature = TeachingReport.with_instructions(
            """
            Assemble a long-form teaching brief in Markdown. Include:
            - An opening context block with file path and intent.
            - Headed sections for overview, section walkthrough, key concepts, workflows,
              pitfalls, integration notes, tests/validation, and references.
            - Expand each bullet into full sentences or sub-bullets to help instructors
              speak to the content without the source file open.
            Ensure the report comfortably exceeds 400 words when source material allows.
            """
        )

        self.overview = dspy.ChainOfThought(
            overview_signature, **self.config.lm_args_for("overview")
        )
        self.teachings = dspy.ChainOfThought(
            teachings_signature, **self.config.lm_args_for("teachings")
        )

        base_report = dspy.ChainOfThought(
            report_signature, **self.config.lm_args_for("report")
        )

        if self.config.report_refine_attempts > 1:

            def report_length_reward(args: dict[str, Any], pred: dspy.Prediction) -> float:
                text = getattr(pred, "report_markdown", "") or ""
                words = _word_count(text)
                source_words = max(int(args.get("source_word_count", 0)), 0)

                dynamic_target = max(
                    self.config.report_min_word_count,
                    int(source_words * self.config.report_target_ratio),
                )

                soft_cap = max(
                    dynamic_target + 150,
                    int(source_words * self.config.report_soft_cap_ratio),
                )

                dynamic_cap = min(self.config.report_max_word_count, soft_cap)

                if words < dynamic_target:
                    return 0.0

                if words >= dynamic_cap:
                    return 1.0

                span = max(dynamic_cap - dynamic_target, 1)
                progress = (words - dynamic_target) / span
                return min(1.0, 0.6 + 0.4 * progress)

            self.report = dspy.Refine(
                module=base_report,
                N=self.config.report_refine_attempts,
                reward_fn=report_length_reward,
                threshold=self.config.report_reward_threshold,
            )
        else:
            self.report = base_report

    def forward(self, *, file_path: str, file_content: str) -> dspy.Prediction:
        overview_pred = self.overview(
            file_path=file_path,
            file_content=file_content,
        )

        teaching_pred = self.teachings(
            file_content=file_content,
        )

        overview_text = _ensure_text(
            getattr(overview_pred, "overview", None),
            "Overview unavailable.",
        )

        section_notes = _with_prefix(
            _ensure_list(
                getattr(overview_pred, "section_notes", None),
                "Section-level breakdown unavailable.",
            ),
            self.config.section_bullet_prefix,
        )

        key_concepts = _with_prefix(
            _ensure_list(
                getattr(teaching_pred, "key_concepts", None),
                "Clarify core concepts manually.",
            ),
            self.config.section_bullet_prefix,
        )

        practical_steps = _with_prefix(
            _ensure_list(
                getattr(teaching_pred, "practical_steps", None),
                "Document workflow steps explicitly.",
            ),
            self.config.section_bullet_prefix,
        )

        pitfalls = _with_prefix(
            _ensure_list(
                getattr(teaching_pred, "pitfalls", None),
                "No pitfalls identified; review source for potential caveats.",
            ),
            self.config.section_bullet_prefix,
        )

        references = _with_prefix(
            _clean_list(getattr(teaching_pred, "references", None)),
            self.config.section_bullet_prefix,
        )

        usage_patterns = _with_prefix(
            _ensure_list(
                getattr(teaching_pred, "usage_patterns", None),
                "Document how this file is applied in real flows.",
            ),
            self.config.section_bullet_prefix,
        )

        key_functions = _with_prefix(
            _ensure_list(
                getattr(teaching_pred, "key_functions", None),
                "Identify primary interfaces and responsibilities manually.",
            ),
            self.config.section_bullet_prefix,
        )

        code_walkthroughs = _ensure_list(
            getattr(teaching_pred, "code_walkthroughs", None),
            "Prepare short code walkthroughs for learners.",
            strip_entries=False,
        )

        integration_notes = _with_prefix(
            _ensure_list(
                getattr(teaching_pred, "integration_notes", None),
                "Outline integration touchpoints manually.",
            ),
            self.config.section_bullet_prefix,
        )

        testing_focus = _with_prefix(
            _ensure_list(
                getattr(teaching_pred, "testing_focus", None),
                "Highlight testing priorities in a follow-up review.",
            ),
            self.config.section_bullet_prefix,
        )

        source_word_count = _word_count(file_content)

        report_pred = self.report(
            file_path=file_path,
            overview=overview_text,
            section_notes=section_notes,
            key_concepts=key_concepts,
            practical_steps=practical_steps,
            pitfalls=pitfalls,
            references=references,
            usage_patterns=usage_patterns,
            key_functions=key_functions,
            code_walkthroughs=code_walkthroughs,
            integration_notes=integration_notes,
            testing_focus=testing_focus,
            source_word_count=source_word_count,
        )

        return dspy.Prediction(
            overview=overview_pred,
            teachings=teaching_pred,
            report=report_pred,
            structured={
                "overview_text": overview_text,
                "section_notes": section_notes,
                "key_concepts": key_concepts,
                "practical_steps": practical_steps,
                "pitfalls": pitfalls,
                "references": references,
                "usage_patterns": usage_patterns,
                "key_functions": key_functions,
                "code_walkthroughs": code_walkthroughs,
                "integration_notes": integration_notes,
                "testing_focus": testing_focus,
            },
        )
