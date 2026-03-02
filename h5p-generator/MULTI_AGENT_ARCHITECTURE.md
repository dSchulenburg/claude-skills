# H5P Multi-Agent Architecture

## Vision

Ein intelligentes System, das aus beliebigen Lernmaterialien (Themen, Arbeitsblätter, Lerneinheiten) automatisch optimale H5P-Inhalte generiert - von einfachen Quizzen bis zu komplexen interaktiven Büchern.

## Architektur-Übersicht

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         ORCHESTRATOR AGENT                               │
│                                                                          │
│  Input: Thema / Arbeitsblatt / Lerneinheit / Dokument                   │
│                                                                          │
│  Phase 1: ANALYSE                                                        │
│  ├── Lernziele extrahieren                                              │
│  ├── Operatoren identifizieren (nennen, zuordnen, erklären...)          │
│  ├── Inhaltsstruktur erkennen (Fakten, Kategorien, Chronologie...)      │
│  └── Komplexität bewerten (einfach → komplex)                           │
│                                                                          │
│  Phase 2: PLANUNG                                                        │
│  ├── Entscheidungsmatrix anwenden                                       │
│  ├── H5P-Typen auswählen (Einzel + Container)                           │
│  ├── Ausführungsplan erstellen                                          │
│  └── Sub-Agents zuweisen                                                │
│                                                                          │
│  Phase 3: KOORDINATION                                                   │
│  ├── Sub-Agents parallel starten                                        │
│  ├── Fortschritt überwachen                                             │
│  ├── Fehler behandeln (Retry, Fallback)                                 │
│  └── Ergebnisse sammeln                                                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            ▼                       ▼                       ▼
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│    QUIZ-AGENT       │  │    CARD-AGENT       │  │    DRAG-AGENT       │
│                     │  │                     │  │                     │
│  Spezialisierung:   │  │  Spezialisierung:   │  │  Spezialisierung:   │
│  • True/False       │  │  • Flashcards       │  │  • Drag & Drop      │
│  • Multiple Choice  │  │  • Accordion        │  │  • Drag the Words   │
│  • Single Choice    │  │  • Timeline         │  │  • Mark the Words   │
│  • Summary          │  │  • Memory Game      │  │  • Fill in Blanks   │
│                     │  │                     │  │                     │
│  Selbst-Korrektur:  │  │  Selbst-Korrektur:  │  │  Selbst-Korrektur:  │
│  • Validierung      │  │  • Validierung      │  │  • Validierung      │
│  • Auto-Retry       │  │  • Auto-Retry       │  │  • Auto-Retry       │
│  • Fallback-Typ     │  │  • Fallback-Typ     │  │  • Fallback-Typ     │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
            │                       │                       │
            └───────────────────────┼───────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          COMBINER AGENT                                  │
│                                                                          │
│  Kombiniert Einzel-Elemente zu komplexen Container-Typen:               │
│                                                                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐          │
│  │ Course          │  │ Column          │  │ Interactive     │          │
│  │ Presentation    │  │                 │  │ Book            │          │
│  │                 │  │                 │  │                 │          │
│  │ Slides mit      │  │ Vertikale       │  │ Kapitel mit     │          │
│  │ eingebetteten   │  │ Anordnung von   │  │ Seiten und      │          │
│  │ H5P-Elementen   │  │ H5P-Elementen   │  │ Unterinhalten   │          │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘          │
│                                                                          │
│  ┌─────────────────┐  ┌─────────────────┐                               │
│  │ Question Set    │  │ Branching       │                               │
│  │                 │  │ Scenario        │                               │
│  │ Sequenz von     │  │                 │                               │
│  │ Quiz-Fragen     │  │ Verzweigte      │                               │
│  │                 │  │ Lernpfade       │                               │
│  └─────────────────┘  └─────────────────┘                               │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │   OUTPUT              │
                        │                       │
                        │   📦 .h5p Datei(en)   │
                        │   📋 Bericht          │
                        │   💾 Template-Update  │
                        └───────────────────────┘
