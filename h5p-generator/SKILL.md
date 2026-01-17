---
name: h5p-generator
description: Generate H5P interactive content files (.h5p) programmatically using Python. Use when users want to create H5P quizzes, drag-and-drop exercises, fill-in-the-blanks, or multiple choice questions without using a web editor. Supports batch creation of H5P content for Moodle, WordPress, or any H5P-compatible LMS.
---

# H5P Generator

Generate .h5p files directly from Python without web editors.

## Supported Content Types

| Type | Function | Use Case |
|------|----------|----------|
| **True/False** | `create_true_false()` | Wahr/Falsch Quizze |
| **Multiple Choice** | `create_multi_choice()` | MC-Fragen mit 4+ Optionen |
| **Fill in Blanks** | `create_fill_blanks()` | Lückentexte mit `*Lücke*` Syntax |
| **Drag and Drop** | `create_drag_drop()` | Zuordnungsaufgaben |

## Quick Start

```python
from h5p_generator import create_true_false, create_fill_blanks, create_multi_choice, create_drag_drop

# True/False Quiz
questions = [
    {
        "text": "Python ist eine Programmiersprache.",
        "correct": True,
        "feedback_correct": "Richtig!",
        "feedback_wrong": "Doch, Python ist eine Sprache."
    }
]
create_true_false("Mein Quiz", questions, "quiz-name")

# Fill in Blanks - Lücken mit *Sternchen* markieren
text = "<p>Die Hauptstadt von Deutschland ist *Berlin*.</p>"
create_fill_blanks("Geografie Test", text, "geo-test")

# Multiple Choice
mc_questions = [
    {
        "question": "Welche Farbe hat der Himmel?",
        "answers": [
            {"text": "Blau", "correct": True},
            {"text": "Grün", "correct": False},
            {"text": "Rot", "correct": False}
        ]
    }
]
create_multi_choice("Farben Quiz", mc_questions, "farben")

# Drag and Drop
dropzones = ["Obst", "Gemüse"]
draggables = [
    {"text": "Apfel", "dropzone": 0},
    {"text": "Karotte", "dropzone": 1}
]
create_drag_drop("Sortieren", "Ordne zu!", dropzones, draggables, "sortieren")
```

## Output

- Dateien werden in `/home/claude/h5p-output/` erstellt
- Format: `{name}.h5p` (ZIP-Archiv)
- Import in WordPress: Media → Add New → .h5p hochladen
- Import in Moodle: Aktivität → H5P → Datei hochladen

## Fill in Blanks Syntax

Lücken mit Sternchen markieren. Mehrere Antworten mit Schrägstrich trennen:

```
Die Einheit ist *µmol/m²/s/Mikromol*.
```

Akzeptiert: µmol/m²/s ODER Mikromol

## Advanced Usage

Für komplexere Anpassungen die Klassen direkt verwenden:

```python
from h5p_generator import TrueFalseGenerator, MultiChoiceGenerator

gen = TrueFalseGenerator(output_dir="/custom/path")
gen.create(title, questions, output_name)
```

## Bundled Script

Der vollständige Generator ist unter `scripts/h5p_generator.py` verfügbar.

## Limitations

- **Image Hotspots**: Nicht unterstützt (Bilder müssen eingebettet werden → Web-Editor nutzen)
- **Branching Scenario**: Zu komplex für programmatische Erstellung
- **Interactive Video**: Benötigt Video-Dateien

Für diese Content-Types: H5P in WordPress/Moodle direkt erstellen.
