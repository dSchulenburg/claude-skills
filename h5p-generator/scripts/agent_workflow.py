#!/usr/bin/env python3
"""
H5P Agent Workflow - Self-Improving Content Generation

Features:
- Generate H5P content with quality validation
- Preview in browser for human feedback
- Save successful templates to library
- Learn from feedback to improve future generations

Usage:
    from agent_workflow import H5PAgent

    agent = H5PAgent()
    result = agent.generate_with_feedback(...)
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from h5p_generator import (
    create_true_false, create_multi_choice, create_fill_blanks,
    create_drag_drop, create_single_choice, create_flashcards,
    create_mark_words, create_summary, create_accordion,
    create_drag_text, create_timeline, create_memory_game,
    THEMES, H5PStyle, H5PResult
)


@dataclass
class FeedbackResult:
    """Result of user feedback on generated content"""
    success: bool
    rating: int  # 1-5 stars
    issues: List[str] = field(default_factory=list)
    notes: str = ""
    save_as_template: bool = False


@dataclass
class AgentDecision:
    """Agent's decision on which content type to use"""
    content_type: str
    reasoning: str
    confidence: float  # 0.0 - 1.0


class H5PAgent:
    """
    Intelligent H5P content generation agent with self-improvement.

    The agent:
    1. Analyzes learning goals to select appropriate content type
    2. Generates content using templates
    3. Validates output against known issues
    4. Collects feedback and improves templates
    """

    def __init__(self, output_dir: str = None, style: H5PStyle = None):
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = Path(output_dir) if output_dir else self.base_dir / "test-output"
        self.template_dir = self.base_dir / "references" / "templates"
        self.feedback_log = self.base_dir / "feedback_history.json"
        self.style = style or THEMES.get('education')

        # Load decision matrix
        self.decision_rules = self._load_decision_rules()

        # Load known issues for validation
        self.known_issues = self._load_known_issues()

    def _load_decision_rules(self) -> Dict:
        """Load content type decision rules from matrix"""
        return {
            # Operator -> Content Type mapping
            "nennen": ["flashcards", "true_false"],
            "beschreiben": ["true_false", "summary"],
            "erklären": ["accordion", "fill_blanks"],
            "zuordnen": ["drag_drop", "drag_text"],
            "ordnen": ["timeline", "drag_drop"],
            "ergänzen": ["fill_blanks", "drag_text"],
            "markieren": ["mark_words"],
            "analysieren": ["accordion", "summary"],
            "bewerten": ["multi_choice", "summary"],
            "vergleichen": ["drag_drop", "true_false"],
        }

    def _load_known_issues(self) -> Dict:
        """Load known issues for each content type"""
        return {
            "drag_drop": [
                {"check": "dropzone_y_too_high", "threshold": 70, "message": "Dropzone y > 70 kann außerhalb des Canvas sein"},
                {"check": "dropzone_height_too_small", "threshold": 20, "message": "Dropzone height < 20 ist zu klein"},
            ],
            "timeline": [
                {"check": "events_empty", "message": "Timeline braucht mindestens 2 Events"},
            ],
        }

    def decide_content_type(self, learning_goal: str, operator: str = None) -> AgentDecision:
        """
        Decide which H5P content type to use based on learning goal.

        Args:
            learning_goal: What should be learned
            operator: Optional cognitive operator (nennen, erklären, zuordnen, etc.)

        Returns:
            AgentDecision with content_type and reasoning
        """
        # Simple keyword matching for operator detection
        operator_keywords = {
            "nennen": ["name", "nenne", "aufzählen", "liste"],
            "beschreiben": ["beschreib", "erkläre", "was ist"],
            "zuordnen": ["zuordn", "ordne zu", "kategori", "sortier"],
            "ordnen": ["reihenfolge", "chronolog", "zeitlich"],
            "ergänzen": ["ergänz", "füll", "lücke", "vervollständ"],
            "markieren": ["markier", "finde", "identifizier"],
        }

        detected_operator = operator
        if not detected_operator:
            goal_lower = learning_goal.lower()
            for op, keywords in operator_keywords.items():
                if any(kw in goal_lower for kw in keywords):
                    detected_operator = op
                    break

        # Get recommended content types
        if detected_operator and detected_operator in self.decision_rules:
            content_types = self.decision_rules[detected_operator]
            return AgentDecision(
                content_type=content_types[0],
                reasoning=f"Operator '{detected_operator}' → {content_types[0]} empfohlen",
                confidence=0.8
            )

        # Default fallback
        return AgentDecision(
            content_type="multi_choice",
            reasoning="Kein spezifischer Operator erkannt, Multiple Choice als Fallback",
            confidence=0.5
        )

    def validate_content(self, result: H5PResult, content_type: str) -> List[str]:
        """
        Validate generated content against known issues.

        Returns list of warnings/issues found.
        """
        issues = []

        if not result.success:
            issues.append(f"Generation failed: {result.error}")
            return issues

        # Type-specific validation
        if content_type in self.known_issues:
            # Read generated content for validation
            try:
                import zipfile
                with zipfile.ZipFile(result.path, 'r') as zf:
                    content = json.loads(zf.read('content/content.json'))

                    if content_type == "drag_drop":
                        # Check dropzone positions
                        dropzones = content.get('question', {}).get('task', {}).get('dropZones', [])
                        for i, dz in enumerate(dropzones):
                            if dz.get('y', 0) > 70:
                                issues.append(f"Dropzone {i}: y={dz['y']} könnte außerhalb sein")
                            if dz.get('height', 0) < 20:
                                issues.append(f"Dropzone {i}: height={dz['height']} ist klein")

            except Exception as e:
                issues.append(f"Validation error: {e}")

        return issues

    def preview(self, h5p_path: Path, port: int = 8080) -> bool:
        """
        Start preview server for the H5P file.

        Returns True if server started successfully.
        """
        viewer_script = self.base_dir / "viewer" / "serve.py"

        if not viewer_script.exists():
            print(f"Warning: Viewer script not found at {viewer_script}")
            return False

        try:
            # Start preview server in background
            subprocess.Popen(
                [sys.executable, str(viewer_script), str(h5p_path), str(port)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"Preview started at http://localhost:{port}/preview.html")
            return True
        except Exception as e:
            print(f"Failed to start preview: {e}")
            return False

    def save_as_template(self, result: H5PResult, name: str, notes: str = "") -> bool:
        """
        Save successful generation as template for future use.
        """
        if not result.success or not result.path:
            return False

        try:
            import zipfile

            # Extract content.json
            with zipfile.ZipFile(result.path, 'r') as zf:
                content = json.loads(zf.read('content/content.json'))
                h5p_meta = json.loads(zf.read('h5p.json'))

            # Save as template
            template = {
                "name": name,
                "content_type": result.content_type,
                "created": datetime.now().isoformat(),
                "notes": notes,
                "h5p_meta": h5p_meta,
                "content_structure": content
            }

            template_path = self.template_dir / "saved" / f"{name}.json"
            template_path.parent.mkdir(parents=True, exist_ok=True)

            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=2, ensure_ascii=False)

            print(f"Template saved: {template_path}")
            return True

        except Exception as e:
            print(f"Failed to save template: {e}")
            return False

    def log_feedback(self, result: H5PResult, feedback: FeedbackResult):
        """
        Log feedback for learning and improvement.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "content_type": result.content_type,
            "title": result.title,
            "success": feedback.success,
            "rating": feedback.rating,
            "issues": feedback.issues,
            "notes": feedback.notes
        }

        # Load existing log
        history = []
        if self.feedback_log.exists():
            try:
                with open(self.feedback_log, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except:
                pass

        # Append and save
        history.append(log_entry)

        with open(self.feedback_log, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def generate(self, content_type: str, **kwargs) -> H5PResult:
        """
        Generate H5P content of specified type.

        This is the main entry point for content generation.
        """
        generators = {
            'true_false': lambda: create_true_false(kwargs['title'], kwargs['questions'], kwargs.get('output_name'), self.style),
            'multi_choice': lambda: create_multi_choice(kwargs['title'], kwargs['questions'], kwargs.get('output_name'), self.style),
            'fill_blanks': lambda: create_fill_blanks(kwargs['title'], kwargs['text'], kwargs.get('output_name'), self.style),
            'drag_drop': lambda: create_drag_drop(kwargs['title'], kwargs.get('task', ''), kwargs['dropzones'], kwargs['draggables'], kwargs.get('output_name'), self.style),
            'single_choice': lambda: create_single_choice(kwargs['title'], kwargs['questions'], kwargs.get('output_name'), self.style),
            'flashcards': lambda: create_flashcards(kwargs['title'], kwargs['cards'], kwargs.get('output_name'), self.style),
            'mark_words': lambda: create_mark_words(kwargs['title'], kwargs['text'], kwargs.get('output_name'), kwargs.get('task', 'Markiere die richtigen Wörter.'), self.style),
            'summary': lambda: create_summary(kwargs['title'], kwargs['items'], kwargs.get('output_name'), kwargs.get('intro', 'Wähle die richtige Aussage.'), self.style),
            'accordion': lambda: create_accordion(kwargs['title'], kwargs['panels'], kwargs.get('output_name'), self.style),
            'drag_text': lambda: create_drag_text(kwargs['title'], kwargs['text'], kwargs.get('output_name'), kwargs.get('task', 'Ziehe die Wörter.'), self.style),
            'timeline': lambda: create_timeline(kwargs['title'], kwargs['events'], kwargs.get('output_name'), kwargs.get('description', ''), self.style),
            'memory_game': lambda: create_memory_game(kwargs['title'], kwargs['cards'], kwargs.get('output_name'), self.style),
        }

        if content_type not in generators:
            return H5PResult(
                success=False,
                error=f"Unknown content type: {content_type}",
                content_type=content_type,
                title=kwargs.get('title', 'Unknown')
            )

        return generators[content_type]()

    def generate_with_validation(self, content_type: str, **kwargs) -> tuple[H5PResult, List[str]]:
        """
        Generate content with automatic validation.

        Returns (result, issues) tuple.
        """
        result = self.generate(content_type, **kwargs)
        issues = self.validate_content(result, content_type)

        return result, issues


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    """CLI interface for the agent workflow"""
    print("H5P Agent Workflow")
    print("=" * 40)

    agent = H5PAgent()

    # Example: Generate with decision
    learning_goal = "Ordne die Scrum-Rollen den richtigen Aufgaben zu"

    decision = agent.decide_content_type(learning_goal)
    print(f"\nLernziel: {learning_goal}")
    print(f"Entscheidung: {decision.content_type}")
    print(f"Begründung: {decision.reasoning}")
    print(f"Konfidenz: {decision.confidence:.0%}")

    # Generate example
    if decision.content_type == "drag_drop":
        result, issues = agent.generate_with_validation(
            "drag_drop",
            title="Scrum-Rollen",
            task="Ordne die Aufgaben zu",
            dropzones=["Product Owner", "Scrum Master", "Dev Team"],
            draggables=[
                {"text": "Priorisiert Backlog", "dropzone": 0},
                {"text": "Entfernt Hindernisse", "dropzone": 1},
                {"text": "Entwickelt Features", "dropzone": 2},
            ]
        )

        print(f"\nErgebnis: {result}")
        if issues:
            print(f"Warnungen: {issues}")

        # Optionally start preview
        if result.success:
            print("\nPreview starten? (y/n): ", end="")
            if input().strip().lower() == 'y':
                agent.preview(result.path)


if __name__ == "__main__":
    main()
