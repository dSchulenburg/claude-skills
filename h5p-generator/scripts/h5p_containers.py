#!/usr/bin/env python3
"""
H5P Container-Generatoren

Container-Typen fuer kombinierte H5P-Inhalte:
- Column: Vertikale Anordnung von Elementen
- QuestionSet: Quiz-Sequenz mit Auswertung
- CoursePresentation: Slide-basierte Praesentation
- InteractiveBook: Kapitel-basiertes Buch (TODO)

Diese Container koennen andere H5P-Elemente enthalten und
werden vom Combiner Agent verwendet.
"""

import json
import zipfile
import os
import shutil
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional, Any

from h5p_generator import H5PGenerator, H5PResult, H5PStyle, THEMES


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
                        "subContentId": elem.get('subContentId', f"col-{i}-{hash(title) % 10000}"),
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
                {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 16},
                {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1}
            ]

            # Zusaetzliche Libraries aus Elementen
            seen_libs = set()
            for elem in elements:
                lib = elem.get('library', '')
                lib_name = lib.split(' ')[0] if ' ' in lib else lib
                if lib_name and lib_name not in seen_libs:
                    seen_libs.add(lib_name)
                    # Parse version
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
                    "subContentId": q.get('subContentId', f"qs-{i}-{hash(title) % 10000}"),
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
            seen_libs = set()
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
# Course Presentation Generator
# =============================================================================

