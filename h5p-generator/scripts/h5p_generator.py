#!/usr/bin/env python3
"""
H5P Generator v2.0 - Erstellt .h5p-Dateien direkt aus Python

Verbesserungen:
- Robuste Fehlerbehandlung
- Input-Validierung
- Styling-Optionen
- Neue Content-Types

Unterstützte Content-Types:
- TrueFalse          - Wahr/Falsch Quizze
- MultiChoice        - Multiple Choice Fragen
- Blanks             - Lückentext
- DragQuestion       - Drag and Drop
- SingleChoiceSet    - Schnelle Single Choice
- DialogCards        - Lernkarten/Flashcards
- MarkTheWords       - Wörter im Text markieren
- Summary            - Zusammenfassungen
- Accordion          - Aufklappbare Abschnitte
"""

import json
import zipfile
import os
from pathlib import Path
from datetime import datetime
import shutil
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union
import re


# =============================================================================
# Result & Error Handling
# =============================================================================

@dataclass
class H5PResult:
    """Strukturiertes Ergebnis einer H5P-Generierung"""
    success: bool
    path: Optional[Path] = None
    error: Optional[str] = None
    content_type: str = ""
    title: str = ""

    def __str__(self):
        if self.success:
            return f"[OK] {self.content_type}: {self.path}"
        return f"[FAIL] {self.content_type}: {self.error}"


class H5PValidationError(Exception):
    """Fehler bei der Validierung von H5P-Eingabedaten"""
    pass


class H5PGenerationError(Exception):
    """Fehler bei der H5P-Generierung"""
    pass


# =============================================================================
# Styling & Design Options
# =============================================================================

@dataclass
class H5PStyle:
    """Styling-Optionen für H5P-Inhalte"""
    # Farben
    primary_color: str = "#1a73e8"      # Hauptfarbe (Buttons, Akzente)
    success_color: str = "#34a853"       # Richtige Antworten
    error_color: str = "#ea4335"         # Falsche Antworten
    background_color: str = "#ffffff"    # Hintergrund
    text_color: str = "#202124"          # Textfarbe

    # Schrift
    font_family: str = "Arial, sans-serif"
    font_size: str = "16px"

    # Layout
    border_radius: str = "8px"
    padding: str = "16px"

    # Feedback-Texte
    feedback_correct: str = "Richtig! Gut gemacht!"
    feedback_wrong: str = "Leider falsch. Versuche es nochmal!"
    feedback_partial: str = "Teilweise richtig."

    # Pass-Threshold
    pass_percentage: int = 60


# Vordefinierte Themes
THEMES = {
    "default": H5PStyle(),
    "dark": H5PStyle(
        primary_color="#8ab4f8",
        background_color="#202124",
        text_color="#e8eaed"
    ),
    "education": H5PStyle(
        primary_color="#4caf50",
        success_color="#4caf50",
        error_color="#f44336",
        feedback_correct="Super! Das ist korrekt!",
        feedback_wrong="Das war leider nicht richtig. Schau dir die Lösung an."
    ),
    "professional": H5PStyle(
        primary_color="#1976d2",
        border_radius="4px",
        font_family="'Segoe UI', Roboto, sans-serif"
    )
}


# =============================================================================
# Base Generator Class
# =============================================================================

class H5PGenerator:
    """Basisklasse für H5P-Generierung mit Fehlerbehandlung"""

    def __init__(self, output_dir: str = "/home/claude/h5p-output", style: H5PStyle = None):
        self.output_dir = Path(output_dir)
        self.style = style or H5PStyle()
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Erstellt das Output-Verzeichnis falls nötig"""
        try:
            self.output_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError as e:
            raise H5PGenerationError(f"Keine Schreibrechte für {self.output_dir}: {e}")
        except Exception as e:
            raise H5PGenerationError(f"Fehler beim Erstellen von {self.output_dir}: {e}")

    def _validate_not_empty(self, value, field_name: str):
        """Prüft ob ein Wert nicht leer ist"""
        if not value:
            raise H5PValidationError(f"{field_name} darf nicht leer sein")
        return value

    def _validate_list(self, items: list, field_name: str, min_items: int = 1):
        """Prüft ob eine Liste die Mindestanzahl an Elementen hat"""
        if not isinstance(items, list):
            raise H5PValidationError(f"{field_name} muss eine Liste sein")
        if len(items) < min_items:
            raise H5PValidationError(f"{field_name} muss mindestens {min_items} Element(e) enthalten")
        return items

    def _sanitize_filename(self, name: str) -> str:
        """Bereinigt einen Dateinamen"""
        # Entferne ungültige Zeichen
        sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
        # Ersetze Leerzeichen durch Unterstriche
        sanitized = re.sub(r'\s+', '_', sanitized)
        # Kürze auf max 50 Zeichen
        return sanitized[:50].strip('_')

    def _create_temp_dir(self, output_name: str) -> Path:
        """Erstellt ein temporäres Verzeichnis"""
        temp_dir = Path("/tmp") / f"h5p_{output_name}_{datetime.now().strftime('%H%M%S')}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        (temp_dir / "content").mkdir(exist_ok=True)
        return temp_dir

    def _write_json(self, path: Path, data: dict):
        """Schreibt JSON-Datei mit Fehlerbehandlung"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise H5PGenerationError(f"Fehler beim Schreiben von {path}: {e}")

    def _package_h5p(self, temp_dir: Path, output_name: str) -> Path:
        """Packt die H5P-Dateien in ein ZIP-Archiv"""
        output_path = self.output_dir / f"{output_name}.h5p"

        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(temp_dir)
                        zf.write(file_path, arcname)
        except Exception as e:
            raise H5PGenerationError(f"Fehler beim Erstellen der H5P-Datei: {e}")

        return output_path

    def _cleanup(self, temp_dir: Path):
        """Räumt temporäre Dateien auf"""
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass  # Cleanup-Fehler ignorieren

    def _create_h5p_meta(self, title: str, main_library: str, dependencies: List[Dict]) -> dict:
        """Erstellt die h5p.json Metadaten"""
        return {
            "title": title,
            "language": "de",
            "mainLibrary": main_library,
            "embedTypes": ["iframe"],
            "license": "CC BY",
            "preloadedDependencies": dependencies
        }

    def _get_question_set_texts(self) -> dict:
        """Standard-Texte für QuestionSet"""
        return {
            "prevButton": "Zurück",
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
        }

    def _get_end_game_config(self) -> dict:
        """Standard End-Screen Konfiguration"""
        return {
            "showResultPage": True,
            "showSolutionButton": True,
            "showRetryButton": True,
            "noResultMessage": "Quiz beendet",
            "message": "Du hast @score von @total Punkten erreicht.",
            "successGreeting": "Gratulation!",
            "successComment": self.style.feedback_correct,
            "failGreeting": "Schade!",
            "failComment": self.style.feedback_wrong,
            "solutionButtonText": "Lösung anzeigen",
            "retryButtonText": "Nochmal versuchen",
            "finishButtonText": "Fertig"
        }


