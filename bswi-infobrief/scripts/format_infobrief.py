#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BS:WI Infobrief Formatter
Konvertiert Markdown-Infobriefe in HTML/PDF mit Corporate Design
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
import html
import io
import base64

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class InfobriefFormatter:
    """Formatiert BS:WI Infobriefe im Corporate Design"""

    def __init__(self, input_file: Path):
        self.input_file = Path(input_file)
        if not self.input_file.exists():
            raise FileNotFoundError(f"Datei nicht gefunden: {input_file}")

        self.content = self.input_file.read_text(encoding='utf-8')
        self.metadata = {}
        self.title = ""
        self.body = ""

        self._parse()

    def _parse(self):
        """Extrahiere Titel, Metadaten und Body"""
        lines = self.content.split('\n')

        # Titel extrahieren (erste Zeile mit #)
        title_match = re.match(r'^#\s+(.+)$', lines[0])
        if title_match:
            self.title = title_match.group(1).strip()

        # Metadaten aus Blockquote extrahieren
        metadata_section = []
        in_metadata = False
        content_start = 0

        for i, line in enumerate(lines):
            if line.strip().startswith('>'):
                in_metadata = True
                metadata_section.append(line.lstrip('> ').strip())
            elif in_metadata and line.strip() == '':
                content_start = i + 1
                break

        # Parse Metadaten
        for meta_line in metadata_section:
            if meta_line.startswith('**Datum:**'):
                self.metadata['datum'] = meta_line.replace('**Datum:**', '').strip()
            elif meta_line.startswith('**Von:**'):
                self.metadata['von'] = meta_line.replace('**Von:**', '').strip()
            elif meta_line.startswith('**Teams-Link:**'):
                self.metadata['teams_link'] = meta_line.replace('**Teams-Link:**', '').strip()

        # Body extrahieren (nach Metadaten und ----)
        body_lines = lines[content_start:]
        # Überspringe --- Trennlinie
        if body_lines and body_lines[0].strip() == '---':
            body_lines = body_lines[1:]

        self.body = '\n'.join(body_lines).strip()

    def _process_body(self) -> str:
        """Verarbeite Body und füge CSS-Klassen hinzu"""
        lines = self.body.split('\n')
        processed = []
        in_need_to_know = False
        in_nice_to_know = False
        in_list = False

        for line in lines:
            # Erkenne Sektionen
            if re.match(r'^Need-to-know:', line, re.IGNORECASE):
                if in_need_to_know or in_nice_to_know:
                    processed.append('</div>')
                processed.append('<div class="section-needtoknow">')
                processed.append('<h3>Need-to-know</h3>')
                in_need_to_know = True
                in_nice_to_know = False
                continue

            elif re.match(r'^Nice-to-know:', line, re.IGNORECASE):
                if in_need_to_know or in_nice_to_know:
                    processed.append('</div>')
                processed.append('<div class="section-nicetoknow">')
                processed.append('<h3>Nice-to-know</h3>')
                in_nice_to_know = True
                in_need_to_know = False
                continue

            # Erkenne Listen
            if re.match(r'^[-*]\s', line):
                if not in_list:
                    processed.append('<ul>')
                    in_list = True
                # Extrahiere List-Item Text
                item_text = re.sub(r'^[-*]\s', '', line)
                # Highlight "Save-the-date"
                if 'save-the-date' in item_text.lower():
                    processed.append(f'<li class="save-the-date">{self._markdown_inline(item_text)}</li>')
                else:
                    processed.append(f'<li>{self._markdown_inline(item_text)}</li>')
                continue
            else:
                if in_list:
                    processed.append('</ul>')
                    in_list = False

            # Normale Zeilen
            if line.strip():
                # Überschriften
                heading_match = re.match(r'^(#{2,6})\s+(.+)$', line)
                if heading_match:
                    level = len(heading_match.group(1))
                    text = heading_match.group(2)
                    processed.append(f'<h{level}>{html.escape(text)}</h{level}>')
                else:
                    # Paragraphen
                    processed.append(f'<p>{self._markdown_inline(line)}</p>')
            else:
                if not in_list:
                    processed.append('')

        # Schließe offene Sektionen
        if in_list:
            processed.append('</ul>')
        if in_need_to_know or in_nice_to_know:
            processed.append('</div>')

        return '\n'.join(processed)

    def _markdown_inline(self, text: str) -> str:
        """Verarbeite Inline-Markdown (Bold, Italic, Links)"""
        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        # Links
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
        # Escape remaining HTML
        # text = html.escape(text)
        return text

    def generate_html(self, include_footer: bool = True) -> str:
        """Generiere komplettes HTML-Dokument"""

        # Lade CSS
        css_path = Path(__file__).parent.parent / 'templates' / 'style.css'
        css_content = ""
        if css_path.exists():
            css_content = css_path.read_text(encoding='utf-8')

        # Logo als Base64 für PDF-Kompatibilität
        logo_path = Path(__file__).parent.parent / 'templates' / 'Logo_BSWI_Quer_RGB.png'
        logo_data_uri = None
        if logo_path.exists():
            with open(logo_path, 'rb') as logo_file:
                logo_base64 = base64.b64encode(logo_file.read()).decode('utf-8')
                logo_data_uri = f'data:image/png;base64,{logo_base64}'

        # Datum formatieren
        datum = self.metadata.get('datum', '')
        von = self.metadata.get('von', 'BS:WI Hamburg')
        teams_link = self.metadata.get('teams_link', '')

        # Metadaten HTML
        metadata_html = '<div class="metadata">'
        if datum:
            metadata_html += f'<p><strong>Datum:</strong> {html.escape(datum)}</p>'
        if von:
            metadata_html += f'<p><strong>Von:</strong> {html.escape(von)}</p>'
        if teams_link:
            metadata_html += f'<p><strong>Teams:</strong> <a href="{html.escape(teams_link)}" class="teams-link">Zum Teams-Beitrag</a></p>'
        metadata_html += '</div>'

        # Body verarbeiten
        body_html = self._process_body()

        # Logo HTML
        logo_html = f'<img src="{logo_data_uri}" alt="BS:WI Hamburg Logo">' if logo_data_uri else ''

        # Footer
        footer_html = ""
        if include_footer:
            footer_html = '''
<div class="footer">
  <div class="footer-logo">
    <p><strong>BS:WI Hamburg</strong></p>
  </div>
  <p>Berufliche Schule für Wirtschaft und Internationales Hamburg</p>
  <p>Kompetent Zukunft gestalten</p>
  <div class="footer-links">
    <a href="https://bswi.hamburg">bswi.hamburg</a>
    <a href="mailto:bs05@hibb.hamburg.de">bs05@hibb.hamburg.de</a>
  </div>
</div>
'''

        # Komplettes HTML
        html_doc = f'''<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(self.title)} - BS:WI Hamburg</title>
  <style>
{css_content}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="header-logo">
        {logo_html}
        <div>
          <p class="header-title">Berufliche Schule für Wirtschaft und Internationales Hamburg</p>
        </div>
      </div>
      <h1>{html.escape(self.title)} <span class="bs-badge">BS 05</span></h1>
    </div>

    {metadata_html}

    <div class="content">
      {body_html}
    </div>

    {footer_html}
  </div>
</body>
</html>
'''

        return html_doc

    def save_html(self, output_path: Optional[Path] = None) -> Path:
        """Speichere HTML-Datei"""
        if output_path is None:
            output_path = self.input_file.with_suffix('.html')

        html_content = self.generate_html()
        output_path.write_text(html_content, encoding='utf-8')

        return output_path

    def save_pdf(self, output_path: Optional[Path] = None) -> Path:
        """Speichere als PDF (benötigt weasyprint)"""
        try:
            from weasyprint import HTML
        except ImportError:
            print("FEHLER: weasyprint nicht installiert. Installiere mit: pip install weasyprint", file=sys.stderr)
            sys.exit(1)

        if output_path is None:
            output_path = self.input_file.with_suffix('.pdf')

        html_content = self.generate_html()
        HTML(string=html_content).write_pdf(output_path)

        return output_path


