#!/usr/bin/env python3
"""
H5P Generator - Erstellt .h5p-Dateien direkt aus Python
Unterstützte Content-Types:
- TrueFalse
- MultiChoice
- Blanks (Fill in the Blanks)
- DragQuestion (Drag and Drop)
- QuestionSet
"""

import json
import zipfile
import os
from pathlib import Path
from datetime import datetime
import shutil

class H5PGenerator:
    """Basisklasse für H5P-Generierung"""
    
    def __init__(self, output_dir="/home/claude/h5p-output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def create_h5p_json(self, title, library, library_version="1.0"):
        """Erstellt die h5p.json Metadaten-Datei"""
        return {
            "title": title,
            "language": "de",
            "mainLibrary": library,
            "embedTypes": ["iframe"],
            "license": "CC BY",
            "preloadedDependencies": [
                {"machineName": library, "majorVersion": 1, "minorVersion": 0}
            ]
        }
    
    def package_h5p(self, temp_dir, output_name):
        """Packt die H5P-Dateien in ein ZIP-Archiv"""
        output_path = self.output_dir / f"{output_name}.h5p"
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    zf.write(file_path, arcname)
        
        return output_path


class TrueFalseGenerator(H5PGenerator):
    """Generator für True/False Fragen"""
    
    def create(self, title, questions, output_name=None):
        """
        Erstellt eine True/False H5P-Datei
        
        Args:
            title: Titel des Quiz
            questions: Liste von Dicts mit:
                - text: Die Aussage
                - correct: True/False
                - feedback_correct: Feedback bei richtiger Antwort
                - feedback_wrong: Feedback bei falscher Antwort
            output_name: Dateiname (ohne .h5p)
        """
        if output_name is None:
            output_name = f"truefalse_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Temp-Verzeichnis erstellen
        temp_dir = Path("/tmp") / f"h5p_{output_name}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        content_dir = temp_dir / "content"
        content_dir.mkdir(exist_ok=True)
        
        # Content für jede Frage
        h5p_questions = []
        for q in questions:
            h5p_questions.append({
                "params": {
                    "question": f"<p>{q['text']}</p>",
                    "correct": "true" if q['correct'] else "false",
                    "l10n": {
                        "trueText": "Wahr",
                        "falseText": "Falsch"
                    },
                    "behaviour": {
                        "enableRetry": True,
                        "enableSolutionsButton": True,
                        "confirmCheckDialog": False,
                        "confirmRetryDialog": False,
                        "autoCheck": False
                    },
                    "confirmCheck": {
                        "header": "Fertig?",
                        "body": "Bist du sicher?",
                        "cancelLabel": "Abbrechen",
                        "confirmLabel": "Bestätigen"
                    },
                    "confirmRetry": {
                        "header": "Nochmal?",
                        "body": "Möchtest du es nochmal versuchen?",
                        "cancelLabel": "Abbrechen",
                        "confirmLabel": "Bestätigen"
                    },
                    "feedbackOnCorrect": q.get('feedback_correct', 'Richtig!'),
                    "feedbackOnWrong": q.get('feedback_wrong', 'Leider falsch.')
                },
                "library": "H5P.TrueFalse 1.8",
                "subContentId": f"tf-{len(h5p_questions)}"
            })
        
        # QuestionSet Content
        content = {
            "introPage": {
                "showIntroPage": True,
                "title": title,
                "introduction": f"<p>Entscheide bei jeder Aussage: Wahr oder Falsch?</p>"
            },
            "progressType": "dots",
            "passPercentage": 60,
            "questions": h5p_questions,
            "texts": {
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
            },
            "endGame": {
                "showResultPage": True,
                "showSolutionButton": True,
                "showRetryButton": True,
                "noResultMessage": "Quiz beendet",
                "message": "Du hast @score von @total Punkten erreicht.",
                "successGreeting": "Gratulation!",
                "successComment": "Du hast das Quiz bestanden!",
                "failGreeting": "Schade!",
                "failComment": "Versuche es nochmal.",
                "solutionButtonText": "Lösung anzeigen",
                "retryButtonText": "Nochmal versuchen",
                "finishButtonText": "Fertig"
            },
            "override": {
                "showSolutionButton": "on",
                "retryButton": "on"
            }
        }
        
        # content.json schreiben
        with open(content_dir / "content.json", 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        # h5p.json schreiben
        h5p_meta = {
            "title": title,
            "language": "de",
            "mainLibrary": "H5P.QuestionSet",
            "embedTypes": ["iframe"],
            "license": "CC BY",
            "preloadedDependencies": [
                {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
                {"machineName": "H5P.TrueFalse", "majorVersion": 1, "minorVersion": 8}
            ]
        }
        
        with open(temp_dir / "h5p.json", 'w', encoding='utf-8') as f:
            json.dump(h5p_meta, f, ensure_ascii=False, indent=2)
        
        # Packen
        output_path = self.package_h5p(temp_dir, output_name)
        
        # Cleanup
        shutil.rmtree(temp_dir)
        
        return output_path


class FillInBlanksGenerator(H5PGenerator):
    """Generator für Fill in the Blanks (Lückentext)"""
    
    def create(self, title, text_with_blanks, output_name=None):
        """
        Erstellt eine Fill in the Blanks H5P-Datei
        
        Args:
            title: Titel
            text_with_blanks: Text mit *Lücken* markiert
                Beispiel: "Die Hauptstadt von Deutschland ist *Berlin*."
                Mehrere Antworten: "Das Licht wird in *PPFD/ppfd* gemessen."
            output_name: Dateiname
        """
        if output_name is None:
            output_name = f"blanks_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        temp_dir = Path("/tmp") / f"h5p_{output_name}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        content_dir = temp_dir / "content"
        content_dir.mkdir(exist_ok=True)
        
        content = {
            "text": text_with_blanks,
            "overallFeedback": [
                {"from": 0, "to": 50, "feedback": "Versuche es nochmal!"},
                {"from": 51, "to": 80, "feedback": "Gut gemacht!"},
                {"from": 81, "to": 100, "feedback": "Ausgezeichnet!"}
            ],
            "showSolutions": "Show solution",
            "tryAgain": "Retry",
            "checkAnswer": "Check",
            "submitAnswer": "Submit",
            "notFilledOut": "Please fill in all blanks",
            "answerIsCorrect": "':ans' is correct",
            "answerIsWrong": "':ans' is wrong",
            "answeredCorrectly": "Answered correctly",
            "answeredIncorrectly": "Answered incorrectly",
            "solutionLabel": "Correct answer:",
            "inputLabel": "Blank input @num of @total",
            "inputHasTipLabel": "Tip available",
            "tipLabel": "Tip",
            "behaviour": {
                "enableRetry": True,
                "enableSolutionsButton": True,
                "enableCheckButton": True,
                "caseSensitive": False,
                "showSolutionsRequiresInput": True,
                "autoCheck": False,
                "separateLines": False,
                "acceptSpellingErrors": True
            },
            "confirmCheck": {
                "header": "Fertig?",
                "body": "Bist du sicher?",
                "cancelLabel": "Abbrechen",
                "confirmLabel": "Bestätigen"
            },
            "confirmRetry": {
                "header": "Nochmal?",
                "body": "Möchtest du es nochmal versuchen?",
                "cancelLabel": "Abbrechen",
                "confirmLabel": "Bestätigen"
            }
        }
        
        with open(content_dir / "content.json", 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        h5p_meta = {
            "title": title,
            "language": "de",
            "mainLibrary": "H5P.Blanks",
            "embedTypes": ["iframe"],
            "license": "CC BY",
            "preloadedDependencies": [
                {"machineName": "H5P.Blanks", "majorVersion": 1, "minorVersion": 14}
            ]
        }
        
        with open(temp_dir / "h5p.json", 'w', encoding='utf-8') as f:
            json.dump(h5p_meta, f, ensure_ascii=False, indent=2)
        
        output_path = self.package_h5p(temp_dir, output_name)
        shutil.rmtree(temp_dir)
        
        return output_path


class MultiChoiceGenerator(H5PGenerator):
    """Generator für Multiple Choice Fragen"""
    
    def create(self, title, questions, output_name=None):
        """
        Erstellt eine Multiple Choice H5P-Datei
        
        Args:
            title: Titel des Quiz
            questions: Liste von Dicts mit:
                - question: Die Frage
                - answers: Liste von Dicts mit:
                    - text: Antworttext
                    - correct: True/False
                    - feedback: Optional, Feedback für diese Antwort
            output_name: Dateiname
        """
        if output_name is None:
            output_name = f"multichoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        temp_dir = Path("/tmp") / f"h5p_{output_name}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        content_dir = temp_dir / "content"
        content_dir.mkdir(exist_ok=True)
        
        h5p_questions = []
        for q in questions:
            answers = []
            for a in q['answers']:
                answers.append({
                    "text": f"<div>{a['text']}</div>",
                    "correct": a.get('correct', False),
                    "tpisTp": a.get('feedback', '')
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
                        "correctText": "Richtig!",
                        "incorrectText": "Falsch!",
                        "shouldCheck": "Sollte ausgewählt sein",
                        "shouldNotCheck": "Sollte nicht ausgewählt sein",
                        "noInput": "Bitte antworte bevor du die Lösung siehst",
                        "a11yCheck": "Antworten prüfen.",
                        "a11yShowSolution": "Lösung anzeigen.",
                        "a11yRetry": "Quiz wiederholen."
                    },
                    "confirmCheck": {
                        "header": "Fertig?",
                        "body": "Bist du sicher?",
                        "cancelLabel": "Abbrechen",
                        "confirmLabel": "Bestätigen"
                    },
                    "confirmRetry": {
                        "header": "Nochmal?",
                        "body": "Möchtest du es nochmal versuchen?",
                        "cancelLabel": "Abbrechen",
                        "confirmLabel": "Bestätigen"
                    }
                },
                "library": "H5P.MultiChoice 1.16",
                "subContentId": f"mc-{len(h5p_questions)}"
            })
        
        content = {
            "introPage": {
                "showIntroPage": True,
                "title": title,
                "introduction": "<p>Beantworte die folgenden Fragen.</p>"
            },
            "progressType": "dots",
            "passPercentage": 60,
            "questions": h5p_questions,
            "texts": {
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
            },
            "endGame": {
                "showResultPage": True,
                "showSolutionButton": True,
                "showRetryButton": True,
                "noResultMessage": "Quiz beendet",
                "message": "Du hast @score von @total Punkten erreicht.",
                "successGreeting": "Gratulation!",
                "successComment": "Du hast das Quiz bestanden!",
                "failGreeting": "Schade!",
                "failComment": "Versuche es nochmal.",
                "solutionButtonText": "Lösung anzeigen",
                "retryButtonText": "Nochmal versuchen",
                "finishButtonText": "Fertig"
            },
            "override": {
                "showSolutionButton": "on",
                "retryButton": "on"
            }
        }
        
        with open(content_dir / "content.json", 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        h5p_meta = {
            "title": title,
            "language": "de",
            "mainLibrary": "H5P.QuestionSet",
            "embedTypes": ["iframe"],
            "license": "CC BY",
            "preloadedDependencies": [
                {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20},
                {"machineName": "H5P.MultiChoice", "majorVersion": 1, "minorVersion": 16}
            ]
        }
        
        with open(temp_dir / "h5p.json", 'w', encoding='utf-8') as f:
            json.dump(h5p_meta, f, ensure_ascii=False, indent=2)
        
        output_path = self.package_h5p(temp_dir, output_name)
        shutil.rmtree(temp_dir)
        
        return output_path


class DragDropGenerator(H5PGenerator):
    """Generator für Drag and Drop Zuordnungsaufgaben"""
    
    def create(self, title, task_description, dropzones, draggables, output_name=None):
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
        """
        if output_name is None:
            output_name = f"dragdrop_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        temp_dir = Path("/tmp") / f"h5p_{output_name}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        content_dir = temp_dir / "content"
        content_dir.mkdir(exist_ok=True)
        
        # Dropzones erstellen
        h5p_dropzones = []
        for i, dz in enumerate(dropzones):
            h5p_dropzones.append({
                "x": 20 + (i * 22),
                "y": 60,
                "width": 20,
                "height": 30,
                "correctElements": [],
                "showLabel": True,
                "backgroundOpacity": 100,
                "tipsAndFeedback": {"tip": ""},
                "single": False,
                "autoAlign": True,
                "label": f"<div>{dz}</div>"
            })
        
        # Draggables erstellen und Dropzones zuweisen
        h5p_draggables = []
        for i, drag in enumerate(draggables):
            h5p_draggables.append({
                "x": 10 + ((i % 4) * 22),
                "y": 5 + ((i // 4) * 12),
                "width": 20,
                "height": 10,
                "dropZones": [str(drag['dropzone'])],
                "type": {
                    "library": "H5P.AdvancedText 1.1",
                    "params": {"text": f"<p>{drag['text']}</p>"}
                },
                "backgroundOpacity": 100,
                "multiple": False
            })
            h5p_dropzones[drag['dropzone']]['correctElements'].append(str(i))
        
        content = {
            "scoreShow": "Punkte anzeigen",
            "tryAgain": "Nochmal",
            "scoreExplanation": "Richtige Zuordnungen geben Punkte.",
            "question": {
                "settings": {"size": {"width": 620, "height": 400}},
                "task": {
                    "elements": h5p_draggables,
                    "dropZones": h5p_dropzones
                }
            },
            "overallFeedback": [
                {"from": 0, "to": 50, "feedback": "Versuche es nochmal!"},
                {"from": 51, "to": 80, "feedback": "Gut gemacht!"},
                {"from": 81, "to": 100, "feedback": "Ausgezeichnet!"}
            ],
            "behaviour": {
                "enableRetry": True,
                "enableCheckButton": True,
                "showSolutionsRequiresInput": True,
                "singlePoint": False,
                "applyPenalties": False,
                "enableScoreExplanation": True,
                "dropZoneHighlighting": "dragging",
                "autoAlignSpacing": 2,
                "enableFullScreen": False,
                "showScorePoints": True,
                "showTitle": True
            },
            "localize": {"fullscreen": "Vollbild", "exitFullscreen": "Vollbild beenden"},
            "grabbablePrefix": "Ziehbares Element {num}.",
            "grabbableSuffix": "Abgelegt in Dropzone {num}.",
            "dropzonePrefix": "Dropzone {num}.",
            "noDropzone": "Keine Dropzone.",
            "tipLabel": "Tipps anzeigen",
            "tipAvailable": "Tipp verfügbar",
            "correctAnswer": "Richtige Antwort",
            "wrongAnswer": "Falsche Antwort",
            "feedbackHeader": "Feedback",
            "scoreBarLabel": "Du hast :num von :total Punkten erreicht",
            "scoreExplanationButtonLabel": "Punkteberechnung anzeigen",
            "a11yCheck": "Antworten überprüfen.",
            "a11yRetry": "Quiz wiederholen.",
            "submit": "Absenden",
            "a11yShowSolution": "Lösung anzeigen.",
            "showSolution": "Lösung anzeigen"
        }
        
        with open(content_dir / "content.json", 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        h5p_meta = {
            "title": title,
            "language": "de",
            "mainLibrary": "H5P.DragQuestion",
            "embedTypes": ["iframe"],
            "license": "CC BY",
            "preloadedDependencies": [
                {"machineName": "H5P.DragQuestion", "majorVersion": 1, "minorVersion": 14},
                {"machineName": "H5P.AdvancedText", "majorVersion": 1, "minorVersion": 1}
            ]
        }
        
        with open(temp_dir / "h5p.json", 'w', encoding='utf-8') as f:
            json.dump(h5p_meta, f, ensure_ascii=False, indent=2)
        
        output_path = self.package_h5p(temp_dir, output_name)
        shutil.rmtree(temp_dir)
        
        return output_path


# Convenience Funktionen
def create_true_false(title, questions, output_name=None):
    """Schnelle True/False Erstellung"""
    gen = TrueFalseGenerator()
    return gen.create(title, questions, output_name)

def create_fill_blanks(title, text, output_name=None):
    """Schnelle Fill in Blanks Erstellung"""
    gen = FillInBlanksGenerator()
    return gen.create(title, text, output_name)

def create_multi_choice(title, questions, output_name=None):
    """Schnelle Multiple Choice Erstellung"""
    gen = MultiChoiceGenerator()
    return gen.create(title, questions, output_name)

def create_drag_drop(title, task, dropzones, draggables, output_name=None):
    """Schnelle Drag & Drop Erstellung"""
    gen = DragDropGenerator()
    return gen.create(title, task, dropzones, draggables, output_name)


if __name__ == "__main__":
    # Test
    print("H5P Generator - Test")
    print("=" * 40)
    
    # True/False Test
    tf_questions = [
        {
            "text": "Python ist eine Programmiersprache.",
            "correct": True,
            "feedback_correct": "Richtig!",
            "feedback_wrong": "Doch, Python ist eine Sprache."
        }
    ]
    path = create_true_false("Test Quiz", tf_questions, "test-truefalse")
    print(f"✓ True/False: {path}")
    
    # Fill in Blanks Test
    blanks = "<p>Die Hauptstadt von Deutschland ist *Berlin*.</p>"
    path = create_fill_blanks("Geo Test", blanks, "test-blanks")
    print(f"✓ Fill in Blanks: {path}")
    
    print("\n✅ Tests erfolgreich!")
