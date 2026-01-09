# BS:WI Infobrief Formatter - Referenzdokumentation

## Übersicht

Vollständige API-Referenz für den BS:WI Infobrief Formatter.

## Kommandozeilen-Tool

### `format_infobrief.py`

Hauptskript zur Konvertierung von Markdown-Infobriefenin HTML oder PDF.

**Syntax:**
```bash
python scripts/format_infobrief.py <input> [optionen]
```

**Positionale Argumente:**
- `input`: Pfad zur Markdown-Datei oder Verzeichnis (bei --batch)

**Optionen:**
- `--output {html,pdf}`: Ausgabeformat (Standard: html)
- `--batch`: Verarbeite alle .md Dateien im Verzeichnis
- `--preview`: Öffne HTML-Ausgabe automatisch im Browser
- `--no-footer`: Erstelle Dokument ohne Footer

### Beispiele

#### Einzelne Datei zu HTML
```bash
python scripts/format_infobrief.py "2025-12-16 - Infobrief.md"
```

**Ausgabe:** `2025-12-16 - Infobrief.html` im gleichen Verzeichnis

#### Einzelne Datei zu PDF
```bash
python scripts/format_infobrief.py "Infobrief.md" --output pdf
```

**Hinweis:** PDF-Export benötigt `weasyprint`:
```bash
pip install weasyprint
```

#### Alle Dateien im Ordner konvertieren
```bash
python scripts/format_infobrief.py "C:\Infobriefe\2025" --batch
```

#### Vorschau im Browser
```bash
python scripts/format_infobrief.py "wichtig.md" --preview
```

Öffnet die generierte HTML-Datei automatisch im Standard-Browser.

## Python API

### Klasse: `InfobriefFormatter`

#### Initialisierung
```python
from format_infobrief import InfobriefFormatter

formatter = InfobriefFormatter(Path("mein-infobrief.md"))
```

#### Attribute
- `input_file` (Path): Pfad zur Eingabedatei
- `content` (str): Roher Markdown-Inhalt
- `metadata` (dict): Extrahierte Metadaten (datum, von, teams_link)
- `title` (str): Extrahierter Titel
- `body` (str): Body-Inhalt (ohne Metadaten)

#### Methoden

##### `generate_html(include_footer: bool = True) -> str`
Generiert vollständiges HTML-Dokument als String.

**Parameter:**
- `include_footer`: Ob Footer eingebunden werden soll (Standard: True)

**Rückgabe:** HTML-String mit kompletter Struktur

**Beispiel:**
```python
formatter = InfobriefFormatter(Path("brief.md"))
html = formatter.generate_html(include_footer=True)
print(html)
```

##### `save_html(output_path: Optional[Path] = None) -> Path`
Speichert HTML-Dokument in Datei.

**Parameter:**
- `output_path`: Ziel-Pfad (Standard: gleicher Name wie Input mit .html)

**Rückgabe:** Path-Objekt der erstellten Datei

**Beispiel:**
```python
formatter = InfobriefFormatter(Path("brief.md"))
output = formatter.save_html()  # Erstellt brief.html
print(f"Gespeichert: {output}")
```

##### `save_pdf(output_path: Optional[Path] = None) -> Path`
Speichert Dokument als PDF.

**Voraussetzung:** `weasyprint` muss installiert sein

**Parameter:**
- `output_path`: Ziel-Pfad (Standard: gleicher Name wie Input mit .pdf)

**Rückgabe:** Path-Objekt der erstellten Datei

**Beispiel:**
```python
formatter = InfobriefFormatter(Path("brief.md"))
output = formatter.save_pdf(Path("ausgabe.pdf"))
```

#### Private Methoden

##### `_parse()`
Extrahiert Titel, Metadaten und Body aus dem Markdown-Inhalt.

##### `_process_body() -> str`
Verarbeitet Body und fügt HTML-Struktur mit CSS-Klassen hinzu.
Erkennt:
- Need-to-know / Nice-to-know Sektionen
- Listen und List-Items
- Save-the-date Markierungen
- Überschriften

##### `_markdown_inline(text: str) -> str`
Verarbeitet Inline-Markdown:
- `**text**` → `<strong>text</strong>`
- `*text*` → `<em>text</em>`
- `[text](url)` → `<a href="url">text</a>`

## Markdown-Format-Anforderungen

### Erwartete Struktur