# =============================================================================
# True/False Generator
# =============================================================================

class TrueFalseGenerator(H5PGenerator):
    """Generator für True/False Fragen"""

    def create(self, title: str, questions: List[Dict], output_name: str = None) -> H5PResult:
        """
        Erstellt eine True/False H5P-Datei

        Args:
            title: Titel des Quiz
            questions: Liste von Dicts mit:
                - text: Die Aussage
                - correct: True/False
                - feedback_correct: Optional, Feedback bei richtiger Antwort
                - feedback_wrong: Optional, Feedback bei falscher Antwort
            output_name: Dateiname (ohne .h5p)

        Returns:
            H5PResult mit Erfolg/Fehler-Info
        """
        try:
            # Validierung
            self._validate_not_empty(title, "Titel")
            self._validate_list(questions, "Fragen", min_items=1)

            for i, q in enumerate(questions):
                if 'text' not in q:
                    raise H5PValidationError(f"Frage {i+1}: 'text' fehlt")
                if 'correct' not in q:
                    raise H5PValidationError(f"Frage {i+1}: 'correct' fehlt")

            # Output-Name generieren
            if not output_name:
                output_name = f"truefalse_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            # H5P-Fragen erstellen
            h5p_questions = []
            for idx, q in enumerate(questions):
                h5p_questions.append({
                    "params": {
                        "question": f"<p>{q['text']}</p>",
                        "correct": "true" if q['correct'] else "false",
                        "l10n": {"trueText": "Wahr", "falseText": "Falsch"},
                        "behaviour": {
                            "enableRetry": True,
                            "enableSolutionsButton": True,
                            "confirmCheckDialog": False,
                            "confirmRetryDialog": False,
                            "autoCheck": False
                        },
                        "feedbackOnCorrect": q.get('feedback_correct', self.style.feedback_correct),
                        "feedbackOnWrong": q.get('feedback_wrong', self.style.feedback_wrong)
                    },
                    "library": "H5P.TrueFalse 1.8",
                    "subContentId": f"tf-{idx}"
                })

            # Content erstellen
            content = {
                "introPage": {
                    "showIntroPage": True,
                    "title": title,
                    "introduction": "<p>Entscheide bei jeder Aussage: Wahr oder Falsch?</p>"
                },
                "progressType": "dots",
                "passPercentage": self.style.pass_percentage,
                "questions": h5p_questions,
                "texts": self._get_question_set_texts(),
                "endGame": self._get_end_game_config(),
                "override": {"showSolutionButton": "on", "retryButton": "on"}
            }

            # Dateien schreiben
            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.QuestionSet",
                [
                    {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
                    {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8}
                ]
            ))

            # Packen
            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(
                success=True,
                path=output_path,
                content_type="TrueFalse",
                title=title
            )

        except H5PValidationError as e:
            return H5PResult(success=False, error=str(e), content_type="TrueFalse", title=title)
        except H5PGenerationError as e:
            return H5PResult(success=False, error=str(e), content_type="TrueFalse", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="TrueFalse", title=title)


# =============================================================================
# Multiple Choice Generator
# =============================================================================

