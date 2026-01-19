# H5P Content Types - JSON Structure Reference

## Overview

H5P files are ZIP archives with:
- `h5p.json` - Metadata and library dependencies
- `content/content.json` - The actual content

## True/False (H5P.TrueFalse)

```json
{
  "question": "<p>Statement text</p>",
  "correct": "true",  // or "false" (string!)
  "l10n": {
    "trueText": "Wahr",
    "falseText": "Falsch"
  },
  "feedbackOnCorrect": "Richtig!",
  "feedbackOnWrong": "Leider falsch."
}
```

## Fill in the Blanks (H5P.Blanks)

Blanks marked with asterisks: `*answer*`

Multiple accepted answers: `*answer1/answer2*`

```json
{
  "text": "<p>Die Hauptstadt ist *Berlin*.</p>",
  "behaviour": {
    "caseSensitive": false,
    "acceptSpellingErrors": true
  }
}
```

## Multiple Choice (H5P.MultiChoice)

```json
{
  "question": "<p>Question text?</p>",
  "answers": [
    {"text": "<div>Option A</div>", "correct": true},
    {"text": "<div>Option B</div>", "correct": false}
  ],
  "behaviour": {
    "randomAnswers": true,
    "singlePoint": false
  }
}
```

## Drag and Drop (H5P.DragQuestion)

**ACHTUNG:** Siehe Abschnitt "KRITISCH: H5P.DragQuestion Positionierung" am Ende!

```json
{
  "question": {
    "settings": {
      "size": {"width": 620, "height": 450},
      "background": {"path": "https://...", "mime": "image/jpeg"}
    },
    "task": {
      "elements": [
        {
          "x": 5, "y": 3,
          "width": 12, "height": 6,
          "dropZones": ["0"],
          "backgroundOpacity": 80,
          "type": {
            "library": "H5P.AdvancedText 1.1",
            "params": {"text": "<p>Draggable text</p>"}
          }
        }
      ],
      "dropZones": [
        {
          "x": 3, "y": 22,
          "width": 10, "height": 73,
          "label": "<div>Zone Name</div>",
          "correctElements": ["0"],
          "showLabel": true,
          "backgroundOpacity": 70,
          "autoAlign": true
        }
      ]
    }
  }
}
```

## Question Set (H5P.QuestionSet)

Wrapper for multiple questions:

```json
{
  "introPage": {
    "showIntroPage": true,
    "title": "Quiz Title",
    "introduction": "<p>Instructions</p>"
  },
  "progressType": "dots",
  "passPercentage": 60,
  "questions": [
    {
      "params": { /* question content */ },
      "library": "H5P.TrueFalse 1.8",
      "subContentId": "unique-id"
    }
  ],
  "endGame": {
    "showResultPage": true,
    "message": "Score: @score / @total"
  }
}
```

## h5p.json Structure

```json
{
  "title": "Content Title",
  "language": "de",
  "mainLibrary": "H5P.QuestionSet",
  "embedTypes": ["iframe"],
  "license": "CC BY",
  "preloadedDependencies": [
    {"machineName": "H5P.QuestionSet", "majorVersion": 1, "minorVersion": 20}
  ]
}
```

## Library Versions (as of 2026)

| Library | Version | Use Case |
|---------|---------|----------|
| H5P.QuestionSet | 1.20 | Wrapper für Fragen |
| H5P.TrueFalse | 1.8 | Wahr/Falsch |
| H5P.MultiChoice | 1.16 | Multiple Choice |
| H5P.Blanks | 1.14 | Lückentext |
| H5P.DragQuestion | 1.14 | Drag & Drop |
| H5P.SingleChoiceSet | 1.11 | Schnelle Single Choice |
| H5P.Dialogcards | 1.9 | Lernkarten |
| H5P.MarkTheWords | 1.11 | Wörter markieren |
| H5P.Summary | 1.10 | Zusammenfassung |
| H5P.Accordion | 1.0 | Aufklappbare Abschnitte |
| H5P.AdvancedText | 1.1 | Text-Komponente |

## New Content Types

### Single Choice Set (H5P.SingleChoiceSet)

```json
{
  "choices": [
    {
      "question": "<p>Question?</p>",
      "answers": ["<p>Correct</p>", "<p>Wrong1</p>", "<p>Wrong2</p>"]
    }
  ],
  "behaviour": {
    "autoContinue": true,
    "timeoutCorrect": 2000,
    "enableRetry": true
  }
}
```

