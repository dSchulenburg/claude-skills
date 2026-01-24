"""
H5P Orchestrator Agent

Zentrale Steuerung des Multi-Agent H5P Workflows:
1. Analyse: Lernziele und Operatoren erkennen
2. Planung: H5P-Typen auswählen und Plan erstellen
3. Koordination: Sub-Agents parallel ausführen
4. Kombination: Elemente zu Container-Typen zusammenführen
"""

import re
import asyncio
from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
from enum import Enum

from sub_agents import QuizAgent, CardAgent, DragAgent, AgentResult


class ContentStructure(Enum):
    """Erkannte Inhaltsstruktur"""
    FACTS = "facts"              # Einzelne Fakten
    CATEGORIES = "categories"    # Kategorien/Zuordnungen
    CHRONOLOGY = "chronology"    # Zeitliche Abfolge
    PROCESS = "process"          # Prozess/Workflow
    DEFINITIONS = "definitions"  # Begriffe/Definitionen
    MIXED = "mixed"              # Gemischt


class Complexity(Enum):
    """Komplexität des Inputs"""
    SIMPLE = "simple"      # 1 Lernziel, einfach
    MEDIUM = "medium"      # 2-3 Lernziele
    COMPLEX = "complex"    # 4+ Lernziele


@dataclass
class ContentAnalysis:
    """Ergebnis der Inhaltsanalyse"""
    learning_goals: list[str]
    operators: list[str]
    content_structure: ContentStructure
    complexity: Complexity
    estimated_elements: int
    suggested_container: str | None  # column, course_presentation, interactive_book
    raw_content: dict = field(default_factory=dict)


@dataclass
class PlannedElement:
    """Ein geplantes H5P-Element"""
    id: str
    content_type: str
    agent_type: str  # quiz, card, drag
    title: str
    params: dict
    priority: int = 1


@dataclass
class ExecutionPlan:
    """Ausführungsplan für Sub-Agents"""
    elements: list[PlannedElement]
    container: str | None
    container_config: dict = field(default_factory=dict)
    parallel_groups: list[list[str]] = field(default_factory=list)


@dataclass
class OrchestratorResult:
    """Gesamtergebnis des Orchestrators"""
    success: bool
    analysis: ContentAnalysis
    plan: ExecutionPlan
    element_results: list[AgentResult]
    combined_result: Any = None  # H5PResult für Container
    errors: list[str] = field(default_factory=list)


