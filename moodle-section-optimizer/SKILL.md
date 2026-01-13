---
name: moodle-section-optimizer
description: Optimiert Moodle-Kursabschnitte basierend auf 4K-Analyse. Erstellt Labels mit Bildern, generiert H5P-Inhalte, fügt Struktur-Elemente hinzu. Nutze nach moodle-section-analyzer oder wenn konkrete Verbesserungen umgesetzt werden sollen.
---

# Moodle Section Optimizer

Setzt konkrete Optimierungen für Moodle-Abschnitte um: Labels, H5P, Struktur, Multimedia.

## Wann nutzen

- Nach Analyse mit `moodle-section-analyzer`
- Konkrete 4K-Lücken schließen
- Abschnitt visuell aufwerten
- Interaktive Elemente hinzufügen

## Voraussetzungen

- **MCP Server**: moodle-mcp, wordpress-mcp (für H5P)
- **Skills**: h5p-generator (für H5P-Erstellung)
- **Analyse**: Idealerweise vorher `moodle-section-analyzer` ausführen

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

**⚠️ KRITISCH: H5P-Embed-URL**

```html
<!-- FALSCH - lädt ZIP herunter! -->
<iframe src="https://example.com/?p=123&h5p=19"></iframe>
<iframe src="https://example.com/wp-content/uploads/h5p/..."></iframe>

<!-- RICHTIG - H5P-Player wird angezeigt -->
<iframe src="https://example.com/wp-admin/admin-ajax.php?action=h5p_embed&id=19"></iframe>
```

Die korrekte Embed-URL ist:
```
https://[DOMAIN]/wp-admin/admin-ajax.php?action=h5p_embed&id=[H5P_ID]
```

**Zwei Einbettungs-Optionen:**

| Option | Methode | Wann nutzen |
|--------|---------|-------------|
| **Label (inline)** | `moodle_create_label` mit iframe | Kurze Quizze, direkt sichtbar |
| **Page (Unterseite)** | `moodle_create_page` mit iframe | Längere Inhalte, aufgeräumter |

**Option A: Label (inline auf Kursseite)**
```html
<div style="background: #f5f5f5; padding: 20px; border-radius: 8px;">
  <h4>🎮 Selbsttest: [TITEL]</h4>
  <iframe src="https://[DOMAIN]/wp-admin/admin-ajax.php?action=h5p_embed&id=[ID]" 
          width="100%" height="450" frameborder="0" allowfullscreen></iframe>
</div>
```

**Option B: Page (separate Seite)**
```html
<iframe src="https://[DOMAIN]/wp-admin/admin-ajax.php?action=h5p_embed&id=[ID]" 
        width="100%" height="600" frameborder="0" allowfullscreen></iframe>
```

**Empfehlung:** Label für Selbsttests (5-10 Fragen), Page für umfangreiche Inhalte.

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

// 3. H5P zu WordPress hochladen
wordpress:wp_import_h5p_content({
  base64Data: "[BASE64]",
  title: "Checkout-Quiz"
})
// → h5pId: 42

// 4. H5P in Moodle einbetten (als Page mit iframe)
moodle:moodle_create_page({
  courseId: "6",
  sectionNum: "2",
  pageName: "🎮 Quiz: Checkout-Basics",
  content: `<iframe src="https://www.dirk-schulenburg.net/?p=123" 
            width="100%" height="500" frameborder="0"></iframe>`
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
| **H5P nur via iframe** | Kein natives Moodle-H5P-Plugin → WordPress-Embed |

### Empfohlener Workflow

1. **Erst analysieren** (moodle-section-analyzer)
2. **Labels + Pages erstellen** (dieser Skill)
3. **In Moodle einloggen** → Module per Drag&Drop sortieren
4. **Foren manuell anlegen** (falls benötigt)

---

*Skill Version: 1.0*
*Abhängigkeiten: moodle-mcp, wordpress-mcp, h5p-generator*