```

---

## Komponenten im Detail

### 1. Orchestrator Agent

**Verantwortung:** Zentrale Steuerung des gesamten Workflows

#### 1.1 Analyse-Phase

```python
class ContentAnalysis:
    """Ergebnis der Inhaltsanalyse"""
    learning_goals: list[str]        # Extrahierte Lernziele
    operators: list[str]             # nennen, zuordnen, erklären...
    content_structure: str           # facts, categories, chronology, process
    complexity: str                  # simple, medium, complex
    estimated_elements: int          # Geschätzte Anzahl H5P-Elemente
    suggested_container: str | None  # column, course_presentation, book
```

**Operator-Erkennung:**

| Operator | Erkennungsmuster | H5P-Empfehlung |
|----------|------------------|----------------|
| nennen | "nenne", "liste auf", "zähle" | Flashcards |
| beschreiben | "beschreibe", "erkläre kurz" | True/False, Summary |
| zuordnen | "ordne zu", "kategorisiere" | Drag & Drop |
| erklären | "erkläre", "begründe" | Accordion |
| ordnen | "ordne chronologisch", "reihenfolge" | Timeline |
| ergänzen | "ergänze", "fülle aus" | Fill Blanks, Drag Text |
| markieren | "markiere", "kennzeichne" | Mark Words |
| bewerten | "bewerte", "entscheide" | Branching Scenario |

#### 1.2 Planungs-Phase

```python
class ExecutionPlan:
    """Ausführungsplan für Sub-Agents"""
    elements: list[PlannedElement]   # Geplante H5P-Elemente
    container: ContainerConfig       # Container-Typ Konfiguration
    execution_order: list[str]       # Reihenfolge der Ausführung
    dependencies: dict[str, list]    # Abhängigkeiten zwischen Elementen
