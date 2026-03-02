#!/usr/bin/env python3
"""
H5P Container-Generatoren v3.0

Container-Typen fuer kombinierte H5P-Inhalte:
- Column: Vertikale Anordnung von Elementen
- QuestionSet: Quiz-Sequenz mit Auswertung
- CoursePresentation: Slide-basierte Praesentation (mit eingebetteten H5P-Typen)
- InteractiveBook: Kapitel-basiertes Buch (Kapitel = H5P.Column Wrapper)

v3.0 Aenderungen:
- InteractiveBook: Kapitel nutzen H5P.Column 1.18 Wrapper (korrekte Struktur)
- CoursePresentation: Template-System, UUID-basierte subContentIds, intelligente Positionierung
- Erweiterte Kompatibilitaetslisten fuer eingebettete Typen
- BS:WI Design-Integration (baseColor, styled Headers)
"""

import json
import zipfile
import os
import shutil
import uuid
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Any

from h5p_generator import H5PGenerator, H5PResult, H5PStyle, THEMES


def _uuid() -> str:
    """Erzeugt eine UUID v4 als subContentId"""
    return str(uuid.uuid4())


# =============================================================================
# Column Generator
# =============================================================================

class ColumnGenerator(H5PGenerator):
    """
    Generator fuer H5P.Column - Vertikale Anordnung von Elementen.

    Ideal fuer:
    - 2-5 Elemente untereinander
    - Gemischte Content-Typen
    - Einfache Lerneinheiten
    """

    def create(
        self,
        title: str,
        elements: List[Dict],
        output_name: str = None,
        separator: bool = True
    ) -> H5PResult:
        """
        Erstellt eine Column mit mehreren H5P-Elementen.

        Args:
            title: Titel der Column
            elements: Liste von Element-Dicts mit:
                - library: H5P-Library Name (z.B. "H5P.AdvancedText 1.1")
                - params: Parameter fuer das Element
                - metadata: Optional, Metadaten
            output_name: Dateiname
            separator: Trennlinien zwischen Elementen

        Returns:
            H5PResult
        """
        try:
            if not elements:
                return H5PResult(
                    success=False,
                    error="Keine Elemente angegeben",
                    content_type="Column",
                    title=title
                )

            if not output_name:
                output_name = f"column_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            # Column-Content erstellen
            column_content = []
            for i, elem in enumerate(elements):
                content_item = {
                    "content": {
                        "library": elem.get('library', 'H5P.AdvancedText 1.1'),
                        "params": elem.get('params', {}),
                        "subContentId": elem.get('subContentId', _uuid()),
                        "metadata": elem.get('metadata', {
                            "contentType": "Text",
                            "license": "U",
                            "title": f"Element {i+1}"
                        })
                    },
                    "useSeparator": "auto" if separator else "disabled"
                }
                column_content.append(content_item)

            content = {
                "content": column_content
            }

            # Abhaengigkeiten sammeln
            dependencies = [
                {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 18},
                {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1}
            ]

            # Zusaetzliche Libraries aus Elementen
            seen_libs = {"H5P.Column", "H5P.AdvancedText"}
            for elem in elements:
                lib = elem.get('library', '')
                lib_name = lib.split(' ')[0] if ' ' in lib else lib
                if lib_name and lib_name not in seen_libs:
                    seen_libs.add(lib_name)
                    if ' ' in lib:
                        parts = lib.split(' ')[1].split('.')
                        if len(parts) >= 2:
                            dependencies.append({
                                "machineName": lib_name,
                                "majorVersion": int(parts[0]),
                                "minorVersion": int(parts[1])
                            })

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.Column", dependencies
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(
                success=True,
                path=output_path,
                content_type="Column",
                title=title
            )

        except Exception as e:
            return H5PResult(
                success=False,
                error=f"Column-Fehler: {e}",
                content_type="Column",
                title=title
            )


# =============================================================================
# Question Set Generator
# =============================================================================

