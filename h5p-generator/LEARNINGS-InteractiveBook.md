# Learnings: H5P Interactive Book Kompatibilität

**Datum:** 2025-01-25
**Kontext:** H5P-Generator Multi-Agent System
**Getestet mit:** Lumi Desktop

## Kompatibilitätsmatrix

### Funktioniert in Interactive Book ✅

| H5P-Typ | Library | Anmerkung |
|---------|---------|-----------|
| **AdvancedText** | H5P.AdvancedText 1.1 | Text, Überschriften |
| **Dialogcards** | H5P.Dialogcards 1.9 | Flashcards/Lernkarten |
| **TrueFalse** | H5P.TrueFalse 1.8 | Wahr/Falsch-Fragen |
| **MultiChoice** | H5P.MultiChoice 1.16 | Multiple-Choice-Quiz |
| **DragText** | H5P.DragText 1.10 | Wörter in Lücken ziehen |

### Funktioniert NICHT ❌

| H5P-Typ | Library | Problem |
|---------|---------|---------|
| **Blanks** | H5P.Blanks 1.14 | Vorschau lädt nicht |
| **DragQuestion** | H5P.DragQuestion 1.14 | Vorschau lädt nicht |

## Empfehlungen

### Alternativen für nicht-funktionierende Typen

| Statt | Nutze | Grund |
|-------|-------|-------|
| Blanks (Lückentext tippen) | **DragText** | Gleiche Funktion, Drag statt Tippen |
| DragQuestion (Bild-Drag) | **MultiChoice** | Simpler, aber funktioniert |

### Struktur für Interactive Book

```python
# Minimale funktionierende Struktur
content = {
    "showCoverPage": False,  # oder True mit bookCover
    "bookCover": {"coverDescription": "", "coverImage": {}, "coverMedium": {}},
    "title": "<p>Titel</p>",
    "chapters": [
        {
            "title": "Kapitel 1",
            "params": {
                "content": [
                    {
                        "content": {
                            "library": "H5P.AdvancedText 1.1",
                            "params": {"text": "<p>Inhalt</p>"},
                            "subContentId": "unique-id",
                            "metadata": {"contentType": "Text", "license": "U", "title": "Titel"}
                        },
                        "useSeparator": "auto"
                    }
                ]
            }
        }
    ],
    "behaviour": {"defaultTableOfContents": True, "progressIndicators": True, "displaySummary": True},
    "l10n": { ... }  # Lokalisierung
}

h5p = {
    "title": "Titel",
    "language": "de",
    "mainLibrary": "H5P.InteractiveBook",
    "embedTypes": ["iframe"],
    "license": "U",
    "preloadedDependencies": [
        {"machineName": "H5P.InteractiveBook", "majorVersion": 1, "minorVersion": 7},
        {"machineName": "H5P.Column", "majorVersion": 1, "minorVersion": 16},
        # + alle verwendeten Content-Typen
    ]
}
```

## Debugging-Tipps

1. **Vorschau lädt nicht?** → Wahrscheinlich inkompatible Library
2. **Schrittweise testen:** Erst nur Text, dann einzelne Elemente hinzufügen
3. **Mehrere Kapitel:** Funktionieren problemlos
4. **Dependencies:** Alle verwendeten Libraries müssen in preloadedDependencies

## QuestionSet-Wrapper entpacken

**Problem:** Der H5P-Generator erzeugt MultiChoice/TrueFalse als QuestionSet mit `questions[]`-Array.
Wenn man das direkt einbettet, fehlen die Antworten.

**Lösung:** Für Quiz-Typen `questions[0].params` extrahieren:

```python
def _unwrap_questionset_content(self, content: dict) -> dict:
    if 'questions' in content and isinstance(content['questions'], list):
        questions = content['questions']
        if len(questions) > 0 and 'params' in questions[0]:
            return questions[0]['params']
    return content
```

## Getestete Kombinationen (funktionieren)

- Flashcards + TrueFalse (2 Kapitel)
- Flashcards + MultiChoice (2 Kapitel)
- Flashcards + DragText (2 Kapitel)
- Text + Flashcards + TrueFalse + MultiChoice (4 Kapitel)
