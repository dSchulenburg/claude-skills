"""
Combiner Agent - Kombiniert H5P-Elemente zu Container-Typen

Der Combiner Agent nimmt fertige H5P-Elemente (AgentResults) und
kombiniert sie zu komplexen Container-Typen:

- Column: Vertikale Anordnung (2-5 Elemente)
- QuestionSet: Quiz-Sequenz (nur Quiz-Typen)
- CoursePresentation: Slides mit Text-Zusammenfassungen
- InteractiveBook: Kapitel mit interaktiven Elementen (empfohlen!)

Workflow:
1. Elemente analysieren (Typen, Anzahl)
2. Container-Typ waehlen oder vorgegeben
3. Elemente extrahieren und einbetten
4. Container generieren

LEARNING (2025-01-25): Interactive Book Kompatibilitaet in Lumi
- Funktioniert: AdvancedText, Dialogcards, TrueFalse, MultiChoice, DragText
- Funktioniert NICHT: Blanks, DragQuestion
- Siehe: LEARNINGS-InteractiveBook.md
"""

import json
import zipfile
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any
from enum import Enum
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from h5p_containers import (
    create_column, create_question_set, create_course_presentation, create_interactive_book,
    ColumnGenerator, QuestionSetGenerator, CoursePresentationGenerator, InteractiveBookGenerator
)
from h5p_generator import H5PResult
from .base_agent import AgentResult, AgentStatus


class ContainerType(Enum):
    """Verfuegbare Container-Typen"""
    COLUMN = "column"
    QUESTION_SET = "question_set"
    COURSE_PRESENTATION = "course_presentation"
    INTERACTIVE_BOOK = "interactive_book"  # TODO
    AUTO = "auto"  # Automatische Auswahl


@dataclass
class CombineResult:
    """Ergebnis einer Kombination"""
    success: bool
    h5p_result: Optional[H5PResult] = None
    container_type: str = ""
    elements_combined: int = 0
    errors: List[str] = field(default_factory=list)

    def __str__(self):
        if self.success:
            return f"[COMBINE OK] {self.container_type}: {self.elements_combined} Elemente"
        return f"[COMBINE FAIL] {'; '.join(self.errors)}"


