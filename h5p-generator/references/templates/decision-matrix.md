# H5P Content-Type Entscheidungsmatrix

## Agentische Entscheidungslogik

```python
def select_h5p_type(lernziel: str, operator: str, komplexität: str) -> str:
    """
    Wählt den passenden H5P-Typ basierend auf didaktischen Kriterien.

    Args:
        lernziel: Was soll gelernt werden?
        operator: Welche kognitive Operation? (nennen, erklären, analysieren, bewerten...)
        komplexität: einfach | mittel | hoch

    Returns:
        H5P Content-Type Name
    """

    # Niveau 1: Reproduktion (nennen, beschreiben)
    if operator in ["nennen", "beschreiben", "auflisten"]:
        if komplexität == "einfach":
            return "Flashcards"  # Begriffe lernen
        else:
            return "Fill-in-Blanks"  # Lückentexte

    # Niveau 2: Reorganisation (erklären, zuordnen)
    if operator in ["erklären", "zuordnen", "ordnen", "klassifizieren"]:
        return "Drag-and-Drop"  # Zuordnungsaufgaben

    # Niveau 3: Transfer (anwenden, berechnen)
    if operator in ["anwenden", "berechnen", "durchführen"]:
        return "Course-Presentation"  # Schritt-für-Schritt

    # Niveau 4: Analyse (analysieren, vergleichen, untersuchen)
    if operator in ["analysieren", "vergleichen", "untersuchen"]:
        return "Interactive-Video"  # Prozesse verstehen

    # Niveau 5: Bewertung (bewerten, begründen, beurteilen)
    if operator in ["bewerten", "begründen", "beurteilen", "entscheiden"]:
        return "Branching-Scenario"  # Entscheidungssimulation

    # Niveau 6: Gestaltung (entwickeln, konzipieren, planen)
    if operator in ["entwickeln", "konzipieren", "planen", "gestalten"]:
        return "Interactive-Book"  # Komplexe Lerneinheit

    # Fallback: Quiz für Wissensprüfung
    return "Question-Set"
```

## Schnellreferenz-Tabelle

| Lernziel | Operator | H5P-Typ | Beispiel |
|----------|----------|---------|----------|
| Begriffe lernen | nennen | Flashcards | Fachbegriffe, Vokabeln |
| Fakten prüfen | beschreiben | True-False | Richtig/Falsch-Aussagen |
| Definitionen | ergänzen | Fill-in-Blanks | Lückentexte mit Fachbegriffen |
| Kategorien | zuordnen | Drag-and-Drop | Elemente in Gruppen sortieren |
| Zusammenhänge | erklären | Accordion | Aufklappbare Erklärungen |
| Schritte | anwenden | Course-Presentation | Rechenwege, Prozesse |
| Prozesse | analysieren | Interactive-Video | Fallbeispiele mit Stopps |
| Optionen | bewerten | Branching-Scenario | Entscheidungsbäume |
| Themenbereich | strukturieren | Interactive-Book | Komplette Lerneinheit |

## Content-Typ Details

### Einfache Typen (Generator unterstützt)

| Typ | Dateiname | Wann verwenden | Wann NICHT verwenden |
|-----|-----------|----------------|----------------------|
| **True-False** | `create_true_false()` | Faktenwissen prüfen | Komplexe Sachverhalte |
| **Multiple-Choice** | `create_multi_choice()` | Mehrere Optionen, eine/mehrere richtig | Offene Fragen |
| **Single-Choice** | `create_single_choice()` | Schnelle Abfrage, eine richtig | Wenn Begründung nötig |
| **Fill-in-Blanks** | `create_fill_blanks()` | Exakte Begriffe einsetzen | Kreative Antworten |
| **Drag-and-Drop** | `create_drag_drop()` | Kategorisieren, Zuordnen | Mehr als 5 Kategorien |
| **Flashcards** | `create_flashcards()` | Vokabeln, Definitionen | Komplexe Konzepte |
| **Mark-the-Words** | `create_mark_words()` | Begriffe im Text finden | Lange Texte |
| **Summary** | `create_summary()` | Kernaussagen identifizieren | Erste Einführung |
| **Accordion** | `create_accordion()` | Strukturierte Infos | Interaktive Übungen |

### Komplexe Typen (manuell in H5P-Editor)

| Typ | Wann verwenden | Aufwand |
|-----|----------------|---------|
| **Interactive-Video** | Prozesse, Fallbeispiele | Hoch (Video nötig) |
| **Branching-Scenario** | Entscheidungstraining, IHK-Simulation | Sehr hoch |
| **Course-Presentation** | Rechenwege, Schritt-für-Schritt | Mittel |
| **Interactive-Book** | Komplette Lernfelder | Sehr hoch |

## Didaktische Regeln

1. **Gamification sparsam einsetzen**
   - Flashcards, Drag&Drop, Fill-in-Blanks = Unterstützend
   - NICHT als Hauptlernform auf IHK/Abitur-Niveau

2. **Quiz nur mit Begründung**
   - Feedback erklärt Denkfehler, nicht nur richtig/falsch
   - Verwende `feedback_correct` und `feedback_wrong` mit Erklärung

3. **Progression beachten**
   - Einführung: Accordion (Infos) → Flashcards (Begriffe)
   - Übung: Fill-in-Blanks → Drag-and-Drop
   - Prüfung: Multiple-Choice mit Begründung → Summary

4. **4K-Integration**
   - **Kreativität**: Open-ended Aufgaben (nicht nur H5P)
   - **Kritisches Denken**: Bewertungsfragen, Branching
   - **Kommunikation**: Diskussionsanlässe schaffen
   - **Kollaboration**: Gruppenaufgaben außerhalb H5P

## Beispiel-Workflow

```
Thema: "Agile Methoden"

1. Accordion: "Was ist Agile?" (Einführung)
2. Flashcards: Begriffe (Scrum, Sprint, Backlog)
3. Drag-and-Drop: Scrum-Rollen zuordnen
4. True-False: Mythen vs. Fakten
5. Summary: Kernprinzipien identifizieren
6. [Manuell] Branching-Scenario: Sprint-Planung simulieren
```
