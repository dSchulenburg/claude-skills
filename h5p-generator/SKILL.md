---
name: h5p-generator
description: Generate H5P interactive content files (.h5p) programmatically using Python. Supports 16 content types, 4 container types, visual verification, and BS:WI branding. Use for quizzes, flashcards, drag-and-drop, interactive books, course presentations, essays, branching scenarios, and interactive videos.
license: MIT
---

# H5P Generator v3.1

Generate .h5p files directly from Python with robust error handling, container types, visual verification, and customizable branding.

## Supported Content Types (16)

| Type | Function | Use Case |
|------|----------|----------|
| **True/False** | `create_true_false()` | Wahr/Falsch Quizze |
| **Multiple Choice** | `create_multi_choice()` | MC-Fragen mit 2+ Optionen |
| **Fill in Blanks** | `create_fill_blanks()` | Lueckentexte mit `*Luecke*` |
| **Drag and Drop** | `create_drag_drop()` | Zuordnungsaufgaben (Kategorien) |
| **Drag the Words** | `create_drag_text()` | Woerter in Luecken ziehen |
| **Single Choice** | `create_single_choice()` | Schnelle Single-Choice |
| **Flashcards** | `create_flashcards()` | Lernkarten (Dialog Cards) |
| **Mark Words** | `create_mark_words()` | Woerter im Text markieren |
| **Summary** | `create_summary()` | Zusammenfassungen |
| **Accordion** | `create_accordion()` | Aufklappbare Abschnitte |
| **Timeline** | `create_timeline()` | Zeitleisten mit Events |
| **Memory Game** | `create_memory_game()` | Memory (benoetigt Bilder) |
| **Essay** | `create_essay()` | Freitext mit Keyword-Bewertung (v3.1) |
| **Sort Paragraphs** | `create_sort_paragraphs()` | Absaetze sortieren (v3.1) |
| **Branching Scenario** | `create_branching_scenario()` | Verzweigte Lernszenarien (v3.1) |
| **Interactive Video** | `create_interactive_video()` | Videos mit eingebetteten Aufgaben (v3.1) |

## Container Types (4) - NEU v3.0

| Container | Function | Use Case |
|-----------|----------|----------|
| **Column** | `create_column()` | 2-5 Elemente vertikal |
| **QuestionSet** | `create_question_set()` | Quiz-Sequenz mit Auswertung |
| **CoursePresentation** | `create_course_presentation()` | Slide-basierte Praesentation mit eingebetteten H5P-Typen |
| **InteractiveBook** | `create_interactive_book()` | Kapitel-basiertes Buch (Kapitel = H5P.Column Wrapper) |

### Container-Empfehlung

| Situation | Container |
|-----------|-----------|
| 2-3 Quiz-Typen | QuestionSet |
| 3-5 gemischte Typen | Column |
| 4+ gemischte mit Struktur | InteractiveBook |
| Praesentationsformat | CoursePresentation |

### Interactive Book (v3.0)

Jedes Kapitel ist ein `H5P.Column 1.18` Wrapper - alle 35+ Column-kompatiblen Typen funktionieren:

```python
from h5p_containers import create_interactive_book

result = create_interactive_book(
    "Scrum-Buch",
    chapters=[
        {
            "title": "Kapitel 1: Rollen",
            "elements": [
                {"library": "H5P.AdvancedText 1.1", "params": {"text": "<h2>Rollen</h2>"}},
                {"library": "H5P.Dialogcards 1.9", "params": {"dialogs": [...]}},
                {"library": "H5P.MultiChoice 1.16", "params": {"question": "...", "answers": [...]}}
            ]
        }
    ],
    cover_description="Ein Buch ueber Scrum",
    base_color="#003366"  # BS:WI Navy
)
```

### Course Presentation (v3.0)

Template-System mit eingebetteten H5P-Typen:

```python
from h5p_containers import create_course_presentation

result = create_course_presentation(
    "Scrum-Praesentation",
    slides=[
        # Layout: title_only (Intro)
        {"layout": "title_only", "title": "Einfuehrung"},

        # Layout: text_content
        {"layout": "text_content", "title": "Was ist Scrum?", "content": "<p>...</p>"},

        # Layout: interactive (Text + H5P-Element)
        {
            "layout": "interactive",
            "title": "Quiz",
            "content": "<p>Beantworte:</p>",
            "interactive": {
                "library": "H5P.TrueFalse 1.8",
                "params": {"question": "<p>Scrum hat 3 Rollen.</p>", "correct": "true"}
            }
        },

        # Layout: interactive_full (vollflaechig)
        {
            "layout": "interactive_full",
            "title": "Zuordnung",
            "interactive": {"library": "H5P.DragText 1.10", "params": {...}}
        },

        # Layout: split (links Text, rechts Interaktion)
        {"layout": "split", "title": "Uebung", "content": "<p>Info</p>", "interactive": {...}}
    ]
)
```