class H5POrchestrator:
    """
    Orchestrator für Multi-Agent H5P-Generierung.

    Workflow:
    1. analyze() - Lernmaterial analysieren
    2. plan() - Ausführungsplan erstellen
    3. execute() - Sub-Agents koordinieren
    4. combine() - Zu Container zusammenführen (optional)
    """

    # Operator → H5P-Typ Mapping (inkl. ASCII-Varianten)
    OPERATOR_MAPPING = {
        # Wissen reproduzieren
        'nennen': ['flashcards', 'true_false'],
        'auflisten': ['flashcards', 'accordion'],
        'beschreiben': ['true_false', 'summary', 'accordion'],
        'definieren': ['flashcards', 'fill_blanks'],

        # Wissen anwenden
        'zuordnen': ['drag_drop', 'drag_text'],
        'kategorisieren': ['drag_drop'],
        'ordnen': ['timeline', 'drag_drop'],
        'ergänzen': ['fill_blanks', 'drag_text'],
        'ergaenzen': ['fill_blanks', 'drag_text'],  # ASCII
        'markieren': ['mark_words'],

        # Wissen analysieren
        'erklären': ['accordion', 'summary'],
        'erklaeren': ['accordion', 'summary'],  # ASCII
        'vergleichen': ['drag_drop', 'true_false'],
        'unterscheiden': ['drag_drop', 'multi_choice'],

        # Wissen bewerten
        'bewerten': ['multi_choice', 'single_choice'],
        'entscheiden': ['single_choice', 'multi_choice'],
        'beurteilen': ['summary', 'multi_choice'],
    }

    # Agent-Zuordnung für Typen
    TYPE_TO_AGENT = {
        'true_false': 'quiz',
        'multi_choice': 'quiz',
        'single_choice': 'quiz',
        'summary': 'quiz',
        'fill_blanks': 'quiz',
        'flashcards': 'card',
        'accordion': 'card',
        'timeline': 'card',
        'memory_game': 'card',
        'drag_drop': 'drag',
        'drag_text': 'drag',
        'mark_words': 'drag',
    }

    def __init__(self, output_dir: Path | str = None):
        self.output_dir = Path(output_dir) if output_dir else Path("../test-output")

        # Sub-Agents initialisieren
        self.agents = {
            'quiz': QuizAgent(self.output_dir),
            'card': CardAgent(self.output_dir),
            'drag': DragAgent(self.output_dir),
        }

    def analyze(self, content: str | dict) -> ContentAnalysis:
        """
        Analysiert Lernmaterial und extrahiert Struktur.

        Args:
            content: Markdown-Text oder strukturiertes Dict

        Returns:
            ContentAnalysis mit Lernzielen, Operatoren, etc.
        """
        if isinstance(content, dict):
            return self._analyze_structured(content)
        else:
            return self._analyze_text(content)

    def _analyze_text(self, text: str) -> ContentAnalysis:
        """Analysiert Freitext/Markdown"""
        learning_goals = []
        operators = []

        # Keywords für Lernziel-Erkennung (mit Umlauten und ASCII-Varianten)
        goal_keywords = ['sollen', 'können', 'koennen', 'lernen', 'wissen', 'verstehen']
        header_keywords = ['lernziel', 'ziel', 'kompetenz']

        # Lernziele extrahieren
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            line_stripped = line.strip('- #*').strip()

            # Überschriften überspringen (nur Keyword, kein Inhalt)
            if any(kw in line_lower for kw in header_keywords):
                if len(line_stripped.split()) <= 2:  # Nur 1-2 Wörter = Überschrift
                    continue

            # Lernziel-Zeilen erkennen
            if any(kw in line_lower for kw in goal_keywords):
                if line_stripped and len(line_stripped) > 10:  # Mindestlänge
                    learning_goals.append(line_stripped)

                    # Operatoren in der Zeile finden (mit Wortgrenzen)
                    for op in self.OPERATOR_MAPPING.keys():
                        # Regex für Wortgrenzen
                        pattern = r'\b' + re.escape(op) + r'\b'
                        if re.search(pattern, line_lower):
                            if op not in operators:
                                operators.append(op)

        # Struktur erkennen
        structure = self._detect_structure(text)

        # Komplexität bestimmen
        if len(learning_goals) <= 1:
            complexity = Complexity.SIMPLE
        elif len(learning_goals) <= 3:
            complexity = Complexity.MEDIUM
        else:
            complexity = Complexity.COMPLEX

        # Container-Empfehlung
        container = self._suggest_container(len(learning_goals), structure)

        # Geschätzte Elemente
        estimated = max(len(learning_goals), len(operators), 1)

        return ContentAnalysis(
            learning_goals=learning_goals if learning_goals else ["Allgemeines Lernziel"],
            operators=operators if operators else ["beschreiben"],
            content_structure=structure,
            complexity=complexity,
            estimated_elements=estimated,
            suggested_container=container,
            raw_content={'text': text}
        )

    def _analyze_structured(self, data: dict) -> ContentAnalysis:
        """Analysiert strukturierte Eingabe"""
        learning_goals = data.get('learning_goals', data.get('lernziele', []))
        operators = data.get('operators', [])

        # Operatoren aus Lernzielen extrahieren falls nicht angegeben
        if not operators:
            for goal in learning_goals:
                for op in self.OPERATOR_MAPPING.keys():
                    if op in goal.lower():
                        if op not in operators:
                            operators.append(op)

        structure = ContentStructure(data.get('structure', 'mixed'))
        complexity = Complexity.MEDIUM

        if len(learning_goals) <= 1:
            complexity = Complexity.SIMPLE
        elif len(learning_goals) > 3:
            complexity = Complexity.COMPLEX

        container = self._suggest_container(len(learning_goals), structure)

        return ContentAnalysis(
            learning_goals=learning_goals,
            operators=operators if operators else ['beschreiben'],
            content_structure=structure,
            complexity=complexity,
            estimated_elements=len(learning_goals),
            suggested_container=container,
            raw_content=data
        )

    def _detect_structure(self, text: str) -> ContentStructure:
        """Erkennt die Inhaltsstruktur aus Text"""
        text_lower = text.lower()

        # Chronologie-Keywords
        if any(kw in text_lower for kw in ['jahrhundert', 'jahr', 'datum', 'chronolog', 'geschichte', 'phase', 'schritt']):
            return ContentStructure.CHRONOLOGY

        # Kategorien-Keywords
        if any(kw in text_lower for kw in ['kategori', 'zuordn', 'art', 'typ', 'gruppe']):
            return ContentStructure.CATEGORIES

        # Definitionen-Keywords
        if any(kw in text_lower for kw in ['definition', 'begriff', 'bedeut', 'heißt', 'nennt man']):
            return ContentStructure.DEFINITIONS

        # Prozess-Keywords
        if any(kw in text_lower for kw in ['prozess', 'ablauf', 'workflow', 'dann', 'danach', 'anschließend']):
            return ContentStructure.PROCESS

        # Listen/Fakten
        if text.count('\n- ') > 3 or text.count('\n* ') > 3:
            return ContentStructure.FACTS

        return ContentStructure.MIXED

    def _suggest_container(self, element_count: int, structure: ContentStructure) -> str | None:
        """Empfiehlt Container-Typ basierend auf Analyse"""
        if element_count <= 1:
            return None  # Kein Container nötig

        if element_count <= 3:
            return 'column'

        if structure == ContentStructure.CHRONOLOGY:
            return 'course_presentation'

        if element_count <= 5:
            return 'course_presentation'

        return 'interactive_book'

    def plan(self, analysis: ContentAnalysis, content_items: list[dict] = None) -> ExecutionPlan:
        """
        Erstellt Ausführungsplan basierend auf Analyse.

        Args:
            analysis: Ergebnis von analyze()
            content_items: Optionale Liste von Content-Dicts für jedes Element

        Returns:
            ExecutionPlan mit H5P-Elementen und Container-Config
        """
        elements = []

        # Für jeden Operator ein Element planen
        for i, operator in enumerate(analysis.operators):
            content_type = self._select_type_for_operator(operator, analysis.content_structure)
            agent_type = self.TYPE_TO_AGENT.get(content_type, 'quiz')

            # Content-Daten holen falls vorhanden
            params = {}
            if content_items and i < len(content_items):
                params = content_items[i]

            element = PlannedElement(
                id=f"element_{i+1}",
                content_type=content_type,
                agent_type=agent_type,
                title=analysis.learning_goals[i] if i < len(analysis.learning_goals) else f"Element {i+1}",
                params=params,
                priority=i + 1
            )
            elements.append(element)

        # Parallel-Gruppen: Alle unabhängigen Elemente parallel
        parallel_groups = [[e.id for e in elements]]

        return ExecutionPlan(
            elements=elements,
            container=analysis.suggested_container,
            container_config={'title': 'Lerneinheit'},
            parallel_groups=parallel_groups
        )

    def _select_type_for_operator(self, operator: str, structure: ContentStructure) -> str:
        """Wählt besten H5P-Typ für Operator und Struktur"""
        candidates = self.OPERATOR_MAPPING.get(operator, ['true_false'])

        # Struktur-basierte Anpassung
        if structure == ContentStructure.CHRONOLOGY and 'timeline' in candidates:
            return 'timeline'
        if structure == ContentStructure.CATEGORIES and 'drag_drop' in candidates:
            return 'drag_drop'
        if structure == ContentStructure.DEFINITIONS and 'flashcards' in candidates:
            return 'flashcards'

        return candidates[0]

    async def execute_async(self, plan: ExecutionPlan) -> list[AgentResult]:
        """
        Führt Plan asynchron aus (parallele Sub-Agents).

        Args:
            plan: Ausführungsplan

        Returns:
            Liste von AgentResults
        """
        results = []

        for group in plan.parallel_groups:
            # Elemente dieser Gruppe parallel ausführen
            group_elements = [e for e in plan.elements if e.id in group]

            tasks = [
                self._execute_element_async(e) for e in group_elements
            ]

            group_results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in group_results:
                if isinstance(result, Exception):
                    results.append(AgentResult(
                        status='failed',
                        h5p_result=None,
                        original_type='unknown',
                        final_type='unknown',
                        error=str(result)
                    ))
                else:
                    results.append(result)

        return results

    async def _execute_element_async(self, element: PlannedElement) -> AgentResult:
        """Führt ein einzelnes Element aus"""
        agent = self.agents.get(element.agent_type)
        if not agent:
            from sub_agents.base_agent import AgentStatus
            return AgentResult(
                status=AgentStatus.FAILED,
                h5p_result=None,
                original_type=element.content_type,
                final_type=element.content_type,
                error=f"Agent '{element.agent_type}' nicht gefunden"
            )

        # Synchrone Generierung in Thread ausführen
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: agent.generate(element.content_type, title=element.title, **element.params)
        )

    def execute(self, plan: ExecutionPlan) -> list[AgentResult]:
        """
        Führt Plan synchron aus.

        Args:
            plan: Ausführungsplan

        Returns:
            Liste von AgentResults
        """
        results = []

        for element in plan.elements:
            agent = self.agents.get(element.agent_type)
            if not agent:
                from sub_agents.base_agent import AgentStatus
                results.append(AgentResult(
                    status=AgentStatus.FAILED,
                    h5p_result=None,
                    original_type=element.content_type,
                    final_type=element.content_type,
                    error=f"Agent '{element.agent_type}' nicht gefunden"
                ))
                continue

            result = agent.generate(element.content_type, title=element.title, **element.params)
            results.append(result)

        return results

    def run(self, content: str | dict, content_items: list[dict] = None) -> OrchestratorResult:
        """
        Vollständiger Workflow: Analyse → Planung → Ausführung.

        Args:
            content: Lernmaterial (Text oder Dict)
            content_items: Optionale Content-Daten pro Element

        Returns:
            OrchestratorResult mit allen Ergebnissen
        """
        errors = []

        # 1. Analyse
        try:
            analysis = self.analyze(content)
        except Exception as e:
            return OrchestratorResult(
                success=False,
                analysis=None,
                plan=None,
                element_results=[],
                errors=[f"Analyse fehlgeschlagen: {str(e)}"]
            )

        # 2. Planung
        try:
            plan = self.plan(analysis, content_items)
        except Exception as e:
            return OrchestratorResult(
                success=False,
                analysis=analysis,
                plan=None,
                element_results=[],
                errors=[f"Planung fehlgeschlagen: {str(e)}"]
            )

        # 3. Ausführung
        try:
            results = self.execute(plan)
        except Exception as e:
            return OrchestratorResult(
                success=False,
                analysis=analysis,
                plan=plan,
                element_results=[],
                errors=[f"Ausführung fehlgeschlagen: {str(e)}"]
            )

        # Erfolg prüfen
        success = all(r.success for r in results)
        for r in results:
            if not r.success:
                errors.append(f"{r.original_type}: {r.error}")

        return OrchestratorResult(
            success=success,
            analysis=analysis,
            plan=plan,
            element_results=results,
            errors=errors
        )

    async def run_async(self, content: str | dict, content_items: list[dict] = None) -> OrchestratorResult:
        """Asynchrone Version von run()"""
        errors = []

        analysis = self.analyze(content)
        plan = self.plan(analysis, content_items)
        results = await self.execute_async(plan)

        success = all(r.success for r in results)
        for r in results:
            if not r.success:
                errors.append(f"{r.original_type}: {r.error}")

        return OrchestratorResult(
            success=success,
            analysis=analysis,
            plan=plan,
            element_results=results,
            errors=errors
        )