def process_batch(input_dir: Path, output_format: str = 'html'):
    """Verarbeite alle Markdown-Dateien in einem Verzeichnis"""
    md_files = list(input_dir.glob('*.md'))

    if not md_files:
        print(f"Keine Markdown-Dateien in {input_dir} gefunden.", file=sys.stderr)
        return

    print(f"Verarbeite {len(md_files)} Dateien...")

    for md_file in md_files:
        try:
            formatter = InfobriefFormatter(md_file)

            if output_format == 'html':
                output = formatter.save_html()
                print(f"✓ {md_file.name} → {output.name}")
            elif output_format == 'pdf':
                output = formatter.save_pdf()
                print(f"✓ {md_file.name} → {output.name}")

        except Exception as e:
            print(f"✗ {md_file.name}: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description='BS:WI Infobrief Formatter - Konvertiert Markdown zu HTML/PDF mit Corporate Design'
    )
    parser.add_argument('input', help='Markdown-Datei oder Verzeichnis')
    parser.add_argument('--output', choices=['html', 'pdf'], default='html', help='Ausgabeformat (default: html)')
    parser.add_argument('--batch', action='store_true', help='Verarbeite alle .md Dateien im Verzeichnis')
    parser.add_argument('--preview', action='store_true', help='Öffne Ausgabe im Browser')
    parser.add_argument('--no-footer', action='store_true', help='Ohne Footer')

    args = parser.parse_args()

    input_path = Path(args.input)

    if not input_path.exists():
        print(f"FEHLER: {input_path} existiert nicht.", file=sys.stderr)
        sys.exit(1)

    try:
        # Batch-Modus
        if args.batch or input_path.is_dir():
            if not input_path.is_dir():
                print("FEHLER: --batch benötigt ein Verzeichnis.", file=sys.stderr)
                sys.exit(1)
            process_batch(input_path, args.output)

        # Einzeldatei
        else:
            formatter = InfobriefFormatter(input_path)

            if args.output == 'html':
                output = formatter.save_html()
                print(f"✓ HTML erstellt: {output}")

                if args.preview:
                    import webbrowser
                    webbrowser.open(output.absolute().as_uri())

            elif args.output == 'pdf':
                output = formatter.save_pdf()
                print(f"✓ PDF erstellt: {output}")

    except Exception as e:
        print(f"FEHLER: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
