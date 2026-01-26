---
name: h5p-generator
description: Generate H5P interactive content files (.h5p) programmatically using Python. Supports 9 content types with error handling, styling themes, and batch creation. Use for quizzes, flashcards, drag-and-drop, and more.
license: MIT
agent: Education
---

# H5P Generator v2.3

Generate .h5p files directly from Python with robust error handling and customizable styling.

## Supported Content Types (12)

| Type | Function | Use Case |
|------|----------|----------|
| **True/False** | `create_true_false()` | Wahr/Falsch Quizze |
| **Multiple Choice** | `create_multi_choice()` | MC-Fragen mit 2+ Optionen |
| **Fill in Blanks** | `create_fill_blanks()` | Lückentexte mit `*Lücke*` |
| **Drag and Drop** | `create_drag_drop()` | Zuordnungsaufgaben (Kategorien) |
| **Drag the Words** | `create_drag_text()` | Wörter in Lücken ziehen |
| **Single Choice** | `create_single_choice()` | Schnelle Single-Choice |
| **Flashcards** | `create_flashcards()` | Lernkarten (Dialog Cards) |
| **Mark Words** | `create_mark_words()` | Wörter im Text markieren |
| **Summary** | `create_summary()` | Zusammenfassungen |
| **Accordion** | `create_accordion()` | Aufklappbare Abschnitte |
| **Timeline** | `create_timeline()` | Zeitleisten mit Events |
| **Memory Game** | `create_memory_game()` | Memory (benötigt Bilder) |

## Entscheidungsmatrix (Wann welcher Typ?)

Siehe `references/templates/decision-matrix.md` für die vollständige Logik.

| Lernziel | Operator | H5P-Typ |
|----------|----------|---------|
| Begriffe lernen | nennen | Flashcards |
| Fakten prüfen | beschreiben | True-False |
| Kategorien | zuordnen | Drag-and-Drop |
| Lücken füllen | ergänzen | Fill-in-Blanks oder Drag-Text |
| Chronologie | ordnen | Timeline |
| Zusammenhänge | erklären | Accordion |
| Optionen | bewerten | Branching (manuell) |

**Didaktische Regel:** Gamification-Typen (Flashcards, Drag&Drop, Memory) nur unterstützend einsetzen, nicht als Hauptlernform auf IHK/Abitur-Niveau.

## Agent Workflow (NEU v2.2)

Der H5P Agent automatisiert die Content-Type-Wahl und lernt aus Feedback:

```python
from agent_workflow import H5PAgent

agent = H5PAgent()

# Automatische Entscheidung
decision = agent.decide_content_type("Ordne die Begriffe zu")
# → drag_drop (80% Konfidenz)

# Generieren mit Validierung
result, issues = agent.generate_with_validation('drag_drop', ...)

# Preview und Feedback
agent.preview(result.path)
agent.save_as_template(result, "name")
```

Siehe `AGENT_WORKFLOW.md` für vollständige Dokumentation.

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

### 10. Drag the Words (NEU v2.2)

Ähnlich wie Fill-in-Blanks, aber Wörter werden gezogen statt getippt:

```python
text = "In *Scrum* arbeitet das Team in *Sprints*. Der *Product Owner* priorisiert."
create_drag_text(
    "Agile Begriffe",
    text,
    "agile-dragtext",
    task="Ziehe die Begriffe an die richtige Stelle."
)
```

### 11. Timeline (NEU v2.2)

Zeitleiste mit chronologischen Events:

```python
events = [
    {"headline": "ARPANET", "start_date": "1969", "text": "Erstes Netzwerk"},
    {"headline": "World Wide Web", "start_date": "1991", "text": "Tim Berners-Lee"},
    {"headline": "Google", "start_date": "1998-09", "text": "Suchmaschine gestartet"},
]
create_timeline("Internet-Geschichte", events, "internet-timeline")
```

Datumsformate: `"2020"`, `"2020-03"`, oder `"2020-03-15"`

### 12. Memory Game (NEU v2.2)

Memory-Spiel (benötigt Bilder für volle Funktion):

