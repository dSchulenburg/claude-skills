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

```json
{
  "question": {
    "task": {
      "elements": [
        {
          "x": 10, "y": 5,
          "dropZones": ["0"],
          "type": {
            "library": "H5P.AdvancedText 1.1",
            "params": {"text": "<p>Draggable text</p>"}
          }
        }
      ],
      "dropZones": [
        {
          "x": 20, "y": 60,
          "label": "<div>Zone Name</div>",
          "correctElements": ["0"]
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

## Library Versions (as of 2024)

| Library | Version |
|---------|---------|
| H5P.QuestionSet | 1.20 |
| H5P.TrueFalse | 1.8 |
| H5P.MultiChoice | 1.16 |
| H5P.Blanks | 1.14 |
| H5P.DragQuestion | 1.14 |
| H5P.AdvancedText | 1.1 |

## Notes

- All text content should be wrapped in HTML tags (`<p>`, `<div>`)
- Boolean values in some fields are strings ("true"/"false")
- Coordinates (x, y) are percentages of canvas size
- subContentId must be unique within a QuestionSet