### Dialog Cards / Flashcards (H5P.Dialogcards)

```json
{
  "title": "<p>Title</p>",
  "dialogs": [
    {
      "text": "<p>Front side</p>",
      "answer": "<p>Back side</p>",
      "tips": [{"text": "Optional hint"}]
    }
  ],
  "behaviour": {
    "enableRetry": true,
    "randomCards": false
  }
}
```

### Mark the Words (H5P.MarkTheWords)

```json
{
  "taskDescription": "<p>Mark the correct words.</p>",
  "textField": "This is *correct* but this is wrong.",
  "behaviour": {
    "enableRetry": true,
    "enableSolutionsButton": true
  }
}
```

### Summary (H5P.Summary)

```json
{
  "intro": "<p>Choose the correct statement.</p>",
  "summaries": [
    {
      "summary": [
        {"text": "<p>Correct statement</p>"},
        {"text": "<p>Wrong statement</p>"}
      ]
    }
  ]
}
```

### Accordion (H5P.Accordion)

```json
{
  "panels": [
    {
      "title": "Section Title",
      "content": {
        "params": {"text": "<p>Content here</p>"},
        "library": "H5P.AdvancedText 1.1"
      }
    }
  ],
  "hTag": "h2"
}
```

## Notes

- All text content should be wrapped in HTML tags (`<p>`, `<div>`)
- Boolean values in some fields are strings ("true"/"false")
- subContentId must be unique within a QuestionSet

---

## KRITISCH: H5P.DragQuestion Positionierung & Größen

**WICHTIG:** Die width/height Werte in DragQuestion sind KEINE Prozente!

### Einheiten-Konvertierung (empirisch ermittelt)

| JSON-Feld | Umrechnung | Beispiel |
|-----------|------------|----------|
| `x`, `y` | ~7px pro Einheit | x: 37 → 259px |
| `width`, `height` | ~18px pro Einheit (EM) | width: 10 → 180px |

### Dropzones ohne Überlappung berechnen

**Problem:** `width: 20` wird zu ~360px → bei 3 Zonen massive Überlappung!

**Lösung:** Kleinere width-Werte verwenden und Positionen berechnen:

```
Beispiel für 3 nicht-überlappende Dropzones (700px Container):

Zone 1: x=3,  width=10  → left=21px,  right=201px (180px breit)
Zone 2: x=37, width=10  → left=259px, right=439px (180px breit)
Zone 3: x=71, width=10  → left=497px, right=677px (180px breit)

Lücken: ~57px zwischen den Zonen ✓
```

### Formel für Positionsberechnung

```
position_px = x_value * 7
width_px = width_value * 18

Für Lücke zwischen Zone A und Zone B:
gap_px = (x_B * 7) - (x_A * 7 + width_A * 18)
```

### Funktionierende Konfiguration (getestet)

```json
"dropZones": [
  {"x": 3,  "y": 22, "width": 10, "height": 73, "correctElements": ["0","1","2"]},
  {"x": 37, "y": 22, "width": 10, "height": 73, "correctElements": ["3","4","5"]},
  {"x": 71, "y": 22, "width": 10, "height": 73, "correctElements": ["6","7","8"]}
]
```

### Draggable Elements (optimale Größen)

**Empfohlene Werte:**
- `width: 6-8` je nach Textlänge (kurz: 6, lang: 8)
- `height: 2` für einzeiligen Text
- `font-size: 12px` im HTML

**Beispiel-Konfiguration:**
```json
{
  "x": 2, "y": 2,
  "width": 7, "height": 2,
  "backgroundOpacity": 80,
  "type": {
    "library": "H5P.AdvancedText 1.1",
    "params": {
      "text": "<p style='text-align:center;margin:0;font-size:12px;font-weight:bold;'>Kurzer Text</p>"
    }
  }
}
```

**Textlänge → Width:**
| Zeichen | Width |
|---------|-------|
| 10-15 | 6 |
| 16-19 | 7 |
| 20+ | 8 |

- Können sich überlappen (wird beim Drag aufgelöst)
- Text darf umbrechen - das ist OK

### Canvas-Größe

```json
"settings": {
  "size": {"width": 620, "height": 450}  // Standard
}
```

### Hintergrundbilder

```json
"background": {
  "path": "https://images.unsplash.com/...",
  "mime": "image/jpeg"
}
```

### Opacity

- `backgroundOpacity: 70` für Elemente (0-100)
- Gilt für Draggables und Dropzones separat
