# LF3 E-Commerce - Vollständiges Beispiel

Referenz-Dokumentation für den lernfeld-zu-moodle-kurs Skill.

## Quell-Material

### Unterlagen (ZIP)

```
📁 OneDrive_1_12.1.2026.zip
├── Checkliste_Check-Out.pdf
├── IB_KPI Nutzerverhalten Onsite.docx
├── Lernsituation_01 - der funktionierende Checkout/
│   ├── 00_LF03_LS01_Matchplan_Funktionierender-Checkout.docx
│   ├── 01_LF03_LS01_DerCheckout.pptx
│   ├── 02_LF03_LS01_Hörverstehen-Fond-of_Lösung.docx
│   ├── 03_Lösung EPK Fondof_Xing.pptm
│   └── 04_eEPK_Fond of_AA und Lösung.docx
├── Lernsituation_02 - Kaufverträge im Internet abschließen/
│   └── (leer)
├── Lernsituation_03 - Zahlungsarten anbieten/
│   ├── LF03_LS03_Matchplan_Zahlungsarten.docx
│   ├── LF03_LS03_Zahlungsarten.pptx
│   ├── LF03_LS03_Zahlungsarten_LuL.pptx
│   ├── LF03_LS03_Zahlungsarten_SuS.pptx
│   ├── Lehrerinfo Zahlungsarten.docx
│   └── upÜ Sandra/
│       ├── 0_Powerpoint_SuS_Version.pptx
│       ├── 1_Anhang 1.pdf
│       ├── 1_Daten (Google Analytics, intern).pdf
│       ├── 2_Raster Expertengruppe.docx
│       └── E-Mails für die Stammgruppen-Entscheidung.pptx
└── Lernsituation_04 - Lieferung & Logistik planen und umsetzen/
    ├── 00_LF03_LS04_Matchplan.docx
    ├── 00_LF03_LS04_Matchplan_Lesehilfe.docx
    ├── 01_LF03_LS04_Logistische_Prozesse_.pptx
    ├── Eigen- Fremdverkehr FALL.docx
    ├── Frachtführer AB.docx
    ├── LF03_LS04_Transport_SuS.pptx
    ├── LS03_LS04_OnePager.docx
    ├── Spediteur_AB.docx
    ├── Übungsaufgaben_Transport.docx
    └── Übungsaufgaben_Transport_Lösungen.docx
```

## Moodle-Kurs (ID: 6)

**URL:** https://moodle.dirk-schulenburg.net/course/view.php?id=6

### Kurs-Metadaten

```yaml
courseId: 6
fullname: "Lernfeld 3 - Verträge im Online-Vertrieb anbahnen und bearbeiten"
shortname: "LF3-ECOM"
format: topics
numsections: 9
```

### Abschnitt 0: Einleitung

```yaml
section:
  id: 45
  name: "Lernfeld 3 - Verträge im Online-Vertrieb anbahnen und bearbeiten"
  visible: true
  
modules:
  - type: label
    id: 130
    content: "Herzlich Willkommen in unserem Lernraum zum Lernfeld 3..."
    
  - type: forum
    id: 131
    name: "Ankündigungen"
    forumtype: news
    
  - type: forum
    id: 132
    name: "Allgemeines Forum"
    forumtype: general
    
  - type: page
    id: 133
    name: "Informationen zur Arbeit mit diesem Modul"
```

### Abschnitt 1: Lehrer-Material (versteckt)

```yaml
section:
  id: 46
  name: "Hinweise für Lehrkräfte (für SuS nicht sichtbar)"
  visible: false
  
modules:
  - type: folder
    id: 134
    name: "Hinweise zur Arbeit mit diesem Lernfeld für Lehrkräfte"
    files:
      - Matchpläne
      - Lösungen
      - Lehrerinfos
```

### Abschnitt 2: Checkout-Prozess (← LS01)

```yaml
section:
  id: 47
  name: "1 Den Checkout-Prozess im Online-Vertrieb analysieren"
  visible: true
  
modules:
  - type: forum
    id: 135
    name: "Forum 1: Den Checkout-Prozess im Online-Vertrieb analysieren"
    
  - type: url
    id: 136
    name: "Den Checkout-Prozess im Online-Vertrieb analysieren (LOOP-Kapitel)"
    externalurl: "https://loop.oncampus.de/..."
    
  - type: forum
    id: 137
    name: "Forum zur Aufgabe 1: Ausgangssituation Verkaufsprozess"
    
  - type: forum
    id: 138
    name: "Forum zur Aufgabe 2: Ausgangssituation zur Exit Rate"
```

### Abschnitt 3: Personenbezogene Daten

