---
name: bswi-infobrief
description: Erstellt schulische Dokumente im offiziellen BS:WI Corporate Design. Nutze diesen Skill für Arbeitsblätter, Handouts, Infobriefe, Formulare, E-Mails oder andere Unterlagen der BS:WI Hamburg. Unterstützt HTML, DOCX und PDF. Trigger-Phrasen: "Schuldokument", "Arbeitsblatt", "BS:WI", "Unterrichtsmaterial", "Handout", "Formular erstellen".
---

# BS:WI Dokument-Generator

Erstellt professionelle Unterlagen im Corporate Design der **Beruflichen Schule für Wirtschaft und Internationales Hamburg** (BS:WI / BS05).

## Verfügbare Templates

| Template | Datei | Verwendung |
|----------|-------|------------|
| Arbeitsblatt | `templates/arbeitsblatt.html` | Übungen, Aufgaben, Tests |
| Infobrief | `templates/infobrief.html` | Newsletter, Mitteilungen |
| Handout | `templates/handout.html` | Kurzanleitungen, DaZ-geeignet |
| Formular | `templates/formular.html` | Anträge, Anmeldungen |
| E-Mail | `templates/email.html` | Professionelle E-Mails |
| Präsentation | `templates/praesentation_guide.md` | PowerPoint mit BSWI_Master.pptx |

## Ausgabeformate

- **HTML**: Direkt im Browser, perfekt für digitale Nutzung
- **DOCX**: Word-Dokument mit `docx-generator.js`
- **PDF**: Aus DOCX via LibreOffice konvertiert

---

## Corporate Design Spezifikationen

### Primärfarben (Blau-Palette)

| Name | HEX | Verwendung |
|------|-----|------------|
| Blau 1 | `#1C3D71` | Headlines, Rahmen, Footer-Border |
| Blau 2 | `#102141` | Dunkler Hintergrund |
| Blau 3 | `#1266B0` | Untertitel, Links, Claim |
| Blau 4 | `#008BC9` | Akzent-Ränder, Buttons |
| Blau 5 | `#41C0F0` | Trennlinien, Highlights |
| Blau 6 | `#A4DBF8` | Tabellen-Rahmen |
| Blau 7 | `#EAF6FE` | Hintergründe (Info-Boxen, Header) |

### Sekundärfarben

| Name | HEX | Verwendung |
|------|-----|------------|
| Akzent | `#E8FF00` | Neongelb für Warnungen, Need-to-know |
| Schwarz | `#000000` | Text |
| Dunkelgrau | `#666666` | Sekundärtext, Labels |
| Hellgrau | `#F6F6F6` | Aufgaben-Box Hintergrund |

### Typografie

- **Schrift**: Montserrat (Google Fonts), Fallback: Arial
- **Titel**: 15-18pt, Bold, Blau 1
- **Untertitel**: 10-12pt, Medium, Blau 3
- **Fließtext**: 11pt, Regular
- **Footer**: 8.5pt

---

## Header-Layout (3-Spalten)

```
┌──────────────────────────────────────────────────────────┐
│ [LOGO]  │  Titel (zentriert)   │  Name: _______         │
│         │  Untertitel          │  Datum: _______        │
├──────────────────────────────────────────────────────────┤
│                    (2.5px Border Blau 1)                 │
```

### Logo SVG (Inline)

```svg
<svg viewBox="0 0 692.7 566.9" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="g1" x1="399.7" y1="366.2" x2="1258.5" y2="80.8" gradientUnits="userSpaceOnUse">
      <stop offset="0.3" stop-color="#41C0F0"/><stop offset="0.4" stop-color="#A4DBF8"/>
    </linearGradient>
    <linearGradient id="g2" x1="212.7" y1="462.7" x2="-54.8" y2="242.1" gradientUnits="userSpaceOnUse">
      <stop offset="0.3" stop-color="#067AA7"/><stop offset="0.6" stop-color="#41C0F0"/><stop offset="1" stop-color="#A4DBF8"/>
    </linearGradient>
    <linearGradient id="g3" x1="241.1" y1="340.2" x2="423.9" y2="424.6" gradientUnits="userSpaceOnUse">
      <stop offset="0.1" stop-color="#067AA7"/><stop offset="0.3" stop-color="#41C0F0"/><stop offset="1" stop-color="#A4DBF8"/>
    </linearGradient>
    <linearGradient id="g4" x1="515.2" y1="15.2" x2="280.7" y2="716.7" gradientUnits="userSpaceOnUse">
      <stop offset="0.1" stop-color="#0E66AF"/><stop offset="0.7" stop-color="#1B3D71"/>
    </linearGradient>
  </defs>
  <path d="M689.4 0 616.1 18.8C603.2 22.1 593.8 31.7 590.4 44.5L450.2 566.9 624.9 566.9 689.4 0Z" fill="url(#g1)"/>
  <path d="M156.2 136.4 29.8 168.7C13.7 172.9 0 189.5 0 206.2L0 567 156.2 567 156.2 136.4Z" fill="url(#g2)"/>
  <path d="M220.5 566.9 385.9 566.9 369.5 163.2 248.5 194.2 220.5 566.9Z" fill="url(#g3)"/>
  <path d="M248.5 194.2 0 566.9 156.2 566.9 369.5 163.2 248.4 194.2ZM460.2 58.7 220.5 567 385.9 567 559.5 33.3 460.2 58.7ZM680 157.5 586.1 60.7 450.3 567 661.6 567 692.6 185.5C693.6 173 689.1 167 680 157.6Z" fill="url(#g4)"/>
</svg>
```