```

**Entscheidungsmatrix:**

```
Input-Komplexität → Container-Empfehlung
─────────────────────────────────────────
1 Lernziel, 1 Operator     → Einzelnes H5P-Element
2-3 Lernziele, ähnlich     → Column
3-5 Lernziele, gemischt    → Course Presentation
5+ Lernziele, strukturiert → Interactive Book
Entscheidungspfade         → Branching Scenario
```

#### 1.3 Koordinations-Phase

```python
async def coordinate_generation(plan: ExecutionPlan):
    """Parallele Ausführung mit Fehlerbehandlung"""

    # Phase 1: Einzel-Elemente parallel generieren
    tasks = [
        generate_element(e) for e in plan.elements
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Phase 2: Fehler behandeln
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            # Retry mit Fallback-Typ
            results[i] = await retry_with_fallback(plan.elements[i])

    # Phase 3: Container erstellen (falls geplant)
    if plan.container:
        return await combine_elements(results, plan.container)

    return results
```

---

### 2. Sub-Agents

#### 2.1 Quiz-Agent

**Spezialisierung:** Wissensabfrage und Prüfungselemente

| Typ | Wann verwenden | Validierung |
|-----|----------------|-------------|
| True/False | Fakten prüfen, schnelle Abfrage | Min. 2 Aussagen |
| Multiple Choice | Mehrere Optionen, Detailwissen | Min. 1 korrekte Antwort |
| Single Choice | Schnelle Entscheidungen | Genau 1 korrekte Antwort |
| Summary | Kernaussagen identifizieren | Min. 2 Aussage-Sets |

**Selbst-Korrektur:**
```python
def validate_and_correct(self, result: H5PResult) -> H5PResult:
    if not result.success:
        # Fallback: MC → SC bei zu wenig Optionen
        if self.type == "multi_choice" and self.error == "not_enough_options":
            return self.generate_as_single_choice()
    return result
```

#### 2.2 Card-Agent

**Spezialisierung:** Lernkarten und strukturierte Informationen

| Typ | Wann verwenden | Validierung |
|-----|----------------|-------------|
| Flashcards | Vokabeln, Definitionen, Begriffe | Min. 3 Karten |
| Accordion | Erklärungen, FAQ, Strukturen | Min. 2 Panels |
| Timeline | Chronologie, Geschichte, Prozesse | Min. 2 Events mit Datum |
| Memory | Zuordnungen visuell, Gamification | Min. 4 Paare, Bilder |

**Selbst-Korrektur:**
```python
def validate_and_correct(self, result: H5PResult) -> H5PResult:
    if self.type == "timeline" and not self.has_valid_dates():
        # Fallback: Timeline → Accordion wenn keine Daten
        return self.generate_as_accordion()
    return result
```

#### 2.3 Drag-Agent

**Spezialisierung:** Interaktive Zuordnungen

| Typ | Wann verwenden | Validierung |
|-----|----------------|-------------|
| Drag & Drop | Kategorien, Klassifikationen | Min. 2 Dropzones, 3 Draggables |
| Drag Text | Lückentexte mit Drag statt Tippen | Min. 2 Lücken |
| Mark Words | Begriffe im Text identifizieren | Min. 2 markierbare Wörter |
| Fill Blanks | Lückentexte mit Eingabe | Min. 1 Lücke |

**Selbst-Korrektur:**
```python
def validate_and_correct(self, result: H5PResult) -> H5PResult:
    if self.type == "drag_drop" and self.dropzones_outside_canvas():
        # Auto-Fix: Koordinaten korrigieren
        return self.regenerate_with_fixed_coordinates()
    return result
```

---

### 3. Combiner Agent

**Verantwortung:** Zusammenführung von Einzelelementen zu komplexen Typen

#### 3.1 Container-Typen

##### Column (Einfachste Kombination)

```json
{
  "mainLibrary": "H5P.Column",
  "content": [
    { "library": "H5P.AdvancedText", "params": {...} },
    { "library": "H5P.MultiChoice", "params": {...} },
    { "library": "H5P.DragQuestion", "params": {...} }
  ]
}
```

**Anwendung:** 2-5 Elemente vertikal anordnen

##### Course Presentation (Slideshow)

```json
{
  "mainLibrary": "H5P.CoursePresentation",
  "slides": [
    {
      "elements": [
        { "library": "H5P.AdvancedText", "x": 0, "y": 0 },
        { "library": "H5P.Image", "x": 50, "y": 0 }
      ]
    },
    {
      "elements": [
        { "library": "H5P.MultiChoice", "x": 0, "y": 0 }
      ]
    }
  ]
}
```

**Anwendung:** Präsentationen, Tutorials mit Navigation

##### Interactive Book (Kapitel)

```json
{
  "mainLibrary": "H5P.InteractiveBook",
  "chapters": [
    {
      "title": "Einführung",
      "content": [
        { "library": "H5P.AdvancedText", "params": {...} }
      ]
    },
    {
      "title": "Übungen",
      "content": [
        { "library": "H5P.QuestionSet", "params": {...} }
      ]
    }
  ]
}
```

**Anwendung:** Umfangreiche Lerneinheiten mit Kapiteln

##### Question Set (Quiz-Sequenz)

```json
{
  "mainLibrary": "H5P.QuestionSet",
  "questions": [
    { "library": "H5P.MultiChoice", "params": {...} },
    { "library": "H5P.TrueFalse", "params": {...} },
    { "library": "H5P.DragText", "params": {...} }
  ],
  "passPercentage": 70,
  "showResults": true
}
```

**Anwendung:** Prüfungen, Tests mit Auswertung

#### 3.2 Container-Entscheidung

```python
def choose_container(elements: list, structure: str) -> str | None:
    """Wählt den optimalen Container-Typ"""

    count = len(elements)

    if count == 1:
        return None  # Kein Container nötig

    if count <= 3 and structure == "sequential":
        return "column"

    if structure == "presentation" or count <= 5:
        return "course_presentation"

    if structure == "chapters" or count > 5:
        return "interactive_book"

    if all(is_quiz_type(e) for e in elements):
        return "question_set"

    return "column"  # Default
```

---

## Implementierungsplan

### Phase 1: Grundlagen ✅ ABGESCHLOSSEN

| Task | Beschreibung | Status |
|------|--------------|--------|
| 1.1 | Orchestrator-Klasse mit Analyse-Logik | ✅ |
| 1.2 | Sub-Agent Basisklasse mit Selbst-Korrektur | ✅ |
| 1.3 | Quiz-Agent implementieren | ✅ |
| 1.4 | Card-Agent implementieren | ✅ |
| 1.5 | Drag-Agent implementieren | ✅ |

### Phase 2: Design & Branding ✅ ABGESCHLOSSEN

| Task | Beschreibung | Status |
|------|--------------|--------|
| 2.1 | Brand-Config mit Presets | ✅ |
| 2.2 | Design-Agent implementieren | ✅ |
| 2.3 | Integration in Orchestrator | ✅ |
| 2.4 | 6 Brand-Presets (bswi, minimal, dark, etc.) | ✅ |

### Phase 3: System-Integration ✅ ABGESCHLOSSEN

| Task | Beschreibung | Status |
|------|--------------|--------|
| 3.1 | H5PSystem Unified API | ✅ |
| 3.2 | CLI Interface | ✅ |
| 3.3 | Quick-Convenience-Funktionen | ✅ |
| 3.4 | Integration Tests (10/10 bestanden) | ✅ |

### Phase 4: Container-Typen (Geplant)

| Task | Beschreibung | Status |
|------|--------------|--------|
| 4.1 | Column-Generator | ⬜ |
| 4.2 | Question Set-Generator | ⬜ |
| 4.3 | Course Presentation-Generator | ⬜ |
| 4.4 | Combiner-Agent Logik | ⬜ |

---

## Beispiel-Workflow

### Input

```markdown
# Scrum-Einführung

## Lernziele
- Die Schüler können die drei Scrum-Rollen nennen
- Die Schüler können Aufgaben den Rollen zuordnen
- Die Schüler können den Sprint-Ablauf erklären

## Inhalte
- Product Owner: Priorisiert Backlog, definiert User Stories
- Scrum Master: Entfernt Hindernisse, moderiert Meetings
- Development Team: Entwickelt Features, schätzt Aufwände

## Sprint-Phasen
1. Sprint Planning (Tag 1)
2. Daily Scrum (täglich)
3. Sprint Review (letzter Tag)
4. Sprint Retrospektive (letzter Tag)
```

### Orchestrator-Analyse

```python
ContentAnalysis(
    learning_goals=[
        "Scrum-Rollen nennen",
        "Aufgaben zuordnen",
        "Sprint-Ablauf erklären"
    ],
    operators=["nennen", "zuordnen", "erklären"],
    content_structure="mixed",
    complexity="medium",
    estimated_elements=4,
    suggested_container="course_presentation"
)
```

### Ausführungsplan

```python
ExecutionPlan(
    elements=[
        PlannedElement(type="flashcards", agent="card", content="Rollen-Definitionen"),
        PlannedElement(type="drag_drop", agent="drag", content="Aufgaben-Zuordnung"),
        PlannedElement(type="timeline", agent="card", content="Sprint-Phasen"),
        PlannedElement(type="summary", agent="quiz", content="Kernaussagen")
    ],
    container=ContainerConfig(type="course_presentation", slides=4),
    execution_order=["parallel:all", "combine"]
)
```

### Output

```
📦 scrum-einfuehrung.h5p
   └── Course Presentation (4 Slides)
       ├── Slide 1: Flashcards (3 Rollen)
       ├── Slide 2: Drag & Drop (Aufgaben → Rollen)
       ├── Slide 3: Timeline (Sprint-Phasen)
       └── Slide 4: Summary (Kernaussagen)
```

---

## Dateistruktur

```
h5p-generator/
├── scripts/
│   ├── __init__.py               # Package exports
│   ├── h5p_generator.py          # Basis-Generator (12 Typen)
│   ├── h5p_system.py             # ✅ Unified API (Haupteinstiegspunkt)
│   ├── cli.py                    # ✅ Command Line Interface
│   ├── orchestrator.py           # ✅ Orchestrator Agent
│   ├── brand_config.py           # ✅ Brand-Konfiguration & Presets
│   ├── agent_workflow.py         # Legacy Agent (deprecated)
│   ├── sub_agents/               # ✅ Sub-Agents
│   │   ├── __init__.py
│   │   ├── base_agent.py         # Basisklasse mit Selbst-Korrektur
│   │   ├── quiz_agent.py         # True/False, MultiChoice, Summary
│   │   ├── card_agent.py         # Flashcards, Accordion, Timeline
│   │   ├── drag_agent.py         # Drag&Drop, DragText, MarkWords
│   │   └── design_agent.py       # ✅ Branding/CI anwenden
│   ├── test_integration.py       # ✅ Integration Tests
│   └── combiner.py               # TODO: Combiner für Container
├── references/
│   ├── templates/
│   │   ├── decision-matrix.md
│   │   └── saved/
│   └── h5p-json-structure.md
├── test-output/                  # Generierte H5P-Dateien
├── SKILL.md
├── AGENT_WORKFLOW.md
└── MULTI_AGENT_ARCHITECTURE.md   # Diese Datei
```

## Aktuelle System-Architektur (v2.0)

```
                    ┌─────────────────────────┐
                    │      H5PSystem          │  ← Unified API
                    │   (h5p_system.py)       │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              │         H5POrchestrator           │
              │      (orchestrator.py)            │
              │  Analyse → Plan → Execute → Design│
              └─────────────────┬─────────────────┘
                                │
        ┌───────────┬───────────┼───────────┬───────────┐
        │           │           │           │           │
        ▼           ▼           ▼           ▼           ▼
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
   │  Quiz   │ │  Card   │ │  Drag   │ │ Design  │ │ Combiner│
   │  Agent  │ │  Agent  │ │  Agent  │ │  Agent  │ │ (TODO)  │
   └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
        │           │           │           │
        └───────────┴───────────┴───────────┘
                        │
                        ▼
              ┌─────────────────────┐
              │  Brand Presets      │
              │  (brand_config.py)  │
              │  bswi, minimal,     │
              │  dark, professional │
              └─────────────────────┘
```

---

## Erfolgskriterien

| Kriterium | Messung | Ziel |
|-----------|---------|------|
| Korrekte Typ-Wahl | Operator → Typ Übereinstimmung | >90% |
| Generierungserfolg | Fehlerfreie H5P-Dateien | >95% |
| Selbst-Korrektur | Automatische Fixes bei Fehlern | >80% |
| Container-Qualität | Sinnvolle Kombinationen | >85% |
| Geschwindigkeit | Zeit für komplette Einheit | <30s |

---

## Quick Start

### Python API

```python
from scripts import H5PSystem

# Einfachste Nutzung
system = H5PSystem(brand='bswi')
result = system.generate_from_text('''
## Lernziele
- Schueler koennen Scrum-Rollen nennen
''', content_items=[
    {'cards': [
        {'front': 'PO', 'back': 'Product Owner'},
        {'front': 'SM', 'back': 'Scrum Master'},
    ]}
])

print(result.summary())
```

### CLI

```bash
# System-Info
python cli.py info

# Aus Datei generieren mit Branding
python cli.py generate -f lerneinheit.md -b bswi

# Batch-Generierung
python cli.py batch elements.json -o ./output

# Brand-Details anzeigen
python cli.py brands bswi

# H5P-Typ-Info
python cli.py types flashcards
```

### Quick Functions

```python
from scripts import quick_flashcards, quick_quiz, quick_drag_drop

# Schnelle Flashcards
result = quick_flashcards('Vokabeln', [
    {'front': 'house', 'back': 'Haus'},
    {'front': 'car', 'back': 'Auto'},
], brand='bswi')

# Schnelles Quiz
result = quick_quiz('Test', [
    {'text': 'Python ist eine Programmiersprache.', 'correct': True}
])

# Schnelles Drag & Drop
result = quick_drag_drop('Zuordnung',
    dropzones=['A', 'B'],
    draggables=[{'text': 'Item1', 'dropzone': 0}]
)
```

---

## Brand Presets

| Preset | Beschreibung | Primary Color |
|--------|--------------|---------------|
| `default` | Standard-Theme | #1a73e8 |
| `bswi` | BS:WI Hamburg | #003366 |
| `minimal` | Minimalistisch | #333333 |
| `dark` | Dark Mode | #8ab4f8 |
| `professional` | Business | #1976d2 |
| `accessible` | High Contrast | #0000ff |

---

## Changelog

### v2.0.0 (Aktuell)
- ✅ H5PSystem als Unified API
- ✅ CLI Interface mit allen Befehlen
- ✅ Design Agent fuer Branding
- ✅ 6 Brand-Presets
- ✅ 10 Integration Tests bestanden
- ✅ Quick-Convenience-Funktionen

### v1.0.0
- ✅ Orchestrator mit Analyse/Plan/Execute
- ✅ Quiz-Agent, Card-Agent, Drag-Agent
- ✅ Basis-Generator mit 12 H5P-Typen
- ✅ Selbst-Korrektur und Fallback-Logik

### v0.1 (Planung)
- Architektur-Dokumentation erstellt
- Implementierungsplan definiert
- Beispiel-Workflow dokumentiert

---

*Multi-Agent H5P Generation System v2.0 - Dokumentation*
