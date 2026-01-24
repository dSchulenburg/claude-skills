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

### Phase 1: Grundlagen (Woche 1)

| Task | Beschreibung | Status |
|------|--------------|--------|
| 1.1 | Orchestrator-Klasse mit Analyse-Logik | ⬜ |
| 1.2 | Sub-Agent Basisklasse mit Selbst-Korrektur | ⬜ |
| 1.3 | Quiz-Agent implementieren | ⬜ |
| 1.4 | Card-Agent implementieren | ⬜ |
| 1.5 | Drag-Agent implementieren | ⬜ |

### Phase 2: Container-Typen (Woche 2)

| Task | Beschreibung | Status |
|------|--------------|--------|
| 2.1 | Column-Generator zum h5p_generator.py | ⬜ |
| 2.2 | Question Set-Generator | ⬜ |
| 2.3 | Course Presentation-Generator | ⬜ |
| 2.4 | Combiner-Agent Logik | ⬜ |

### Phase 3: Integration (Woche 3)

| Task | Beschreibung | Status |
|------|--------------|--------|
| 3.1 | Async-Koordination mit asyncio | ⬜ |
| 3.2 | Fehlerbehandlung und Retry | ⬜ |
| 3.3 | Template-Lernen aus Ergebnissen | ⬜ |
| 3.4 | Tests und Dokumentation | ⬜ |

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
│   ├── h5p_generator.py          # Basis-Generator (12 Typen)
│   ├── agent_workflow.py         # Aktueller einfacher Agent
│   ├── orchestrator.py           # NEU: Orchestrator Agent
│   ├── sub_agents/               # NEU: Sub-Agents
│   │   ├── __init__.py
│   │   ├── base_agent.py         # Basisklasse mit Selbst-Korrektur
│   │   ├── quiz_agent.py
│   │   ├── card_agent.py
│   │   └── drag_agent.py
│   └── combiner.py               # NEU: Combiner für Container
├── references/
│   ├── templates/
│   │   ├── decision-matrix.md
│   │   ├── container-types.json  # NEU: Container-Strukturen
│   │   └── saved/
│   └── h5p-json-structure.md
├── SKILL.md
├── AGENT_WORKFLOW.md
└── MULTI_AGENT_ARCHITECTURE.md   # Diese Datei
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

## Changelog

### v0.1 (Planung)
- Architektur-Dokumentation erstellt
- Implementierungsplan definiert
- Beispiel-Workflow dokumentiert

---

*Multi-Agent H5P Generation System - Planungsdokument*
