---
name: h5p-designer
description: Analysiere, debugge und optimiere H5P-Dateien für bessere Benutzerfreundlichkeit und Design.
license: MIT
---

# H5P Designer Skill

Analysiere, debugge und optimiere H5P-Dateien für bessere Benutzerfreundlichkeit und Design.

## Wann verwenden

- H5P-Übungen sind schwer zu bedienen (zu kleine Elemente, schlechtes Spacing)
- Drag & Drop Dropzones sind zu klein für die Anzahl der Items
- Text wird abgeschnitten oder ist unleserlich
- Deutsche Umlaute werden falsch dargestellt
- Layout-Probleme bei interaktiven Elementen

## Workflow

```
1. ANALYZE    → H5P-Datei analysieren, Issues identifizieren
2. DIAGNOSE   → Probleme kategorisieren (Größe, Spacing, Encoding)
3. FIX        → Auto-Fixes anwenden + Layout optimieren
4. VERIFY     → Optimierte Datei prüfen
5. (OPTIONAL) → In WordPress hochladen + Browser-Screenshot
```

## Quick Start

```bash
# H5P analysieren
python scripts/h5p_designer.py pfad/zur/datei.h5p

# H5P analysieren UND automatisch fixen
python scripts/h5p_designer.py pfad/zur/datei.h5p --fix

# Mit spezifischem Output-Pfad
python scripts/h5p_designer.py pfad/zur/datei.h5p --fix --output neue-datei.h5p
```

## Unterstützte Content-Types

| Typ | Analyse | Auto-Fix | Layout-Optimierung |
|-----|---------|----------|-------------------|
| H5P.DragQuestion (Drag & Drop) | ✅ | ✅ | ✅ |
| H5P.MultiChoice | ✅ | Teilweise | - |
| H5P.Blanks (Lückentext) | Basis | - | - |
| H5P.TrueFalse | Basis | - | - |
| H5P.DialogCards | Basis | - | - |

## Issue-Kategorien

### 1. Size Issues (Größe)
- Draggables zu klein (< 12% Breite, < 8% Höhe)
- Dropzones zu klein für erwartete Items
- Canvas zu klein für Inhalt

### 2. Spacing Issues (Abstände)
- Elemente zu nah beieinander (< 3% Abstand)
- Überlappende Dropzones
- Ungleichmäßige Verteilung

### 3. Encoding Issues (Zeichensatz)
- Deutsche Umlaute als ae/oe/ue statt ä/ö/ü
- Falsche Sonderzeichen

### 4. Layout Issues
- Dropzone zu klein für Anzahl korrekter Items
- Unlogische Anordnung

## Beispiel-Analyse

```
============================================================
H5P Analysis: Scrum-Rollen zuordnen
Type: DragQuestion
============================================================

Found 8 issues:
  - Errors: 0
  - Warnings: 8
  - Auto-fixable: 2

Details:
  1. [WARN] [encoding] Draggable 6: "schaetzt" should be "schätzt" [FIX]
  2. [WARN] [spacing] Elements 1 and 2 are too close (2.0%)
  3. [WARN] [spacing] Elements 2 and 3 are too close (2.0%)
  ...
```

## Optimierungen für Drag & Drop

Das Script wendet folgende Optimierungen an:

### Canvas
- Minimum: 700x500px (vorher oft 620x450)
- Besseres Seitenverhältnis für Interaktion

### Draggables
- Breite: ~20% (statt oft 18%)
- Höhe: ~11% (statt oft 10%)
- Gleichmäßige Grid-Anordnung
- Optimaler Abstand zwischen Elementen

### Dropzones
- Breite: ~25% (je nach Anzahl)
- Höhe: ~30%
- Gleichmäßige horizontale Verteilung
- Position: Untere Hälfte des Canvas

## Programmatische Nutzung

```python
from h5p_designer import H5PDesigner, analyze_h5p, optimize_h5p

# Einfache Analyse
analysis = analyze_h5p("meine-uebung.h5p")
print(analysis.summary())
for issue in analysis.issues:
    print(f"{issue.severity}: {issue.message}")

# Optimieren und speichern
saved_path, results = optimize_h5p("meine-uebung.h5p")
print(f"Optimierte Datei: {saved_path}")

# Detaillierte Kontrolle
designer = H5PDesigner("meine-uebung.h5p")
analysis = designer.analyze()

# Nur bestimmte Fixes anwenden
designer.apply_fixes([i for i in analysis.issues if i.category == 'encoding'])

# Eigene Werte setzen
designer.set_content_value('question.settings.size.width', 800)

# Speichern
designer.save("custom-output.h5p")
```

## Design-Empfehlungen

### Drag & Drop

| Element | Minimum | Empfohlen | Maximum |
|---------|---------|-----------|---------|
| Canvas Breite | 600px | 700-800px | 1000px |
| Canvas Höhe | 400px | 500-600px | 800px |
| Draggable Breite | 12% | 18-22% | 30% |
| Draggable Höhe | 8% | 10-14% | 20% |
| Dropzone Breite | 15% | 20-30% | 40% |
| Dropzone Höhe | 20% | 25-35% | 50% |
| Element-Abstand | 3% | 5% | - |

### Text in Draggables

```html
<!-- Gut: Kurz und lesbar -->
<p style='margin:0;font-size:12px;'>Kurzer Text</p>

<!-- Schlecht: Zu viel Text -->
<p style='margin:0;font-size:10px;'>Dieser sehr lange Text wird abgeschnitten und ist unleserlich</p>
```

## Integration mit WordPress/Moodle

Nach der Optimierung kann die H5P-Datei hochgeladen werden:

```python
# 1. H5P optimieren
saved_path, _ = optimize_h5p("original.h5p")

# 2. Zu WordPress hochladen (via wp-mcp)
# wp_upload_h5p(saved_path)

# 3. In Moodle einbetten
# moodle_add_h5p_activity(course_id, saved_path)
```

## Bekannte Limitierungen

1. **Kein Live-Preview:** Das Script kann H5P nicht rendern - nur content.json analysieren
2. **Beschränkte Content-Types:** Volle Unterstützung nur für DragQuestion
3. **Layout ist Schätzung:** Optimale Größen sind heuristisch, nicht perfekt

## Dateien

```
h5p-designer/
├── SKILL.md              # Diese Dokumentation
└── scripts/
    └── h5p_designer.py   # Hauptscript
```

---

## Logging

Bei Ausführung dieses Skills wird automatisch geloggt:

| Feld | Wert |
|------|------|
| **Agent** | education |
| **Action** | h5p:design |
| **Context** | h5p_file, content_type, issues_found, fixes_applied |
| **Result** | success/failure |

**Beispiel-Log:**
```json
{
  "agent": "education",
  "action": "h5p:design",
  "context": "{\"h5p_file\": \"scrum-rollen.h5p\", \"content_type\": \"DragQuestion\", \"issues_found\": 8, \"fixes_applied\": 2}",
  "result": "success"
}
```

## Changelog

| Version | Datum | Änderungen |
|---------|-------|------------|
| 1.0.0 | 2026-01-19 | Initial: DragQuestion Analyzer, Auto-Fix, Layout-Optimierung |