class MultiChoiceGenerator(H5PGenerator):
    """Generator für Multiple Choice Fragen"""

    def create(self, title: str, questions: List[Dict], output_name: str = None) -> H5PResult:
        """
        Erstellt eine Multiple Choice H5P-Datei

        Args:
            title: Titel des Quiz
            questions: Liste von Dicts mit:
                - question: Die Frage
                - answers: Liste von Dicts mit:
                    - text: Antworttext
                    - correct: True/False
                    - feedback: Optional
                - tip: Optional, Hinweis zur Frage
            output_name: Dateiname

        Returns:
            H5PResult
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_list(questions, "Fragen", min_items=1)

            for i, q in enumerate(questions):
                if 'question' not in q:
                    raise H5PValidationError(f"Frage {i+1}: 'question' fehlt")
                if 'answers' not in q or len(q['answers']) < 2:
                    raise H5PValidationError(f"Frage {i+1}: Mindestens 2 Antworten erforderlich")
                if not any(a.get('correct', False) for a in q['answers']):
                    raise H5PValidationError(f"Frage {i+1}: Mindestens eine korrekte Antwort erforderlich")

            if not output_name:
                output_name = f"multichoice_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            h5p_questions = []
            for idx, q in enumerate(questions):
                answers = []
                for a in q['answers']:
                    answers.append({
                        "text": f"<div>{a['text']}</div>",
                        "correct": a.get('correct', False),
                        "tipsAndFeedback": {"tip": a.get('feedback', '')}
                    })

                h5p_questions.append({
                    "params": {
                        "question": f"<p>{q['question']}</p>",
                        "answers": answers,
                        "behaviour": {
                            "enableRetry": True,
                            "enableSolutionsButton": True,
                            "enableCheckButton": True,
                            "type": "auto",
                            "singlePoint": False,
                            "randomAnswers": True,
                            "showSolutionsRequiresInput": True,
                            "confirmCheckDialog": False,
                            "confirmRetryDialog": False,
                            "autoCheck": False,
                            "passPercentage": 100
                        },
                        "UI": {
                            "checkAnswerButton": "Prüfen",
                            "submitAnswerButton": "Absenden",
                            "showSolutionButton": "Lösung zeigen",
                            "tryAgainButton": "Nochmal",
                            "correctText": self.style.feedback_correct,
                            "incorrectText": self.style.feedback_wrong
                        }
                    },
                    "library": "H5P.MultiChoice 1.16",
                    "subContentId": f"mc-{idx}"
                })

            content = {
                "introPage": {
                    "showIntroPage": True,
                    "title": title,
                    "introduction": "<p>Wähle die richtige(n) Antwort(en).</p>"
                },
                "progressType": "dots",
                "passPercentage": self.style.pass_percentage,
                "questions": h5p_questions,
                "texts": self._get_question_set_texts(),
                "endGame": self._get_end_game_config(),
                "override": {"showSolutionButton": "on", "retryButton": "on"}
            }

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.QuestionSet",
                [
                    {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
                    {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16}
                ]
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="MultiChoice", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="MultiChoice", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="MultiChoice", title=title)


# =============================================================================
# Fill in the Blanks Generator
# =============================================================================

class FillInBlanksGenerator(H5PGenerator):
    """Generator für Lückentexte"""

    def create(self, title: str, text_with_blanks: str, output_name: str = None) -> H5PResult:
        """
        Erstellt eine Fill in the Blanks H5P-Datei

        Args:
            title: Titel
            text_with_blanks: Text mit *Lücken* markiert
                Beispiel: "Die Hauptstadt ist *Berlin*."
                Mehrere Antworten: "*Berlin/berlin*"
            output_name: Dateiname

        Returns:
            H5PResult
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_not_empty(text_with_blanks, "Text")

            # Prüfe ob mindestens eine Lücke vorhanden
            if '*' not in text_with_blanks:
                raise H5PValidationError("Text enthält keine Lücken (markiere mit *Lücke*)")

            blanks_count = text_with_blanks.count('*') // 2
            if blanks_count < 1:
                raise H5PValidationError("Text muss mindestens eine Lücke enthalten")

            if not output_name:
                output_name = f"blanks_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            content = {
                "text": text_with_blanks,
                "overallFeedback": [
                    {"from": 0, "to": 50, "feedback": self.style.feedback_wrong},
                    {"from": 51, "to": 80, "feedback": self.style.feedback_partial},
                    {"from": 81, "to": 100, "feedback": self.style.feedback_correct}
                ],
                "showSolutions": "Lösung anzeigen",
                "tryAgain": "Nochmal",
                "checkAnswer": "Prüfen",
                "submitAnswer": "Absenden",
                "notFilledOut": "Bitte fülle alle Lücken aus",
                "answerIsCorrect": "':ans' ist richtig",
                "answerIsWrong": "':ans' ist falsch",
                "answeredCorrectly": "Richtig beantwortet",
                "answeredIncorrectly": "Falsch beantwortet",
                "solutionLabel": "Richtige Antwort:",
                "inputLabel": "Lücke @num von @total",
                "behaviour": {
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "enableCheckButton": True,
                    "caseSensitive": False,
                    "showSolutionsRequiresInput": True,
                    "autoCheck": False,
                    "separateLines": False,
                    "acceptSpellingErrors": True
                }
            }

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.Blanks",
                [{"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14}]
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="FillInBlanks", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="FillInBlanks", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="FillInBlanks", title=title)


# =============================================================================
# Drag and Drop Generator
# =============================================================================

class DragDropGenerator(H5PGenerator):
    """Generator für Drag and Drop Zuordnungsaufgaben"""

    def create(self, title: str, task_description: str, dropzones: List[str],
               draggables: List[Dict], output_name: str = None,
               background_image: str = None) -> H5PResult:
        """
        Erstellt eine Drag and Drop H5P-Datei

        Args:
            title: Titel
            task_description: Aufgabenstellung
            dropzones: Liste von Dropzone-Namen
            draggables: Liste von Dicts mit:
                - text: Der zu ziehende Text
                - dropzone: Index der korrekten Dropzone (0-basiert)
            output_name: Dateiname
            background_image: Optional - URL zu einem Hintergrundbild (PNG/SVG)

        Returns:
            H5PResult
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_list(dropzones, "Dropzones", min_items=1)
            self._validate_list(draggables, "Draggables", min_items=1)

            max_dropzone = len(dropzones) - 1
            for i, d in enumerate(draggables):
                if 'text' not in d:
                    raise H5PValidationError(f"Draggable {i+1}: 'text' fehlt")
                if 'dropzone' not in d:
                    raise H5PValidationError(f"Draggable {i+1}: 'dropzone' fehlt")
                if d['dropzone'] < 0 or d['dropzone'] > max_dropzone:
                    raise H5PValidationError(f"Draggable {i+1}: dropzone {d['dropzone']} ungültig (0-{max_dropzone})")

            if not output_name:
                output_name = f"dragdrop_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            # =================================================================
            # Background Image (optional)
            # =================================================================
            bg_settings = None
            if background_image:
                try:
                    import requests
                    from pathlib import Path as PathLib

                    # Download the image
                    response = requests.get(background_image, timeout=30, headers={
                        'User-Agent': 'H5P-Generator/2.0'
                    })
                    response.raise_for_status()

                    # Determine filename and mime type
                    if '.svg' in background_image.lower():
                        bg_filename = "background.svg"
                        bg_mime = "image/svg+xml"
                    elif '.png' in background_image.lower():
                        bg_filename = "background.png"
                        bg_mime = "image/png"
                    else:
                        bg_filename = "background.jpg"
                        bg_mime = "image/jpeg"

                    # Save to content/images/
                    images_dir = temp_dir / "content" / "images"
                    images_dir.mkdir(parents=True, exist_ok=True)
                    (images_dir / bg_filename).write_bytes(response.content)

                    bg_settings = {
                        "path": f"images/{bg_filename}",
                        "mime": bg_mime,
                        "copyright": {"license": "U"}
                    }
                except Exception as e:
                    print(f"[WARN] Background image download failed: {e}")

            # =================================================================
            # Canvas
            # =================================================================
            canvas_width = 620
            canvas_height = 450  # Match v13 reference

            # =================================================================
            # DRAGGABLES: Based on working v13 reference
            # Width 6-8 depending on text length, height 2
            # =================================================================
            h5p_draggables = []

            items_per_row = 5
            h_gap = 1.5
            v_gap = 0.8
            start_x = 2
            start_y = 2

            for i, drag in enumerate(draggables):
                row = i // items_per_row
                col = i % items_per_row

                # Calculate width based on text length (6-8 range)
                text_len = len(drag['text'])
                if text_len <= 12:
                    item_width = 6
                elif text_len <= 18:
                    item_width = 7
                else:
                    item_width = 8

                item_height = 2

                x_pos = start_x + col * (8 + h_gap)  # Use max width for spacing
                y_pos = start_y + row * (item_height + v_gap)

                h5p_draggables.append({
                    "x": round(x_pos, 2),
                    "y": round(y_pos, 2),
                    "width": item_width,
                    "height": item_height,
                    "dropZones": [str(drag['dropzone'])],
                    "type": {
                        "library": "H5P.AdvancedText 1.1",
                        "params": {
                            "text": f"<p style='text-align:center;margin:0;font-size:12px;font-weight:bold;'>{drag['text']}</p>"
                        },
                        "subContentId": f"drag-{i}",
                        "metadata": {"contentType": "Text", "license": "U", "title": drag['text']}
                    },
                    "backgroundOpacity": 80,
                    "multiple": False
                })

            # =================================================================
            # DROPZONES: Based on working v13 reference
            # Fixed positions: x=3,37,71 for 3 zones, width=10, height=73
            # =================================================================
            num_zones = len(dropzones)

            zone_height = 73   # Tall dropzones (v13 reference)
            zone_y = 22        # Start below draggables (v13 reference)
            zone_width = 10    # Wide enough for content (v13 reference)

            # Fixed X-positions based on number of zones (v13 pattern)
            # These create non-overlapping zones on a 620px canvas
            if num_zones == 2:
                zone_positions = [10, 55]
            elif num_zones == 3:
                zone_positions = [3, 37, 71]  # v13 reference values
            elif num_zones == 4:
                zone_positions = [2, 26, 50, 74]
            elif num_zones == 5:
                zone_positions = [2, 20, 38, 56, 74]
            else:
                # Distribute evenly for other counts
                spacing = 90 // max(1, num_zones)
                zone_positions = [3 + i * spacing for i in range(num_zones)]

            zone_colors = ["#e3f2fd", "#fce4ec", "#e8f5e9", "#fff8e1", "#f3e5f5", "#e0f7fa"]

            h5p_dropzones = []
            for i, dz in enumerate(dropzones):
                bg_color = zone_colors[i % len(zone_colors)]
                x_pos = zone_positions[i]

                h5p_dropzones.append({
                    "x": x_pos,
                    "y": zone_y,
                    "width": zone_width,
                    "height": zone_height,
                    "correctElements": [],
                    "showLabel": True,
                    "backgroundOpacity": 70,
                    "tipsAndFeedback": {"tip": ""},
                    "single": False,
                    "autoAlign": True,
                    "label": f"<div style='text-align:center;font-weight:bold;font-size:14px;'>{dz}</div>"
                })

            # Weise Draggables den Dropzones zu
            for i, drag in enumerate(draggables):
                h5p_dropzones[drag['dropzone']]['correctElements'].append(str(i))

            # Build settings with optional background
            question_settings = {
                "size": {"width": canvas_width, "height": canvas_height}
            }
            if bg_settings:
                question_settings["background"] = bg_settings

            content = {
                "scoreShow": "Punkte anzeigen",
                "tryAgain": "Nochmal",
                "scoreExplanation": "Richtige Zuordnungen geben Punkte.",
                "question": {
                    "settings": question_settings,
                    "task": {
                        "elements": h5p_draggables,
                        "dropZones": h5p_dropzones
                    }
                },
                "overallFeedback": [
                    {"from": 0, "to": 50, "feedback": self.style.feedback_wrong},
                    {"from": 51, "to": 80, "feedback": self.style.feedback_partial},
                    {"from": 81, "to": 100, "feedback": self.style.feedback_correct}
                ],
                "behaviour": {
                    "enableRetry": True,
                    "enableCheckButton": True,
                    "showSolutionsRequiresInput": True,
                    "singlePoint": False,
                    "applyPenalties": False,
                    "enableScoreExplanation": True,
                    "dropZoneHighlighting": "always",
                    "autoAlignSpacing": 2,
                    "enableFullScreen": True,
                    "showScorePoints": True,
                    "showTitle": True
                },
                "grabbablePrefix": "Ziehbares Element {num}.",
                "dropzonePrefix": "Dropzone {num}.",
                "tipLabel": "Tipps anzeigen",
                "correctAnswer": "Richtige Antwort",
                "wrongAnswer": "Falsche Antwort",
                "scoreBarLabel": "Du hast :num von :total Punkten",
                "showSolution": "Lösung anzeigen",
                "submit": "Absenden"
            }

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.DragQuestion",
                [
                    {"machineName": "H5P.DragQuestion", "majorVersion": 1, "minorVersion": 14},
                    {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1}
                ]
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="DragDrop", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="DragDrop", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="DragDrop", title=title)


# =============================================================================
# NEW: Single Choice Set Generator
# =============================================================================

class SingleChoiceSetGenerator(H5PGenerator):
    """Generator für schnelle Single Choice Fragen (ohne QuestionSet-Wrapper)"""

    def create(self, title: str, questions: List[Dict], output_name: str = None) -> H5PResult:
        """
        Erstellt ein Single Choice Set - schnelle Frage/Antwort ohne Intro

        Args:
            title: Titel
            questions: Liste von Dicts mit:
                - question: Die Frage
                - answers: Liste von Strings (erste ist korrekt!)
            output_name: Dateiname

        Returns:
            H5PResult
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_list(questions, "Fragen", min_items=1)

            for i, q in enumerate(questions):
                if 'question' not in q:
                    raise H5PValidationError(f"Frage {i+1}: 'question' fehlt")
                if 'answers' not in q or len(q['answers']) < 2:
                    raise H5PValidationError(f"Frage {i+1}: Mindestens 2 Antworten erforderlich")

            if not output_name:
                output_name = f"singlechoice_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            h5p_questions = []
            for q in questions:
                h5p_questions.append({
                    "question": f"<p>{q['question']}</p>",
                    "answers": [f"<p>{a}</p>" for a in q['answers']]
                })

            content = {
                "choices": h5p_questions,
                "overallFeedback": [
                    {"from": 0, "to": 50, "feedback": self.style.feedback_wrong},
                    {"from": 51, "to": 80, "feedback": self.style.feedback_partial},
                    {"from": 81, "to": 100, "feedback": self.style.feedback_correct}
                ],
                "behaviour": {
                    "autoContinue": True,
                    "timeoutCorrect": 2000,
                    "timeoutWrong": 3000,
                    "soundEffectsEnabled": False,
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "passPercentage": self.style.pass_percentage
                },
                "l10n": {
                    "nextButtonLabel": "Weiter",
                    "showSolutionButtonLabel": "Lösung zeigen",
                    "retryButtonLabel": "Nochmal",
                    "solutionViewTitle": "Lösung",
                    "correctText": "Richtig!",
                    "incorrectText": "Falsch!",
                    "muteButtonLabel": "Ton aus",
                    "closeButtonLabel": "Schließen",
                    "slideOfTotal": "Frage :num von :total",
                    "scoreBarLabel": "Du hast :num von :total Punkten",
                    "resultSlideTitle": "Ergebnis"
                }
            }

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.SingleChoiceSet",
                [{"machineName": "H5P.SingleChoiceSet", "majorVersion": 1, "minorVersion": 11}]
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="SingleChoiceSet", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="SingleChoiceSet", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="SingleChoiceSet", title=title)


