"""
Base H5P Agent mit Selbst-Korrektur
Basisklasse für alle spezialisierten Sub-Agents
"""

from dataclasses import dataclass, field
from typing import Any, Callable
from pathlib import Path
from enum import Enum
import sys
import os

# Parent-Verzeichnis zum Path hinzufügen für h5p_generator Import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from h5p_generator import H5PResult


class AgentStatus(Enum):
    """Status eines Agent-Durchlaufs"""
    SUCCESS = "success"
    CORRECTED = "corrected"      # Selbst-korrigiert
    FALLBACK = "fallback"        # Fallback-Typ verwendet
    FAILED = "failed"


@dataclass
class AgentResult:
    """Ergebnis eines Sub-Agent-Durchlaufs"""
    status: AgentStatus
    h5p_result: H5PResult | None
    original_type: str
    final_type: str
    corrections: list[str] = field(default_factory=list)
    attempts: int = 1
    error: str | None = None

    @property
    def success(self) -> bool:
        return self.status in (AgentStatus.SUCCESS, AgentStatus.CORRECTED, AgentStatus.FALLBACK)

    def __str__(self) -> str:
        icon = "✓" if self.success else "✗"
        if self.status == AgentStatus.CORRECTED:
            return f"{icon} {self.final_type} (korrigiert nach {self.attempts} Versuchen)"
        elif self.status == AgentStatus.FALLBACK:
            return f"{icon} {self.final_type} (Fallback von {self.original_type})"
        elif self.success:
            return f"{icon} {self.final_type}"
        else:
            return f"{icon} {self.original_type}: {self.error}"


@dataclass
class ValidationIssue:
    """Ein Validierungsproblem"""
    severity: str  # "error", "warning", "info"
    message: str
    auto_fixable: bool = False
    fix_action: str | None = None


