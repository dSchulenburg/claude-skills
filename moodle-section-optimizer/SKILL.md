---
name: moodle-section-optimizer
description: Optimiert Moodle-Kursabschnitte basierend auf 4K-Analyse. Erstellt Labels mit Bildern, generiert H5P-Inhalte, fügt Struktur-Elemente hinzu. Nutze nach moodle-section-analyzer oder wenn konkrete Verbesserungen umgesetzt werden sollen.
license: MIT
agent: Education
---

# Moodle Section Optimizer

Setzt konkrete Optimierungen für Moodle-Abschnitte um: Labels, H5P, Struktur, Multimedia.

## Wann nutzen

- Nach Analyse mit `moodle-section-analyzer`
- Konkrete 4K-Lücken schließen
- Abschnitt visuell aufwerten
- Interaktive Elemente hinzufügen

## Voraussetzungen

- **MCP Server**: moodle-mcp (v2.4.0+) mit H5P-Tools
- **Skills**: h5p-generator (für H5P-Erstellung)
- **Analyse**: Idealerweise vorher `moodle-section-analyzer` ausführen
- **Optional**: wordpress-mcp (nur falls WordPress H5P benötigt wird)

## Optimierungs-Bausteine

### 1. Phasen-Labels (Struktur)

Visuelle Trenner für Abschnittsphasen:

```html
<!-- Phase-Start Label -->
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
  <h3 style="margin: 0;">🎯 Phase 1: Orientierung</h3>
  <p style="margin: 5px 0 0 0; opacity: 0.9;">ca. 15 Minuten</p>
</div>
```

**Farb-Schema nach Phase:**

| Phase | Farbe | Hex |
|-------|-------|-----|
| Orientierung | Blau-Lila | #667eea → #764ba2 |
| Motivation | Orange-Rot | #f093fb → #f5576c |
| Erarbeitung | Grün | #4facfe → #00f2fe |
| Analyse | Gelb-Orange | #fa709a → #fee140 |
| Anwendung | Türkis | #30cfd0 → #330867 |
| Reflexion | Grün-Blau | #38f9d7 → #43e97b |
| Abschluss | Gold | #f7971e → #ffd200 |

### 2. Einführungs-Labels (Multimedia)

```html
<!-- Mit Bild (Base64 oder URL) -->
<div style="display: flex; align-items: center; gap: 20px; padding: 15px; 
            background: #f8f9fa; border-radius: 8px; border-left: 4px solid #667eea;">
  <img src="[BILD_URL]" style="width: 120px; border-radius: 8px;" alt="Thema">
  <div>
    <h3 style="margin: 0 0 8px 0;">🛒 Der Checkout-Prozess</h3>
    <p style="margin: 0; color: #666;">In dieser Einheit analysieren Sie...</p>
  </div>
</div>
```

**Bildquellen:**
- undraw.co (kostenlos, SVG)
- Flaticon (Icons)
- Eigene Screenshots

### 3. Lernziel-Labels

```html
<div style="background: #e8f5e9; padding: 15px; border-radius: 8px; 
            border-left: 4px solid #4caf50;">
  <h4 style="margin: 0 0 10px 0;">🎯 Lernziele</h4>
  <ul style="margin: 0; padding-left: 20px;">
    <li>Den Checkout-Prozess beschreiben können</li>
    <li>Abbruchgründe analysieren und bewerten</li>
    <li>Optimierungsvorschläge entwickeln</li>
  </ul>
</div>
```

### 4. Abschluss-Labels

```html
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; padding: 20px; border-radius: 8px; text-align: center;">
  <h3 style="margin: 0;">🎉 Geschafft!</h3>
  <p style="margin: 10px 0 0 0;">Sie haben Phase 1 abgeschlossen.<br>
     Weiter geht's mit: Zahlungsarten</p>
</div>
```

### 5. H5P-Elemente (via h5p-generator)

| 4K-Defizit | H5P-Typ | Beispiel |
|------------|---------|----------|
| Kreativität ↓ | Drag & Drop | Checkout-Schritte zuordnen |
| Krit. Denken ↓ | Quiz / True-False | Wissen überprüfen |
| Krit. Denken ↓ | Fill in Blanks | Definitionen vervollständigen |
| Kommunikation ↓ | Documentation Tool | Strukturierte Reflexion |

**✅ EMPFOHLEN: Native Moodle H5P (Content Bank)**

Seit dem `local_h5p_api` Plugin können H5P-Inhalte direkt in Moodle gespeichert werden:

| Vorteil | Beschreibung |
|---------|--------------|
| Im Backup | H5P wird mit Kurs exportiert |
| Keine Abhängigkeit | WordPress muss nicht laufen |
| Filter-Syntax | `{h5p:contentid}` in Moodle möglich |

**Workflow für native Moodle H5P:**