# =============================================================================
# NEW: Dialog Cards Generator (Flashcards)
# =============================================================================

class DialogCardsGenerator(H5PGenerator):
    """Generator für Lernkarten (Flashcards)"""

    def create(self, title: str, cards: List[Dict], output_name: str = None) -> H5PResult:
        """
        Erstellt Dialog Cards (Lernkarten)

        Args:
            title: Titel
            cards: Liste von Dicts mit:
                - front: Vorderseite (Frage)
                - back: Rückseite (Antwort)
                - tip: Optional, Hinweis
            output_name: Dateiname

        Returns:
            H5PResult
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_list(cards, "Karten", min_items=1)

            for i, c in enumerate(cards):
                if 'front' not in c:
                    raise H5PValidationError(f"Karte {i+1}: 'front' fehlt")
                if 'back' not in c:
                    raise H5PValidationError(f"Karte {i+1}: 'back' fehlt")

            if not output_name:
                output_name = f"flashcards_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            h5p_cards = []
            for c in cards:
                card = {
                    "text": f"<p style=\"text-align:center;\">{c['front']}</p>",
                    "answer": f"<p style=\"text-align:center;\">{c['back']}</p>"
                }
                if c.get('tip'):
                    card["tips"] = [{"text": c['tip']}]
                h5p_cards.append(card)

            content = {
                "title": f"<p>{title}</p>",
                "mode": "normal",
                "description": "<p>Klicke auf die Karte um sie umzudrehen.</p>",
                "dialogs": h5p_cards,
                "behaviour": {
                    "enableRetry": True,
                    "disableBackwardsNavigation": False,
                    "scaleTextNotCard": False,
                    "randomCards": False,
                    "maxProficiency": 5,
                    "quickProgression": False
                },
                "answer": "Umdrehen",
                "next": "Weiter",
                "prev": "Zurück",
                "retry": "Nochmal",
                "correctAnswer": "Ich wusste es!",
                "incorrectAnswer": "Ich wusste es nicht",
                "round": "Runde @round",
                "cardsLeft": "Noch @number Karten",
                "nextRound": "Nächste Runde",
                "showSummary": "Zusammenfassung",
                "summary": "Zusammenfassung",
                "summaryCardsRight": "Karten richtig:",
                "summaryCardsWrong": "Karten falsch:",
                "summaryCardsNotShown": "Karten nicht gezeigt:",
                "summaryOverallScore": "Gesamtpunktzahl:",
                "summaryCardsCompleted": "Abgeschlossene Karten:",
                "summaryCompletedRounds": "Abgeschlossene Runden:",
                "progressText": "@card von @total"
            }

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.Dialogcards",
                [{"machineName": "H5P.Dialogcards", "majorVersion": 1, "minorVersion": 9}]
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="DialogCards", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="DialogCards", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="DialogCards", title=title)


# =============================================================================
# NEW: Mark the Words Generator
# =============================================================================

class MarkTheWordsGenerator(H5PGenerator):
    """Generator für 'Markiere die Wörter' Aufgaben"""

    def create(self, title: str, text_with_marks: str, output_name: str = None,
               task_description: str = "Markiere alle korrekten Wörter.") -> H5PResult:
        """
        Erstellt eine Mark the Words Aufgabe

        Args:
            title: Titel
            text_with_marks: Text mit *korrekten Wörtern* markiert
                Beispiel: "Berlin ist die *Hauptstadt* von *Deutschland*."
            task_description: Aufgabenstellung
            output_name: Dateiname

        Returns:
            H5PResult
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_not_empty(text_with_marks, "Text")

            if '*' not in text_with_marks:
                raise H5PValidationError("Text enthält keine markierten Wörter (markiere mit *Wort*)")

            if not output_name:
                output_name = f"markwords_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            content = {
                "taskDescription": f"<p>{task_description}</p>",
                "textField": text_with_marks,
                "overallFeedback": [
                    {"from": 0, "to": 50, "feedback": self.style.feedback_wrong},
                    {"from": 51, "to": 80, "feedback": self.style.feedback_partial},
                    {"from": 81, "to": 100, "feedback": self.style.feedback_correct}
                ],
                "behaviour": {
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "enableCheckButton": True,
                    "showScorePoints": True
                },
                "checkAnswerButton": "Prüfen",
                "tryAgainButton": "Nochmal",
                "showSolutionButton": "Lösung zeigen",
                "correctAnswer": "Richtige Antwort!",
                "incorrectAnswer": "Falsche Antwort!",
                "missedAnswer": "Verpasst!",
                "displaySolutionDescription": "Die Lösung wird mit einem Stern markiert."
            }

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.MarkTheWords",
                [{"machineName": "H5P.MarkTheWords", "majorVersion": 1, "minorVersion": 11}]
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="MarkTheWords", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="MarkTheWords", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="MarkTheWords", title=title)


