---
name: bswi-infobrief
description: Formatiert Markdown-Infobriefe im Corporate Design der BS:WI Hamburg. Nutze diesen Skill, um Infobriefe professionell zu gestalten, HTML/PDF zu exportieren und das CI der Schule (Farben, Logo, Layout) anzuwenden.
license: MIT
agent: Education
allowed-tools: Read, Glob, Bash(python:*), Write, Edit
---

# BS:WI Infobrief Formatter

## Überblick

Dieser Skill formatiert deine Markdown-Infobriefe im Corporate Design der Beruflichen Schule für Wirtschaft und Internationales Hamburg (BS:WI). Er wandelt einfache Markdown-Dateien in professionell gestaltete HTML- oder PDF-Dokumente mit dem offiziellen CI um.

**Features:**
- Automatische Anwendung der BS:WI Farben (Dunkelblau, Hellblau, Neongelb)
- Professionelles Header-Design mit Schullogo
- Strukturierte Darstellung von "Need-to-know" und "Nice-to-know" Abschnitten
- HTML-Export für E-Mail-Versand oder Web-Veröffentlichung
- Optional: PDF-Export für Druck oder Archivierung
- Metadaten-Extraktion (Datum, Autor, Teams-Link)

## Verwendung

### HTML-Datei erstellen
```bash
python scripts/format_infobrief.py "pfad/zur/datei.md" --output html
```

### PDF erstellen
```bash
python scripts/format_infobrief.py "pfad/zur/datei.md" --output pdf
```

### Alle Infobriefe im Ordner konvertieren
```bash
python scripts/format_infobrief.py "ordner/" --batch --output html
```

### Vorschau im Browser
```bash
python scripts/format_infobrief.py "datei.md" --preview
```

## Corporate Design Details

**Farben:**
- **Primär Dunkelblau:** #003366 (Header, Footer, Überschriften)
- **Akzent Hellblau:** #00A3E0 (Links, Highlights)
- **Signal Neongelb:** #B5E505 (Wichtige Markierungen, BS05-Branding)
- **Hintergrund Weiß:** #FFFFFF
- **Text Dunkelgrau:** #333333

**Typografie:**
- Überschriften: Sans-Serif (Arial, Helvetica)
- Fließtext: Sans-Serif (Arial, Helvetica)
- Zeilenhöhe: 1.6 für optimale Lesbarkeit

**Layout:**
- Maximale Breite: 800px
- Seitenränder: 40px
- Abschnitte klar getrennt mit visuellen Markern

## Beispiele

### Beispiel 1: Einzelner Infobrief
```bash
python scripts/format_infobrief.py "2025-12-16 - Infobrief.md" --output html
```

Erstellt: `2025-12-16 - Infobrief.html` im gleichen Ordner

### Beispiel 2: Batch-Konvertierung
```bash
python scripts/format_infobrief.py "C:\Infobriefe\2025" --batch --output html
```

Konvertiert alle `.md` Dateien im Ordner zu HTML

### Beispiel 3: PDF mit Logo
```bash
python scripts/format_infobrief.py "wichtig.md" --output pdf --logo templates/bswi-logo.png
```

## Konfiguration

Erstelle eine `.bswi-config.yml` im Projektordner für benutzerdefinierte Einstellungen:

```yaml
colors:
  primary: "#003366"
  accent: "#00A3E0"
  highlight: "#B5E505"

layout:
  max_width: 800
  font_family: "Arial, Helvetica, sans-serif"

export:
  include_toc: false
  include_footer: true
  footer_text: "BS:WI Hamburg – Kompetent Zukunft gestalten"
```

## Struktur-Erkennung

Der Skill erkennt automatisch:
- **Metadaten:** Datum, Autor, Teams-Link (aus Blockquote am Anfang)
- **Kategorien:** Need-to-know, Nice-to-know (mit visuellen Markern)
- **Listen:** Automatische Formatierung mit Bullet-Points
- **Links:** Teams-Links werden hervorgehoben

## Weitere Optionen

Siehe [REFERENCE.md](REFERENCE.md) für vollständige API-Dokumentation und erweiterte Optionen.
