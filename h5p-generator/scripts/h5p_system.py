#!/usr/bin/env python3
"""
H5P Multi-Agent System - Unified API

Zentraler Einstiegspunkt fuer das gesamte H5P-Generierungssystem.

Architektur:
    Input (Text/Dict)
         │
         ▼
    ┌─────────────────┐
    │   H5PSystem     │  ◄── Unified API
    └─────────────────┘
         │
         ▼
    ┌─────────────────┐
    │  Orchestrator   │  ◄── Analyse → Plan → Execute
    └─────────────────┘
         │
    ┌────┼────┬────┐
    ▼    ▼    ▼    ▼
   Quiz Card Drag Design  ◄── Sub-Agents
         │
         ▼
    ┌─────────────────┐
    │  H5P-Dateien    │  ◄── Output
    └─────────────────┘

Usage:
    # Quick Start
    from h5p_system import H5PSystem

    system = H5PSystem()
    result = system.generate_from_text('''
        ## Lernziele
        - Schueler koennen Scrum-Rollen nennen
    ''')

    # Mit Branding
    system = H5PSystem(brand='bswi')

    # Mit Custom Output
    system = H5PSystem(output_dir='./my-output', brand='professional')
"""

import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Union, List, Dict, Any

# Imports aus dem System
from h5p_generator import (
    H5PResult, H5PStyle, THEMES,
    create_true_false, create_multi_choice, create_fill_blanks,
    create_drag_drop, create_single_choice, create_flashcards,
    create_mark_words, create_summary, create_accordion,
    create_drag_text, create_timeline, create_memory_game,
    batch_create
)

from orchestrator import (
    H5POrchestrator, OrchestratorResult,
    ContentAnalysis, ExecutionPlan, ContentStructure, Complexity
)

from sub_agents import (
    QuizAgent, CardAgent, DragAgent, DesignAgent,
    AgentResult, DesignResult, BaseH5PAgent,
    CombinerAgent, CombineResult, ContainerType,
    # Text-zu-Quiz Agents (NEU v2.3)
    TextParserAgent, ParsedQuestion, ParseResult, QuestionType,
    DistractorGenerator, DistractorResult
)

from h5p_containers import (
    create_column, create_question_set, create_course_presentation
)

from brand_config import (
    BrandConfig, ColorScheme, LogoConfig, FeedbackTexts,
    get_brand_preset, list_brand_presets, create_brand_config
)


@dataclass
class SystemResult:
    """Ergebnis einer H5P-Generierung durch das Gesamtsystem"""
    success: bool
    h5p_files: List[Path] = field(default_factory=list)
    orchestrator_result: Optional[OrchestratorResult] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    statistics: Dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        if self.success:
            files = ", ".join(str(f.name) for f in self.h5p_files)
            return f"[OK] {len(self.h5p_files)} H5P-Datei(en) erstellt: {files}"
        return f"[FAIL] {'; '.join(self.errors)}"

    def summary(self) -> str:
        """Gibt detaillierte Zusammenfassung zurueck"""
        lines = []
        lines.append("=" * 60)
        lines.append("H5P System - Ergebnis")
        lines.append("=" * 60)

        lines.append(f"\nStatus: {'Erfolg' if self.success else 'Fehlgeschlagen'}")
        lines.append(f"Dateien: {len(self.h5p_files)}")

        if self.h5p_files:
            lines.append("\nErstelle Dateien:")
            for f in self.h5p_files:
                lines.append(f"  - {f}")

        if self.orchestrator_result:
            or_result = self.orchestrator_result
            if or_result.analysis:
                lines.append(f"\nAnalyse:")
                lines.append(f"  Lernziele: {len(or_result.analysis.learning_goals)}")
                lines.append(f"  Operatoren: {or_result.analysis.operators}")
                lines.append(f"  Komplexitaet: {or_result.analysis.complexity.value}")

            if or_result.design_results:
                lines.append(f"\nDesign angewendet:")
                for dr in or_result.design_results:
                    status = "OK" if dr.success else "Fehler"
                    changes = ", ".join(dr.changes_applied) if dr.changes_applied else "-"
                    lines.append(f"  [{status}] {dr.content_type}: {changes}")

        if self.warnings:
            lines.append(f"\nWarnungen:")
            for w in self.warnings:
                lines.append(f"  - {w}")

        if self.errors:
            lines.append(f"\nFehler:")
            for e in self.errors:
                lines.append(f"  - {e}")

        if self.statistics:
            lines.append(f"\nStatistiken:")
            for k, v in self.statistics.items():
                lines.append(f"  {k}: {v}")

        lines.append("\n" + "=" * 60)
        return "\n".join(lines)