# =============================================================================
# NEW: Summary Generator
# =============================================================================

class SummaryGenerator(H5PGenerator):
    """Generator für Zusammenfassungen mit Auswahl"""

    def create(self, title: str, summary_items: List[Dict], output_name: str = None,
               intro_text: str = "Wähle die korrekte Aussage.") -> H5PResult:
        """
        Erstellt eine Summary (Zusammenfassung zum Durcharbeiten)

        Args:
            title: Titel
            summary_items: Liste von Dicts mit:
                - statements: Liste von Aussagen (erste ist korrekt!)
                - tip: Optional
            intro_text: Einführungstext
            output_name: Dateiname

        Returns:
            H5PResult
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_list(summary_items, "Summary Items", min_items=1)

            for i, item in enumerate(summary_items):
                if 'statements' not in item or len(item['statements']) < 2:
                    raise H5PValidationError(f"Item {i+1}: Mindestens 2 Aussagen erforderlich")

            if not output_name:
                output_name = f"summary_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            h5p_summaries = []
            for item in summary_items:
                h5p_summaries.append({
                    "summary": [f"<p>{s}</p>\n" for s in item['statements']],  # Must be strings, not objects!
                    "tip": item.get('tip', '')
                })

            content = {
                "intro": f"<p>{intro_text}</p>",
                "summaries": h5p_summaries,
                "overallFeedback": [
                    {"from": 0, "to": 50, "feedback": self.style.feedback_wrong},
                    {"from": 51, "to": 80, "feedback": self.style.feedback_partial},
                    {"from": 81, "to": 100, "feedback": self.style.feedback_correct}
                ],
                "solvedLabel": "Gelöst:",
                "scoreLabel": "Falsche Versuche:",
                "resultLabel": "Dein Ergebnis",
                "labelCorrect": "Richtig!",
                "labelIncorrect": "Falsch! Versuche es nochmal.",
                "alternativeIncorrectLabel": "Falsch",
                "labelCorrectAnswers": "Richtige Antworten.",
                "tipButtonLabel": "Tipp zeigen",
                "scoreBarLabel": "Du hast @score von @total",
                "progressText": "Fortschritt @current von @total"
            }

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.Summary",
                [{"machineName": "H5P.Summary", "majorVersion": 1, "minorVersion": 10}]
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="Summary", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="Summary", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="Summary", title=title)


# =============================================================================
# NEW: Accordion Generator
# =============================================================================

class AccordionGenerator(H5PGenerator):
    """Generator für aufklappbare Inhaltsabschnitte"""

    def create(self, title: str, panels: List[Dict], output_name: str = None) -> H5PResult:
        """
        Erstellt ein Accordion (aufklappbare Abschnitte)

        Args:
            title: Titel
            panels: Liste von Dicts mit:
                - title: Abschnittsüberschrift
                - content: Inhalt (HTML erlaubt)
            output_name: Dateiname

        Returns:
            H5PResult
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_list(panels, "Abschnitte", min_items=1)

            for i, p in enumerate(panels):
                if 'title' not in p:
                    raise H5PValidationError(f"Abschnitt {i+1}: 'title' fehlt")
                if 'content' not in p:
                    raise H5PValidationError(f"Abschnitt {i+1}: 'content' fehlt")

            if not output_name:
                output_name = f"accordion_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            h5p_panels = []
            for idx, p in enumerate(panels):
                h5p_panels.append({
                    "title": p['title'],
                    "content": {
                        "params": {"text": f"<p>{p['content']}</p>"},
                        "library": "H5P.AdvancedText 1.1",
                        "subContentId": f"acc-{idx}-{hash(p['title']) % 10000}",
                        "metadata": {
                            "contentType": "Text",
                            "license": "U",
                            "title": p['title']
                        }
                    }
                })

            content = {
                "panels": h5p_panels,
                "hTag": "h2"
            }

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.Accordion",
                [
                    {"machineName": "H5P.Accordion", "majorVersion": 1, "minorVersion": 0},
                    {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1},
                    {"machineName": "FontAwesome", "majorVersion": 4, "minorVersion": 5}
                ]
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="Accordion", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="Accordion", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="Accordion", title=title)


