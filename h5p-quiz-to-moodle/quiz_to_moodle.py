#!/usr/bin/env python3
"""
H5P Quiz to Moodle - Generiert Quiz und laedt zu Moodle hoch

Usage:
    python quiz_to_moodle.py --questions "Q1\\nQ2\\n..." --title "Quiz" --course 2

Oder als Modul:
    from quiz_to_moodle import create_and_upload_quiz
    result = create_and_upload_quiz(questions_text, title, course_id)
"""

import argparse
import base64
import json
import os
import sys
import requests
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# H5P Generator importieren
sys.path.insert(0, str(Path(__file__).parent.parent / "h5p-generator" / "scripts"))


@dataclass
class QuizResult:
    """Ergebnis der Quiz-Erstellung und Upload"""
    success: bool
    content_id: Optional[int] = None
    title: Optional[str] = None
    filename: Optional[str] = None
    course_id: Optional[int] = None
    embed_url: Optional[str] = None
    h5p_path: Optional[str] = None
    error: Optional[str] = None
    questions_count: int = 0

    def __str__(self):
        if self.success:
            return f"""
H5P Quiz erstellt und zu Moodle hochgeladen!

| Eigenschaft | Wert |
|-------------|------|
| Content ID | {self.content_id} |
| Titel | {self.title} |
| Fragen | {self.questions_count} |
| Kurs ID | {self.course_id} |

Embed URL: {self.embed_url}
"""
        else:
            return f"Fehler: {self.error}"


def create_and_upload_quiz(
    questions_text: str,
    title: str = "Quiz",
    course_id: int = 2,
    domain: str = None,
    mcp_url: str = None,
    api_key: str = None
) -> QuizResult:
    """
    Erstellt H5P Quiz und laedt es zu Moodle hoch.

    Args:
        questions_text: Fragen im h5p-generator Format
        title: Quiz-Titel
        course_id: Moodle Kurs-ID
        domain: Fachbereich fuer Distraktoren
        mcp_url: Moodle MCP URL (default: aus env)
        api_key: MCP API Key (default: aus env)

    Returns:
        QuizResult
    """
    # Defaults aus Umgebung
    mcp_url = mcp_url or os.environ.get(
        "MOODLE_MCP_URL",
        "https://mcp-moodle.dirk-schulenburg.net/mcp"
    )
    api_key = api_key or os.environ.get(
        "MOODLE_MCP_API_KEY",
        "ae9ee37c6c6fb8e22e49a15c12bc819b8cd9e338ec27af4a5414affd5b1e7d61"
    )

    try:
        # 1. H5P erstellen
        from h5p_system import H5PSystem

        # Output-Verzeichnis
        output_dir = Path(__file__).parent / "output"
        output_dir.mkdir(exist_ok=True)

        system = H5PSystem(output_dir=str(output_dir))
        result = system.generate_from_questions(
            questions_text,
            title=title,
            domain=domain
        )

        if not result.success or not result.h5p_files:
            return QuizResult(
                success=False,
                error=f"H5P-Generierung fehlgeschlagen: {'; '.join(result.errors)}"
            )

        h5p_path = result.h5p_files[0]
        questions_count = result.statistics.get('questions_parsed', 0)

        # 2. H5P Datei als Base64 lesen
        with open(h5p_path, 'rb') as f:
            h5p_base64 = base64.b64encode(f.read()).decode('utf-8')

        # 3. Zu Moodle hochladen
        safe_title = "".join(c if c.isalnum() or c in '-_ ' else '-' for c in title)
        filename = f"{safe_title.lower().replace(' ', '-')}.h5p"

        payload = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': 'tools/call',
            'params': {
                'name': 'moodle_upload_h5p',
                'arguments': {
                    'base64data': h5p_base64,
                    'filename': filename,
                    'title': title,
                    'courseid': course_id
                }
            }
        }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream',
            'x-api-key': api_key
        }

        response = requests.post(mcp_url, json=payload, headers=headers, timeout=60, stream=True)

        if response.status_code != 200:
            return QuizResult(
                success=False,
                error=f"Moodle Upload fehlgeschlagen: HTTP {response.status_code}",
                h5p_path=str(h5p_path),
                questions_count=questions_count
            )

        # SSE Response parsen
        raw = response.content.decode('utf-8')
        content_id = None
        embed_url = None

        for line in raw.split('\n'):
            if line.startswith('data:'):
                try:
                    event_data = json.loads(line[5:].strip())
                    if 'result' in event_data:
                        text = event_data['result'].get('content', [{}])[0].get('text', '')

                        # Content ID extrahieren
                        import re
                        id_match = re.search(r'\*\*Content ID\*\*\s*\|\s*(\d+)', text)
                        if id_match:
                            content_id = int(id_match.group(1))

                        # Embed URL extrahieren
                        url_match = re.search(r'\*\*Embed URL:\*\*\s*(https?://[^\s]+)', text)
                        if url_match:
                            embed_url = url_match.group(1)
                except:
                    pass

        return QuizResult(
            success=True,
            content_id=content_id,
            title=title,
            filename=filename,
            course_id=course_id,
            embed_url=embed_url,
            h5p_path=str(h5p_path),
            questions_count=questions_count
        )

    except ImportError as e:
        return QuizResult(
            success=False,
            error=f"h5p-generator nicht gefunden: {e}"
        )
    except Exception as e:
        return QuizResult(
            success=False,
            error=f"Unerwarteter Fehler: {type(e).__name__}: {e}"
        )


def main():
    parser = argparse.ArgumentParser(
        description='Erstellt H5P Quiz und laedt zu Moodle hoch'
    )
    parser.add_argument(
        '--questions', '-q',
        required=True,
        help='Fragen im h5p-generator Format (oder @datei.txt)'
    )
    parser.add_argument(
        '--title', '-t',
        default='Quiz',
        help='Quiz-Titel'
    )
    parser.add_argument(
        '--course', '-c',
        type=int,
        default=2,
        help='Moodle Kurs-ID (default: 2)'
    )
    parser.add_argument(
        '--domain', '-d',
        choices=['accounting', 'scrum', 'it', 'business'],
        help='Fachbereich fuer Distraktoren'
    )

    args = parser.parse_args()

    # Fragen aus Datei oder direkt
    if args.questions.startswith('@'):
        filepath = args.questions[1:]
        with open(filepath, 'r', encoding='utf-8') as f:
            questions_text = f.read()
    else:
        questions_text = args.questions.replace('\\n', '\n')

    result = create_and_upload_quiz(
        questions_text=questions_text,
        title=args.title,
        course_id=args.course,
        domain=args.domain
    )

    print(result)
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