class BaseH5PAgent:
    """
    Basisklasse für H5P Sub-Agents mit Selbst-Korrektur.

    Features:
    - Validierung vor Generierung
    - Automatische Korrektur bei bekannten Problemen
    - Fallback auf alternative Typen
    - Retry-Logik bei Fehlern
    """

    # Überschreiben in Subklassen
    SUPPORTED_TYPES: list[str] = []
    FALLBACK_MAP: dict[str, str] = {}  # type -> fallback_type
    MAX_RETRIES: int = 3

    def __init__(self, output_dir: Path | str = None):
        self.output_dir = Path(output_dir) if output_dir else Path("../test-output")
        self._generators: dict[str, Callable] = {}
        self._validators: dict[str, Callable] = {}
        self._fixers: dict[str, Callable] = {}

    def register_generator(self, content_type: str, generator: Callable):
        """Registriert eine Generator-Funktion für einen Typ"""
        self._generators[content_type] = generator

    def register_validator(self, content_type: str, validator: Callable):
        """Registriert eine Validierungs-Funktion für einen Typ"""
        self._validators[content_type] = validator

    def register_fixer(self, content_type: str, fixer: Callable):
        """Registriert eine Auto-Fix-Funktion für einen Typ"""
        self._fixers[content_type] = fixer

    def validate(self, content_type: str, **params) -> list[ValidationIssue]:
        """
        Validiert Parameter vor der Generierung.
        Gibt Liste von ValidationIssues zurück.
        """
        issues = []

        # Allgemeine Validierung
        if not params.get('title'):
            issues.append(ValidationIssue(
                severity="error",
                message="Titel ist erforderlich",
                auto_fixable=True,
                fix_action="default_title"
            ))

        # Typ-spezifische Validierung
        if content_type in self._validators:
            type_issues = self._validators[content_type](**params)
            issues.extend(type_issues)

        return issues

    def auto_fix(self, content_type: str, issues: list[ValidationIssue], **params) -> dict:
        """
        Versucht, auto-fixable Issues zu korrigieren.
        Gibt korrigierte Parameter zurück.
        """
        fixed_params = dict(params)
        fixes_applied = []

        for issue in issues:
            if not issue.auto_fixable:
                continue

            if issue.fix_action == "default_title":
                fixed_params['title'] = f"H5P {content_type}"
                fixes_applied.append(f"Titel auf '{fixed_params['title']}' gesetzt")

            # Typ-spezifische Fixes
            if content_type in self._fixers:
                fixed_params, fix_msg = self._fixers[content_type](issue, fixed_params)
                if fix_msg:
                    fixes_applied.append(fix_msg)

        return fixed_params, fixes_applied

    def generate(self, content_type: str, **params) -> AgentResult:
        """
        Generiert H5P-Content mit Selbst-Korrektur.

        1. Validierung
        2. Auto-Fix bei Problemen
        3. Generierung
        4. Retry bei Fehler
        5. Fallback bei dauerhaftem Fehler
        """
        if content_type not in self.SUPPORTED_TYPES:
            return AgentResult(
                status=AgentStatus.FAILED,
                h5p_result=None,
                original_type=content_type,
                final_type=content_type,
                error=f"Typ '{content_type}' nicht unterstützt. Verfügbar: {self.SUPPORTED_TYPES}"
            )

        corrections = []
        current_params = dict(params)
        current_type = content_type
        attempts = 0

        while attempts < self.MAX_RETRIES:
            attempts += 1

            # 1. Validierung
            issues = self.validate(current_type, **current_params)
            errors = [i for i in issues if i.severity == "error"]
            fixable_errors = [i for i in errors if i.auto_fixable]

            # 2. Auto-Fix versuchen
            if fixable_errors:
                current_params, fixes = self.auto_fix(current_type, fixable_errors, **current_params)
                corrections.extend(fixes)

            # Nicht-fixierbare Errors?
            non_fixable = [i for i in errors if not i.auto_fixable]
            if non_fixable and attempts == 1:
                # Fallback versuchen
                if current_type in self.FALLBACK_MAP:
                    fallback_type = self.FALLBACK_MAP[current_type]
                    corrections.append(f"Fallback: {current_type} → {fallback_type}")
                    current_type = fallback_type
                    continue

            # 3. Generierung
            if current_type not in self._generators:
                return AgentResult(
                    status=AgentStatus.FAILED,
                    h5p_result=None,
                    original_type=content_type,
                    final_type=current_type,
                    attempts=attempts,
                    error=f"Kein Generator für '{current_type}' registriert"
                )

            try:
                result = self._generators[current_type](**current_params)

                if result.success:
                    # Erfolg!
                    if corrections:
                        status = AgentStatus.CORRECTED
                    elif current_type != content_type:
                        status = AgentStatus.FALLBACK
                    else:
                        status = AgentStatus.SUCCESS

                    return AgentResult(
                        status=status,
                        h5p_result=result,
                        original_type=content_type,
                        final_type=current_type,
                        corrections=corrections,
                        attempts=attempts
                    )
                else:
                    # Generierung fehlgeschlagen - Retry
                    corrections.append(f"Versuch {attempts}: {result.error}")

            except Exception as e:
                corrections.append(f"Versuch {attempts}: Exception {str(e)}")

        # Alle Retries erschöpft - Fallback versuchen
        if content_type in self.FALLBACK_MAP and current_type == content_type:
            fallback_type = self.FALLBACK_MAP[content_type]
            corrections.append(f"Finale Fallback: {content_type} → {fallback_type}")

            # Rekursiver Aufruf mit Fallback-Typ
            fallback_result = self.generate(fallback_type, **params)
            fallback_result.original_type = content_type
            fallback_result.corrections = corrections + fallback_result.corrections
            return fallback_result

        # Endgültig fehlgeschlagen
        return AgentResult(
            status=AgentStatus.FAILED,
            h5p_result=None,
            original_type=content_type,
            final_type=current_type,
            corrections=corrections,
            attempts=attempts,
            error="Alle Versuche fehlgeschlagen"
        )

    def can_handle(self, content_type: str) -> bool:
        """Prüft ob dieser Agent den Typ verarbeiten kann"""
        return content_type in self.SUPPORTED_TYPES

    def get_supported_types(self) -> list[str]:
        """Gibt alle unterstützten Typen zurück"""
        return self.SUPPORTED_TYPES.copy()