# =============================================================================
# NEW: Drag the Words Generator (v2.1)
# =============================================================================

class DragTextGenerator(H5PGenerator):
    """Generator für 'Drag the Words' - Wörter in Lücken ziehen"""

    def create(self, title: str, text_with_blanks: str, output_name: str = None,
               task_description: str = "Ziehe die Wörter an die richtige Stelle.") -> H5PResult:
        """
        Erstellt eine Drag the Words Aufgabe

        Args:
            title: Titel
            text_with_blanks: Text mit *Lücken* markiert
                Beispiel: "Die *Hauptstadt* von Deutschland ist *Berlin*."
            task_description: Aufgabenstellung
            output_name: Dateiname

        Returns:
            H5PResult
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_not_empty(text_with_blanks, "Text")

            if '*' not in text_with_blanks:
                raise H5PValidationError("Text enthält keine Lücken (markiere mit *Wort*)")

            blanks_count = text_with_blanks.count('*') // 2
            if blanks_count < 1:
                raise H5PValidationError("Text muss mindestens eine Lücke enthalten")

            if not output_name:
                output_name = f"dragtext_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            content = {
                "taskDescription": f"<p>{task_description}</p>",
                "textField": text_with_blanks,
                "overallFeedback": [
                    {"from": 0, "to": 50, "feedback": self.style.feedback_wrong},
                    {"from": 51, "to": 80, "feedback": self.style.feedback_partial},
                    {"from": 81, "to": 100, "feedback": self.style.feedback_correct}
                ],
                "checkAnswer": "Prüfen",
                "tryAgain": "Nochmal",
                "showSolution": "Lösung anzeigen",
                "dropZoneIndex": "Lücke @index.",
                "empty": "Lücke @index ist leer.",
                "contains": "Lücke @index enthält @draggable.",
                "ariaDraggableIndex": "@index von @count ziehbare Elemente.",
                "tipLabel": "Tipp anzeigen",
                "correctText": "Richtig!",
                "incorrectText": "Falsch!",
                "resetDropTitle": "Zurücksetzen",
                "resetDropDescription": "Bist du sicher?",
                "grabbed": "Gezogen.",
                "cancelledDragging": "Ziehen abgebrochen.",
                "correctAnswer": "Richtige Antwort:",
                "behaviour": {
                    "enableRetry": True,
                    "enableSolutionsButton": True,
                    "enableCheckButton": True,
                    "instantFeedback": False
                }
            }

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.DragText",
                [{"machineName": "H5P.DragText", "majorVersion": 1, "minorVersion": 10}]
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="DragText", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="DragText", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="DragText", title=title)


# =============================================================================
# NEW: Timeline Generator (v2.1)
# =============================================================================

class TimelineGenerator(H5PGenerator):
    """Generator für Zeitleisten/Timelines"""

    def create(self, title: str, events: List[Dict], output_name: str = None,
               description: str = "") -> H5PResult:
        """
        Erstellt eine Timeline

        Args:
            title: Titel der Timeline
            events: Liste von Dicts mit:
                - headline: Überschrift des Events
                - text: Beschreibung
                - start_date: Startdatum als String (z.B. "2020", "2020-03", "2020-03-15")
                - end_date: Optional, Enddatum
                - media: Optional, URL zu Bild/Video
            description: Optionale Gesamtbeschreibung
            output_name: Dateiname

        Returns:
            H5PResult
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_list(events, "Events", min_items=1)

            for i, e in enumerate(events):
                if 'headline' not in e:
                    raise H5PValidationError(f"Event {i+1}: 'headline' fehlt")
                if 'start_date' not in e:
                    raise H5PValidationError(f"Event {i+1}: 'start_date' fehlt")

            if not output_name:
                output_name = f"timeline_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            # Build timeline events
            # Note: startDate must be a STRING with just the year!
            timeline_events = []
            for e in events:
                # Extract just the year from date string
                date_str = str(e['start_date'])
                start_year = date_str.split('-')[0] if '-' in date_str else date_str

                event = {
                    "headline": e['headline'],
                    "text": f"<p>{e.get('text', '')}</p>",
                    "startDate": start_year,  # Just the year as string
                    "endDate": start_year,    # Required field
                    "asset": {
                        "media": e.get('media', ''),
                        "credit": e.get('credit', '')
                    }
                }
                if e.get('end_date'):
                    end_str = str(e['end_date'])
                    event["endDate"] = end_str.split('-')[0] if '-' in end_str else end_str

                timeline_events.append(event)

            # Build content structure matching official h5p.org format exactly
            content = {
                "timeline": {
                    "headline": title,
                    "text": f"<p>{description}</p>" if description else "<p></p>",
                    "date": timeline_events,
                    "era": [],
                    "asset": {
                        "media": "",
                        "credit": ""
                    },
                    "defaultZoomLevel": 0,
                    "height": 600,
                    "language": "de"
                }
            }

            self._write_json(temp_dir / "content" / "content.json", content)

            # Timeline needs special h5p.json with div embedType and TimelineJS dependency
            h5p_meta = {
                "title": title,
                "language": "de",
                "mainLibrary": "H5P.Timeline",
                "embedTypes": ["div"],  # Timeline requires div, not iframe!
                "license": "CC BY",
                "preloadedDependencies": [
                    {"machineName": "H5P.Timeline", "majorVersion": 1, "minorVersion": 1},
                    {"machineName": "TimelineJS", "majorVersion": 1, "minorVersion": 1}
                ]
            }
            self._write_json(temp_dir / "h5p.json", h5p_meta)

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="Timeline", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="Timeline", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="Timeline", title=title)


