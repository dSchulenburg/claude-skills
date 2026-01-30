---
name: lernfeld-zu-moodle-kurs
description: |
  Erstellt Moodle-Kurse aus Lernfeld-Materialien (Matchpläne, Präsentationen, Arbeitsblätter).
  Use when: Lehrer möchte Unterrichtsmaterial in Moodle-Kursstruktur umwandeln,
  Lernfelder/Lernsituationen digitalisieren, oder bestehende Kurse als Template nutzen.
license: MIT
allowed-tools:
  - moodle:moodle_create_course
  - moodle:moodle_create_section
  - moodle:moodle_update_section
  - moodle:moodle_create_page
  - moodle:moodle_create_label
  - moodle:moodle_create_url
  - moodle:moodle_create_folder
---

# Lernfeld zu Moodle-Kurs

Workflow zur Transformation von Lernfeld-Materialien (Matchpläne, PPT, Arbeitsblätter) in strukturierte Moodle-Kurse.

## Wann diesen Skill nutzen

- Lernfeld-Unterlagen in Moodle-Kurs umwandeln
- Matchpläne als Basis für Kursstruktur verwenden
- Konsistente Kursstrukturen über Lernfelder hinweg erstellen
- Bestehende Präsenzmaterialien digitalisieren

## Voraussetzungen

### MCP Server
- **moodle-mcp** mit Tools: create_course, create_section, create_page, create_label, create_url, create_folder

### Input-Materialien
- **Matchpläne** (.docx) - Unterrichtsplanung mit Folienreferenzen
- **Präsentationen** (.pptx) - LuL und SuS Versionen
- **Arbeitsblätter** (.docx) - Übungen, Lösungen
- **Optional:** LOOP-Links, externe Ressourcen

## Kurs-Struktur-Template

Basierend auf dem E-Commerce Lernfeld 3 Referenzkurs:

```yaml
kurs:
  fullname: "LF[X] - [Lernfeld-Titel]"
  shortname: "LF[X]-[Bildungsgang]"
  format: topics
  
abschnitte:
  # Abschnitt 0: Meta/Einleitung
  - position: 0
    name: "[Lernfeld-Titel]"
    inhalte:
      - type: label
        text: "Willkommen im Lernraum..."
      - type: forum
        name: "Ankündigungen"
        typ: news
      - type: forum
        name: "Allgemeines Forum"
      - type: page
        name: "Informationen zur Arbeit mit diesem Modul"
  
  # Abschnitt 1: Lehrer-Material (versteckt)
  - position: 1
    name: "Hinweise für Lehrkräfte (für SuS nicht sichtbar)"
    visible: false
    inhalte:
      - type: folder
        name: "Hinweise zur Arbeit mit diesem Lernfeld"
        files: [matchpläne, lösungen, lehrerinfos]
  
  # Abschnitte 2+: Lernsituationen/Kapitel
  - position: 2
    name: "[Nr] [Kapitel-Titel]"
    inhalte:
      - type: forum
        name: "Forum [Nr]: [Kapitel-Titel]"
      - type: url
        name: "[Kapitel-Titel] (LOOP-Kapitel)"
        url: "https://loop.oncampus.de/..."
      - type: forum
        name: "Forum zur Aufgabe [X]: [Aufgaben-Titel]"
      - type: assign
        name: "Aufgabe [X]: [Aufgaben-Titel]"
        # Optional, wenn Abgabe erforderlich
```

## Workflow

### Phase 1: Material-Analyse (10 Min)

**Input sammeln:**
```
📁 Lernfeld-Material/
├── Lernsituation_01/
│   ├── Matchplan.docx          ← Hauptquelle für Struktur
│   ├── Präsentation_LuL.pptx   ← Folienreferenzen
│   ├── Präsentation_SuS.pptx   ← Für Schüler
│   └── Arbeitsblätter/
├── Lernsituation_02/
│   └── ...
└── Allgemein/
    └── Lehrerinfo.docx
```

**Matchplan analysieren:**