Logo PNG: `Logo_BSWI_Quer_RGB.png` (562x180px, Seitenverhältnis 3.12:1)

---

## Footer-Layout

```
┌──────────────────────────────────────────────────────────┐
│ (2px Border Blau 1)                                      │
│ Dirk Schulenburg · BS:WI    Kompetent Zukunft Gestalten  │
│                             (kursiv, Blau 3)   Seite X/Y │
└──────────────────────────────────────────────────────────┘
```

- Weißer Hintergrund
- Obere Trennlinie: 2px Blau 1
- Links: "Dirk Schulenburg · BS:WI" (grau)
- Mitte/Rechts: Claim kursiv in Blau 3
- Bei mehrseitigen Dokumenten: "Seite X von Y"

---

## Design-Komponenten

### Aufgaben-Box

```css
.bswi-task {
    background: #F6F6F6;
    border: 2px solid #008BC9;
    border-left-width: 6px;
    border-radius: 10px;
    padding: 14px 18px;
}
```

- Header mit Icon 📝, Titel und Punkte-Badge
- Hellgrauer Hintergrund
- Dicker Akzent-Rand links (Blau 4)

### Info-Box / Tipp

```css
.bswi-info {
    background: #EAF6FE;
    border-left: 5px solid #008BC9;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
}
```

- Icon 💡 für Tipps, ✅ für Selbstkontrolle
- Blau 7 Hintergrund

### Formel-Box

```css
.formel-box {
    background: #1C3D71;
    color: #fff;
    border-radius: 10px;
    padding: 16px 20px;
    text-align: center;
    font-family: 'Times New Roman', serif;
    font-style: italic;
}
```

### Lernziele-Box

```css
.lernziele-box {
    background: linear-gradient(135deg, #EAF6FE 0%, #fff 100%);
    border: 2px solid #008BC9;
    border-radius: 12px;
}
```

- Icon 🎯
- Bullet-Liste mit Lernzielen

### Tabellen

- Header: Blau 1 Hintergrund, weiße Schrift
- Zeilen: Zebra-Streifen mit Blau 7
- Rahmen: Blau 6

### Eingabezeilen (Print)

```css
.bswi-input-line { border-bottom: 1.5px solid #666; min-height: 2em; }
.bswi-input-line.short { width: 40%; }
.bswi-input-line.inline { width: 60px; display: inline-block; }
```

---

## Mehrseitige Dokumente

### HTML: Seitenumbrüche

```css
.page {
    width: 210mm;
    height: 297mm;
    page-break-after: always;
    page-break-inside: avoid;
}

@media print {
    .page { page-break-after: always; }
    .page:last-child { page-break-after: auto; }
}
```

### DOCX: Seitenumbrüche

```javascript
new Paragraph({ children: [new PageBreak()] })
```

### Seitenzahlen im Footer

- HTML: Manuell "Seite 1 von 2" in jeder `.page`
- DOCX: `PageNumber.CURRENT` und `PageNumber.TOTAL_PAGES`

---

## DOCX-Erstellung

Verwende `docx-generator.js` für Word-Dokumente:

```bash
npm install docx
node docx-generator.js
```

### Logo in DOCX (korrektes Seitenverhältnis)

```javascript
new ImageRun({
    data: logoBuffer,
    transformation: { width: 112, height: 36 }, // 562:180 = 3.12:1
    type: "png"
})
```

### Header-Tabelle (3 Spalten)

```javascript
new Table({
    columnWidths: [2000, 5500, 2966],
    rows: [
        new TableRow({
            children: [
                // Logo links
                new TableCell({ children: [logoImage] }),
                // Titel mitte
                new TableCell({ children: [title, subtitle] }),
                // Name/Datum rechts
                new TableCell({ children: [nameField, dateField] })
            ]
        })
    ]
})
```

---

## PDF-Erstellung

```bash
python3 scripts/office/soffice.py --headless --convert-to pdf dokument.docx --outdir ./
```

---

## Kontaktdaten

```
Dirk Schulenburg
BS:WI – Berufliche Schule für Wirtschaft und Internationales
Hinrichsenstraße 35 · 20535 Hamburg
dirk.schulenburg@bs05.hamburg.de
Tel: +49 40 428 976 - 0
www.bswi.hamburg
```

---

## Claim

> **Kompetent Zukunft Gestalten**

---

## Bildsprache

> **Echt, freundlich, weltoffen, international**