```python
# 1. H5P generieren mit h5p-generator
from h5p_generator import create_multi_choice
questions = [...]
create_multi_choice("Checkout-Quiz", questions, "checkout-quiz")
# → Datei: checkout-quiz.h5p

# 2. H5P zu Moodle hochladen (via MCP)
moodle_upload_h5p({
    "base64data": "[BASE64_ENCODED_H5P]",
    "filename": "checkout-quiz.h5p",
    "title": "Checkout-Quiz",
    "courseid": 6
})
# → Response: { contentid: 42, embedurl: "...", iframecode: "..." }

# 3. In Section einbetten (via moodle_update_section oder moodle_create_label)
```

**Moodle H5P Embed-Format:**
```
https://moodle.example.com/h5p/embed.php?url=https%3A%2F%2Fmoodle.example.com%2Fpluginfile.php%2F[contextid]%2Fcontentbank%2Fpublic%2F[contentid]%2F[filename]
```

**Zwei Einbettungs-Optionen:**

| Option | Methode | Wann nutzen |
|--------|---------|-------------|
| **In Section Summary** | `moodle_update_section` mit iframe | Direkt im Abschnitt sichtbar |
| **Als Label** | `moodle_create_label` mit iframe | Mehr Kontrolle über Position |
| **Als Page** | `moodle_create_page` mit iframe | Längere Inhalte, aufgeräumter |

**Beispiel: H5P in Section Summary:**
```html
<h4>Wissenstest</h4>
<iframe src="https://moodle.example.com/h5p/embed.php?url=..."
        width="100%" height="600" frameborder="0" allowfullscreen></iframe>
```

**Alternative: WordPress H5P (Legacy)**

Falls WordPress H5P noch benötigt wird:
```
https://[DOMAIN]/wp-admin/admin-ajax.php?action=h5p_embed&id=[H5P_ID]
```

**Erstellung:**
```python
# Via h5p-generator Skill
from h5p_generator import create_multi_choice, create_fill_blanks

# Quiz für Kritisches Denken
questions = [
    {
        "question": "Was ist der wichtigste Faktor für Kaufabbrüche?",
        "answers": [
            {"text": "Zu hohe Versandkosten", "correct": True},
            {"text": "Schlechtes Design", "correct": False},
            {"text": "Lange Ladezeiten", "correct": False}
        ]
    }
]
create_multi_choice("Checkout-Quiz", questions, "checkout-quiz")
```

## Workflow

### Schritt 1: Analyse-Ergebnis prüfen

```yaml
input:
  kurs_id: 6
  abschnitt_num: 2
  diagnose:
    4k_defizite: [Kreativität, Kritisches Denken]
    fehlend: [Bilder, Quiz, Struktur-Labels]
```

### Schritt 2: Optimierungsplan erstellen

```yaml
plan:
  - aktion: "Phase-Label erstellen"
    typ: label
    position: "Anfang"
    inhalt: "🎯 Phase 1: Orientierung"
    
  - aktion: "Einführungs-Label mit Bild"
    typ: label
    position: "Nach Phase-Label"
    bild: "checkout-illustration.svg"
    
  - aktion: "H5P Quiz erstellen"
    typ: h5p
    h5p_typ: "multi_choice"
    fragen: 5
    
  - aktion: "Abschluss-Label"
    typ: label
    position: "Ende"
    inhalt: "🎉 Geschafft!"
```

### Schritt 3: Module erstellen

```javascript
// 1. Phase-Label
moodle:moodle_create_label({
  courseId: "6",
  sectionNum: "2",
  labelText: `<div style="background: linear-gradient(...)">
    <h3>🎯 Phase 1: Orientierung</h3>
  </div>`
})

// 2. H5P erstellen (via h5p-generator)
// → Datei: checkout-quiz.h5p

// 3. H5P zu Moodle Content Bank hochladen (empfohlen)
moodle:moodle_upload_h5p({
  base64data: "[BASE64]",
  filename: "checkout-quiz.h5p",
  title: "Checkout-Quiz",
  courseid: "6"
})
// → { contentid: 42, embedurl: "...", iframecode: "..." }

// 4. H5P in Abschnitt einbetten
moodle:moodle_update_section({
  courseId: "6",
  sectionNum: "2",
  summary: `<h4>🎮 Quiz: Checkout-Basics</h4>
            <iframe src="[embedurl from response]"
            width="100%" height="600" frameborder="0" allowfullscreen></iframe>`
})
```

## Optimierungs-Rezepte

### Rezept 1: "Quick Win" – Visuelle Aufwertung (15 Min)

```yaml
schritte:
  1. Phase-Label am Anfang (Gradient + Emoji)
  2. Lernziel-Label nach Einführung
  3. Abschluss-Label am Ende
  
aufwand: ⭐
4k_impact: Gering (Orientierung verbessert)
```

### Rezept 2: "Interaktivität" – H5P hinzufügen (30 Min)