class QuestionSetGenerator(H5PGenerator):
    """
    Generator fuer H5P.QuestionSet - Quiz-Sequenz mit Auswertung.

    Ideal fuer:
    - Tests und Pruefungen
    - Kombinierte Quiz-Typen
    - Fortschrittsverfolgung
    """

    def create(
        self,
        title: str,
        questions: List[Dict],
        output_name: str = None,
        pass_percentage: int = 60,
        randomize: bool = False,
        show_intro: bool = True,
        intro_text: str = None
    ) -> H5PResult:
        """
        Erstellt ein QuestionSet mit mehreren Fragen.

        Args:
            title: Titel des Quiz
            questions: Liste von Frage-Dicts mit:
                - library: H5P-Library (z.B. "H5P.MultiChoice 1.16")
                - params: Frage-Parameter
            output_name: Dateiname
            pass_percentage: Bestehensgrenze in %
            randomize: Fragen zufaellig mischen
            show_intro: Intro-Seite anzeigen
            intro_text: Text fuer Intro-Seite

        Returns:
            H5PResult
        """
        try:
            if not questions:
                return H5PResult(
                    success=False,
                    error="Keine Fragen angegeben",
                    content_type="QuestionSet",
                    title=title
                )

            if not output_name:
                output_name = f"questionset_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            # Fragen formatieren
            h5p_questions = []
            for i, q in enumerate(questions):
                question = {
                    "library": q.get('library', 'H5P.MultiChoice 1.16'),
                    "params": q.get('params', {}),
                    "subContentId": q.get('subContentId', _uuid()),
                    "metadata": q.get('metadata', {
                        "contentType": "Multiple Choice",
                        "license": "U",
                        "title": f"Frage {i+1}"
                    })
                }
                h5p_questions.append(question)

            content = {
                "introPage": {
                    "showIntroPage": show_intro,
                    "title": title,
                    "introduction": intro_text or f"<p>Beantworte die folgenden {len(questions)} Fragen.</p>"
                },
                "progressType": "dots",
                "passPercentage": pass_percentage,
                "questions": h5p_questions,
                "texts": {
                    "prevButton": "Zurueck",
                    "nextButton": "Weiter",
                    "finishButton": "Fertig",
                    "submitButton": "Absenden",
                    "textualProgress": "Frage @current von @total",
                    "jumpToQuestion": "Frage %d",
                    "questionLabel": "Frage",
                    "readSpeakerProgress": "Frage @current von @total",
                    "unansweredText": "Nicht beantwortet",
                    "answeredText": "Beantwortet",
                    "currentQuestionText": "Aktuelle Frage",
                    "navigationLabel": "Fragen"
                },
                "endGame": {
                    "showResultPage": True,
                    "showSolutionButton": True,
                    "showRetryButton": True,
                    "noResultMessage": "Quiz beendet",
                    "message": "Du hast @score von @total Punkten erreicht.",
                    "successGreeting": "Gratulation!",
                    "successComment": self.style.feedback_correct,
                    "failGreeting": "Schade!",
                    "failComment": self.style.feedback_wrong,
                    "solutionButtonText": "Loesung anzeigen",
                    "retryButtonText": "Nochmal versuchen",
                    "finishButtonText": "Fertig"
                },
                "override": {
                    "showSolutionButton": "on",
                    "retryButton": "on"
                },
                "behaviour": {
                    "enableBackwardsNavigation": True,
                    "randomQuestions": randomize,
                    "disableBackwardsNavigation": False
                }
            }

            # Abhaengigkeiten
            dependencies = [
                {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20}
            ]

            # Libraries aus Fragen
            seen_libs = {"H5P.QuestionSet"}
            for q in questions:
                lib = q.get('library', '')
                lib_name = lib.split(' ')[0] if ' ' in lib else lib
                if lib_name and lib_name not in seen_libs:
                    seen_libs.add(lib_name)
                    if ' ' in lib:
                        parts = lib.split(' ')[1].split('.')
                        if len(parts) >= 2:
                            dependencies.append({
                                "machineName": lib_name,
                                "majorVersion": int(parts[0]),
                                "minorVersion": int(parts[1])
                            })

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.QuestionSet", dependencies
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(
                success=True,
                path=output_path,
                content_type="QuestionSet",
                title=title
            )

        except Exception as e:
            return H5PResult(
                success=False,
                error=f"QuestionSet-Fehler: {e}",
                content_type="QuestionSet",
                title=title
            )


