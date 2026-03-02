"""
Scenario Agent - Spezialisiert auf nicht-lineare Lernszenarien

Unterstützte Typen:
- BranchingScenario
"""

from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from h5p_generator import create_branching_scenario, THEMES
from .base_agent import BaseH5PAgent, ValidationIssue


class ScenarioAgent(BaseH5PAgent):
    """
    Scenario Agent für verzweigte Lernszenarien.

    Validierung:
    - Mindestens 2 Nodes
    - Warnung wenn kein Question-Node vorhanden
    - Prüfung der next-Verweise
    """

    SUPPORTED_TYPES = ['branching_scenario']

    FALLBACK_MAP = {}  # Kein Fallback für Szenarien

    def __init__(self, output_dir: Path | str = None, style=None):
        super().__init__(output_dir)
        self.style = style or THEMES.get('education')
        self._register_generators()
        self._register_validators()

    def _register_generators(self):
        """Registriert alle Scenario-Generatoren"""

        def gen_branching_scenario(title, nodes, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'branch')
            return create_branching_scenario(title, nodes, fname, style=self.style, **kwargs)

        self.register_generator('branching_scenario', gen_branching_scenario)

    def _register_validators(self):
        """Registriert Validatoren"""

        def validate_branching_scenario(nodes=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not nodes:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Nodes angegeben"
                ))
                return issues

            if len(nodes) < 2:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Mindestens 2 Nodes erforderlich"
                ))

            # Warnung wenn kein Question-Node
            has_question = any(n.get('type') == 'question' for n in nodes)
            if not has_question:
                issues.append(ValidationIssue(
                    severity="warning",
                    message="Kein Question-Node vorhanden - Szenario ist rein linear"
                ))

            # Prüfe Node-Struktur
            for i, node in enumerate(nodes):
                if 'type' not in node:
                    issues.append(ValidationIssue(
                        severity="error",
                        message=f"Node {i}: 'type' fehlt (text oder question)"
                    ))
                elif node['type'] == 'text':
                    if 'content' not in node:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Node {i}: 'content' fehlt"
                        ))
                    if 'next' not in node:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Node {i}: 'next' fehlt (-1 für Ende)"
                        ))
                elif node['type'] == 'question':
                    if 'question' not in node:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Node {i}: 'question' fehlt"
                        ))
                    alts = node.get('alternatives', [])
                    if len(alts) < 2:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Node {i}: Mindestens 2 Alternativen nötig"
                        ))

            return issues

        self.register_validator('branching_scenario', validate_branching_scenario)

    def _make_filename(self, title: str, type_suffix: str) -> str:
        """Erstellt einen Dateinamen aus Titel"""
        safe_title = "".join(c if c.isalnum() or c in '-_' else '-' for c in title.lower())
        safe_title = safe_title[:30]
        return f"{safe_title}-{type_suffix}"

    # Convenience-Methoden

    def create_branching_scenario(self, title: str, nodes: list[dict], filename: str = None, **kwargs):
        """
        Erstellt ein verzweigtes Lernszenario.

        Args:
            title: Titel des Szenarios
            nodes: Liste von Node-Dicts (text/question)
            filename: Optional, wird aus Titel generiert
        """
        return self.generate('branching_scenario', title=title, nodes=nodes, filename=filename, **kwargs)
