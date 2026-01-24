# H5P Agent Workflow

## Übersicht

Der H5P Agent ist ein selbst-verbessernder Workflow für die automatische Generierung von H5P-Inhalten mit:

- **Automatische Content-Type-Wahl** basierend auf Lernziel/Operator
- **Qualitätsvalidierung** gegen bekannte Probleme
- **Preview-System** für schnelles Testen
- **Template-Bibliothek** die aus Feedback lernt

## Architektur

```
┌─────────────────────────────────────────────────────────────┐
│                     H5P Education Agent                      │
├─────────────────────────────────────────────────────────────┤
│  1. ANALYSE                                                  │
│     - Lernziel analysieren                                  │
│     - Operator erkennen (nennen, zuordnen, erklären...)     │
│     - Content-Type wählen mit Konfidenz                     │
├─────────────────────────────────────────────────────────────┤
│  2. GENERIERUNG                                              │
│     - Template aus Bibliothek laden                         │
│     - Inhalte einsetzen                                      │
│     - H5P-Datei erstellen                                   │
├─────────────────────────────────────────────────────────────┤
│  3. VALIDIERUNG                                              │
│     - Gegen bekannte Probleme prüfen                        │
│     - Warnungen ausgeben                                    │
│     - Ggf. automatisch korrigieren                          │
├─────────────────────────────────────────────────────────────┤
│  4. PREVIEW & FEEDBACK                                       │
│     - Lokaler Preview-Server starten                        │
│     - User-Feedback sammeln (1-5 Sterne)                    │
│     - Gute Ergebnisse als Template speichern                │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agent_workflow import H5PAgent

agent = H5PAgent()

# 1. Automatische Content-Type-Wahl
decision = agent.decide_content_type("Ordne die Scrum-Rollen zu")
print(f"Empfehlung: {decision.content_type}")  # → drag_drop

# 2. Generieren mit Validierung
result, issues = agent.generate_with_validation(
    'drag_drop',
    title="Scrum-Rollen",
    dropzones=["Product Owner", "Scrum Master", "Dev Team"],
    draggables=[
        {"text": "Priorisiert Backlog", "dropzone": 0},
        {"text": "Entfernt Hindernisse", "dropzone": 1},
        {"text": "Entwickelt Features", "dropzone": 2},
    ]
)

# 3. Preview starten
if result.success:
    agent.preview(result.path)

# 4. Feedback speichern (bei Erfolg)
agent.save_as_template(result, "scrum-rollen-zuordnung", "Gut für Einführung")
```

## Entscheidungslogik

Der Agent erkennt Operatoren im Lernziel und wählt automatisch:

| Operator | Content-Type | Beispiel-Lernziel |
|----------|--------------|-------------------|
| nennen | Flashcards | "Nenne die Scrum-Rollen" |
| beschreiben | True-False, Summary | "Beschreibe agile Werte" |
| erklären | Accordion | "Erkläre den Sprint-Prozess" |
| zuordnen | Drag-Drop | "Ordne Aufgaben zu Rollen" |
| ordnen | Timeline | "Ordne chronologisch" |
| ergänzen | Fill-in-Blanks, Drag-Text | "Ergänze die Lücken" |
| markieren | Mark-Words | "Markiere die Verben" |

## Validierung

Der Agent prüft automatisch gegen bekannte Probleme:

### Drag & Drop
- Dropzone y > 70 → Warnung (könnte außerhalb Canvas sein)
- Dropzone height < 20 → Warnung (zu klein)
- Mehr als 5 Dropzones → Hinweis (wird unübersichtlich)

### Timeline
- Weniger als 2 Events → Fehler
- Keine Datumsangaben → Fehler

### Allgemein
- Leerer Titel → Fehler
- Keine Inhalte → Fehler

## Preview-System

```bash
# Manuell starten
cd viewer
python serve.py ../test-output/meine-datei.h5p

# Öffnet automatisch: http://localhost:8080/preview.html
```

Der Preview nutzt h5p-standalone für lokales Rendering ohne WordPress/Moodle.

## Template-Bibliothek

Erfolgreiche Generierungen können als Templates gespeichert werden:

```python
# Nach erfolgreichem Test
agent.save_as_template(result, "name", "Notizen")
# → Speichert nach references/templates/saved/name.json
```

### Verzeichnisstruktur

```
references/templates/
├── OVERVIEW.md              # Kategorisierte Übersicht
├── decision-matrix.md       # Entscheidungslogik
├── dragdrop-working.json    # Validierte Drag&Drop-Werte
├── all-types.json           # Manuelle Referenz
├── all-examples.json        # 24 extrahierte Templates
└── saved/                   # Vom Agent gespeicherte Templates
    └── *.json
```

## Feedback-Log

Alle Generierungen werden mit Feedback protokolliert:

```json
{
  "timestamp": "2026-01-24T...",
  "content_type": "drag_drop",
  "title": "Scrum-Rollen",
  "success": true,
  "rating": 5,
  "issues": [],
  "notes": "Funktioniert perfekt"
}
```

Der Log wird für zukünftige Verbesserungen genutzt.

## Integration mit Claude Code

Der Agent kann direkt in Claude Code Skill-Prompts verwendet werden:

```
Erstelle eine H5P-Zuordnungsaufgabe für Scrum-Rollen.
- Product Owner: Priorisiert Backlog, Definiert User Stories
- Scrum Master: Entfernt Hindernisse, Moderiert Retrospektive
- Dev Team: Entwickelt Features, Schätzt Aufwände
```

Claude Code:
1. Erkennt "Zuordnung" → `drag_drop`
2. Generiert mit korrekten Koordinaten (v13-Template)
3. Validiert automatisch
4. Speichert bei Erfolg als Template

## Nächste Schritte

1. **Screenshot-basiertes Feedback**: Automatisch Screenshots machen für Qualitätsprüfung
2. **A/B-Testing**: Verschiedene Layouts vergleichen
3. **Adaptive Templates**: Templates basierend auf Feedback-Score priorisieren
4. **Multi-Step Workflows**: Komplexe Lernpfade automatisch generieren
