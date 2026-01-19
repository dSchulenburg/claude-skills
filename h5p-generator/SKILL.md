---
name: h5p-generator
description: Generate H5P interactive content files (.h5p) programmatically using Python. Supports 9 content types with error handling, styling themes, and batch creation. Use for quizzes, flashcards, drag-and-drop, and more.
license: MIT
agent: Education
---

# H5P Generator v2.0

Generate .h5p files directly from Python with robust error handling and customizable styling.

## Supported Content Types (9)

| Type | Function | Use Case |
|------|----------|----------|
| **True/False** | `create_true_false()` | Wahr/Falsch Quizze |
| **Multiple Choice** | `create_multi_choice()` | MC-Fragen mit 2+ Optionen |
| **Fill in Blanks** | `create_fill_blanks()` | Lückentexte mit `*Lücke*` |
| **Drag and Drop** | `create_drag_drop()` | Zuordnungsaufgaben |
| **Single Choice** | `create_single_choice()` | Schnelle Single-Choice |
| **Flashcards** | `create_flashcards()` | Lernkarten (Dialog Cards) |
| **Mark Words** | `create_mark_words()` | Wörter im Text markieren |
| **Summary** | `create_summary()` | Zusammenfassungen |
| **Accordion** | `create_accordion()` | Aufklappbare Abschnitte |

## Quick Start

```python
from h5p_generator import (
    create_true_false, create_multi_choice, create_fill_blanks,
    create_drag_drop, create_single_choice, create_flashcards,
    create_mark_words, create_summary, create_accordion,
    THEMES, H5PStyle
)

# Mit Education-Theme
style = THEMES['education']

# True/False Quiz
result = create_true_false(
    "Python Basics",
    [
        {"text": "Python ist eine Programmiersprache.", "correct": True},
        {"text": "Python wurde 2020 erfunden.", "correct": False}
    ],
    "python-quiz",
    style=style
)

if result.success:
    print(f"Erstellt: {result.path}")
else:
    print(f"Fehler: {result.error}")
```

## Error Handling

Alle Funktionen geben ein `H5PResult` zurück:

```python
@dataclass
class H5PResult:
    success: bool           # True = OK, False = Fehler
    path: Path | None       # Pfad zur .h5p Datei
    error: str | None       # Fehlermeldung
    content_type: str       # z.B. "TrueFalse"
    title: str              # Titel des Inhalts
```

**Beispiel Fehlerbehandlung:**

```python
result = create_true_false("Test", [])  # Leere Fragen-Liste

if not result.success:
    print(f"Fehler bei {result.content_type}: {result.error}")
    # Output: "Fehler bei TrueFalse: Fragen muss mindestens 1 Element(e) enthalten"
```

## Styling & Themes

Vordefinierte Themes:

| Theme | Beschreibung |
|-------|--------------|
| `default` | Blaue Akzente, neutral |
| `dark` | Dunkler Hintergrund |
| `education` | Grüne Akzente, Schüler-freundlich |
| `professional` | Business-Look |

```python
from h5p_generator import THEMES, H5PStyle

# Theme verwenden
style = THEMES['education']

# Eigenes Theme erstellen
my_style = H5PStyle(
    primary_color="#ff6600",
    feedback_correct="Super gemacht!",
    feedback_wrong="Versuch es nochmal!",
    pass_percentage=70
)
```

## Content Types im Detail

### 1. True/False

```python
questions = [
    {
        "text": "Die Erde ist rund.",
        "correct": True,
        "feedback_correct": "Richtig!",  # Optional
        "feedback_wrong": "Leider falsch."  # Optional
    }
]
create_true_false("Geo Quiz", questions, "geo-quiz")
```

### 2. Multiple Choice

```python
questions = [
    {
        "question": "Was ist die Hauptstadt von Deutschland?",
        "answers": [
            {"text": "Berlin", "correct": True},
            {"text": "Hamburg", "correct": False},
            {"text": "München", "correct": False},
            {"text": "Köln", "correct": False}
        ]
    }
]
create_multi_choice("Städte Quiz", questions, "staedte")
```

### 3. Fill in Blanks (Lückentext)

Lücken mit `*Sternchen*` markieren. Mehrere Antworten mit `/`:

