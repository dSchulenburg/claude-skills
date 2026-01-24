"""
Quiz Agent - Spezialisiert auf Wissensabfrage-Typen

Unterstützte Typen:
- True/False
- Multiple Choice
- Single Choice
- Summary
- Fill in Blanks
"""

from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from h5p_generator import (
    create_true_false,
    create_multi_choice,
    create_single_choice,
    create_summary,
    create_fill_blanks,
    THEMES
)
from .base_agent import BaseH5PAgent, ValidationIssue


class QuizAgent(BaseH5PAgent):
    """
    Quiz Agent für Wissensabfrage-Elemente.

    Selbst-Korrektur:
    - MC → SC bei zu wenig Optionen
    - True/False → MC bei zu komplexen Aussagen
    - Automatische Antwort-Validierung
    """

    SUPPORTED_TYPES = ['true_false', 'multi_choice', 'single_choice', 'summary', 'fill_blanks']

    FALLBACK_MAP = {
        'multi_choice': 'single_choice',  # MC → SC bei Problemen
        'summary': 'true_false',          # Summary → TF bei zu wenig Aussagen
    }

    def __init__(self, output_dir: Path | str = None, style=None):
        super().__init__(output_dir)
        self.style = style or THEMES.get('education')
        self._register_generators()
        self._register_validators()

    def _register_generators(self):
        """Registriert alle Quiz-Generatoren"""

        def gen_true_false(title, questions, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'tf')
            return create_true_false(title, questions, fname, style=self.style)

        def gen_multi_choice(title, questions, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'mc')
            return create_multi_choice(title, questions, fname, style=self.style)

        def gen_single_choice(title, questions, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'sc')
            return create_single_choice(title, questions, fname, style=self.style)

        def gen_summary(title, items, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'sum')
            return create_summary(title, items, fname, style=self.style)

        def gen_fill_blanks(title, text, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'blanks')
            return create_fill_blanks(title, text, fname, style=self.style)

        self.register_generator('true_false', gen_true_false)
        self.register_generator('multi_choice', gen_multi_choice)
        self.register_generator('single_choice', gen_single_choice)
        self.register_generator('summary', gen_summary)
        self.register_generator('fill_blanks', gen_fill_blanks)

    def _register_validators(self):
        """Registriert Validatoren für jeden Typ"""

        def validate_true_false(questions=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not questions:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Fragen angegeben"
                ))
            elif len(questions) < 2:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Weniger als 2 Aussagen - Quiz sehr kurz"
                ))

            # Prüfe ob alle Fragen text und correct haben
            if questions:
                for i, q in enumerate(questions):
                    if 'text' not in q:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Frage {i+1}: 'text' fehlt"
                        ))
                    if 'correct' not in q:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Frage {i+1}: 'correct' (True/False) fehlt"
                        ))
            return issues

        def validate_multi_choice(questions=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not questions:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Fragen angegeben"
                ))
                return issues

            for i, q in enumerate(questions):
                if 'question' not in q:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Frage {i+1}: 'question' fehlt"
                    ))
                if 'answers' not in q or len(q.get('answers', [])) < 2:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Frage {i+1}: Mindestens 2 Antworten erforderlich",
                        auto_fixable=False
                    ))
                else:
                    # Prüfe ob mindestens eine Antwort korrekt ist
                    correct_count = sum(1 for a in q['answers'] if a.get('correct'))
                    if correct_count == 0:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Frage {i+1}: Keine korrekte Antwort markiert",
                            auto_fixable=True,
                            fix_action="mark_first_correct"
                        ))
            return issues

        def validate_single_choice(questions=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not questions:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Fragen angegeben"
                ))
                return issues

            for i, q in enumerate(questions):
                if 'question' not in q:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Frage {i+1}: 'question' fehlt"
                    ))
                if 'answers' not in q or len(q.get('answers', [])) < 2:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Frage {i+1}: Mindestens 2 Antworten erforderlich"
                    ))
            return issues

        def validate_summary(items=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not items:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Summary-Items angegeben"
                ))
                return issues

            if len(items) < 2:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Weniger als 2 Items - Summary sehr kurz"
                ))

            for i, item in enumerate(items):
                if 'statements' not in item or len(item.get('statements', [])) < 2:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Item {i+1}: Mindestens 2 Aussagen erforderlich"
                    ))
            return issues

        def validate_fill_blanks(text=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not text:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Kein Text angegeben"
                ))
                return issues

            # Zähle Lücken (mit *markiert*)
            blank_count = text.count('*') // 2
            if blank_count == 0:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Lücken im Text (mit *Sternchen* markieren)"
                ))
            elif blank_count < 2:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Nur 1 Lücke - sehr einfacher Lückentext"
                ))
            return issues

        self.register_validator('true_false', validate_true_false)
        self.register_validator('multi_choice', validate_multi_choice)
        self.register_validator('single_choice', validate_single_choice)
        self.register_validator('summary', validate_summary)
        self.register_validator('fill_blanks', validate_fill_blanks)

    def _make_filename(self, title: str, type_suffix: str) -> str:
        """Erstellt einen Dateinamen aus Titel"""
        safe_title = "".join(c if c.isalnum() or c in '-_' else '-' for c in title.lower())
        safe_title = safe_title[:30]  # Maximal 30 Zeichen
        return f"{safe_title}-{type_suffix}"

    # Convenience-Methoden für direkte Generierung

    def create_true_false(self, title: str, questions: list[dict], filename: str = None):
        """
        Erstellt True/False Quiz.

        Args:
            title: Titel des Quiz
            questions: Liste von {"text": str, "correct": bool}
            filename: Optional, wird aus Titel generiert
        """
        return self.generate('true_false', title=title, questions=questions, filename=filename)

    def create_multi_choice(self, title: str, questions: list[dict], filename: str = None):
        """
        Erstellt Multiple Choice Quiz.

        Args:
            title: Titel des Quiz
            questions: Liste von {"question": str, "answers": [{"text": str, "correct": bool}]}
        """
        return self.generate('multi_choice', title=title, questions=questions, filename=filename)

    def create_single_choice(self, title: str, questions: list[dict], filename: str = None):
        """
        Erstellt Single Choice Quiz.
        Erste Antwort ist immer korrekt!

        Args:
            title: Titel des Quiz
            questions: Liste von {"question": str, "answers": [str, str, ...]}
        """
        return self.generate('single_choice', title=title, questions=questions, filename=filename)

    def create_summary(self, title: str, items: list[dict], filename: str = None):
        """
        Erstellt Summary.
        Erste Aussage ist immer korrekt!

        Args:
            title: Titel
            items: Liste von {"statements": [str, str, ...]}
        """
        return self.generate('summary', title=title, items=items, filename=filename)

    def create_fill_blanks(self, title: str, text: str, filename: str = None):
        """
        Erstellt Lückentext.

        Args:
            title: Titel
            text: Text mit *Lücken* markiert
        """
        return self.generate('fill_blanks', title=title, text=text, filename=filename)