**Verfuegbare Slide-Layouts:** `title_only`, `text_content`, `interactive`, `interactive_full`, `split`

## BS:WI Design (v3.0)

```python
from h5p_system import H5PSystem

# BS:WI-Branding wird automatisch angewendet
system = H5PSystem(brand='bswi')
result = system.generate_from_text(...)
```

**Farben:**
- `#003366` Navy: Buttons, Navigation, Ueberschriften
- `#00A3E0` Lightblue: Links, Fortschrittsbalken, Akzente
- `#B5E505` Yellow: Erfolg, Highlights
- `#333333` Gray: Textfarbe

**Was passiert:** CSS wird als `<style>` Block in H5P-Inhalte injiziert. InteractiveBook bekommt Navy-Navigation und gestylte Kapitel-Header.

## Visuelle Verifikation (v3.0)

```python
from h5p_system import H5PSystem

system = H5PSystem(brand='bswi')

# Generieren + automatisch verifizieren
result = system.generate_and_verify(lernmaterial, content_items)
# result.statistics['verification'] enthaelt Screenshots + Check-Ergebnisse

# Einzelne Datei verifizieren
from visual_verify import verify_h5p
vr = verify_h5p("path/to/file.h5p")
print(vr.summary())
# Screenshot: path/to/file_verify.png
```

**Checks:**
- Content sichtbar (nicht leer)?
- Interaktive Elemente vorhanden (Buttons)?
- Keine Fehlermeldungen?
- Keine ueberlappenden Elemente (CoursePresentation)?
- Navigation vorhanden (InteractiveBook)?

**Voraussetzung:** Node.js + `npm install` in `scripts/` (puppeteer-core, zip-lib)

## Unified API (H5PSystem)

```python
from h5p_system import H5PSystem

system = H5PSystem(brand='bswi')

# HIGH-LEVEL: Freitext rein, H5P raus
result = system.generate_from_text(lernmaterial, content_items)

# HIGH-LEVEL: Text-zu-Quiz
result = system.generate_from_questions("Was ist X? - A [correct] - B - C")

# HIGH-LEVEL: Generieren + Verifizieren
result = system.generate_and_verify(lernmaterial, content_items, combine=True)

# MID-LEVEL: Strukturierte Elemente
result = system.generate_elements([
    {'type': 'flashcards', 'title': 'Vokabeln', 'cards': [...]},
    {'type': 'drag_drop', 'title': 'Zuordnung', 'dropzones': [...], 'draggables': [...]}
])

# LOW-LEVEL: Direkte Agent-Nutzung
system.quiz_agent.generate('multi_choice', title='Quiz', questions=[...])
```

## Quick Start

```python
from h5p_generator import create_true_false, THEMES

result = create_true_false(
    "Python Basics",
    [
        {"text": "Python ist eine Programmiersprache.", "correct": True},
        {"text": "Python wurde 2020 erfunden.", "correct": False}
    ],
    "python-quiz",
    style=THEMES['education']
)

if result.success:
    print(f"Erstellt: {result.path}")
```

## Content Types im Detail

### True/False
```python
questions = [
    {"text": "Die Erde ist rund.", "correct": True},
    {"text": "HTML ist eine Programmiersprache.", "correct": False}
]
create_true_false("Quiz", questions, "quiz")
```

### Multiple Choice
```python
questions = [
    {
        "question": "Was ist die Hauptstadt?",
        "answers": [
            {"text": "Berlin", "correct": True},
            {"text": "Hamburg", "correct": False}
        ]
    }
]
create_multi_choice("Staedte", questions, "staedte")
```

### Fill in Blanks
```python
text = "<p>Die Hauptstadt ist *Berlin*. Die Waehrung ist der *Euro/EUR*.</p>"
create_fill_blanks("Deutschland", text, "de-luecken")
```

### Drag and Drop
```python
dropzones = ["Obst", "Gemuese"]
draggables = [
    {"text": "Apfel", "dropzone": 0},
    {"text": "Karotte", "dropzone": 1}
]
create_drag_drop("Lebensmittel", "Ordne zu!", dropzones, draggables, "food")
```

### Drag the Words
```python
text = "In *Scrum* arbeitet das Team in *Sprints*."
create_drag_text("Agile", text, "agile-drag", task="Ziehe die Begriffe.")
```

### Flashcards
```python
cards = [
    {"front": "Haus", "back": "house", "tip": "Beginnt mit H"},
    {"front": "Auto", "back": "car"}
]
create_flashcards("Vokabeln", cards, "vokabeln")
```

### Accordion
```python
panels = [
    {"title": "Einfuehrung", "content": "Dies ist..."},
    {"title": "Hauptteil", "content": "Der Hauptteil..."}
]
create_accordion("Lerneinheit", panels, "lerneinheit")
```