```yaml
schritte:
  1. Quiz mit 5 Fragen erstellen (h5p-generator)
  2. Fill-in-Blanks für Definitionen
  3. In Moodle als Page einbetten
  
aufwand: ⭐⭐
4k_impact: Kritisches Denken ↑↑
```

### Rezept 3: "Vollständig" – Alle 4K abdecken (60 Min)

```yaml
schritte:
  1. Struktur-Labels (Phasen)
  2. Einführungs-Label mit Bild
  3. H5P Quiz (Kritisches Denken)
  4. H5P Drag&Drop (Kreativität)
  5. Forum-Aufgabe umformulieren (Kollaboration)
  6. Peer-Review-Anweisung (Kommunikation)
  7. Abschluss-Label mit Badge-Hinweis
  
aufwand: ⭐⭐⭐
4k_impact: Alle 4K verbessert
```

## HTML-Templates

### Template: Info-Box

```html
<div style="background: #e3f2fd; padding: 15px; border-radius: 8px; 
            border-left: 4px solid #2196f3; margin: 10px 0;">
  <strong>💡 Info:</strong> [TEXT]
</div>
```

### Template: Warnung

```html
<div style="background: #fff3e0; padding: 15px; border-radius: 8px; 
            border-left: 4px solid #ff9800; margin: 10px 0;">
  <strong>⚠️ Wichtig:</strong> [TEXT]
</div>
```

### Template: Aufgaben-Box

```html
<div style="background: #f3e5f5; padding: 15px; border-radius: 8px; 
            border-left: 4px solid #9c27b0; margin: 10px 0;">
  <strong>📋 Arbeitsauftrag:</strong>
  <ol style="margin: 10px 0 0 0;">
    <li>[SCHRITT 1]</li>
    <li>[SCHRITT 2]</li>
  </ol>
</div>
```

### Template: Zeitangabe

```html
<div style="display: inline-block; background: #e8eaf6; padding: 5px 12px; 
            border-radius: 15px; font-size: 0.9em; color: #3f51b5;">
  ⏱️ ca. 15 Minuten
</div>
```

## Best Practices

1. **Konsistente Farben**: Ein Farbschema pro Kurs durchhalten
2. **Emoji-Sprache**: Einheitliche Emojis für gleiche Konzepte
3. **Nicht überladen**: Max. 2-3 neue Elemente pro Iteration
4. **Testen**: Nach jeder Änderung im Browser prüfen
5. **Mobile-First**: Inline-Styles responsive halten

## Reihenfolge der Module

Nach Optimierung sollte ein Abschnitt folgende Struktur haben:

```
📁 Abschnitt X: [Thema]
├── 🏷️ Phase-Label (Einführung)
├── 🏷️ Lernziele
├── 🏷️ Einführungs-Label mit Bild
├── 🔗 LOOP/Theorie-Link
├── 🎮 H5P Selbsttest (Verständnissicherung)
├── 📋 Arbeitsauftrag / Assignment
├── 💬 Forum zur Aufgabe
├── 🎮 H5P Quiz (Abschlusstest)
└── 🏷️ Abschluss-Label
```

## Limitations

### Bekannte Einschränkungen

| Limitation | Workaround |
|------------|------------|
| **Module immer am Ende** | Moodle-API hat keinen `position` Parameter → Manuell in Moodle sortieren |
| **Keine Modul-Sortierung** | Moodle Web-Services unterstützen kein `move_module` → Drag&Drop im Browser |
| **Kein Forum/Quiz erstellen** | Moodle-API-Limitation → Manuell anlegen oder Template-Kurs nutzen |

### Empfohlener Workflow

1. **Erst analysieren** (moodle-section-analyzer)
2. **H5P generieren** (h5p-generator)
3. **H5P zu Moodle hochladen** (moodle_upload_h5p)
4. **Labels + Pages erstellen** (dieser Skill)
5. **In Moodle einloggen** → Module per Drag&Drop sortieren
6. **Foren manuell anlegen** (falls benötigt)

## ⚠️ Kritische Warnung: Berechtigungen

Nach CLI-Befehlen im Moodle-Container können Berechtigungsprobleme auftreten!

**Symptom:** "Invalid permissions detected when trying to create a directory"

**Lösung:**
```bash
docker exec moodle chown -R daemon:daemon /bitnami/moodledata/
```

Siehe: [[Moodle-Learnings#KRITISCH moodledata Berechtigungsproblem]]

## Referenzen

- [[Moodle]] - MCP Server Dokumentation v2.4.0+
- [[Moodle-Learnings]] - Troubleshooting & Best Practices
- [[local_h5p_api Plugin]] - H5P Upload/Embed API

---

*Skill Version: 1.1*
*Abhängigkeiten: moodle-mcp (v2.4.0+), h5p-generator*
*Letzte Aktualisierung: 2026-01-15*
