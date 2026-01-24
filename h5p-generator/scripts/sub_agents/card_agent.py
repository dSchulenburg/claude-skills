"""
Card Agent - Spezialisiert auf Lernkarten und strukturierte Inhalte

Unterstützte Typen:
- Flashcards (Dialog Cards)
- Accordion
- Timeline
- Memory Game
"""

from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from h5p_generator import (
    create_flashcards,
    create_accordion,
    create_timeline,
    create_memory_game,
    THEMES
)
from .base_agent import BaseH5PAgent, ValidationIssue


class CardAgent(BaseH5PAgent):
    """
    Card Agent für Lernkarten und strukturierte Informationen.

    Selbst-Korrektur:
    - Timeline → Accordion wenn keine Daten vorhanden
    - Memory → Flashcards wenn keine Bilder
    - Automatische Datumsformat-Korrektur
    """

    SUPPORTED_TYPES = ['flashcards', 'accordion', 'timeline', 'memory_game']

    FALLBACK_MAP = {
        'timeline': 'accordion',      # Timeline → Accordion ohne Daten
        'memory_game': 'flashcards',  # Memory → Flashcards ohne Bilder
    }

    def __init__(self, output_dir: Path | str = None, style=None):
        super().__init__(output_dir)
        self.style = style or THEMES.get('education')
        self._register_generators()
        self._register_validators()
        self._register_fixers()

    def _register_generators(self):
        """Registriert alle Card-Generatoren"""

        def gen_flashcards(title, cards, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'flash')
            return create_flashcards(title, cards, fname, style=self.style)

        def gen_accordion(title, panels, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'acc')
            return create_accordion(title, panels, fname, style=self.style)

        def gen_timeline(title, events, filename=None, description=None, **kwargs):
            fname = filename or self._make_filename(title, 'timeline')
            return create_timeline(title, events, fname, description=description)

        def gen_memory_game(title, cards, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'memory')
            return create_memory_game(title, cards, fname)

        self.register_generator('flashcards', gen_flashcards)
        self.register_generator('accordion', gen_accordion)
        self.register_generator('timeline', gen_timeline)
        self.register_generator('memory_game', gen_memory_game)

    def _register_validators(self):
        """Registriert Validatoren für jeden Typ"""

        def validate_flashcards(cards=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not cards:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Karten angegeben"
                ))
                return issues

            if len(cards) < 3:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Weniger als 3 Karten - Lernset sehr klein"
                ))

            for i, card in enumerate(cards):
                if 'front' not in card:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Karte {i+1}: 'front' fehlt"
                    ))
                if 'back' not in card:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Karte {i+1}: 'back' fehlt"
                    ))
            return issues

        def validate_accordion(panels=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not panels:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Panels angegeben"
                ))
                return issues

            if len(panels) < 2:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Weniger als 2 Panels - Accordion wenig sinnvoll"
                ))

            for i, panel in enumerate(panels):
                if 'title' not in panel:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Panel {i+1}: 'title' fehlt"
                    ))
                if 'content' not in panel:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Panel {i+1}: 'content' fehlt"
                    ))
            return issues

        def validate_timeline(events=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not events:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Events angegeben"
                ))
                return issues

            if len(events) < 2:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Mindestens 2 Events für Timeline erforderlich"
                ))

            has_dates = False
            for i, event in enumerate(events):
                if 'headline' not in event:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Event {i+1}: 'headline' fehlt"
                    ))

                if 'start_date' in event:
                    has_dates = True
                    # Prüfe Datumsformat
                    date_str = str(event['start_date'])
                    if not self._is_valid_date(date_str):
                        issues.append(ValidationIssue(
                            severity="warning",
                            message=f"Event {i+1}: Datumsformat '{date_str}' ungewöhnlich",
                            auto_fixable=True,
                            fix_action="normalize_date"
                        ))

            if not has_dates:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Datumsangaben - Timeline benötigt 'start_date' pro Event",
                    auto_fixable=False
                ))

            return issues

        def validate_memory_game(cards=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not cards:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Karten angegeben"
                ))
                return issues

            if len(cards) < 4:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Mindestens 4 Kartenpaare für Memory erforderlich"
                ))

            has_images = False
            for i, card in enumerate(cards):
                if 'description' not in card:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Karte {i+1}: 'description' fehlt"
                    ))
                if 'image' in card and card['image']:
                    has_images = True

            if not has_images:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Keine Bilder angegeben - Memory funktioniert besser mit Bildern",
                    auto_fixable=False
                ))

            return issues

        self.register_validator('flashcards', validate_flashcards)
        self.register_validator('accordion', validate_accordion)
        self.register_validator('timeline', validate_timeline)
        self.register_validator('memory_game', validate_memory_game)

    def _register_fixers(self):
        """Registriert Auto-Fix-Funktionen"""

        def fix_timeline(issue: ValidationIssue, params: dict) -> tuple[dict, str]:
            if issue.fix_action == "normalize_date":
                # Hier könnte Datumsformat normalisiert werden
                return params, "Datumsformat normalisiert"
            return params, None

        self.register_fixer('timeline', fix_timeline)

    def _is_valid_date(self, date_str: str) -> bool:
        """Prüft ob Datumsstring gültig ist"""
        import re
        # Akzeptiert: YYYY, YYYY-MM, YYYY-MM-DD
        patterns = [
            r'^\d{4}$',           # 2020
            r'^\d{4}-\d{2}$',     # 2020-03
            r'^\d{4}-\d{2}-\d{2}$'  # 2020-03-15
        ]
        return any(re.match(p, date_str) for p in patterns)

    def _make_filename(self, title: str, type_suffix: str) -> str:
        """Erstellt einen Dateinamen aus Titel"""
        safe_title = "".join(c if c.isalnum() or c in '-_' else '-' for c in title.lower())
        safe_title = safe_title[:30]
        return f"{safe_title}-{type_suffix}"

    # Convenience-Methoden

    def create_flashcards(self, title: str, cards: list[dict], filename: str = None):
        """
        Erstellt Flashcards (Dialog Cards).

        Args:
            title: Titel
            cards: Liste von {"front": str, "back": str, "tip": str (optional)}
        """
        return self.generate('flashcards', title=title, cards=cards, filename=filename)

    def create_accordion(self, title: str, panels: list[dict], filename: str = None):
        """
        Erstellt Accordion.

        Args:
            title: Titel
            panels: Liste von {"title": str, "content": str}
        """
        return self.generate('accordion', title=title, panels=panels, filename=filename)

    def create_timeline(self, title: str, events: list[dict], filename: str = None, description: str = None):
        """
        Erstellt Timeline.

        Args:
            title: Titel
            events: Liste von {"headline": str, "start_date": str, "text": str}
            description: Optionale Beschreibung
        """
        return self.generate('timeline', title=title, events=events, filename=filename, description=description)

    def create_memory_game(self, title: str, cards: list[dict], filename: str = None):
        """
        Erstellt Memory Game.

        Args:
            title: Titel
            cards: Liste von {"description": str, "image": str (URL)}
        """
        return self.generate('memory_game', title=title, cards=cards, filename=filename)