| Spalte | Extrahieren |
|--------|-------------|
| Lehrhandeln | Folienbezug, Zeitangaben |
| Schülerhandeln | Arbeitsaufträge → Aktivitäten |
| Begründung | Lernziele → Abschnittsbeschreibung |

### Phase 2: Struktur-Mapping (15 Min)

**Matchplan-Zeile → Moodle-Aktivität:**

| Matchplan-Element | Moodle-Aktivität |
|-------------------|------------------|
| "Schüler diskutieren..." | Forum |
| "Schüler recherchieren..." | URL (externe Quelle) |
| "Arbeitsauftrag siehe Folie" | Page mit Aufgabenstellung |
| "Schüler bearbeiten AB" | Assignment |
| "Gruppenarbeit..." | Forum oder Wiki |
| "Präsentation der Ergebnisse" | Forum |

**Folien-Cluster → Moodle-Abschnitt:**

```
Folien 1-2: Orientierung     ─┐
Folie 3: Einstieg             │── Abschnitt 2: "Thema A"
Folien 4-8: Hauptteil        ─┘

Folien 9-14: Neues Thema     ─── Abschnitt 3: "Thema B"
```

### Phase 3: Kurs erstellen (MCP)

**Schritt 1: Kurs anlegen**

```javascript
moodle:moodle_create_course({
  fullname: "LF3 - Verträge im Online-Vertrieb anbahnen und bearbeiten",
  shortname: "LF3-ECOM",
  categoryid: "1",
  format: "topics",
  numsections: "9"
})
// → courseId: 6
```

**Schritt 2: Abschnitte benennen**

```javascript
// Abschnitt 0: Einleitung
moodle:moodle_update_section({
  courseId: "6",
  sectionNum: "0",
  name: "Lernfeld 3 - Verträge im Online-Vertrieb",
  summary: "Willkommen im Lernraum zum Lernfeld 3"
})

// Abschnitt 1: Lehrer-Material
moodle:moodle_update_section({
  courseId: "6",
  sectionNum: "1",
  name: "Hinweise für Lehrkräfte (für SuS nicht sichtbar)",
  visible: "0"
})

// Abschnitt 2: Erstes Kapitel
moodle:moodle_update_section({
  courseId: "6",
  sectionNum: "2",
  name: "1 Den Checkout-Prozess im Online-Vertrieb analysieren"
})
```

**Schritt 3: Aktivitäten hinzufügen**

```javascript
// Willkommens-Label
moodle:moodle_create_label({
  courseId: "6",
  sectionNum: "0",
  labelText: `
    <h3>Herzlich Willkommen!</h3>
    <p>In diesem Lernfeld bearbeiten Sie...</p>
  `
})

// Info-Seite
moodle:moodle_create_page({
  courseId: "6",
  sectionNum: "0",
  pageName: "Informationen zur Arbeit mit diesem Modul",
  content: "<h3>Arbeitshinweise</h3><p>...</p>"
})

// LOOP-Link
moodle:moodle_create_url({
  courseId: "6",
  sectionNum: "2",
  name: "Den Checkout-Prozess analysieren (LOOP-Kapitel)",
  url: "https://loop.oncampus.de/loop/..."
})

// Lehrer-Ordner
moodle:moodle_create_folder({
  courseId: "6",
  sectionNum: "1",
  name: "Hinweise zur Arbeit mit diesem Lernfeld",
  itemId: "0"  // Leerer Ordner, Dateien später hochladen
})
```

## Referenz-Beispiel: LF3 E-Commerce

### Input: 4 Lernsituationen

| LS | Titel | Matchplan |
|----|-------|-----------|
| 01 | Der funktionierende Checkout | 14 Folien, ~4h |
| 02 | Kaufverträge im Internet | (Material fehlt) |
| 03 | Zahlungsarten anbieten | 9 Folien, Expertengruppen |
| 04 | Lieferung & Logistik | Projektauftrag-Struktur |

### Output: 9 Moodle-Abschnitte