# =============================================================================
# NEW: Memory Game Generator (v2.1)
# =============================================================================

class MemoryGameGenerator(H5PGenerator):
    """Generator für Memory-Spiele"""

    def create(self, title: str, cards: List[Dict], output_name: str = None) -> H5PResult:
        """
        Erstellt ein Memory-Spiel

        Args:
            title: Titel
            cards: Liste von Dicts mit:
                - image: URL oder Pfad zum Bild
                - description: Beschreibung des Bildes
                - match_image: Optional, anderes Bild für das Paar
            output_name: Dateiname

        Returns:
            H5PResult

        Note:
            Benötigt Bilder. Für text-basiertes Memory siehe Flashcards.
        """
        try:
            self._validate_not_empty(title, "Titel")
            self._validate_list(cards, "Karten", min_items=2)

            for i, c in enumerate(cards):
                if 'image' not in c and 'description' not in c:
                    raise H5PValidationError(f"Karte {i+1}: 'image' oder 'description' fehlt")

            if not output_name:
                output_name = f"memory_{self._sanitize_filename(title)}"
            else:
                output_name = self._sanitize_filename(output_name)

            temp_dir = self._create_temp_dir(output_name)

            # Build memory cards
            memory_cards = []
            for i, c in enumerate(cards):
                card = {
                    "description": c.get('description', f'Karte {i+1}'),
                    "imageAlt": c.get('description', f'Karte {i+1}')
                }
                if c.get('image'):
                    card["image"] = {
                        "path": c['image'],
                        "mime": "image/jpeg",
                        "copyright": {"license": "U"}
                    }
                memory_cards.append(card)

            content = {
                "cards": memory_cards,
                "behaviour": {
                    "useGrid": True,
                    "allowRetry": True
                },
                "l10n": {
                    "cardTurns": "Züge",
                    "timeSpent": "Zeit",
                    "feedback": "Gut gemacht!",
                    "tryAgain": "Nochmal",
                    "closeLabel": "Schließen",
                    "label": f"Memory: {title}",
                    "done": "Alle Paare gefunden!",
                    "cardPrefix": "Karte %num:",
                    "cardUnturned": "Nicht umgedreht.",
                    "cardMatched": "Paar gefunden."
                },
                "lookNFeel": {
                    "themeColor": self.style.primary_color
                }
            }

            self._write_json(temp_dir / "content" / "content.json", content)
            self._write_json(temp_dir / "h5p.json", self._create_h5p_meta(
                title, "H5P.MemoryGame",
                [{"machineName": "H5P.MemoryGame", "majorVersion": 1, "minorVersion": 3}]
            ))

            output_path = self._package_h5p(temp_dir, output_name)
            self._cleanup(temp_dir)

            return H5PResult(success=True, path=output_path, content_type="MemoryGame", title=title)

        except (H5PValidationError, H5PGenerationError) as e:
            return H5PResult(success=False, error=str(e), content_type="MemoryGame", title=title)
        except Exception as e:
            return H5PResult(success=False, error=f"Unerwarteter Fehler: {e}", content_type="MemoryGame", title=title)


# =============================================================================
# Convenience Functions
# =============================================================================

def create_true_false(title: str, questions: List[Dict], output_name: str = None,
                      style: H5PStyle = None) -> H5PResult:
    """Erstellt ein True/False Quiz"""
    gen = TrueFalseGenerator(style=style)
    return gen.create(title, questions, output_name)


def create_multi_choice(title: str, questions: List[Dict], output_name: str = None,
                        style: H5PStyle = None) -> H5PResult:
    """Erstellt ein Multiple Choice Quiz"""
    gen = MultiChoiceGenerator(style=style)
    return gen.create(title, questions, output_name)


def create_fill_blanks(title: str, text: str, output_name: str = None,
                       style: H5PStyle = None) -> H5PResult:
    """Erstellt einen Lückentext"""
    gen = FillInBlanksGenerator(style=style)
    return gen.create(title, text, output_name)