# =============================================================================
# Course Presentation Generator (v3.0 - Template System)
# =============================================================================

# Slide-Layout Templates
SLIDE_LAYOUTS = {
    "title_only": {
        "description": "Nur Ueberschrift (Intro/Outro)",
        "elements": [
            {"role": "title", "x": 5, "y": 30, "width": 90, "height": 40}
        ]
    },
    "text_content": {
        "description": "Titel + Text-Inhalt",
        "elements": [
            {"role": "title", "x": 5, "y": 2, "width": 90, "height": 15},
            {"role": "content", "x": 5, "y": 20, "width": 90, "height": 70}
        ]
    },
    "interactive": {
        "description": "Titel + Text + eingebettetes H5P-Element",
        "elements": [
            {"role": "title", "x": 5, "y": 2, "width": 90, "height": 12},
            {"role": "content", "x": 5, "y": 16, "width": 90, "height": 30},
            {"role": "interactive", "x": 5, "y": 48, "width": 90, "height": 48}
        ]
    },
    "interactive_full": {
        "description": "Titel + vollflaechiges H5P-Element",
        "elements": [
            {"role": "title", "x": 5, "y": 2, "width": 90, "height": 12},
            {"role": "interactive", "x": 5, "y": 16, "width": 90, "height": 78}
        ]
    },
    "split": {
        "description": "Links Text, rechts Interaktion",
        "elements": [
            {"role": "title", "x": 5, "y": 2, "width": 90, "height": 12},
            {"role": "content", "x": 5, "y": 16, "width": 43, "height": 78},
            {"role": "interactive", "x": 52, "y": 16, "width": 43, "height": 78}
        ]
    }
}

# Typen die in CoursePresentation eingebettet werden koennen
COURSE_PRESENTATION_EMBEDDABLE = {
    'H5P.AdvancedText', 'H5P.MultiChoice', 'H5P.TrueFalse',
    'H5P.DragQuestion', 'H5P.DragText', 'H5P.Blanks',
    'H5P.SingleChoiceSet', 'H5P.Summary', 'H5P.MarkTheWords',
    'H5P.Image', 'H5P.Audio', 'H5P.Video', 'H5P.Table',
    'H5P.Link', 'H5P.Shape', 'H5P.GoToSlide',
    'H5P.ContinuousText', 'H5P.Chart', 'H5P.TwitterUserFeed',
    'H5P.ExportableTextArea', 'H5P.IVHotspot', 'H5P.Nil',
    'H5P.Essay', 'H5P.SortParagraphs',
}


