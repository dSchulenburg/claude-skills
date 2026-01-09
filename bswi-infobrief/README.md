# BS:WI Infobrief Formatter

Ein Claude Code Skill zur professionellen Formatierung von Markdown-Infobriefenim Corporate Design der Beruflichen Schule für Wirtschaft und Internationales Hamburg (BS:WI).

## Features

- **Corporate Design:** Automatische Anwendung der BS:WI Farben und Layouts
- **HTML-Export:** Professionell gestaltete HTML-Dateien für E-Mail oder Web
- **PDF-Export:** Druckfertige PDF-Dokumente (optional)
- **Batch-Verarbeitung:** Konvertiere mehrere Dateien auf einmal
- **Struktur-Erkennung:** Automatische Formatierung von Need-to-know/Nice-to-know Sektionen
- **Responsive Design:** Optimiert für Desktop und Mobile

## Schnellstart

### 1. Einzelnen Infobrief konvertieren

```bash
python scripts/format_infobrief.py "mein-infobrief.md"
```

Erstellt: `mein-infobrief.html` im gleichen Verzeichnis

### 2. Alle Infobriefe im Ordner konvertieren

```bash
python scripts/format_infobrief.py "C:\Infobriefe\2025" --batch
```

### 3. PDF erstellen

```bash
python scripts/format_infobrief.py "wichtig.md" --output pdf
```

**Hinweis:** PDF-Export benötigt `weasyprint`:
```bash
pip install weasyprint
```

### 4. Vorschau im Browser

```bash
python scripts/format_infobrief.py "brief.md" --preview
```

## Markdown-Format

Deine Infobriefe sollten folgende Struktur haben:

```markdown
# Titel des Infobriefs

> **Datum:** 16.12.2025 12:27
> **Von:** Malte Baumann
> **Teams-Link:** https://teams.microsoft.com/...

---

Liebes Kollegium BS05

Need-to-know:

- Save-the-date: Am 21.01.26 findet die LK statt
- Wichtige Information 2
- Wichtige Information 3

Nice-to-know:

- Zusätzliche Information 1
- Zusätzliche Information 2

Abschlusstext...
```

### Metadaten

Die Metadaten werden aus dem Blockquote am Anfang extrahiert:

- **Datum:** Anzeige-Datum
- **Von:** Autor/Absender
- **Teams-Link:** Wird als klickbarer Button angezeigt

### Sektionen

- **Need-to-know:** Wichtige Informationen (gelber Highlight)
- **Nice-to-know:** Zusätzliche Informationen (blauer Highlight)
- **Save-the-date:** Automatisch hervorgehoben bei Erwähnung in Listen

## Corporate Design

### Farben

- **Dunkelblau (#003366):** Header, Footer, Überschriften
- **Hellblau (#00A3E0):** Links, Akzente
- **Neongelb (#B5E505):** BS05-Badge, wichtige Markierungen
- **Weiß (#FFFFFF):** Hintergrund
- **Dunkelgrau (#333333):** Text

### Schriftart

- Arial, Helvetica, sans-serif
- Zeilenhöhe: 1.6 für optimale Lesbarkeit

### Layout

- Maximale Breite: 800px
- Responsive Design für Mobile
- Professionelle Schatten und Abstände

## Kommandozeilen-Optionen

```
python scripts/format_infobrief.py <input> [optionen]

Positionale Argumente:
  input                 Markdown-Datei oder Verzeichnis

Optionen:
  --output {html,pdf}   Ausgabeformat (Standard: html)
  --batch               Alle .md Dateien im Verzeichnis verarbeiten
  --preview             HTML im Browser öffnen
  --no-footer           Ohne Footer erstellen
```

## Beispiele

### Beispiel 1: Einfacher Export
```bash
python scripts/format_infobrief.py "2025-12-16 - Infobrief.md"
```

**Ausgabe:** HTML-Datei mit vollem CI-Design

### Beispiel 2: Batch-Konvertierung
```bash
python scripts/format_infobrief.py "C:\Infobriefe\2025" --batch
```

**Ausgabe:** Alle `.md` Dateien werden zu `.html` konvertiert

### Beispiel 3: PDF für Archivierung
```bash
python scripts/format_infobrief.py "jahresabschluss.md" --output pdf
```

**Ausgabe:** Druckfertige PDF-Datei

### Beispiel 4: Vorschau
```bash
python scripts/format_infobrief.py "entwurf.md" --preview
```

**Ausgabe:** HTML wird erstellt und im Browser geöffnet

## Nutzung in Claude Code

Wenn du in Claude Code arbeitest, kannst du einfach sagen:

```
Formatiere alle Infobriefe im Ordner 2025 im BS:WI Design
```

oder

```
Konvertiere den aktuellen Infobrief zu HTML
```

Der Skill wird automatisch erkannt und verwendet.

## Dateistruktur

```
~/.claude/skills/bswi-infobrief/
├── SKILL.md                    # Skill-Definition
├── README.md                   # Diese Datei
├── REFERENCE.md                # Vollständige API-Dokumentation
├── scripts/
│   └── format_infobrief.py    # Haupt-Konvertierungs-Skript
└── templates/
    └── style.css               # BS:WI Corporate Design CSS
```

## Anpassungen

### Farben ändern

Bearbeite `templates/style.css` und passe die CSS-Variablen an:

```css
:root {
  --bswi-navy: #003366;
  --bswi-lightblue: #00A3E0;
  --bswi-yellow: #B5E505;
  /* ... */
}
```

### Layout anpassen

Ändere die Layout-Variablen in `style.css`:

```css
:root {
  --max-width: 800px;  /* Maximale Breite */
  --spacing: 20px;     /* Standard-Abstände */
}
```

## Fehlerbehebung

### Problem: `FileNotFoundError`
**Lösung:** Überprüfe den Pfad zur Markdown-Datei

### Problem: `ImportError: weasyprint`
**Lösung:** Installiere weasyprint für PDF-Export:
```bash
pip install weasyprint
```

### Problem: Metadaten werden nicht erkannt
**Lösung:** Stelle sicher, dass die Metadaten im Blockquote-Format sind:
```markdown
> **Datum:** ...
> **Von:** ...
```

### Problem: Need-to-know/Nice-to-know nicht formatiert
**Lösung:** Achte auf korrekte Schreibweise:
```markdown
Need-to-know:

- Punkt 1
```

## Weitere Informationen

- **REFERENCE.md:** Vollständige API-Dokumentation
- **SKILL.md:** Skill-Definition und Verwendung in Claude Code

## Support

Bei Fragen oder Problemen:
- Erstelle ein Issue im Repository
- Kontaktiere die IT-Abteilung der BS:WI

---

**Entwickelt für BS:WI Hamburg**
*Kompetent Zukunft gestalten*