| Abschnitt | Titel | Basiert auf |
|-----------|-------|-------------|
| 0 | Einleitung & Willkommen | - |
| 1 | Lehrer-Hinweise (versteckt) | Alle Matchpläne |
| 2 | Checkout-Prozess analysieren | LS01 |
| 3 | Personenbezogene Daten | Ergänzung |
| 4 | Versandmöglichkeiten | LS04 (Teil) |
| 5 | Zahlungskonditionen | LS03 |
| 6 | Checkout beurteilen | Ergänzung |
| 7 | Verträge rechtssicher | LS02 |
| 8 | Ware versenden | LS04 (Teil) |

### Aktivitäten-Pattern pro Abschnitt

```
Abschnitt X: [Titel]
├── 💬 Forum X: [Titel] (Hauptdiskussion)
├── 🔗 [Titel] (LOOP-Kapitel) (Theorie)
├── 💬 Forum zur Aufgabe Y (Bearbeitung)
├── 📋 Aufgabe Y (falls Abgabe nötig)
└── 📝 Wiki (falls kollaborativ)
```

## Best Practices

### Struktur
- **Konsistente Nummerierung:** "1 Titel", "2 Titel" (nicht "LS01")
- **Abschnitt 0** immer für Meta-Infos (Willkommen, Foren)
- **Abschnitt 1** versteckt für Lehrer-Material
- **Foren vor Aufgaben:** Erst diskutieren, dann abgeben

### Benennung
- Hauptforum: "Forum X: [Kapitel-Titel]"
- Aufgabenforum: "Forum zur Aufgabe X: [Kontext]"
- LOOP-Links: "[Titel] (LOOP-Kapitel)"
- Assignments: "Aufgabe X: [Aufgaben-Titel]"

### Material-Zuordnung
- Matchpläne → Lehrer-Ordner (Abschnitt 1)
- Lösungen → Lehrer-Ordner
- SuS-Präsentationen → Als Ressource oder Page
- Arbeitsblätter → Als Ressource oder in Aufgabe eingebettet

## Limitationen

### Was dieser Skill NICHT kann:
- **Foren automatisch erstellen** (Moodle-API unterstützt das nicht)
- **Assignments erstellen** (benötigt mod_assign Capability)
- **Dateien hochladen** (benötigt separaten Upload-Workflow)
- **Quiz/H5P erstellen** (siehe h5p-generator Skill)

### Workarounds:
- Foren: Manuell in Moodle erstellen oder Kurs-Template nutzen
- Dateien: Über Moodle-UI oder WebDAV hochladen
- Assignments: Manuell anlegen, Struktur als Vorlage nutzen

## Erweiterungen

### Mit h5p-generator kombinieren

```
1. Aus Matchplan Fragen extrahieren
2. h5p-generator: Quiz erstellen
3. WordPress: H5P hochladen
4. Moodle: Als Page mit iframe einbetten
```

### Mit LOOP-Integration

```
1. LOOP-Kapitel-URLs sammeln
2. Pro Abschnitt als URL-Ressource hinzufügen
3. Konsistente Benennung: "[Titel] (LOOP-Kapitel)"
```

## Referenz-Dateien

- `references/lf3-ecommerce-example.md` - Vollständiges Beispiel
- `references/matchplan-struktur.md` - Matchplan-Analyse
- `references/aktivitaeten-mapping.md` - Matchplan → Moodle Mapping

---

## Logging

Bei Ausführung dieses Skills wird automatisch geloggt:

| Feld | Wert |
|------|------|
| **Agent** | education |
| **Action** | moodle:create_lernfeld_course |
| **Context** | lernfeld, course_id, section_count, activity_count |
| **Result** | success/failure |

**Beispiel-Log:**
```json
{
  "agent": "education",
  "action": "moodle:create_lernfeld_course",
  "context": "{\"lernfeld\": \"LF3\", \"course_id\": 6, \"section_count\": 9, \"activity_count\": 24}",
  "result": "success"
}
```

---

*Skill basiert auf dem E-Commerce Lernfeld 3 Kurs (Kurs-ID 6) der BS:WI Hamburg.*
