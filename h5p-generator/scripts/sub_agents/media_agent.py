"""
Media Agent - Spezialisiert auf video-zentrierte Inhalte

Unterstützte Typen:
- InteractiveVideo
"""

from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from h5p_generator import create_interactive_video, THEMES
from .base_agent import BaseH5PAgent, ValidationIssue


class MediaAgent(BaseH5PAgent):
    """
    Media Agent für video-zentrierte H5P-Inhalte.

    Validierung:
    - Video-URL vorhanden
    - Interaktionstypen gültig
    """

    SUPPORTED_TYPES = ['interactive_video']

    FALLBACK_MAP = {}  # Kein Fallback

    def __init__(self, output_dir: Path | str = None, style=None):
        super().__init__(output_dir)
        self.style = style or THEMES.get('education')
        self._register_generators()
        self._register_validators()

    def _register_generators(self):
        """Registriert alle Media-Generatoren"""

        def gen_interactive_video(title, video_url, interactions=None, filename=None, **kwargs):
            fname = filename or self._make_filename(title, 'ivideo')
            return create_interactive_video(title, video_url, interactions, fname, style=self.style, **kwargs)

        self.register_generator('interactive_video', gen_interactive_video)

    def _register_validators(self):
        """Registriert Validatoren"""

        def validate_interactive_video(video_url=None, interactions=None, **kwargs) -> list[ValidationIssue]:
            issues = []
            if not video_url:
                issues.append(ValidationIssue(
                    severity="error",
                    message="Keine Video-URL angegeben"
                ))

            if interactions:
                from h5p_generator import InteractiveVideoGenerator
                valid_types = set(InteractiveVideoGenerator.SUPPORTED_INTERACTIONS.keys())
                for i, interaction in enumerate(interactions):
                    int_type = interaction.get('type', '')
                    if int_type not in valid_types:
                        issues.append(ValidationIssue(
                            severity="error",
                            message=f"Interaktion {i+1}: Unbekannter Typ '{int_type}'. "
                                    f"Verfügbar: {sorted(valid_types)}"
                        ))

            return issues

        self.register_validator('interactive_video', validate_interactive_video)

    def _make_filename(self, title: str, type_suffix: str) -> str:
        """Erstellt einen Dateinamen aus Titel"""
        safe_title = "".join(c if c.isalnum() or c in '-_' else '-' for c in title.lower())
        safe_title = safe_title[:30]
        return f"{safe_title}-{type_suffix}"

    # Convenience-Methoden

    def create_interactive_video(self, title: str, video_url: str, interactions: list[dict] = None,
                                  filename: str = None, **kwargs):
        """
        Erstellt ein interaktives Video.

        Args:
            title: Titel des Videos
            video_url: YouTube-URL oder MP4-URL
            interactions: Optionale Interaktionsliste
            filename: Optional, wird aus Titel generiert
        """
        return self.generate('interactive_video', title=title, video_url=video_url,
                           interactions=interactions, filename=filename, **kwargs)