class H5PSystem:
    """
    Unified API fuer das H5P Multi-Agent System.

    Das System bietet drei Abstraktionsebenen:

    1. HIGH-LEVEL: generate_from_text()
       - Freitext/Markdown rein, H5P-Dateien raus
       - Automatische Analyse, Planung, Generierung

    2. MID-LEVEL: generate_elements()
       - Strukturierte Eingabe mit Content-Items
       - Volle Kontrolle ueber H5P-Typen

    3. LOW-LEVEL: Direkter Zugriff auf Sub-Agents
       - system.quiz_agent, system.card_agent, etc.
       - Fuer spezielle Anwendungsfaelle

    Beispiele:
        # High-Level
        system = H5PSystem(brand='bswi')
        result = system.generate_from_text(lernmaterial)

        # Mid-Level
        result = system.generate_elements([
            {'type': 'flashcards', 'title': 'Vokabeln', 'cards': [...]},
            {'type': 'drag_drop', 'title': 'Zuordnung', 'dropzones': [...]}
        ])

        # Low-Level
        flashcards = system.card_agent.create_flashcards('Test', cards=[...])
    """

    VERSION = "2.3.0"

    def __init__(
        self,
        output_dir: Union[str, Path] = None,
        brand: Union[str, BrandConfig] = None,
        style: H5PStyle = None
    ):
        """
        Initialisiert das H5P System.

        Args:
            output_dir: Ausgabeverzeichnis fuer H5P-Dateien
            brand: Brand-Preset Name ('bswi', 'minimal', etc.) oder BrandConfig
            style: Legacy H5PStyle (wird von brand ueberschrieben wenn angegeben)
        """
        # Output-Verzeichnis
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = Path(__file__).parent.parent / "test-output"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Brand-Konfiguration
        if isinstance(brand, BrandConfig):
            self.brand_config = brand
        elif isinstance(brand, str):
            self.brand_config = get_brand_preset(brand)
        else:
            self.brand_config = None

        # Style (fuer Legacy-Kompatibilitaet)
        self.style = style or THEMES.get('education')

        # Orchestrator initialisieren
        self._orchestrator = H5POrchestrator(
            output_dir=self.output_dir,
            brand_config=self.brand_config
        )

        # Sub-Agents direkt verfuegbar machen
        self.quiz_agent = self._orchestrator.agents['quiz']
        self.card_agent = self._orchestrator.agents['card']
        self.drag_agent = self._orchestrator.agents['drag']
        self.design_agent = self._orchestrator._design_agent
        self.combiner_agent = self._orchestrator._combiner_agent

    # =========================================================================
    # HIGH-LEVEL API
    # =========================================================================

    def generate_from_text(
        self,
        content: str,
        content_items: List[Dict] = None,
        apply_design: bool = True,
        combine: bool = False,
        combine_type: str = 'auto',
        combine_title: str = None
    ) -> SystemResult:
        """
        Generiert H5P-Inhalte aus Freitext/Markdown.

        Dies ist der empfohlene Einstiegspunkt fuer die meisten Anwendungsfaelle.
        Das System analysiert den Text, erkennt Lernziele und Operatoren,
        waehlt passende H5P-Typen und generiert die Dateien.

        Args:
            content: Lernmaterial als Freitext oder Markdown
            content_items: Optionale Content-Daten pro Element
            apply_design: Branding anwenden (default: True)
            combine: Elemente zu Container kombinieren (default: False)
            combine_type: Container-Typ: 'auto', 'column', 'question_set', 'course_presentation'
            combine_title: Titel fuer den kombinierten Container

        Returns:
            SystemResult mit generierten H5P-Dateien

        Beispiel:
            # Einzelne Elemente
            result = system.generate_from_text(lernmaterial, content_items)

            # Mit automatischer Kombination
            result = system.generate_from_text(
                lernmaterial,
                content_items,
                combine=True,
                combine_type='column',
                combine_title='Scrum-Lerneinheit'
            )
        """
        errors = []
        warnings = []
        h5p_files = []

        try:
            # Orchestrator ausfuehren
            or_result = self._orchestrator.run(
                content=content,
                content_items=content_items,
                apply_design=apply_design,
                combine=combine_type if combine else False,
                combine_title=combine_title
            )

            # H5P-Dateien sammeln
            for agent_result in or_result.element_results:
                if agent_result.success and agent_result.h5p_result:
                    if agent_result.h5p_result.path:
                        h5p_files.append(Path(agent_result.h5p_result.path))
                else:
                    if agent_result.error:
                        errors.append(f"{agent_result.original_type}: {agent_result.error}")

            # Design-Warnungen
            for dr in or_result.design_results:
                if not dr.success and dr.error:
                    warnings.append(f"Design {dr.content_type}: {dr.error}")

            # Kombiniertes Ergebnis hinzufuegen
            combined_file = None
            if or_result.combined_result and or_result.combined_result.success:
                if or_result.combined_result.h5p_result and or_result.combined_result.h5p_result.path:
                    combined_file = Path(or_result.combined_result.h5p_result.path)
                    h5p_files.append(combined_file)

            # Errors aus Orchestrator
            errors.extend(or_result.errors)

            # Statistiken
            stats = {
                'lernziele_erkannt': len(or_result.analysis.learning_goals) if or_result.analysis else 0,
                'operatoren': or_result.analysis.operators if or_result.analysis else [],
                'elemente_geplant': len(or_result.plan.elements) if or_result.plan else 0,
                'elemente_erstellt': len(h5p_files) - (1 if combined_file else 0),
                'design_angewendet': len([dr for dr in or_result.design_results if dr.success]),
                'kombiniert': or_result.combined_result.container_type if or_result.combined_result and or_result.combined_result.success else None,
                'kombinierte_datei': str(combined_file) if combined_file else None
            }

            return SystemResult(
                success=or_result.success and len(h5p_files) > 0,
                h5p_files=h5p_files,
                orchestrator_result=or_result,
                errors=errors,
                warnings=warnings,
                statistics=stats
            )

        except Exception as e:
            return SystemResult(
                success=False,
                errors=[f"System-Fehler: {str(e)}"]
            )

    def generate_from_dict(
        self,
        data: Dict,
        apply_design: bool = True
    ) -> SystemResult:
        """
        Generiert H5P-Inhalte aus strukturiertem Dict.

        Args:
            data: Strukturierte Eingabe mit learning_goals, operators, etc.
            apply_design: Branding anwenden

        Returns:
            SystemResult
        """
        return self.generate_from_text(
            content=data,
            content_items=data.get('content_items'),
            apply_design=apply_design
        )

    def generate_from_questions(
        self,
        questions_text: str,
        title: str = "Quiz",
        output_format: str = 'auto',
        generate_distractors: bool = True,
        domain: str = None,
        apply_design: bool = True
    ) -> SystemResult:
        """
        Generiert H5P-Quiz aus Freitext-Fragen.

        Dies ist der einfachste Einstiegspunkt fuer Quiz-Erstellung:
        Einfach Fragen als Text eingeben, H5P-Quiz als Output.

        Args:
            questions_text: Freitext mit Fragen in einem der unterstuetzten Formate:
                - Simple: "Nenne 3 Merkmale..."
                - With Answers: "Was ist X? - Option A - Option B [correct]"
                - Batch TF: "--- Q: Aussage A: wahr ---"
            title: Titel des Quiz
            output_format: 'auto', 'true_false', 'multi_choice', 'question_set'
            generate_distractors: Bei offenen Fragen Distraktoren generieren
            domain: Fachbereich fuer Distraktoren ('accounting', 'scrum', 'it', 'business')
            apply_design: Branding anwenden (default: True)

        Returns:
            SystemResult mit generierter H5P-Datei

        Beispiele:
            # Multiple Choice mit Antworten
            result = system.generate_from_questions('''
                Was ist ein Debitor?
                - Ein Schuldner
                - Ein Glaeubiger [correct]
                - Ein Lieferant
            ''', title="Rechnungswesen Quiz")

            # Batch True/False
            result = system.generate_from_questions('''
                ---
                Q: Python ist eine Programmiersprache.
                A: wahr
                ---
                Q: Python wurde 2020 erfunden.
                A: falsch
            ''', title="Python Quiz")

            # Einfache Aussagen (werden zu TF)
            result = system.generate_from_questions('''
                Die Bilanz zeigt Vermoegen und Kapital.
                Kreditoren erscheinen auf der Aktivseite.
            ''', title="Buchfuehrung Quiz", domain="accounting")
        """
        errors = []
        warnings = []
        h5p_files = []

        try:
            # 1. Text parsen
            parser = TextParserAgent()
            parse_result = parser.parse(questions_text)

            if not parse_result.success:
                return SystemResult(
                    success=False,
                    errors=[f"Parse-Fehler: {'; '.join(parse_result.errors)}"]
                )

            warnings.extend(parse_result.warnings)

            # 2. Output-Format bestimmen
            if output_format == 'auto':
                if parse_result.detected_type == QuestionType.MULTI_CHOICE:
                    output_format = 'multi_choice'
                elif parse_result.detected_type == QuestionType.TRUE_FALSE:
                    output_format = 'true_false'
                elif parse_result.detected_type == QuestionType.OPEN:
                    # Offene Fragen brauchen Distraktoren -> MC
                    if generate_distractors:
                        output_format = 'multi_choice'
                    else:
                        output_format = 'true_false'
                else:
                    output_format = 'true_false'

            # 3. Distraktoren generieren falls noetig
            if generate_distractors and output_format == 'multi_choice':
                distractor_gen = DistractorGenerator()
                for q in parse_result.questions:
                    if q.question_type == QuestionType.OPEN or not q.answers:
                        # Distraktoren fuer offene Fragen generieren
                        # Die Frage selbst als "korrekte Antwort" verwenden (fuer Fakten-Aussagen)
                        if q.bloom_operator in ['nennen', 'beschreiben', 'definieren']:
                            # Aus der Frage extrahierte Konzepte als Basis
                            concepts = parser.extract_key_concepts(q.question_text)
                            if concepts:
                                correct_concept = concepts[0]
                                dist_result = distractor_gen.generate(
                                    correct_answer=correct_concept,
                                    question=q.question_text,
                                    domain=domain,
                                    count=3
                                )
                                q.answers = [{"text": correct_concept, "correct": True}]
                                for d in dist_result.distractors:
                                    q.answers.append({"text": d, "correct": False})
                                q.question_type = QuestionType.MULTI_CHOICE
                                warnings.extend(dist_result.warnings)

            # 4. Quiz-Daten erstellen
            if output_format == 'true_false':
                questions_data = parse_result.to_true_false_list()
                result = self.generate_single(
                    'true_false',
                    title=title,
                    questions=questions_data,
                    apply_design=apply_design
                )
            elif output_format == 'multi_choice':
                questions_data = []
                for q in parse_result.questions:
                    if q.answers:
                        questions_data.append({
                            "question": q.question_text,
                            "answers": q.answers
                        })
                    else:
                        # Fallback: Als True/False behandeln
                        warnings.append(f"Frage ohne Antworten: {q.question_text[:30]}...")

                if questions_data:
                    result = self.generate_single(
                        'multi_choice',
                        title=title,
                        questions=questions_data,
                        apply_design=apply_design
                    )
                else:
                    return SystemResult(
                        success=False,
                        errors=["Keine gueltigen Multiple-Choice-Fragen gefunden"]
                    )
            elif output_format == 'question_set':
                # Als QuestionSet (mehrere Fragen in einem Container)
                elements = []
                for q in parse_result.questions:
                    if q.answers:
                        elements.append({
                            'type': 'multi_choice',
                            'title': q.question_text[:50],
                            'questions': [{
                                "question": q.question_text,
                                "answers": q.answers
                            }]
                        })
                    else:
                        elements.append({
                            'type': 'true_false',
                            'title': q.question_text[:50],
                            'questions': [q.to_true_false()]
                        })

                result = self.generate_elements(elements, apply_design=apply_design)
            else:
                return SystemResult(
                    success=False,
                    errors=[f"Unbekanntes Output-Format: {output_format}"]
                )

            # 5. Ergebnis zusammenstellen
            h5p_files = result.h5p_files
            errors.extend(result.errors)
            warnings.extend(result.warnings)

            # Statistiken
            stats = {
                'detected_format': parse_result.detected_format.value,
                'detected_type': parse_result.detected_type.value,
                'questions_parsed': parse_result.question_count,
                'output_format': output_format,
                'distractors_generated': generate_distractors,
                'domain': domain
            }

            return SystemResult(
                success=result.success,
                h5p_files=h5p_files,
                errors=errors,
                warnings=warnings,
                statistics=stats
            )

        except Exception as e:
            return SystemResult(
                success=False,
                errors=[f"System-Fehler: {str(e)}"]
            )

    # =========================================================================
    # MID-LEVEL API
    # =========================================================================

    def generate_elements(
        self,
        elements: List[Dict],
        apply_design: bool = True
    ) -> SystemResult:
        """
        Generiert mehrere H5P-Elemente aus einer Element-Liste.

        Nutzt die batch_create Funktion fuer effiziente Verarbeitung.

        Args:
            elements: Liste von Element-Dicts mit 'type' und typ-spezifischen Feldern
            apply_design: Branding anwenden

        Returns:
            SystemResult

        Beispiel:
            result = system.generate_elements([
                {
                    'type': 'flashcards',
                    'title': 'Scrum-Rollen',
                    'cards': [
                        {'front': 'PO', 'back': 'Product Owner'},
                        {'front': 'SM', 'back': 'Scrum Master'},
                    ]
                },
                {
                    'type': 'true_false',
                    'title': 'Scrum Quiz',
                    'questions': [
                        {'text': 'Der PO priorisiert das Backlog.', 'correct': True}
                    ]
                }
            ])
        """
        errors = []
        warnings = []
        h5p_files = []

        try:
            # batch_create nutzen
            results = batch_create(elements, style=self.style)

            for result in results:
                if result.success and result.path:
                    h5p_path = Path(result.path)
                    h5p_files.append(h5p_path)

                    # Design anwenden wenn gewuenscht
                    if apply_design and self.design_agent:
                        # Fake AgentResult fuer Design Agent
                        from sub_agents.base_agent import AgentStatus
                        fake_agent_result = AgentResult(
                            status=AgentStatus.SUCCESS,
                            h5p_result=result,
                            original_type=result.content_type,
                            final_type=result.content_type
                        )
                        design_result = self.design_agent.apply_branding(fake_agent_result)
                        if not design_result.success:
                            warnings.append(f"Design {result.content_type}: {design_result.error}")
                else:
                    errors.append(f"{result.content_type}: {result.error}")

            return SystemResult(
                success=len(h5p_files) > 0,
                h5p_files=h5p_files,
                errors=errors,
                warnings=warnings,
                statistics={
                    'elemente_angefragt': len(elements),
                    'elemente_erstellt': len(h5p_files)
                }
            )

        except Exception as e:
            return SystemResult(
                success=False,
                errors=[f"Batch-Generierung fehlgeschlagen: {str(e)}"]
            )

    def generate_single(
        self,
        content_type: str,
        apply_design: bool = True,
        **kwargs
    ) -> SystemResult:
        """
        Generiert ein einzelnes H5P-Element.

        Args:
            content_type: H5P-Typ (flashcards, drag_drop, etc.)
            apply_design: Branding anwenden
            **kwargs: Typ-spezifische Parameter

        Returns:
            SystemResult

        Beispiel:
            result = system.generate_single(
                'flashcards',
                title='Vokabeln',
                cards=[{'front': 'Haus', 'back': 'house'}]
            )
        """
        element = {'type': content_type, **kwargs}
        return self.generate_elements([element], apply_design=apply_design)

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def analyze_content(self, content: str) -> ContentAnalysis:
        """
        Analysiert Content ohne Generierung.

        Nuetzlich um zu sehen, wie das System den Input interpretiert.
        """
        return self._orchestrator.analyze(content)

    def create_plan(
        self,
        content: str,
        content_items: List[Dict] = None
    ) -> ExecutionPlan:
        """
        Erstellt Ausfuehrungsplan ohne Generierung.

        Nuetzlich fuer Debugging und Vorschau.
        """
        analysis = self._orchestrator.analyze(content)
        return self._orchestrator.plan(analysis, content_items)

    def apply_design_to_file(self, h5p_path: Union[str, Path]) -> DesignResult:
        """
        Wendet Branding auf existierende H5P-Datei an.
        """
        if not self.design_agent:
            return DesignResult(
                success=False,
                original_path=Path(h5p_path),
                error="Kein Design Agent konfiguriert (brand fehlt)"
            )
        return self.design_agent.style_h5p_file(h5p_path)

    @staticmethod
    def list_content_types() -> List[str]:
        """Gibt alle verfuegbaren H5P-Typen zurueck"""
        return [
            'true_false', 'multi_choice', 'single_choice',
            'fill_blanks', 'drag_drop', 'drag_text',
            'flashcards', 'accordion', 'timeline', 'memory_game',
            'mark_words', 'summary'
        ]

    @staticmethod
    def list_brand_presets() -> List[str]:
        """Gibt alle verfuegbaren Brand-Presets zurueck"""
        return list_brand_presets()

    def get_system_info(self) -> Dict:
        """Gibt System-Informationen zurueck"""
        return {
            'version': self.VERSION,
            'output_dir': str(self.output_dir),
            'brand': self.brand_config.name if self.brand_config else None,
            'content_types': self.list_content_types(),
            'brand_presets': self.list_brand_presets(),
            'design_agent_active': self.design_agent is not None
        }