```yaml
section:
  id: 48
  name: "2 Personenbezogene Daten rechtskonform speichern und verarbeiten"
  visible: true
  
modules:
  - type: forum
    id: 139
    name: "Forum 2: Personenbezogene Daten rechtskonform speichern und verarbeiten"
    
  - type: url
    id: 140
    name: "Personenbezogene Daten rechtskonform speichern und verarbeiten (LOOP-Kapitel)"
    
  - type: forum
    id: 141
    name: "Forum zur Aufgabe 3: Ausgangssituation Kontaktformular (1-2)"
    
  - type: assign
    id: 142
    name: "Aufgabe 3: Ausgangssituation Kontaktformular (3-6)"
    
  - type: forum
    id: 143
    name: "Forum zur Aufgabe 4: Folgesituation Datenschutzerklärung"
    
  - type: assign
    id: 144
    name: "Aufgabe 5: Folgesituation Newsletterversand"
```

### Abschnitt 4: Versandmöglichkeiten (← LS04 Teil)

```yaml
section:
  id: 49
  name: "3 Versandmöglichkeiten kriteriengeleitet anbieten"
  visible: true
  
modules:
  - type: forum
    id: 145
    name: "Forum 3: Versandmöglichkeiten kriteriengeleitet anbieten"
    
  - type: url
    id: 146
    name: "Versandmöglichkeiten kriteriengeleitet anbieten (LOOP-Kapitel)"
    
  - type: forum
    id: 147
    name: "Forum zur Aufgabe 8: Anschließende Überlegung"
```

### Abschnitt 5: Zahlungskonditionen (← LS03)

```yaml
section:
  id: 50
  name: "4 Zahlungskonditionen kriteriengeleitet anbieten"
  visible: true
  
modules:
  - type: forum
    id: 148
    name: "Forum 4: Zahlungskonditionen kriteriengeleitet anbieten"
    
  - type: url
    id: 149
    name: "Zahlungskonditionen kriteriengeleitet anbieten (LOOP-Kapitel)"
    
  - type: forum
    id: 150
    name: "Forum zur Aufgabe 9: Ausgangssituation Bezahlverfahren"
    
  - type: assign
    id: 151
    name: "Aufgabe 11: Ausgangssituation Kredite"
    
  - type: wiki
    id: 152
    name: "Aufgabe 15: Ausgangssituation Onlinebezahlverfahren"
```

### Abschnitt 6: Checkout beurteilen

```yaml
section:
  id: 51
  name: "5 Den Checkout-Prozess beurteilen und optimieren"
  visible: true
  
modules:
  - type: forum
    id: 153
    name: "Forum 5: Den Checkout-Prozess beurteilen und optimieren"
    
  - type: url
    id: 154
    name: "Den Checkout-Prozess beurteilen und optimieren (LOOP-Kapitel)"
    
  - type: assign
    id: 155
    name: "Aufgabe 17: Ausgangssituation Usability"
```

### Abschnitt 7: Verträge rechtssicher (← LS02)

```yaml
section:
  id: 52
  name: "6 Verträge (im E-Commerce) rechtssicher abschließen"
  visible: true
  
modules:
  - type: forum
    id: 156
    name: "Forum 6: Verträge (im E-Commerce) rechtssicher abschließen"
    
  - type: url
    id: 157
    name: "Verträge (im E-Commerce) rechtssicher abschließen (LOOP-Kapitel)"
    
  - type: assign
    id: 158
    name: "Aufgabe 20: Kaufvertrag"
    
  - type: assign
    id: 159
    name: "Aufgabe 22: Ausgangssituation Widerruf"
    
  - type: forum
    id: 160
    name: "Forum zur Aufgabe 24: Ausgangssituation Rechtssicherer Checkout"
```

### Abschnitt 8: Ware versenden (← LS04 Teil)

```yaml
section:
  id: 53
  name: "7 Ware versenden und Kundenbindung betreiben"
  visible: true
  
modules:
  - type: forum
    id: 161
    name: "Forum 7: Ware versenden und Kundenbindung betreiben"
    
  - type: url
    id: 162
    name: "Ware versenden und Kundenbindung betreiben (LOOP-Kapitel)"
    
  - type: forum
    id: 163
    name: "Forum zur Aufgabe 25: Ausgangssituation Verpackung und Versand"
    
  - type: forum
    id: 164
    name: "Forum zur Aufgabe 26: Ausgangssituation Werbung und Nachhaltigkeit"
```

## Mapping: Lernsituation → Moodle-Abschnitt

| Lernsituation | Moodle-Abschnitt(e) | Anmerkung |
|---------------|---------------------|-----------|
| LS01: Checkout | Abschnitt 2, 6 | Analyse + Optimierung |
| LS02: Kaufverträge | Abschnitt 7 | Verträge rechtssicher |
| LS03: Zahlungsarten | Abschnitt 5 | Zahlungskonditionen |
| LS04: Lieferung | Abschnitt 4, 8 | Versand + Ware versenden |
| (Ergänzung) | Abschnitt 3 | Datenschutz (DSGVO) |