class CombinerAgent:
    """
    Agent fuer die Kombination von H5P-Elementen zu Containern.

    Features:
    - Automatische Container-Typ-Auswahl
    - Extraktion von content.json aus fertigen H5P-Dateien
    - Einbettung in Container-Strukturen
    - Quiz-spezifische QuestionSet-Erstellung
    """

    # Mapping: H5P-Typ -> Kann in QuestionSet eingebettet werden
    QUIZ_TYPES = {
        'H5P.TrueFalse',
        'H5P.MultiChoice',
        'H5P.DragQuestion',
        'H5P.DragText',
        'H5P.Blanks',
        'H5P.MarkTheWords',
        'H5P.Summary',
        'H5P.SingleChoiceSet',
    }

    # LEARNING: Typen die in Interactive Book (Lumi) funktionieren
    # Getestet: 2025-01-25
    INTERACTIVE_BOOK_COMPATIBLE = {
        'H5P.AdvancedText',
        'H5P.Dialogcards',    # Flashcards
        'H5P.TrueFalse',
        'H5P.MultiChoice',
        'H5P.DragText',       # Alternative zu Blanks
    }

    # LEARNING: Typen die in Interactive Book NICHT funktionieren
    INTERACTIVE_BOOK_INCOMPATIBLE = {
        'H5P.Blanks',         # Vorschau laedt nicht
        'H5P.DragQuestion',   # Vorschau laedt nicht
    }

    # Fallback-Mapping fuer inkompatible Typen in Interactive Book
    INTERACTIVE_BOOK_FALLBACK = {
        'fill_blanks': 'drag_text',      # Blanks -> DragText
        'FillInBlanks': 'drag_text',
        'drag_drop': 'multi_choice',      # DragQuestion -> MultiChoice
        'DragDrop': 'multi_choice',
    }

    # Mapping: Content-Type String -> H5P Library
    TYPE_TO_LIBRARY = {
        'true_false': 'H5P.TrueFalse 1.8',
        'TrueFalse': 'H5P.TrueFalse 1.8',
        'multi_choice': 'H5P.MultiChoice 1.16',
        'MultiChoice': 'H5P.MultiChoice 1.16',
        'single_choice': 'H5P.SingleChoiceSet 1.11',
        'SingleChoiceSet': 'H5P.SingleChoiceSet 1.11',
        'drag_drop': 'H5P.DragQuestion 1.14',
        'DragDrop': 'H5P.DragQuestion 1.14',
        'drag_text': 'H5P.DragText 1.10',
        'DragText': 'H5P.DragText 1.10',
        'fill_blanks': 'H5P.Blanks 1.14',
        'FillInBlanks': 'H5P.Blanks 1.14',
        'mark_words': 'H5P.MarkTheWords 1.11',
        'MarkTheWords': 'H5P.MarkTheWords 1.11',
        'summary': 'H5P.Summary 1.10',
        'Summary': 'H5P.Summary 1.10',
        'flashcards': 'H5P.Dialogcards 1.9',
        'DialogCards': 'H5P.Dialogcards 1.9',
        'accordion': 'H5P.Accordion 1.0',
        'Accordion': 'H5P.Accordion 1.0',
        'timeline': 'H5P.Timeline 1.1',
        'Timeline': 'H5P.Timeline 1.1',
    }

    def __init__(self, output_dir: Path = None):
        self.output_dir = Path(output_dir) if output_dir else Path("../test-output")

    def combine(
        self,
        elements: List[AgentResult],
        container_type: ContainerType = ContainerType.AUTO,
        title: str = "Kombinierte Lerneinheit",
        **kwargs
    ) -> CombineResult:
        """
        Kombiniert mehrere AgentResults zu einem Container.

        Args:
            elements: Liste von AgentResults mit fertigen H5P-Dateien
            container_type: Gewuenschter Container-Typ oder AUTO
            title: Titel des Containers
            **kwargs: Zusaetzliche Container-spezifische Optionen

        Returns:
            CombineResult
        """
        errors = []

        # Erfolgreiche Elemente filtern
        valid_elements = [e for e in elements if e.success and e.h5p_result]
        if len(valid_elements) < 2:
            return CombineResult(
                success=False,
                errors=["Mindestens 2 gueltige Elemente fuer Kombination benoetigt"]
            )

        # Container-Typ bestimmen
        if container_type == ContainerType.AUTO:
            container_type = self._choose_container_type(valid_elements)

        # Content aus H5P-Dateien extrahieren
        extracted = []
        for elem in valid_elements:
            try:
                content_data = self._extract_h5p_content(elem.h5p_result.path)
                content_data['original_type'] = elem.final_type
                extracted.append(content_data)
            except Exception as e:
                errors.append(f"Extraktion fehlgeschlagen fuer {elem.final_type}: {e}")

        if not extracted:
            return CombineResult(
                success=False,
                errors=errors or ["Keine Inhalte extrahiert"]
            )

        # Container erstellen
        try:
            if container_type == ContainerType.COLUMN:
                result = self._create_column(title, extracted, **kwargs)
            elif container_type == ContainerType.QUESTION_SET:
                result = self._create_question_set(title, extracted, **kwargs)
            elif container_type == ContainerType.COURSE_PRESENTATION:
                result = self._create_course_presentation(title, extracted, **kwargs)
            elif container_type == ContainerType.INTERACTIVE_BOOK:
                result = self._create_interactive_book(title, extracted, **kwargs)
            else:
                return CombineResult(
                    success=False,
                    errors=[f"Container-Typ {container_type} nicht unterstuetzt"]
                )

            return CombineResult(
                success=result.success,
                h5p_result=result,
                container_type=container_type.value,
                elements_combined=len(extracted),
                errors=errors if not result.success else []
            )

        except Exception as e:
            return CombineResult(
                success=False,
                errors=[f"Container-Erstellung fehlgeschlagen: {e}"]
            )

    def _choose_container_type(self, elements: List[AgentResult]) -> ContainerType:
        """
        Waehlt automatisch den besten Container-Typ.

        Logik:
        - Nur Quiz-Typen -> QuestionSet
        - 2-3 Elemente -> Column
        - 4+ Elemente -> InteractiveBook (beste Interaktivitaet)
        """
        # Pruefen ob alle Quiz-Typen
        all_quiz = all(
            self._is_quiz_type(e.final_type) for e in elements
        )

        if all_quiz and len(elements) >= 2:
            return ContainerType.QUESTION_SET

        if len(elements) <= 3:
            return ContainerType.COLUMN

        # Bei 4+ Elementen: InteractiveBook fuer volle Interaktivitaet
        return ContainerType.INTERACTIVE_BOOK

    def _is_quiz_type(self, content_type: str) -> bool:
        """Prueft ob ein Typ ein Quiz-Typ ist"""
        library = self.TYPE_TO_LIBRARY.get(content_type, '')
        lib_name = library.split(' ')[0] if library else ''
        return lib_name in self.QUIZ_TYPES

    def _extract_h5p_content(self, h5p_path: Path) -> Dict:
        """
        Extrahiert content.json und h5p.json aus einer H5P-Datei.

        Returns:
            Dict mit 'content', 'h5p_meta', 'library'
        """
        with zipfile.ZipFile(h5p_path, 'r') as zf:
            content = json.loads(zf.read('content/content.json'))
            h5p_meta = json.loads(zf.read('h5p.json'))

        return {
            'content': content,
            'h5p_meta': h5p_meta,
            'library': h5p_meta.get('mainLibrary', ''),
            'dependencies': h5p_meta.get('preloadedDependencies', [])
        }

    def _unwrap_questionset_content(self, content: dict, element_type: str) -> dict:
        """
        Entpackt QuestionSet-Wrapper fuer einzelne Quiz-Elemente.

        Der H5P-Generator erzeugt MultiChoice/TrueFalse als QuestionSet mit
        questions[]-Array. Fuer Interactive Book brauchen wir nur die
        einzelne Frage (questions[0].params).
        """
        # Pruefe ob QuestionSet-Struktur vorliegt
        if 'questions' in content and isinstance(content['questions'], list):
            questions = content['questions']
            if len(questions) > 0:
                first_q = questions[0]
                # QuestionSet hat questions[].params mit der eigentlichen Frage
                if 'params' in first_q:
                    return first_q['params']
                # Oder direkt die Frage-Struktur
                return first_q

        # Kein QuestionSet - Content direkt zurueckgeben
        return content

    def _create_column(self, title: str, extracted: List[Dict], **kwargs) -> H5PResult:
        """Erstellt Column aus extrahierten Elementen"""
        elements = []

        for i, data in enumerate(extracted):
            # Library-Version ermitteln
            lib = data['library']
            version = "1.0"
            for dep in data.get('dependencies', []):
                if dep.get('machineName') == lib:
                    version = f"{dep['majorVersion']}.{dep['minorVersion']}"
                    break

            elements.append({
                'library': f"{lib} {version}",
                'params': data['content'],
                'subContentId': f"col-elem-{i}",
                'metadata': {
                    'contentType': data.get('original_type', 'Content'),
                    'license': 'U',
                    'title': f"Element {i+1}"
                }
            })

        return create_column(title, elements)

    def _create_question_set(self, title: str, extracted: List[Dict], **kwargs) -> H5PResult:
        """Erstellt QuestionSet aus extrahierten Quiz-Elementen"""
        questions = []

        for i, data in enumerate(extracted):
            lib = data['library']
            version = "1.0"
            for dep in data.get('dependencies', []):
                if dep.get('machineName') == lib:
                    version = f"{dep['majorVersion']}.{dep['minorVersion']}"
                    break

            questions.append({
                'library': f"{lib} {version}",
                'params': data['content'],
                'subContentId': f"qs-q-{i}",
                'metadata': {
                    'contentType': data.get('original_type', 'Question'),
                    'license': 'U',
                    'title': f"Frage {i+1}"
                }
            })

        pass_percentage = kwargs.get('pass_percentage', 60)
        return create_question_set(title, questions, pass_percentage=pass_percentage)

    def _create_course_presentation(self, title: str, extracted: List[Dict], **kwargs) -> H5PResult:
        """
        Erstellt CoursePresentation mit Text-basierten Slides.

        HINWEIS: CoursePresentation kann keine komplexen H5P-Typen einbetten.
        Stattdessen werden informative Text-Slides erstellt, die den Inhalt
        der einzelnen Elemente zusammenfassen.
        """
        slides = []

        # Titel-Slide
        slides.append({
            'title': title,
            'content': f'<p>Diese Präsentation enthält <strong>{len(extracted)} Lernelemente</strong>.</p><p>Navigiere mit den Pfeiltasten oder klicke auf die Punkte unten.</p>'
        })

        for i, data in enumerate(extracted):
            element_type = data.get('original_type', 'Unbekannt')
            content = data.get('content', {})

            # Slide-Inhalt basierend auf Typ erstellen
            slide_content = self._extract_summary_for_slide(element_type, content)

            slide = {
                'title': f'{i+1}. {element_type.replace("_", " ").title()}',
                'content': slide_content
            }
            slides.append(slide)

        # Abschluss-Slide
        slides.append({
            'title': 'Zusammenfassung',
            'content': f'<p>Du hast alle {len(extracted)} Elemente durchgearbeitet!</p><p>Die interaktiven Übungen findest du als separate H5P-Dateien.</p>'
        })

        return create_course_presentation(title, slides)

    def _create_interactive_book(self, title: str, extracted: List[Dict], **kwargs) -> H5PResult:
        """
        Erstellt Interactive Book mit echten interaktiven Elementen.

        Das Interactive Book kann im Gegensatz zu CoursePresentation
        komplexe H5P-Typen einbetten und bietet volle Interaktivitaet.
        """
        chapters = []

        # Einfuehrungs-Kapitel
        intro_chapter = {
            'title': 'Einfuehrung',
            'elements': [
                {
                    'library': 'H5P.AdvancedText 1.1',
                    'params': {
                        'text': f'<h2>Willkommen</h2><p>Dieses Buch enthaelt <strong>{len(extracted)} interaktive Lernelemente</strong>.</p><p>Nutze das Inhaltsverzeichnis links zur Navigation.</p>'
                    }
                }
            ]
        }
        chapters.append(intro_chapter)

        # Ein Kapitel pro Element
        chapter_num = 0
        for i, data in enumerate(extracted):
            element_type = data.get('original_type', 'Unbekannt')
            content = data.get('content', {})
            library = data.get('library', 'H5P.AdvancedText')

            # Vollstaendige Library-Version
            full_library = self.TYPE_TO_LIBRARY.get(element_type, f'{library} 1.0')
            lib_name = full_library.split(' ')[0] if ' ' in full_library else full_library

            # LEARNING: Pruefen ob Typ in Interactive Book kompatibel ist
            if lib_name in self.INTERACTIVE_BOOK_INCOMPATIBLE:
                # Inkompatiblen Typ als Text-Zusammenfassung darstellen
                chapter_num += 1
                summary = self._extract_summary_for_slide(element_type, content)
                chapter = {
                    'title': f'Kapitel {chapter_num}: {element_type.replace("_", " ").title()}',
                    'elements': [
                        {
                            'library': 'H5P.AdvancedText 1.1',
                            'params': {
                                'text': f'<h2>{element_type.replace("_", " ").title()}</h2><p><em>(Dieser Inhaltstyp ist nicht interaktiv einbettbar)</em></p>{summary}'
                            }
                        }
                    ]
                }
                chapters.append(chapter)
                continue

            chapter_num += 1

            # Quiz-Typen: QuestionSet-Wrapper entpacken
            if lib_name in self.QUIZ_TYPES:
                embedded_content = self._unwrap_questionset_content(content, element_type)
            else:
                embedded_content = content

            chapter = {
                'title': f'Kapitel {chapter_num}: {element_type.replace("_", " ").title()}',
                'elements': [
                    {
                        'library': 'H5P.AdvancedText 1.1',
                        'params': {
                            'text': f'<h2>{element_type.replace("_", " ").title()}</h2>'
                        }
                    },
                    {
                        'library': full_library,
                        'params': embedded_content,
                        'subContentId': f'book-ch{chapter_num}-elem',
                        'metadata': {
                            'contentType': element_type,
                            'license': 'U',
                            'title': f'Element {chapter_num}'
                        }
                    }
                ]
            }
            chapters.append(chapter)

        # Zusammenfassungs-Kapitel
        summary_chapter = {
            'title': 'Zusammenfassung',
            'elements': [
                {
                    'library': 'H5P.AdvancedText 1.1',
                    'params': {
                        'text': f'<h2>Geschafft!</h2><p>Du hast alle {len(extracted)} Kapitel durchgearbeitet.</p><p>Nutze die Fortschrittsanzeige oben, um deinen Lernfortschritt zu sehen.</p>'
                    }
                }
            ]
        }
        chapters.append(summary_chapter)

        cover_description = kwargs.get('cover_description', f'Ein interaktives Lernbuch mit {len(extracted)} Elementen')
        return create_interactive_book(title, chapters, cover_description=cover_description)

    def _extract_summary_for_slide(self, element_type: str, content: dict) -> str:
        """Extrahiert eine lesbare Zusammenfassung aus einem H5P-Element"""

        if element_type in ['flashcards', 'DialogCards']:
            # Flashcards: Zeige die Karten als Liste
            cards = content.get('dialogs', [])
            if cards:
                items = []
                for c in cards[:5]:  # Max 5 Karten
                    front = c.get('text', '')
                    # HTML-Tags entfernen fuer einfache Darstellung
                    import re
                    front_clean = re.sub(r'<[^>]+>', '', front)[:50]
                    items.append(f'<li>{front_clean}</li>')
                return f'<p><strong>Lernkarten:</strong></p><ul>{"".join(items)}</ul>'

        elif element_type in ['true_false', 'TrueFalse']:
            question = content.get('question', '')
            import re
            q_clean = re.sub(r'<[^>]+>', '', question)
            return f'<p><strong>Wahr/Falsch-Frage:</strong></p><p>{q_clean}</p>'

        elif element_type in ['drag_drop', 'DragQuestion']:
            # Dropzones anzeigen
            dropzones = content.get('question', {}).get('task', {}).get('dropZones', [])
            if dropzones:
                names = [dz.get('label', '') for dz in dropzones[:5]]
                import re
                names_clean = [re.sub(r'<[^>]+>', '', n) for n in names]
                return f'<p><strong>Drag & Drop - Kategorien:</strong></p><p>{", ".join(names_clean)}</p>'

        elif element_type in ['fill_blanks', 'Blanks', 'FillInBlanks']:
            text = content.get('text', '')
            import re
            # Zeige Text mit Platzhaltern
            text_preview = re.sub(r'\*([^*]+)\*', '[___]', text)
            text_clean = re.sub(r'<[^>]+>', '', text_preview)[:200]
            return f'<p><strong>Lückentext:</strong></p><p>{text_clean}...</p>'

        elif element_type in ['timeline', 'Timeline']:
            events = content.get('timeline', {}).get('date', [])
            if events:
                items = []
                for e in events[:4]:
                    # headline ist direkt im Event, nicht unter text
                    headline = e.get('headline', '')
                    items.append(f'<li>{headline}</li>')
                return f'<p><strong>Timeline:</strong></p><ul>{"".join(items)}</ul>'

        elif element_type in ['accordion', 'Accordion']:
            panels = content.get('panels', [])
            if panels:
                items = []
                for p in panels[:5]:
                    title = p.get('title', '')
                    items.append(f'<li>{title}</li>')
                return f'<p><strong>Accordion-Themen:</strong></p><ul>{"".join(items)}</ul>'

        # Fallback
        return f'<p>Interaktives Element vom Typ <strong>{element_type}</strong></p><p>Öffne die separate H5P-Datei für die volle Interaktivität.</p>'

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def combine_to_column(
        self,
        elements: List[AgentResult],
        title: str = "Lerneinheit"
    ) -> CombineResult:
        """Kombiniert zu Column"""
        return self.combine(elements, ContainerType.COLUMN, title)

    def combine_to_quiz(
        self,
        elements: List[AgentResult],
        title: str = "Quiz",
        pass_percentage: int = 60
    ) -> CombineResult:
        """Kombiniert zu QuestionSet"""
        return self.combine(
            elements,
            ContainerType.QUESTION_SET,
            title,
            pass_percentage=pass_percentage
        )

    def combine_to_presentation(
        self,
        elements: List[AgentResult],
        title: str = "Praesentation"
    ) -> CombineResult:
        """Kombiniert zu CoursePresentation"""
        return self.combine(elements, ContainerType.COURSE_PRESENTATION, title)

    def combine_auto(
        self,
        elements: List[AgentResult],
        title: str = "Lerneinheit"
    ) -> CombineResult:
        """Kombiniert mit automatischer Typ-Auswahl"""
        return self.combine(elements, ContainerType.AUTO, title)