class CoursePresentationGenerator(H5PGenerator):
    """
    Generator fuer H5P.CoursePresentation - Slide-basierte Praesentation.

    Ideal fuer:
    - Tutorials mit Navigation
    - Praesentationen mit Text-Inhalten
    - Strukturierte Lernpfade

    HINWEIS: Verwendet H5P.AdvancedText fuer stabiles Rendering.
    Fuer komplexe eingebettete H5P-Typen wird Column empfohlen.
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
            slides: Liste von Slide-Dicts mit:
                - title: Slide-Titel (wird als Ueberschrift angezeigt)
                - content: HTML-Inhalt oder Text
                - elements: (Optional) Liste von Elementen auf dem Slide
                - keywords: Optional, Slide-Titel/Keywords
            output_name: Dateiname
            show_summary: Zusammenfassung am Ende

        Returns:
            H5PResult

        Beispiel:
            slides = [
                {"title": "Einführung", "content": "<p>Willkommen!</p>"},
                {"title": "Hauptteil", "content": "<p>Der Inhalt...</p>"}
            ]
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
            for i, slide in enumerate(slides):
                elements = []

                # Wenn 'elements' direkt angegeben, verwende diese
                if 'elements' in slide and slide['elements']:
                    for j, elem in enumerate(slide['elements']):
                        # Vereinfachte Text-Elemente
                        if 'text' in elem or 'content' in elem:
                            text_content = elem.get('text') or elem.get('content', '')
                            element = {
                                "x": elem.get('x', 5),
                                "y": elem.get('y', 5),
                                "width": elem.get('width', 90),
                                "height": elem.get('height', 90),
                                "action": {
                                    "library": "H5P.AdvancedText 1.1",
                                    "params": {"text": text_content},
                                    "subContentId": f"cp-{i}-{j}-{hash(title) % 10000}",
                                    "metadata": {"contentType": "Text", "license": "U", "title": "Text"}
                                },
                                "backgroundOpacity": 0,
                                "displayAsButton": False
                            }
                            elements.append(element)
                        else:
                            # Komplexere Elemente mit library
                            element = {
                                "x": elem.get('x', 5),
                                "y": elem.get('y', 5),
                                "width": elem.get('width', 90),
                                "height": elem.get('height', 90),
                                "action": {
                                    "library": elem.get('library', 'H5P.AdvancedText 1.1'),
                                    "params": elem.get('params', {}),
                                    "subContentId": elem.get('subContentId', f"cp-{i}-{j}-{hash(title) % 10000}"),
                                    "metadata": elem.get('metadata', {"contentType": "Text", "license": "U", "title": "Element"})
                                },
                                "backgroundOpacity": elem.get('backgroundOpacity', 0),
                                "displayAsButton": elem.get('displayAsButton', False)
                            }
                            elements.append(element)
                else:
                    # Einfaches Format: title + content als Text
                    slide_title = slide.get('title', f'Folie {i+1}')
                    slide_content = slide.get('content', '')

                    # Kombiniere Titel und Inhalt mit Styling (font-size:24px fuer Lumi-Kompatibilitaet)
                    html_content = f'<div style="font-size:24px;"><h1>{slide_title}</h1>{slide_content}</div>'

                    element = {
                        "x": 5,
                        "y": 5,
                        "width": 90,
                        "height": 90,
                        "action": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {"text": html_content},
                            "subContentId": f"slide{i+1}-text",
                            "metadata": {"contentType": "Text", "license": "U", "title": slide_title}
                        },
                        "backgroundOpacity": 0,
                        "displayAsButton": False
                    }
                    elements.append(element)

                # Slide-Keywords
                slide_title = slide.get('title') or slide.get('keywords', [{}])[0].get('main') or f"Slide {i+1}"
                h5p_slide = {
                    "elements": elements,
                    "slideBackgroundSelector": {},  # Wichtig fuer korrektes Rendering
                    "keywords": slide.get('keywords', [{"main": slide_title}])
                }
                h5p_slides.append(h5p_slide)

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

            # Libraries aus Slides
            seen_libs = set()
            for slide in slides:
                for elem in slide.get('elements', []):
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


# =============================================================================
# Interactive Book Generator
# =============================================================================

class InteractiveBookGenerator(H5PGenerator):
    """
    Generator fuer H5P.InteractiveBook - Kapitel-basiertes Buch.

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
        show_cover: bool = True
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

        Returns:
            H5PResult

        Beispiel:
            chapters = [
                {
                    "title": "Kapitel 1",
                    "elements": [
                        {"library": "H5P.AdvancedText 1.1", "params": {"text": "<p>Intro</p>"}},
                        {"library": "H5P.Dialogcards 1.9", "params": {...}}
                    ]
                }
            ]
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

            # Kapitel formatieren
            h5p_chapters = []
            all_dependencies = set()

            for i, chapter in enumerate(chapters):
                chapter_content = []

                for j, elem in enumerate(chapter.get('elements', [])):
                    lib = elem.get('library', 'H5P.AdvancedText 1.1')
                    lib_name = lib.split(' ')[0]
                    all_dependencies.add(lib)

                    content_item = {
                        "content": {
                            "library": lib,
                            "params": elem.get('params', {}),
                            "subContentId": elem.get('subContentId', f"ch{i+1}-elem{j+1}"),
                            "metadata": elem.get('metadata', {
                                "contentType": lib_name.replace('H5P.', ''),
                                "license": "U",
                                "title": f"Element {j+1}"
                            })
                        },
                        "useSeparator": "auto"
                    }
                    chapter_content.append(content_item)

                h5p_chapters.append({
                    "title": chapter.get('title', f'Kapitel {i+1}'),
                    "params": {
                        "content": chapter_content
                    }
                })

            content = {
                "showCoverPage": show_cover,
                "bookCover": {
                    "coverDescription": f"<p>{cover_description or title}</p>",
                    "coverImage": {},
                    "coverMedium": {}
                },
                "title": f"<p>{title}</p>",
                "chapters": h5p_chapters,
                "behaviour": {
                    "defaultTableOfContents": True,
                    "progressIndicators": True,
                    "displaySummary": True
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
                {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 7},
                {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 16},
                {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5}
            ]

            for lib in all_dependencies:
                if ' ' in lib:
                    lib_name = lib.split(' ')[0]
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
    style: H5PStyle = None
) -> H5PResult:
    """Erstellt ein Interactive Book"""
    gen = InteractiveBookGenerator(style=style)
    return gen.create(title, chapters, output_name, cover_description)


# =============================================================================
# Test
# =============================================================================

if __name__ == "__main__":
    print("H5P Container-Generatoren - Test")
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

    # Test Course Presentation
    print("\n3. CoursePresentation Test...")
    result = create_course_presentation(
        "Test-Praesentation",
        [
            {
                "elements": [
                    {
                        "library": "H5P.AdvancedText 1.1",
                        "params": {"text": "<h1>Folie 1</h1><p>Einfuehrung</p>"},
                        "x": 10, "y": 10, "width": 80, "height": 80
                    }
                ],
                "keywords": [{"main": "Einfuehrung"}]
            },
            {
                "elements": [
                    {
                        "library": "H5P.AdvancedText 1.1",
                        "params": {"text": "<h1>Folie 2</h1><p>Hauptteil</p>"},
                        "x": 10, "y": 10, "width": 80, "height": 80
                    }
                ],
                "keywords": [{"main": "Hauptteil"}]
            }
        ]
    )
    print(f"  {result}")

    print("\n" + "=" * 50)
    print("Tests abgeschlossen!")