```python
cards = [
    {"description": "Scrum Master", "image": "https://example.com/sm.jpg"},
    {"description": "Product Owner", "image": "https://example.com/po.jpg"},
]
create_memory_game("Scrum-Rollen Memory", cards, "scrum-memory")
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

## Template-Bibliothek

Validierte JSON-Templates für konsistente Ergebnisse:

| Datei | Beschreibung |
|-------|--------------|
| `references/templates/decision-matrix.md` | Wann welcher Content-Type |
| `references/templates/dragdrop-working.json` | Funktionierende Drag&Drop-Werte |
| `references/templates/all-types.json` | JSON-Strukturen aller Typen |
| `references/h5p-json-structure.md` | Technische Referenz |

## Beispiel-Bibliothek

Offizielle h5p.org Beispiele in `examples/h5p/`:
- `drag-and-drop-712.h5p` - Drag & Drop Referenz
- `fill-in-the-blanks-837.h5p` - Lückentext
- `dialog-cards-620.h5p` - Flashcards
- `single-choice-set-1515.h5p` - Single Choice
- ... und 30+ weitere

## Limitations

- **Image Hotspots**: Nicht unterstützt (Web-Editor nutzen)
- **Branching Scenario**: Zu komplex (manuell erstellen)
- **Interactive Video**: Benötigt Video-Dateien
- **Course Presentation**: Zu komplex (manuell erstellen)
- **Interactive Book**: Manuell in H5P-Editor erstellen

Für komplexe Typen: H5P in WordPress/Moodle direkt erstellen.

## Text-zu-Quiz (NEU v2.3)

Die einfachste Art, Quizze zu erstellen: Fragen als Freitext eingeben, H5P-Quiz als Output.

### generate_from_questions()

```python
from h5p_system import H5PSystem

system = H5PSystem()

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

# Mit Domain fuer bessere Distraktoren
result = system.generate_from_questions(
    "Die Bilanz zeigt Vermoegen und Kapital.",
    title="Buchfuehrung",
    domain="accounting"  # Generiert passende Distraktoren
)
```

### Unterstuetzte Eingabeformate

| Format | Beispiel | Ergebnis |
|--------|----------|----------|
| **With Answers** | `Was ist X? - A [correct] - B - C` | Multiple Choice |
| **Batch TF** | `--- Q: Aussage A: wahr ---` | True/False |
| **Simple** | `Ein Debitor ist ein Glaeubiger.` | True/False |

### Convenience-Funktion

```python
from h5p_system import quick_quiz_from_text

result = quick_quiz_from_text('''
    Was ist ein Debitor?
    - Ein Schuldner
    - Ein Glaeubiger [correct]
''', title="Quiz", domain="accounting")
```

### Domains fuer Distraktoren

| Domain | Konzepte |
|--------|----------|
| `accounting` | Debitor, Kreditor, Aktiva, Passiva, Soll, Haben, Bilanz, GuV |
| `scrum` | Product Owner, Scrum Master, Sprint, Backlog, Daily, Review |
| `it` | Server, Client, CPU, RAM, Netzwerk, Datenbank, Protokoll |
| `business` | Angebot, Nachfrage, Preis, Gewinn, Verlust, Kosten |

## Changelog

### v2.3 (2026-01-26)
- **Neu:** `generate_from_questions()` - Text-zu-Quiz Funktionalitaet
- **Neu:** `TextParserAgent` - Parst Freitext in strukturierte Fragen
- **Neu:** `DistractorGenerator` - Generiert plausible Falsch-Antworten
- **Neu:** `quick_quiz_from_text()` - Convenience-Funktion
- **Neu:** Domain-Templates fuer accounting, scrum, it, business

### v2.2 (2026-01-24)
- **Neu:** Drag the Words (`create_drag_text()`) - Woerter in Luecken ziehen
- **Neu:** Timeline (`create_timeline()`) - Zeitleisten mit Events
- **Neu:** Memory Game (`create_memory_game()`) - Memory-Spiel
- **Gesamt:** 12 Content-Typen unterstuetzt

### v2.1 (2026-01-24)
- **Fix:** Drag & Drop Positionierung korrigiert (war ausserhalb Canvas)
- **Neu:** Dynamische Draggable-Breite nach Textlaenge
- **Neu:** Entscheidungsmatrix fuer Content-Type-Wahl
- **Neu:** Template-Bibliothek mit validierten JSON-Strukturen
- **Neu:** 33 Beispiel-H5P-Dateien als Referenz

### v2.0
- Fehlerbehandlung mit H5PResult
- Themes und Styling
- 5 neue Content-Types (Single Choice, Flashcards, Mark Words, Summary, Accordion)

---

*Version 2.3 - Text-zu-Quiz mit Distractor-Generator*