def create_drag_drop(title: str, task: str, dropzones: List[str],
                     draggables: List[Dict], output_name: str = None,
                     style: H5PStyle = None,
                     background_image: str = None) -> H5PResult:
    """Erstellt eine Drag & Drop Aufgabe

    Args:
        background_image: Optional URL zu einem Hintergrundbild (SVG/PNG/JPG)
    """
    gen = DragDropGenerator(style=style)
    return gen.create(title, task, dropzones, draggables, output_name, background_image)


def create_single_choice(title: str, questions: List[Dict], output_name: str = None,
                         style: H5PStyle = None) -> H5PResult:
    """Erstellt ein Single Choice Set"""
    gen = SingleChoiceSetGenerator(style=style)
    return gen.create(title, questions, output_name)


def create_flashcards(title: str, cards: List[Dict], output_name: str = None,
                      style: H5PStyle = None) -> H5PResult:
    """Erstellt Lernkarten (Dialog Cards)"""
    gen = DialogCardsGenerator(style=style)
    return gen.create(title, cards, output_name)


def create_mark_words(title: str, text: str, output_name: str = None,
                      task: str = "Markiere alle korrekten Wörter.",
                      style: H5PStyle = None) -> H5PResult:
    """Erstellt eine 'Markiere die Wörter' Aufgabe"""
    gen = MarkTheWordsGenerator(style=style)
    return gen.create(title, text, output_name, task)


def create_summary(title: str, items: List[Dict], output_name: str = None,
                   intro: str = "Wähle die korrekte Aussage.",
                   style: H5PStyle = None) -> H5PResult:
    """Erstellt eine Summary"""
    gen = SummaryGenerator(style=style)
    return gen.create(title, items, output_name, intro)


def create_accordion(title: str, panels: List[Dict], output_name: str = None,
                     style: H5PStyle = None) -> H5PResult:
    """Erstellt ein Accordion"""
    gen = AccordionGenerator(style=style)
    return gen.create(title, panels, output_name)


def create_drag_text(title: str, text: str, output_name: str = None,
                     task: str = "Ziehe die Wörter an die richtige Stelle.",
                     style: H5PStyle = None) -> H5PResult:
    """Erstellt eine 'Drag the Words' Aufgabe - Wörter in Lücken ziehen"""
    gen = DragTextGenerator(style=style)
    return gen.create(title, text, output_name, task)


def create_timeline(title: str, events: List[Dict], output_name: str = None,
                    description: str = "", style: H5PStyle = None) -> H5PResult:
    """Erstellt eine Timeline/Zeitleiste"""
    gen = TimelineGenerator(style=style)
    return gen.create(title, events, output_name, description)


def create_memory_game(title: str, cards: List[Dict], output_name: str = None,
                       style: H5PStyle = None) -> H5PResult:
    """Erstellt ein Memory-Spiel (benötigt Bilder)"""
    gen = MemoryGameGenerator(style=style)
    return gen.create(title, cards, output_name)


# =============================================================================
# Batch Generation
# =============================================================================

def batch_create(content_list: List[Dict], style: H5PStyle = None) -> List[H5PResult]:
    """
    Erstellt mehrere H5P-Inhalte auf einmal

    Args:
        content_list: Liste von Dicts mit:
            - type: 'true_false', 'multi_choice', 'fill_blanks', 'drag_drop',
                    'single_choice', 'flashcards', 'mark_words', 'summary', 'accordion'
            - title: Titel
            - ... weitere typ-spezifische Felder
        style: Optionales Styling

    Returns:
        Liste von H5PResult
    """
    results = []

    type_mapping = {
        'true_false': ('questions', create_true_false),
        'multi_choice': ('questions', create_multi_choice),
        'fill_blanks': ('text', create_fill_blanks),
        'single_choice': ('questions', create_single_choice),
        'flashcards': ('cards', create_flashcards),
        'mark_words': ('text', create_mark_words),
        'summary': ('items', create_summary),
        'accordion': ('panels', create_accordion),
        'drag_text': ('text', create_drag_text),
        'timeline': ('events', create_timeline),
        'memory_game': ('cards', create_memory_game),
    }

    for item in content_list:
        content_type = item.get('type', '').lower()
        title = item.get('title', 'Untitled')
        output_name = item.get('output_name')

        if content_type == 'drag_drop':
            result = create_drag_drop(
                title,
                item.get('task', ''),
                item.get('dropzones', []),
                item.get('draggables', []),
                output_name,
                style
            )
        elif content_type in type_mapping:
            data_key, func = type_mapping[content_type]
            data = item.get(data_key)
            result = func(title, data, output_name, style=style)
        else:
            result = H5PResult(
                success=False,
                error=f"Unbekannter Typ: {content_type}",
                content_type=content_type,
                title=title
            )

        results.append(result)

    return results


# =============================================================================
# Main / Test
# =============================================================================

if __name__ == "__main__":
    print("H5P Generator v2.0 - Test")
    print("=" * 50)

    # Test mit Education Theme
    style = THEMES['education']

    # True/False Test
    tf = create_true_false(
        "Python Basics",
        [
            {"text": "Python ist eine Programmiersprache.", "correct": True},
            {"text": "Python wurde 2020 erfunden.", "correct": False}
        ],
        "test-truefalse",
        style=style
    )
    print(tf)

    # Fill in Blanks Test
    blanks = create_fill_blanks(
        "Geografie Test",
        "<p>Die Hauptstadt von Deutschland ist *Berlin*. Die größte Stadt ist *Berlin/Hamburg*.</p>",
        "test-blanks",
        style=style
    )
    print(blanks)

    # Flashcards Test
    cards = create_flashcards(
        "Vokabeln",
        [
            {"front": "Haus", "back": "house"},
            {"front": "Auto", "back": "car"}
        ],
        "test-flashcards",
        style=style
    )
    print(cards)

    # Mark Words Test
    mark = create_mark_words(
        "Hauptstädte",
        "Berlin ist die *Hauptstadt* von *Deutschland*. Paris ist keine deutsche Stadt.",
        "test-markwords",
        style=style
    )
    print(mark)

    # Validation Error Test
    bad = create_true_false("Empty", [], "test-empty")
    print(bad)

    print("\n" + "=" * 50)
    print("✅ Tests abgeschlossen!")