# =============================================================================
# Convenience Functions (fuer schnellen Zugriff)
# =============================================================================

def quick_generate(content: str, brand: str = None) -> SystemResult:
    """
    Schnelle Generierung ohne explizite System-Erstellung.

    Args:
        content: Lernmaterial als Text
        brand: Optionales Brand-Preset

    Returns:
        SystemResult

    Beispiel:
        result = quick_generate('## Lernziele\\n- Schueler koennen...')
    """
    system = H5PSystem(brand=brand)
    return system.generate_from_text(content)


def quick_flashcards(title: str, cards: List[Dict], brand: str = None) -> SystemResult:
    """Schnelle Flashcard-Erstellung"""
    system = H5PSystem(brand=brand)
    return system.generate_single('flashcards', title=title, cards=cards)


def quick_quiz(title: str, questions: List[Dict], brand: str = None) -> SystemResult:
    """Schnelle Quiz-Erstellung (True/False)"""
    system = H5PSystem(brand=brand)
    return system.generate_single('true_false', title=title, questions=questions)


def quick_drag_drop(
    title: str,
    dropzones: List[str],
    draggables: List[Dict],
    brand: str = None
) -> SystemResult:
    """Schnelle Drag&Drop-Erstellung"""
    system = H5PSystem(brand=brand)
    return system.generate_single(
        'drag_drop',
        title=title,
        task='Ordne zu.',
        dropzones=dropzones,
        draggables=draggables
    )