```markdown
# Titel des Infobriefs

> **Datum:** 16.12.2025 12:27
> **Von:** Malte Baumann
> **Teams-Link:** https://teams.microsoft.com/...

---

Einleitungstext...

Need-to-know:

- Wichtiger Punkt 1
- Save-the-date: Termin am...
- Wichtiger Punkt 2

Nice-to-know:

- Zusatzinfo 1
- Zusatzinfo 2

Abschlusstext...
```

### Metadaten

Metadaten werden aus dem Blockquote am Anfang extrahiert:
```markdown
> **Datum:** <datum>
> **Von:** <autor>
> **Teams-Link:** <url>
```

**Unterstützte Felder:**
- `Datum`: Wird im Metadaten-Bereich angezeigt
- `Von`: Autor/Absender
- `Teams-Link`: Wird als Button verlinkt

### Sektionen

#### Need-to-know
Markiert wichtige Informationen mit gelbem Highlight.

```markdown
Need-to-know:

- Punkt 1
- Punkt 2
```

#### Nice-to-know
Markiert zusätzliche Informationen mit blauem Highlight.

```markdown
Nice-to-know:

- Info 1
- Info 2
```

### Spezielle Markierungen

#### Save-the-date
Listen-Punkte mit "Save-the-date" werden besonders hervorgehoben:

```markdown
- Save-the-date: Am 21.01.26 findet die LK statt
```

## CSS-Anpassungen

Die Standard-Styles befinden sich in `templates/style.css`.

### CSS-Variablen

```css
:root {
  --bswi-navy: #003366;        /* Primärfarbe */
  --bswi-lightblue: #00A3E0;   /* Akzentfarbe */
  --bswi-yellow: #B5E505;      /* Highlight */
  --bswi-white: #FFFFFF;
  --bswi-gray: #333333;
  --bswi-lightgray: #F5F5F5;

  --max-width: 800px;          /* Maximale Breite */
  --spacing: 20px;
  --border-radius: 4px;
}
```

### CSS-Klassen

| Klasse | Beschreibung |
|--------|--------------|
| `.container` | Haupt-Container (max-width, Schatten) |
| `.header` | Header mit Gradient und Logo |
| `.header-logo` | Logo-Bereich |
| `.bs-badge` | "BS 05" Badge in Gelb |
| `.metadata` | Metadaten-Box (Datum, Von, Teams) |
| `.content` | Haupt-Inhaltsbereich |
| `.section-needtoknow` | Need-to-know Sektion (gelb) |
| `.section-nicetoknow` | Nice-to-know Sektion (blau) |
| `.teams-link` | Teams-Button |
| `.save-the-date` | Save-the-date Highlight |
| `.footer` | Footer mit Kontaktdaten |

### Eigene Styles einbinden

Erstelle eine Datei `custom-style.css` und modifiziere das Skript, um sie einzubinden.

## Fehlerbehandlung

### Häufige Fehler

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| `FileNotFoundError` | Datei existiert nicht | Pfad überprüfen |
| `ImportError: weasyprint` | weasyprint nicht installiert | `pip install weasyprint` |
| `UnicodeDecodeError` | Falsche Kodierung | Datei muss UTF-8 sein |

### Debugging

Fehlerhafte Metadaten oder Struktur? Teste mit:

```python
formatter = InfobriefFormatter(Path("brief.md"))
print(formatter.metadata)  # Zeigt extrahierte Metadaten
print(formatter.title)     # Zeigt Titel
```

## Erweiterungen

### Logo hinzufügen

1. Speichere Logo als `templates/bswi-logo.png`
2. Modifiziere `generate_html()`:

```python
logo_path = Path(__file__).parent.parent / 'templates' / 'bswi-logo.png'
if logo_path.exists():
    # Logo als Base64 einbetten oder verlinken
    pass
```

### Konfigurationsdatei

Erstelle `.bswi-config.yml` im Projektroot:

```yaml
colors:
  primary: "#003366"
  accent: "#00A3E0"
  highlight: "#B5E505"

layout:
  max_width: 800
  font_family: "Arial, Helvetica, sans-serif"

export:
  include_footer: true
  footer_text: "BS:WI Hamburg – Kompetent Zukunft gestalten"
```

## Performance

- **HTML-Generierung:** < 100ms pro Datei
- **PDF-Generierung:** ~ 1-2s pro Datei (abhängig von weasyprint)

**Tipp:** Für große Mengen nutze `--batch` für parallele Verarbeitung.

## Lizenz & Support

Entwickelt für BS:WI Hamburg.

Bei Fragen oder Problemen wende dich an die IT-Abteilung oder erstelle ein Issue im Repository.
