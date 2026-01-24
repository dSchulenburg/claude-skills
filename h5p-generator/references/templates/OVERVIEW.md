# H5P Template-Bibliothek - Übersicht

## Verfügbare Templates (24 Typen)

### Generator-unterstützt (9 Typen)

Diese Typen können mit dem Python-Generator erstellt werden:

| Typ | Library | Generator-Funktion | Datei |
|-----|---------|-------------------|-------|
| True/False | H5P.TrueFalse 1.8 | `create_true_false()` | `truefalse` |
| Multiple Choice | H5P.MultiChoice 1.16 | `create_multi_choice()` | - |
| Fill in Blanks | H5P.Blanks 1.14 | `create_fill_blanks()` | `blanks` |
| Drag and Drop | H5P.DragQuestion 1.14 | `create_drag_drop()` | `dragquestion` |
| Single Choice | H5P.SingleChoiceSet 1.11 | `create_single_choice()` | `singlechoiceset` |
| Flashcards/Dialog Cards | H5P.Dialogcards 1.9 | `create_flashcards()` | `dialogcards` |
| Mark the Words | H5P.MarkTheWords 1.11 | `create_mark_words()` | `markthewords` |
| Summary | H5P.Summary 1.10 | `create_summary()` | `summary` |
| Accordion | H5P.Accordion 1.0 | `create_accordion()` | `accordion` |

### Manuell in H5P-Editor (15 Typen)

Diese Typen sind zu komplex für automatische Generierung:

#### Hohe Priorität (didaktisch wertvoll)

| Typ | Library | Verwendung | Komplexität |
|-----|---------|------------|-------------|
| **Question Set** | H5P.QuestionSet | Quiz mit mehreren Fragen | Mittel |
| **Column** | H5P.Column | Mehrere H5P in einem | Mittel |
| **Timeline** | H5P.Timeline | Zeitstrahl mit Events | Hoch |
| **Drag the Words** | H5P.DragText | Wörter in Text ziehen | Mittel |

#### Medien-basiert

| Typ | Library | Verwendung | Komplexität |
|-----|---------|------------|-------------|
| **Audio** | H5P.Audio | Audio-Player | Niedrig |
| **Image Slider** | H5P.ImageSlider | Bildergalerie | Niedrig |
| **Image Juxtaposition** | H5P.ImageJuxtaposition | Vorher/Nachher Bilder | Niedrig |
| **Memory Game** | H5P.MemoryGame | Paare finden | Mittel |

#### Speziell

| Typ | Library | Verwendung | Komplexität |
|-----|---------|------------|-------------|
| **Dictation** | H5P.Dictation | Diktat mit Audio | Hoch |
| **Essay** | H5P.Essay | Freier Text mit Keywords | Mittel |
| **Speak the Words** | H5P.SpeakTheWords | Spracheingabe | Hoch |
| **Personality Quiz** | H5P.PersonalityQuiz | Persönlichkeitstest | Hoch |
| **Guess the Answer** | H5P.GuessTheAnswer | Bild mit versteckter Antwort | Niedrig |
| **Arithmetic Quiz** | H5P.ArithmeticQuiz | Mathe-Übungen | Mittel |
| **Chart** | H5P.Chart | Diagramme | Mittel |
| **Flashcards (alt)** | H5P.Flashcards | Ältere Kartenversion | Niedrig |

## Dateistruktur

```
references/templates/
├── OVERVIEW.md              # Diese Datei
├── decision-matrix.md       # Wann welcher Typ
├── dragdrop-working.json    # Validierte Drag&Drop Werte
├── all-types.json           # Manuelle Template-Sammlung
└── all-examples.json        # Aus 33 Beispielen extrahiert
```

## Beispiel-Quellen

| Quelle | Anzahl | Beschreibung |
|--------|--------|--------------|
| h5p.org | 20 | Offizielle Referenz-Beispiele |
| UBC | 13 | University of British Columbia (akademisch) |

## Nutzung

### Generator verwenden

```python
from h5p_generator import create_drag_drop, THEMES

result = create_drag_drop(
    "Mein Quiz",
    "Ordne zu!",
    ["Kategorie A", "Kategorie B"],
    [{"text": "Item 1", "dropzone": 0}, {"text": "Item 2", "dropzone": 1}],
    style=THEMES['education']
)
```

### Template als Referenz nutzen

```python
import json

# Lade Template-Struktur
with open('references/templates/all-examples.json') as f:
    templates = json.load(f)

# Zeige Struktur für Timeline
print(json.dumps(templates['timeline']['structure'], indent=2))
```

## Nächste Schritte

1. **Interactive Video** Template hinzufügen (erfordert Video-Upload)
2. **Branching Scenario** Template hinzufügen (komplexe Entscheidungsbäume)
3. **Course Presentation** Template hinzufügen (Folien mit Interaktionen)
4. **Interactive Book** Template hinzufügen (mehrseitige Lerneinheiten)

Diese 4 Typen sind die komplexesten und wertvollsten für IHK/Abitur-Niveau.