def quick_quiz_from_text(
    questions_text: str,
    title: str = "Quiz",
    domain: str = None,
    brand: str = None
) -> SystemResult:
    """
    Schnelle Quiz-Erstellung aus Freitext.

    Args:
        questions_text: Fragen als Freitext (siehe generate_from_questions)
        title: Quiz-Titel
        domain: Fachbereich fuer Distraktoren ('accounting', 'scrum', 'it', 'business')
        brand: Optionales Brand-Preset

    Returns:
        SystemResult

    Beispiel:
        result = quick_quiz_from_text('''
            Was ist ein Debitor?
            - Ein Schuldner
            - Ein Glaeubiger [correct]
            - Ein Lieferant
        ''', title="Rechnungswesen", domain="accounting")
    """
    system = H5PSystem(brand=brand)
    return system.generate_from_questions(
        questions_text,
        title=title,
        domain=domain
    )


# =============================================================================
# CLI Entry Point
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("H5P Multi-Agent System v" + H5PSystem.VERSION)
    print("=" * 60)

    # Demo
    system = H5PSystem(brand='bswi')
    info = system.get_system_info()

    print(f"\nAusgabe-Verzeichnis: {info['output_dir']}")
    print(f"Brand: {info['brand']}")
    print(f"Design Agent: {'aktiv' if info['design_agent_active'] else 'inaktiv'}")
    print(f"\nVerfuegbare H5P-Typen: {len(info['content_types'])}")
    print(f"  {', '.join(info['content_types'])}")
    print(f"\nVerfuegbare Brand-Presets:")
    print(f"  {', '.join(info['brand_presets'])}")

    # Beispiel-Generierung
    print("\n" + "=" * 60)
    print("Demo: Scrum-Lerneinheit generieren")
    print("=" * 60)

    result = system.generate_from_text('''
## Lernziele
- Schueler koennen die drei Scrum-Rollen nennen
- Schueler koennen Aufgaben den Rollen zuordnen
    ''', content_items=[
        {
            'cards': [
                {'front': 'Product Owner', 'back': 'Priorisiert das Product Backlog und definiert User Stories'},
                {'front': 'Scrum Master', 'back': 'Entfernt Hindernisse und moderiert Scrum-Events'},
                {'front': 'Development Team', 'back': 'Entwickelt Features und schaetzt Aufwaende'},
            ]
        },
        {
            'task_description': 'Ordne die Aufgaben den richtigen Scrum-Rollen zu.',
            'dropzones': ['Product Owner', 'Scrum Master', 'Development Team'],
            'draggables': [
                {'text': 'Priorisiert Backlog', 'dropzone': 0},
                {'text': 'Entfernt Hindernisse', 'dropzone': 1},
                {'text': 'Entwickelt Features', 'dropzone': 2},
                {'text': 'Definiert User Stories', 'dropzone': 0},
                {'text': 'Moderiert Daily', 'dropzone': 1},
            ]
        }
    ])

    print(result.summary())
