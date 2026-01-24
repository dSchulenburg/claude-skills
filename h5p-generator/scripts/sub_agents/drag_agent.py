"""
Drag Agent - Spezialisiert auf interaktive Zuordnungen

Unterstützte Typen:
- Drag & Drop
- Drag the Words
- Mark the Words
"""

from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from h5p_generator import (
    create_drag_drop,
    create_drag_text,
    create_mark_words,
    THEMES
)
from .base_agent import BaseH5PAgent, ValidationIssue


class DragAgent(BaseH5PAgent):
    """
    Drag Agent für interaktive Zuordnungsaufgaben.

    Selbst-Korrektur:
    - Drag & Drop Koordinaten automatisch korrigieren
    - Drag Text → Mark Words bei zu wenig Lücken
    - Automatische Dropzone-Positionierung
    """

    SUPPORTED_TYPES = ['drag_drop', 'drag_text', 'mark_words']

    FALLBACK_MAP = {
        'drag_text': 'mark_words',  # Drag Text → Mark Words bei Problemen
    }

    def __init__(self, output_dir: Path | str = None, style=None):
        super().__init__(output_dir)
        self.style = style or THEMES.get('education')
        self._register_generators()
        self._register_validators()
        self._register_fixers()

    def _register_generators(self):
        """Registriert alle Drag-Generatoren"""

        def gen_drag_drop(title, task_description, dropzones, draggables, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'dragdrop')
            return create_drag_drop(title, task_description, dropzones, draggables, fname, style=self.style)

        def gen_drag_text(title, text, filename=None, task=None, **kwargs):
            fname = filename or self._make_filename(title, 'dragtext')
            return create_drag_text(title, text, fname, task=task, style=self.style)

        def gen_mark_words(title, text, filename=None, task=None, **kwargs):
            fname = filename or self._make_filename(title, 'mark')
            return create_mark_words(title, text, fname, task=task, style=self.style)

        self.register_generator('drag_drop', gen_drag_drop)
        self.register_generator('drag_text', gen_drag_text)
        self.register_generator('mark_words', gen_mark_words)

    def _register_validators(self):
        """Registriert Validatoren für jeden Typ"""

        def validate_drag_drop(dropzones=None, draggables=None, task_description=None, **kwargs) -> list[ValidationIssue]:
            issues = []

            if not task_description:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Keine Aufgabenbeschreibung - wird automatisch generiert",
                    auto_fixable=True,
                    fix_action="default_task"
                ))

            if not dropzones:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Dropzones angegeben"
                ))
            elif len(dropzones) < 2:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Weniger als 2 Dropzones - Zuordnung trivial"
                ))
            elif len(dropzones) > 5:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Mehr als 5 Dropzones - kann unübersichtlich werden"
                ))

            if not draggables:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Draggables angegeben"
                ))
            else:
                for i, d in enumerate(draggables):
                    if 'text' not in d:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Draggable {i+1}: 'text' fehlt"
                        ))
                    if 'dropzone' not in d:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Draggable {i+1}: 'dropzone' (Index) fehlt"
                        ))
                    elif dropzones and d.get('dropzone', 0) >= len(dropzones):
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Draggable {i+1}: dropzone {d['dropzone']} existiert nicht (max: {len(dropzones)-1})"
                        ))

            return issues

        def validate_drag_text(text=None, **kwargs) -> list[ValidationIssue]:
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
                    message="Nur 1 Lücke - sehr einfache Aufgabe"
                ))
            elif blank_count > 10:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Mehr als 10 Lücken - kann überfordernd sein"
                ))

            return issues

        def validate_mark_words(text=None, **kwargs) -> list[ValidationIssue]:
            issues = []

            if not text:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Kein Text angegeben"
                ))
                return issues

            # Zähle markierbare Wörter (mit *markiert*)
            mark_count = text.count('*') // 2
            if mark_count == 0:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine markierbaren Wörter (mit *Sternchen* markieren)"
                ))
            elif mark_count < 2:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Nur 1 markierbares Wort - sehr einfache Aufgabe"
                ))

            return issues

        self.register_validator('drag_drop', validate_drag_drop)
        self.register_validator('drag_text', validate_drag_text)
        self.register_validator('mark_words', validate_mark_words)

    def _register_fixers(self):
        """Registriert Auto-Fix-Funktionen"""

        def fix_drag_drop(issue: ValidationIssue, params: dict) -> tuple[dict, str]:
            if issue.fix_action == "default_task":
                params['task_description'] = "Ordne die Begriffe den richtigen Kategorien zu."
                return params, "Standard-Aufgabenbeschreibung gesetzt"
            return params, None

        self.register_fixer('drag_drop', fix_drag_drop)

    def _make_filename(self, title: str, type_suffix: str) -> str:
        """Erstellt einen Dateinamen aus Titel"""
        safe_title = "".join(c if c.isalnum() or c in '-_' else '-' for c in title.lower())
        safe_title = safe_title[:30]
        return f"{safe_title}-{type_suffix}"

    # Convenience-Methoden

    def create_drag_drop(self, title: str, task_description: str, dropzones: list[str],
                         draggables: list[dict], filename: str = None):
        """
        Erstellt Drag & Drop Zuordnung.

        Args:
            title: Titel
            task_description: Aufgabenstellung
            dropzones: Liste von Kategorienamen
            draggables: Liste von {"text": str, "dropzone": int (Index)}
        """
        return self.generate('drag_drop', title=title, task_description=task_description,
                            dropzones=dropzones, draggables=draggables, filename=filename)

    def create_drag_text(self, title: str, text: str, filename: str = None, task: str = None):
        """
        Erstellt Drag the Words.

        Args:
            title: Titel
            text: Text mit *Lücken* markiert
            task: Optionale Aufgabenstellung
        """
        return self.generate('drag_text', title=title, text=text, filename=filename, task=task)

    def create_mark_words(self, title: str, text: str, filename: str = None, task: str = None):
        """
        Erstellt Mark the Words.

        Args:
            title: Titel
            text: Text mit *markierbaren Wörtern*
            task: Optionale Aufgabenstellung
        """
        return self.generate('mark_words', title=title, text=text, filename=filename, task=task)