## Matchplan-Struktur

### LS01 Matchplan-Auszug

```
| Lehrhandeln | Schülerhandeln | Begründung |
|-------------|----------------|------------|
| Folien 1-2: Orientierung LF3 | Gemeinsamer Blick | Verankerung im Gesamtkonstrukt |
| Folie 3: "Kauf, du Arsch" | Spagat formulieren (15 min) | Bedeutsamkeit verankern |
| Folie 4-5: Begriffsklärung | Arbeitsauftrag zu zweit | Klärung Checkout-Begriff |
| Folien 6-8: Abbruchgründe | Einzelarbeit (60 min) | Kundensicht fokussieren |
| Folie 9: Fond-of Imagefilm | Aufmerksam gucken | Unternehmen kennenlernen |
| Folie 10: Webshop erkunden | Durchklicken | Orientierung verschaffen |
| Folie 11: Checkout-Prozess | Siehe Folie (45 min) | Schritt ins Unternehmen |
| Folie 12: Deep Dive EPK | Fragen beantworten (30 min) | Abstrahierung |
| Folie 13: EPK anwenden | Prozess visualisieren | EPK-Sprache lernen |
| Folie 14: Offene Fragen | (15 min) | Klärung oder Auslagerung |
```

### Mapping zu Moodle-Aktivitäten

| Matchplan-Element | Moodle-Aktivität |
|-------------------|------------------|
| "Gemeinsamer Blick" | → Label (Einführungstext) |
| "Arbeitsauftrag zu zweit" | → Forum (Diskussion) |
| "Einzelarbeit 60 min" | → Aufgabe oder Forum |
| "Aufmerksam gucken" | → URL (Video-Link) |
| "Durchklicken" | → URL (Webshop-Link) |
| "Fragen beantworten" | → Forum oder Page |
| "Prozess visualisieren" | → Aufgabe (Abgabe) |

## Aktivitäten-Statistik

| Aktivitätstyp | Anzahl | Verwendung |
|---------------|--------|------------|
| Forum | 16 | Hauptdiskussion + Aufgabenforen |
| URL | 7 | LOOP-Kapitel Links |
| Assign | 6 | Aufgaben mit Abgabe |
| Page | 1 | Info-Seite |
| Label | 1 | Willkommenstext |
| Folder | 1 | Lehrer-Material |
| Wiki | 1 | Kollaborative Aufgabe |

## Erstellungs-Befehle (MCP)

### Kurs erstellen

```javascript
// Bereits existiert: Kurs 6
// Bei Neu-Erstellung:
moodle:moodle_create_course({
  fullname: "LF3 - Verträge im Online-Vertrieb anbahnen und bearbeiten",
  shortname: "LF3-ECOM-NEU",
  categoryid: "1",
  format: "topics",
  numsections: "9"
})
```

### Abschnitte konfigurieren

```javascript
// Abschnitt 0
moodle:moodle_update_section({
  courseId: "6",
  sectionNum: "0",
  name: "Lernfeld 3 - Verträge im Online-Vertrieb anbahnen und bearbeiten"
})

// Abschnitt 1 (versteckt)
moodle:moodle_update_section({
  courseId: "6",
  sectionNum: "1",
  name: "Hinweise für Lehrkräfte (für SuS nicht sichtbar)",
  visible: "0"
})

// Abschnitt 2
moodle:moodle_update_section({
  courseId: "6",
  sectionNum: "2",
  name: "1 Den Checkout-Prozess im Online-Vertrieb analysieren"
})

// ... weitere Abschnitte analog
```

### Aktivitäten hinzufügen

```javascript
// Willkommens-Label
moodle:moodle_create_label({
  courseId: "6",
  sectionNum: "0",
  labelText: "<h3>Herzlich Willkommen!</h3><p>In diesem Lernfeld...</p>"
})

// Info-Page
moodle:moodle_create_page({
  courseId: "6",
  sectionNum: "0",
  pageName: "Informationen zur Arbeit mit diesem Modul",
  content: "<h3>Arbeitshinweise</h3><p>So arbeiten Sie mit diesem Kurs...</p>"
})

// LOOP-Link
moodle:moodle_create_url({
  courseId: "6",
  sectionNum: "2",
  name: "Den Checkout-Prozess im Online-Vertrieb analysieren (LOOP-Kapitel)",
  url: "https://loop.oncampus.de/loop/Checkout-Prozess"
})

// Lehrer-Ordner
moodle:moodle_create_folder({
  courseId: "6",
  sectionNum: "1",
  name: "Hinweise zur Arbeit mit diesem Lernfeld für Lehrkräfte",
  itemId: "0"
})
```

---

*Dokumentiert am 2026-01-12 basierend auf Kurs-ID 6 von moodle.dirk-schulenburg.net*