class CoursePresentationGenerator(H5PGenerator):
    """
    Generator fuer H5P.CoursePresentation - Slide-basierte Praesentation.

    v3.0: Template-System, eingebettete H5P-Typen, UUID subContentIds.

    Slide-Layouts:
    - title_only: Nur Ueberschrift (Intro/Outro)
    - text_content: Titel + Text
    - interactive: Titel + Text + H5P-Element
    - interactive_full: Titel + vollflaechiges H5P-Element
    - split: Links Text, rechts Interaktion
    """

    def create(
        self,
        title: str,
        slides: List[Dict],
        output_name: str = None,
        show_summary: bool = True
    ) -> H5PResult:
        """
        Erstellt eine Course Presentation mit Slides.

        Args:
            title: Titel der Praesentation
            slides: Liste von Slide-Dicts. Unterstuetzte Formate:

                Format 1 - Einfach (title + content):
                {"title": "Folie 1", "content": "<p>Text</p>"}

                Format 2 - Mit Layout-Template:
                {
                    "layout": "interactive",
                    "title": "Quiz-Folie",
                    "content": "<p>Beantworte die Frage:</p>",
                    "interactive": {
                        "library": "H5P.MultiChoice 1.16",
                        "params": {...}
                    }
                }

                Format 3 - Vollstaendig (elements direkt):
                {
                    "elements": [{
                        "library": "H5P.AdvancedText 1.1",
                        "params": {"text": "..."},
                        "x": 5, "y": 5, "width": 90, "height": 90
                    }],
                    "keywords": [{"main": "Folie 1"}]
                }

            output_name: Dateiname
            show_summary: Zusammenfassung am Ende

        Returns:
            H5PResult
        """
        try:
            if not slides:
                return H5PResult(
                    success=False,
                    error="Keine Slides angegeben",
                    content_type="CoursePresentation",
                    title=title
                )

            if not output_name:
                output_name = f"presentation_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            # Slides formatieren
            h5p_slides = []
            all_libraries = set()

            for i, slide in enumerate(slides):
                h5p_slide, libs = self._build_slide(slide, i)
                h5p_slides.append(h5p_slide)
                all_libraries.update(libs)

            content = {
                "presentation": {
                    "slides": h5p_slides,
                    "keywordListEnabled": True,
                    "globalBackgroundSelector": {},
                    "keywordListAlwaysShow": False,
                    "keywordListAutoHide": False,
                    "keywordListOpacity": 90
                },
                "l10n": {
                    "slide": "Folie",
                    "yourScore": "Punkte",
                    "maxScore": "Max",
                    "total": "Gesamt",
                    "showSolutions": "Loesungen",
                    "retry": "Nochmal",
                    "exportAnswers": "Export",
                    "hideKeywords": "Keywords verbergen",
                    "showKeywords": "Keywords zeigen",
                    "fullscreen": "Vollbild",
                    "exitFullscreen": "Beenden",
                    "prevSlide": "Zurueck",
                    "nextSlide": "Weiter",
                    "currentSlide": "Aktuell",
                    "lastSlide": "Letzte",
                    "solutionModeTitle": "Loesung",
                    "solutionModeText": "Loesungsmodus",
                    "summaryMultipleTaskText": "Aufgaben",
                    "scoreMessage": ":achieved/:max Punkte",
                    "printTitle": "Drucken",
                    "summary": "Zusammenfassung",
                    "solutionsButtonTitle": "Zeigen"
                },
                "override": {
                    "activeSurface": False,
                    "hideSummarySlide": not show_summary,
                    "summarySlideSolutionButton": False,
                    "summarySlideRetryButton": False
                }
            }

            # Abhaengigkeiten
            dependencies = [
                {"machineName": "H5P.CoursePresentation", "majorVersion": 1, "minorVersion": 25},
                {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
                {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5}
            ]

            # Libraries aus Slides hinzufuegen
            seen_libs = {"H5P.CoursePresentation", "H5P.AdvancedText", "FontAwesome"}
            for lib in all_libraries:
                lib_name = lib.split(' ')[0] if ' ' in lib else lib
                if lib_name not in seen_libs:
                    seen_libs.add(lib_name)
                    if ' ' in lib:
                        parts = lib.split(' ')[1].split('.')
                        if len(parts) >= 2:
                            dependencies.append({
                                "machineName": lib_name,
                                "majorVersion": int(parts[0]),
                                "minorVersion": int(parts[1])
                            })

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.CoursePresentation", dependencies
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(
                success=True,
                path=output_path,
                content_type="CoursePresentation",
                title=title
            )

        except Exception as e:
            return H5PResult(
                success=False,
                error=f"CoursePresentation-Fehler: {e}",
                content_type="CoursePresentation",
                title=title
            )

    def _build_slide(self, slide: Dict, index: int) -> tuple:
        """
        Baut einen einzelnen Slide. Unterstuetzt 3 Formate.

        Returns:
            (slide_dict, set_of_libraries_used)
        """
        libraries_used = set()

        # Format 3: elements direkt angegeben
        if 'elements' in slide and slide['elements']:
            elements = []
            for j, elem in enumerate(slide['elements']):
                element, lib = self._build_element(elem, index, j)
                elements.append(element)
                if lib:
                    libraries_used.add(lib)

            slide_title = slide.get('title') or slide.get('keywords', [{}])[0].get('main') or f"Slide {index+1}"
            return {
                "elements": elements,
                "slideBackgroundSelector": {},
                "keywords": slide.get('keywords', [{"main": slide_title}])
            }, libraries_used

        # Format 2: Layout-Template
        layout_name = slide.get('layout', None)
        if layout_name and layout_name in SLIDE_LAYOUTS:
            return self._build_slide_from_template(slide, layout_name, index, libraries_used)

        # Format 1 oder Auto-Detection: title + content (+ optional interactive)
        has_interactive = 'interactive' in slide and slide['interactive']
        if has_interactive:
            layout_name = 'interactive'
        else:
            layout_name = 'text_content'

        return self._build_slide_from_template(slide, layout_name, index, libraries_used)

    def _build_slide_from_template(self, slide: Dict, layout_name: str, index: int, libraries_used: set) -> tuple:
        """Baut Slide aus Template-Layout."""
        layout = SLIDE_LAYOUTS.get(layout_name, SLIDE_LAYOUTS['text_content'])
        elements = []
        slide_title = slide.get('title', f'Folie {index+1}')

        for j, slot in enumerate(layout['elements']):
            role = slot['role']
            x, y, w, h = slot['x'], slot['y'], slot['width'], slot['height']

            if role == 'title':
                element = self._make_text_element(
                    f'<h2 style="font-size:1.5em;color:#003366;">{slide_title}</h2>',
                    x, y, w, h, index, j
                )
                elements.append(element)

            elif role == 'content':
                content_html = slide.get('content', '')
                if content_html:
                    element = self._make_text_element(content_html, x, y, w, h, index, j)
                    elements.append(element)

            elif role == 'interactive':
                interactive = slide.get('interactive', None)
                if interactive and isinstance(interactive, dict):
                    lib = interactive.get('library', 'H5P.AdvancedText 1.1')
                    lib_name = lib.split(' ')[0] if ' ' in lib else lib

                    # Nur einbettbare Typen verwenden
                    if lib_name in COURSE_PRESENTATION_EMBEDDABLE:
                        libraries_used.add(lib)
                        display_as_button = interactive.get('displayAsButton', False)
                        element = {
                            "x": x,
                            "y": y,
                            "width": w,
                            "height": h,
                            "action": {
                                "library": lib,
                                "params": interactive.get('params', {}),
                                "subContentId": _uuid(),
                                "metadata": interactive.get('metadata', {
                                    "contentType": lib_name.replace('H5P.', ''),
                                    "license": "U",
                                    "title": slide_title
                                })
                            },
                            "backgroundOpacity": 0,
                            "displayAsButton": display_as_button
                        }
                        if display_as_button:
                            element["buttonSize"] = "big"
                            element["goToSlideType"] = "specified"
                        elements.append(element)
                    else:
                        # Fallback: als Text darstellen
                        element = self._make_text_element(
                            f'<p><em>Element: {lib_name}</em></p>',
                            x, y, w, h, index, j
                        )
                        elements.append(element)

        return {
            "elements": elements,
            "slideBackgroundSelector": {},
            "keywords": slide.get('keywords', [{"main": slide_title}])
        }, libraries_used

    def _build_element(self, elem: Dict, slide_idx: int, elem_idx: int) -> tuple:
        """Baut ein einzelnes Slide-Element. Returns (element_dict, library_string_or_None)."""
        # Text-Shorthand
        if 'text' in elem or ('content' in elem and not 'library' in elem):
            text_content = elem.get('text') or elem.get('content', '')
            return self._make_text_element(
                text_content,
                elem.get('x', 5), elem.get('y', 5),
                elem.get('width', 90), elem.get('height', 90),
                slide_idx, elem_idx
            ), None

        # Volle Element-Definition
        lib = elem.get('library', 'H5P.AdvancedText 1.1')
        element = {
            "x": elem.get('x', 5),
            "y": elem.get('y', 5),
            "width": elem.get('width', 90),
            "height": elem.get('height', 90),
            "action": {
                "library": lib,
                "params": elem.get('params', {}),
                "subContentId": elem.get('subContentId', _uuid()),
                "metadata": elem.get('metadata', {
                    "contentType": "Text",
                    "license": "U",
                    "title": "Element"
                })
            },
            "backgroundOpacity": elem.get('backgroundOpacity', 0),
            "displayAsButton": elem.get('displayAsButton', False)
        }
        return element, lib

    def _make_text_element(self, html: str, x: int, y: int, w: int, h: int,
                           slide_idx: int, elem_idx: int) -> Dict:
        """Erstellt ein AdvancedText-Element fuer Slides."""
        return {
            "x": x,
            "y": y,
            "width": w,
            "height": h,
            "action": {
                "library": "H5P.AdvancedText 1.1",
                "params": {"text": html},
                "subContentId": _uuid(),
                "metadata": {"contentType": "Text", "license": "U", "title": "Text"}
            },
            "backgroundOpacity": 0,
            "displayAsButton": False
        }


# =============================================================================
# Interactive Book Generator (v3.0 - H5P.Column Wrapper)
# =============================================================================

# Alle Typen die in H5P.Column (und damit InteractiveBook) eingebettet werden koennen
INTERACTIVE_BOOK_COMPATIBLE = {
    'H5P.AdvancedText', 'H5P.Accordion', 'H5P.Agamotto',
    'H5P.Audio', 'H5P.AudioRecorder', 'H5P.Blanks',
    'H5P.Chart', 'H5P.Collage', 'H5P.CoursePresentation',
    'H5P.Dialogcards', 'H5P.DocumentationTool', 'H5P.DragQuestion',
    'H5P.DragText', 'H5P.Essay', 'H5P.GoToSlide',
    'H5P.GuessTheAnswer', 'H5P.IFrameEmbed', 'H5P.Image',
    'H5P.ImageHotspotQuestion', 'H5P.ImageHotspots',
    'H5P.ImageSequencing', 'H5P.InteractiveVideo',
    'H5P.KewArCode', 'H5P.MarkTheWords', 'H5P.MemoryGame',
    'H5P.MultiChoice', 'H5P.Questionnaire', 'H5P.QuestionSet',
    'H5P.SingleChoiceSet', 'H5P.Summary', 'H5P.Table',
    'H5P.Timeline', 'H5P.TrueFalse', 'H5P.TwitterUserFeed',
    'H5P.Video', 'H5P.SortParagraphs', 'H5P.BranchingScenario',
}


class InteractiveBookGenerator(H5PGenerator):
    """
    Generator fuer H5P.InteractiveBook - Kapitel-basiertes Buch.

    v3.0: Jedes Kapitel wird korrekt als H5P.Column 1.18 Wrapper erstellt.
    Erweiterte Kompatibilitaet fuer 35+ eingebettete Typen.

    Ideal fuer:
    - Strukturierte Lerneinheiten mit mehreren Kapiteln
    - Kombination verschiedener interaktiver Elemente
    - Fortschrittsverfolgung und Zusammenfassung
    """

    def create(
        self,
        title: str,
        chapters: List[Dict],
        output_name: str = None,
        cover_description: str = None,
        show_cover: bool = True,
        base_color: str = "#003366"
    ) -> H5PResult:
        """
        Erstellt ein Interactive Book mit Kapiteln.

        Args:
            title: Titel des Buchs
            chapters: Liste von Kapitel-Dicts mit:
                - title: Kapitel-Titel
                - elements: Liste von H5P-Elementen (wie bei Column)
            output_name: Dateiname
            cover_description: Beschreibung auf der Titelseite
            show_cover: Titelseite anzeigen
            base_color: Navigationsfarbe (default: BS:WI Navy)

        Returns:
            H5PResult
        """
        try:
            if not chapters:
                return H5PResult(
                    success=False,
                    error="Keine Kapitel angegeben",
                    content_type="InteractiveBook",
                    title=title
                )

            if not output_name:
                output_name = f"book_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            # Kapitel formatieren - jedes Kapitel ist ein H5P.Column 1.18
            h5p_chapters = []
            all_dependencies = set()

            for i, chapter in enumerate(chapters):
                column_content = []

                for j, elem in enumerate(chapter.get('elements', [])):
                    lib = elem.get('library', 'H5P.AdvancedText 1.1')
                    lib_name = lib.split(' ')[0]
                    all_dependencies.add(lib)

                    content_item = {
                        "content": {
                            "library": lib,
                            "params": elem.get('params', {}),
                            "subContentId": elem.get('subContentId', _uuid()),
                            "metadata": elem.get('metadata', {
                                "contentType": lib_name.replace('H5P.', ''),
                                "license": "U",
                                "title": f"Element {j+1}"
                            })
                        },
                        "useSeparator": "auto"
                    }
                    column_content.append(content_item)

                # Kapitel = H5P.Column 1.18 (flache Struktur, kein "chapter"-Wrapper)
                # H5P.InteractiveBook semantics hat eine Gruppe mit nur 1 Feld,
                # diese wird vom H5P-Validator "flattened" - das Library-Objekt
                # muss direkt im chapters-Array liegen.
                h5p_chapters.append({
                    "library": "H5P.Column 1.18",
                    "params": {
                        "content": column_content
                    },
                    "subContentId": _uuid(),
                    "metadata": {
                        "contentType": "Column",
                        "license": "U",
                        "title": chapter.get('title', f'Kapitel {i+1}')
                    }
                })

            content = {
                "showCoverPage": show_cover,
                "bookCover": {
                    "coverDescription": f"<p>{cover_description or title}</p>"
                },
                "chapters": h5p_chapters,
                "behaviour": {
                    "defaultTableOfContents": True,
                    "progressIndicators": True,
                    "progressAuto": True,
                    "displaySummary": True,
                    "baseColor": base_color
                },
                "l10n": {
                    "nextPage": "Weiter",
                    "previousPage": "Zurueck",
                    "navigateToTop": "Nach oben",
                    "fullscreen": "Vollbild",
                    "exitFullscreen": "Vollbild beenden",
                    "bookProgressSubtext": "@count von @total Seiten",
                    "interactionsProgressSubtext": "@count von @total Interaktionen",
                    "submitReport": "Absenden",
                    "restartLabel": "Neustart",
                    "summaryHeader": "Zusammenfassung",
                    "allInteractions": "Alle Interaktionen",
                    "unansweredInteractions": "Unbeantwortet",
                    "scoreText": "Punkte:",
                    "leftOfScore": "von",
                    "noInteractions": "Keine Interaktionen",
                    "score": "Punkte",
                    "maxScore": "Max Punkte",
                    "bookProgress": "Buchfortschritt",
                    "interactionsProgress": "Interaktionen",
                    "totalScoreLabel": "Gesamtpunkte"
                }
            }

            # Dependencies sammeln
            dependencies = [
                {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 11},
                {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 18},
                {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5}
            ]

            seen_libs = {"H5P.InteractiveBook", "H5P.Column", "FontAwesome"}
            for lib in all_dependencies:
                if ' ' in lib:
                    lib_name = lib.split(' ')[0]
                    if lib_name not in seen_libs:
                        seen_libs.add(lib_name)
                        version_parts = lib.split(' ')[1].split('.')
                        if len(version_parts) >= 2:
                            dependencies.append({
                                "machineName": lib_name,
                                "majorVersion": int(version_parts[0]),
                                "minorVersion": int(version_parts[1])
                            })

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.InteractiveBook", dependencies
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(
                success=True,
                path=output_path,
                content_type="InteractiveBook",
                title=title
            )

        except Exception as e:
            return H5PResult(
                success=False,
                error=f"InteractiveBook-Fehler: {e}",
                content_type="InteractiveBook",
                title=title
            )


# =============================================================================
# Convenience Functions
# =============================================================================

def create_column(
    title: str,
    elements: List[Dict],
    output_name: str = None,
    style: H5PStyle = None
) -> H5PResult:
    """Erstellt eine Column"""
    gen = ColumnGenerator(style=style)
    return gen.create(title, elements, output_name)


def create_question_set(
    title: str,
    questions: List[Dict],
    output_name: str = None,
    pass_percentage: int = 60,
    style: H5PStyle = None
) -> H5PResult:
    """Erstellt ein QuestionSet"""
    gen = QuestionSetGenerator(style=style)
    return gen.create(title, questions, output_name, pass_percentage)


def create_course_presentation(
    title: str,
    slides: List[Dict],
    output_name: str = None,
    style: H5PStyle = None
) -> H5PResult:
    """Erstellt eine Course Presentation"""
    gen = CoursePresentationGenerator(style=style)
    return gen.create(title, slides, output_name)


def create_interactive_book(
    title: str,
    chapters: List[Dict],
    output_name: str = None,
    cover_description: str = None,
    style: H5PStyle = None,
    base_color: str = "#003366"
) -> H5PResult:
    """Erstellt ein Interactive Book"""
    gen = InteractiveBookGenerator(style=style)
    return gen.create(title, chapters, output_name, cover_description, base_color=base_color)


# =============================================================================
# Test
# =============================================================================

if __name__ == "__main__":
    print("H5P Container-Generatoren v3.0 - Test")
    print("=" * 50)

    # Test Column
    print("\n1. Column Test...")
    result = create_column(
        "Test-Column",
        [
            {
                "library": "H5P.AdvancedText 1.1",
                "params": {"text": "<h2>Willkommen</h2><p>Dies ist ein Test.</p>"}
            },
            {
                "library": "H5P.AdvancedText 1.1",
                "params": {"text": "<p>Zweiter Abschnitt mit mehr Text.</p>"}
            }
        ]
    )
    print(f"  {result}")

    # Test QuestionSet
    print("\n2. QuestionSet Test...")
    result = create_question_set(
        "Test-Quiz",
        [
            {
                "library": "H5P.TrueFalse 1.8",
                "params": {
                    "question": "<p>Python ist eine Programmiersprache.</p>",
                    "correct": "true",
                    "l10n": {"trueText": "Wahr", "falseText": "Falsch"}
                }
            },
            {
                "library": "H5P.TrueFalse 1.8",
                "params": {
                    "question": "<p>HTML ist eine Programmiersprache.</p>",
                    "correct": "false",
                    "l10n": {"trueText": "Wahr", "falseText": "Falsch"}
                }
            }
        ],
        pass_percentage=50
    )
    print(f"  {result}")

    # Test Course Presentation with template
    print("\n3. CoursePresentation Test (Template)...")
    result = create_course_presentation(
        "Test-Praesentation",
        [
            {
                "layout": "title_only",
                "title": "Einfuehrung in Scrum"
            },
            {
                "layout": "text_content",
                "title": "Was ist Scrum?",
                "content": "<p>Scrum ist ein agiles Framework...</p>"
            },
            {
                "layout": "interactive",
                "title": "Quiz-Folie",
                "content": "<p>Beantworte die Frage:</p>",
                "interactive": {
                    "library": "H5P.TrueFalse 1.8",
                    "params": {
                        "question": "<p>Scrum hat 3 Rollen.</p>",
                        "correct": "true",
                        "l10n": {"trueText": "Wahr", "falseText": "Falsch"}
                    }
                }
            }
        ]
    )
    print(f"  {result}")

    # Test Interactive Book (v3.0 Column Wrapper)
    print("\n4. InteractiveBook Test (Column Wrapper)...")
    result = create_interactive_book(
        "Scrum-Buch",
        [
            {
                "title": "Kapitel 1: Rollen",
                "elements": [
                    {
                        "library": "H5P.AdvancedText 1.1",
                        "params": {"text": "<h2>Die Scrum-Rollen</h2><p>Es gibt drei Rollen...</p>"}
                    },
                    {
                        "library": "H5P.Dialogcards 1.9",
                        "params": {
                            "dialogs": [
                                {"text": "<p>Product Owner</p>", "answer": "<p>Priorisiert das Backlog</p>"},
                                {"text": "<p>Scrum Master</p>", "answer": "<p>Entfernt Hindernisse</p>"}
                            ]
                        }
                    }
                ]
            },
            {
                "title": "Kapitel 2: Quiz",
                "elements": [
                    {
                        "library": "H5P.AdvancedText 1.1",
                        "params": {"text": "<h2>Teste dein Wissen</h2>"}
                    },
                    {
                        "library": "H5P.MultiChoice 1.16",
                        "params": {
                            "question": "<p>Welche Rolle priorisiert das Backlog?</p>",
                            "answers": [
                                {"text": "<p>Product Owner</p>", "correct": True},
                                {"text": "<p>Scrum Master</p>", "correct": False},
                                {"text": "<p>Developer</p>", "correct": False}
                            ]
                        }
                    }
                ]
            }
        ],
        cover_description="Ein interaktives Buch ueber Scrum"
    )
    print(f"  {result}")

    print("\n" + "=" * 50)
    print("Tests abgeschlossen!")