```python
text = "<p>Die Hauptstadt ist *Berlin*. Die Währung ist der *Euro/EUR*.</p>"
create_fill_blanks("Deutschland", text, "de-luecken")
```

### 4. Drag and Drop

```python
dropzones = ["Obst", "Gemüse", "Fleisch"]
draggables = [
    {"text": "Apfel", "dropzone": 0},
    {"text": "Karotte", "dropzone": 1},
    {"text": "Steak", "dropzone": 2},
    {"text": "Banane", "dropzone": 0}
]
create_drag_drop("Lebensmittel", "Ordne zu!", dropzones, draggables, "food")
```

### 5. Single Choice Set (schnell)

Erste Antwort ist immer korrekt:

```python
questions = [
    {
        "question": "Was ist 2 + 2?",
        "answers": ["4", "3", "5", "6"]  # Erste = korrekt
    }
]
create_single_choice("Mathe", questions, "mathe-quick")
```

### 6. Flashcards (Lernkarten)

```python
cards = [
    {"front": "Haus", "back": "house", "tip": "Beginnt mit H"},
    {"front": "Auto", "back": "car"},
    {"front": "Baum", "back": "tree"}
]
create_flashcards("Englisch Vokabeln", cards, "vokabeln")
```

### 7. Mark the Words

```python
text = "Berlin ist die *Hauptstadt* von *Deutschland*. Paris liegt in Frankreich."
create_mark_words(
    "Geografie",
    text,
    "geo-mark",
    task="Markiere alle Begriffe, die zu Deutschland gehören."
)
```

### 8. Summary

Erste Aussage ist immer korrekt:

```python
items = [
    {
        "statements": [
            "Python ist interpretiert",  # Korrekt
            "Python ist kompiliert",
            "Python ist assembler"
        ]
    },
    {
        "statements": [
            "Python hat dynamische Typisierung",  # Korrekt
            "Python hat statische Typisierung"
        ]
    }
]
create_summary("Python Facts", items, "python-summary")
```

### 9. Accordion

```python
panels = [
    {"title": "Einführung", "content": "Dies ist die Einführung..."},
    {"title": "Hauptteil", "content": "Der Hauptteil behandelt..."},
    {"title": "Fazit", "content": "Zusammenfassend lässt sich sagen..."}
]
create_accordion("Lerneinheit", panels, "lerneinheit")
```

## Batch-Erstellung

Mehrere H5P-Dateien auf einmal erstellen:

```python
from h5p_generator import batch_create, THEMES

content = [
    {
        "type": "true_false",
        "title": "Quiz 1",
        "questions": [{"text": "Test", "correct": True}]
    },
    {
        "type": "flashcards",
        "title": "Vokabeln",
        "cards": [{"front": "Hallo", "back": "Hello"}]
    },
    {
        "type": "fill_blanks",
        "title": "Lücken",
        "text": "<p>Die Antwort ist *42*.</p>"
    }
]

results = batch_create(content, style=THEMES['education'])

for r in results:
    print(r)  # ✓ TrueFalse: /path/to/quiz1.h5p
```

## Output

- Dateien werden in `/home/claude/h5p-output/` erstellt
- Format: `{name}.h5p` (ZIP-Archiv)
- Import: WordPress Media → Add New, oder Moodle H5P Aktivität

## Validierung

Der Generator validiert automatisch:
- Nicht-leere Titel
- Mindestanzahl an Fragen/Karten
- Korrekte Antworten vorhanden
- Gültige Dropzone-Indizes
- Lücken im Text vorhanden

Bei Fehlern wird ein `H5PResult` mit `success=False` und Fehlerbeschreibung zurückgegeben.

## Bundled Script

Der vollständige Generator: `scripts/h5p_generator.py`

## Limitations

- **Image Hotspots**: Nicht unterstützt (Web-Editor nutzen)
- **Branching Scenario**: Zu komplex
- **Interactive Video**: Benötigt Video-Dateien
- **Course Presentation**: Zu komplex

Für diese: H5P in WordPress/Moodle direkt erstellen.

---

*Version 2.0 - Mit Fehlerbehandlung, Themes, und 5 neuen Content-Types*