### Essay (v3.1)
```python
keywords = [
    {"keyword": "Product Owner", "alternatives": ["PO"], "points": 2},
    {"keyword": "Scrum Master", "alternatives": ["SM"]},
    {"keyword": "Development Team"}
]
create_essay("Scrum-Rollen", "Erklaere die drei Scrum-Rollen.", keywords)
```

### Sort Paragraphs (v3.1)
```python
# Reihenfolge = korrekte Reihenfolge (H5P shuffelt automatisch)
paragraphs = [
    "Sprint Planning: Das Team plant die Arbeit.",
    "Daily Scrum: Taegliches 15-Minuten-Meeting.",
    "Sprint Review: Ergebnisse praesentieren.",
    "Retrospektive: Prozess reflektieren."
]
create_sort_paragraphs("Sprint-Ablauf", paragraphs)
```

### Branching Scenario (v3.1)
```python
nodes = [
    {"type": "text", "title": "Start", "content": "<p>Ein Kunde kommt.</p>", "next": 1},
    {"type": "question", "question": "Wie reagieren Sie?",
     "alternatives": [
         {"text": "Freundlich begruessen", "next": 2},
         {"text": "Ignorieren", "next": 3}
     ]},
    {"type": "text", "title": "Gut", "content": "<p>Kunde zufrieden!</p>", "next": -1},
    {"type": "text", "title": "Schlecht", "content": "<p>Kunde geht.</p>", "next": -1}
]
create_branching_scenario("Kundengespraech", nodes)
```
- `next: -1` = Ende (End-Screen wird automatisch generiert)
- Mindestens 2 Nodes, empfohlen mind. 1 Question-Node

### Interactive Video (v3.1)
```python
interactions = [
    {
        "type": "multi_choice",
        "time_from": 30, "time_to": 40,
        "pause": True,
        "params": {
            "question": "<p>Was ist Python?</p>",
            "answers": [
                {"text": "<p>Programmiersprache</p>", "correct": True},
                {"text": "<p>Schlange</p>", "correct": False}
            ]
        }
    }
]
create_interactive_video("Tutorial", "https://youtube.com/watch?v=...", interactions)
```
- URL-only: YouTube oder direkte MP4-URL (kein Datei-Upload)
- 8 Interaktionstypen: multi_choice, true_false, fill_blanks, drag_text, mark_words, single_choice, summary, text

## Brand Presets

| Preset | Beschreibung |
|--------|--------------|
| `bswi` | BS:WI Hamburg (Navy, Lightblue, Yellow) |
| `default` | Standard (Blau) |
| `dark` | Dunkler Hintergrund |
| `education` | Gruene Akzente |
| `professional` | Business-Look |
| `minimal` | Minimalistisch |
| `accessible` | High Contrast |

## Output

- Dateien in `/home/claude/h5p-output/`
- Format: `{name}.h5p` (ZIP-Archiv)
- Import: Moodle H5P Aktivitaet, WordPress, Lumi

## Changelog

### v3.1 (2026-03-02)
- **Essay:** Freitext-Aufgaben mit Keyword-basierter Bewertung (H5P.Essay 1.5)
- **Sort Paragraphs:** Absaetze in richtige Reihenfolge bringen (H5P.SortParagraphs 1.3)
- **Branching Scenario:** Verzweigte Lernszenarien mit Text- und Frage-Nodes (H5P.BranchingScenario 1.8)
- **Interactive Video:** Videos mit eingebetteten Aufgaben, YouTube + MP4 (H5P.InteractiveVideo 1.27)
- **ScenarioAgent + MediaAgent:** Neue Sub-Agents fuer Szenarien und Video-Inhalte
- **QuizAgent:** Erweitert um Essay und SortParagraphs
- **16 Content-Types** (vorher 12), 5 Sub-Agents (vorher 3)

### v3.0 (2026-03-02)
- **InteractiveBook:** Kapitel nutzen H5P.Column 1.18 Wrapper (korrekte H5P-Struktur)
- **InteractiveBook:** 35+ eingebettete Typen (statt 5), baseColor, progressAuto
- **CoursePresentation:** Template-System (title_only, text_content, interactive, split)
- **CoursePresentation:** Eingebettete H5P-Typen (MultiChoice, TrueFalse, DragText, etc.)
- **CoursePresentation:** UUID-basierte subContentIds
- **BS:WI Design:** CSS-Injection in H5P-Packages (Navy Buttons, Lightblue Progress, Yellow Erfolg)
- **BS:WI Design:** Gestylte Kapitel-Header in InteractiveBook
- **Visuelle Verifikation:** Puppeteer-basierte Screenshots + automatische Checks
- **generate_and_verify():** Generierung + Verifikation in einem Schritt

### v2.3 (2026-01-26)
- Text-zu-Quiz mit Distractor-Generator

### v2.2 (2026-01-24)
- Drag the Words, Timeline, Memory Game (12 Content-Types gesamt)

---

*Version 3.1 - Essay, SortParagraphs, BranchingScenario, InteractiveVideo*