# CLI-Interface
if __name__ == "__main__":
    import sys

    orchestrator = H5POrchestrator()

    # Beispiel-Content
    example_content = """
    # Scrum-Einführung

    ## Lernziele
    - Die Schüler können die drei Scrum-Rollen nennen
    - Die Schüler können Aufgaben den Rollen zuordnen
    - Die Schüler können den Sprint-Ablauf erklären

    ## Inhalte
    - Product Owner: Priorisiert Backlog, definiert User Stories
    - Scrum Master: Entfernt Hindernisse, moderiert Meetings
    - Development Team: Entwickelt Features, schätzt Aufwände
    """

    # Content-Items für jeden Operator
    content_items = [
        # nennen → Flashcards
        {
            'cards': [
                {'front': 'Product Owner', 'back': 'Priorisiert das Product Backlog und definiert User Stories'},
                {'front': 'Scrum Master', 'back': 'Entfernt Hindernisse und moderiert Scrum-Events'},
                {'front': 'Development Team', 'back': 'Entwickelt Features und schätzt Aufwände'},
            ]
        },
        # zuordnen → Drag & Drop
        {
            'task_description': 'Ordne die Aufgaben den richtigen Scrum-Rollen zu.',
            'dropzones': ['Product Owner', 'Scrum Master', 'Development Team'],
            'draggables': [
                {'text': 'Priorisiert Backlog', 'dropzone': 0},
                {'text': 'Entfernt Hindernisse', 'dropzone': 1},
                {'text': 'Entwickelt Features', 'dropzone': 2},
                {'text': 'Definiert User Stories', 'dropzone': 0},
                {'text': 'Moderiert Daily', 'dropzone': 1},
                {'text': 'Schätzt Aufwände', 'dropzone': 2},
            ]
        },
        # erklären → Accordion
        {
            'panels': [
                {'title': 'Sprint Planning', 'content': 'Am Anfang jedes Sprints plant das Team die Arbeit für die nächsten 2-4 Wochen.'},
                {'title': 'Daily Scrum', 'content': 'Tägliches 15-Minuten-Meeting zur Synchronisation des Teams.'},
                {'title': 'Sprint Review', 'content': 'Präsentation der Ergebnisse am Ende des Sprints.'},
                {'title': 'Retrospektive', 'content': 'Reflexion über den Prozess und Verbesserungen.'},
            ]
        }
    ]

    print("=" * 60)
    print("H5P Orchestrator - Demo")
    print("=" * 60)

    result = orchestrator.run(example_content, content_items)

    print(f"\n📊 Analyse:")
    print(f"   Lernziele: {len(result.analysis.learning_goals)}")
    print(f"   Operatoren: {result.analysis.operators}")
    print(f"   Struktur: {result.analysis.content_structure.value}")
    print(f"   Komplexität: {result.analysis.complexity.value}")
    print(f"   Container: {result.analysis.suggested_container or 'Keiner'}")

    print(f"\n📋 Plan:")
    for e in result.plan.elements:
        print(f"   {e.id}: {e.content_type} ({e.agent_type})")

    print(f"\n🎯 Ergebnisse:")
    for r in result.element_results:
        print(f"   {r}")

    print(f"\n{'✅ Erfolg!' if result.success else '❌ Fehler!'}")
    if result.errors:
        for err in result.errors:
            print(f"   ⚠️ {err}")
