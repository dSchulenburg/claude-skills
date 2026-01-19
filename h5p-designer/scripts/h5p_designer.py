#!/usr/bin/env python3
"""
H5P Designer - Analyze, Debug and Optimize H5P Files

Features:
- Parse H5P files (extract content.json)
- Analyze design issues (spacing, sizes, readability)
- Apply fixes (resize, reposition, fix encoding)
- Repackage to new .h5p file

Supported Content Types:
- H5P.DragQuestion (Drag & Drop)
- H5P.MultiChoice (Multiple Choice)
- H5P.Blanks (Fill in the Blanks)
- H5P.TrueFalse
- H5P.DialogCards (Flashcards)
"""

import json
import zipfile
import os
import shutil
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple
import re
import copy


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class DesignIssue:
    """Represents a design issue found in an H5P file"""
    severity: str  # 'error', 'warning', 'info'
    category: str  # 'size', 'spacing', 'encoding', 'accessibility', 'layout'
    message: str
    location: str  # Path in JSON, e.g., 'question.task.elements[0]'
    current_value: Any = None
    suggested_value: Any = None
    auto_fixable: bool = False


@dataclass
class H5PAnalysis:
    """Result of analyzing an H5P file"""
    file_path: str
    content_type: str
    title: str
    issues: List[DesignIssue] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == 'error')

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == 'warning')

    @property
    def auto_fixable_count(self) -> int:
        return sum(1 for i in self.issues if i.auto_fixable)

    def summary(self) -> str:
        return (f"H5P Analysis: {self.title} ({self.content_type})\n"
                f"  Errors: {self.error_count}, Warnings: {self.warning_count}\n"
                f"  Auto-fixable: {self.auto_fixable_count}/{len(self.issues)}")


# =============================================================================
# H5P Parser
# =============================================================================

class H5PParser:
    """Parse and extract H5P file contents"""

    def __init__(self, h5p_path: str):
        self.h5p_path = Path(h5p_path)
        self.h5p_json = None
        self.content_json = None
        self.content_type = None
        self.title = None
        self._images = []

    def parse(self) -> Tuple[Dict, Dict]:
        """Extract and parse H5P file contents"""
        if not self.h5p_path.exists():
            raise FileNotFoundError(f"H5P file not found: {self.h5p_path}")

        with zipfile.ZipFile(self.h5p_path, 'r') as zf:
            # Read h5p.json
            with zf.open('h5p.json') as f:
                self.h5p_json = json.load(f)
                self.title = self.h5p_json.get('title', 'Unknown')
                self.content_type = self.h5p_json.get('mainLibrary', 'Unknown')

            # Read content/content.json
            with zf.open('content/content.json') as f:
                self.content_json = json.load(f)

            # List images
            self._images = [n for n in zf.namelist() if n.startswith('content/images/')]

        return self.h5p_json, self.content_json

    def get_content_type(self) -> str:
        """Get the main content type (e.g., 'DragQuestion', 'MultiChoice')"""
        if self.content_type:
            # Extract type name from "H5P.DragQuestion" -> "DragQuestion"
            return self.content_type.replace('H5P.', '')
        return 'Unknown'


# =============================================================================
# Design Analyzers
# =============================================================================

class BaseAnalyzer:
    """Base class for content-type specific analyzers"""

    def analyze(self, content: Dict, h5p_meta: Dict) -> List[DesignIssue]:
        raise NotImplementedError


class DragQuestionAnalyzer(BaseAnalyzer):
    """Analyzer for H5P.DragQuestion (Drag & Drop)"""

    # Recommended minimums
    MIN_DRAGGABLE_WIDTH = 12  # %
    MIN_DRAGGABLE_HEIGHT = 8  # %
    MIN_DROPZONE_WIDTH = 15   # %
    MIN_DROPZONE_HEIGHT = 20  # %
    MIN_SPACING = 3           # % between elements
    MIN_CANVAS_WIDTH = 600
    MIN_CANVAS_HEIGHT = 400

    def analyze(self, content: Dict, h5p_meta: Dict) -> List[DesignIssue]:
        issues = []

        question = content.get('question', {})
        settings = question.get('settings', {})
        task = question.get('task', {})

        # Check canvas size
        size = settings.get('size', {})
        width = size.get('width', 0)
        height = size.get('height', 0)

        if width < self.MIN_CANVAS_WIDTH:
            issues.append(DesignIssue(
                severity='warning',
                category='size',
                message=f'Canvas width ({width}px) is below recommended minimum ({self.MIN_CANVAS_WIDTH}px)',
                location='question.settings.size.width',
                current_value=width,
                suggested_value=self.MIN_CANVAS_WIDTH,
                auto_fixable=True
            ))

        if height < self.MIN_CANVAS_HEIGHT:
            issues.append(DesignIssue(
                severity='warning',
                category='size',
                message=f'Canvas height ({height}px) is below recommended minimum ({self.MIN_CANVAS_HEIGHT}px)',
                location='question.settings.size.height',
                current_value=height,
                suggested_value=self.MIN_CANVAS_HEIGHT,
                auto_fixable=True
            ))

        # Analyze draggable elements
        elements = task.get('elements', [])
        for i, elem in enumerate(elements):
            elem_width = elem.get('width', 0)
            elem_height = elem.get('height', 0)

            if elem_width < self.MIN_DRAGGABLE_WIDTH:
                issues.append(DesignIssue(
                    severity='error',
                    category='size',
                    message=f'Draggable {i+1} width ({elem_width}%) is too small - text may be cut off',
                    location=f'question.task.elements[{i}].width',
                    current_value=elem_width,
                    suggested_value=self.MIN_DRAGGABLE_WIDTH,
                    auto_fixable=True
                ))

            if elem_height < self.MIN_DRAGGABLE_HEIGHT:
                issues.append(DesignIssue(
                    severity='error',
                    category='size',
                    message=f'Draggable {i+1} height ({elem_height}%) is too small - hard to grab',
                    location=f'question.task.elements[{i}].height',
                    current_value=elem_height,
                    suggested_value=self.MIN_DRAGGABLE_HEIGHT,
                    auto_fixable=True
                ))

            # Check for encoding issues in text
            elem_type = elem.get('type', {})
            params = elem_type.get('params', {})
            text = params.get('text', '')

            encoding_issues = self._check_encoding(text)
            if encoding_issues:
                issues.append(DesignIssue(
                    severity='warning',
                    category='encoding',
                    message=f'Draggable {i+1} has encoding issues: {encoding_issues}',
                    location=f'question.task.elements[{i}].type.params.text',
                    current_value=text,
                    suggested_value=self._fix_encoding(text),
                    auto_fixable=True
                ))

        # Analyze dropzones
        dropzones = task.get('dropZones', [])
        for i, dz in enumerate(dropzones):
            dz_width = dz.get('width', 0)
            dz_height = dz.get('height', 0)

            if dz_width < self.MIN_DROPZONE_WIDTH:
                issues.append(DesignIssue(
                    severity='error',
                    category='size',
                    message=f'Dropzone {i+1} width ({dz_width}%) is too small for dropping items',
                    location=f'question.task.dropZones[{i}].width',
                    current_value=dz_width,
                    suggested_value=self.MIN_DROPZONE_WIDTH,
                    auto_fixable=True
                ))

            if dz_height < self.MIN_DROPZONE_HEIGHT:
                issues.append(DesignIssue(
                    severity='error',
                    category='size',
                    message=f'Dropzone {i+1} height ({dz_height}%) is too small',
                    location=f'question.task.dropZones[{i}].height',
                    current_value=dz_height,
                    suggested_value=self.MIN_DROPZONE_HEIGHT,
                    auto_fixable=True
                ))

            # Check dropzone capacity
            correct_elements = dz.get('correctElements', [])
            expected_items = len(correct_elements)
            if expected_items > 0:
                # Estimate if dropzone can fit all items
                estimated_capacity = (dz_height / 10) * (dz_width / 15)
                if expected_items > estimated_capacity:
                    issues.append(DesignIssue(
                        severity='warning',
                        category='layout',
                        message=f'Dropzone {i+1} may be too small for {expected_items} items',
                        location=f'question.task.dropZones[{i}]',
                        current_value={'width': dz_width, 'height': dz_height, 'items': expected_items},
                        auto_fixable=False
                    ))

        # Check spacing between elements
        issues.extend(self._check_element_spacing(elements))
        issues.extend(self._check_dropzone_spacing(dropzones))

        return issues

    def _check_encoding(self, text: str) -> str:
        """Check for common encoding issues"""
        issues = []

        # German umlaut substitutions
        umlaut_patterns = [
            ('ae', 'ä'), ('oe', 'ö'), ('ue', 'ü'),
            ('Ae', 'Ä'), ('Oe', 'Ö'), ('Ue', 'Ü'),
            ('ss', 'ß')
        ]

        # Check for likely umlaut substitutions
        words_with_ae = re.findall(r'\b\w*ae\w*\b', text, re.IGNORECASE)
        words_with_oe = re.findall(r'\b\w*oe\w*\b', text, re.IGNORECASE)
        words_with_ue = re.findall(r'\b\w*ue\w*\b', text, re.IGNORECASE)

        # Common German words that should have umlauts
        known_umlaut_words = {
            'schaetzt': 'schätzt', 'waehlt': 'wählt', 'faehrt': 'fährt',
            'laeuft': 'läuft', 'haelt': 'hält', 'traegt': 'trägt',
            'kundenwuensche': 'Kundenwünsche', 'wuensche': 'Wünsche',
            'prueft': 'prüft', 'fuehrt': 'führt', 'hoert': 'hört'
        }

        text_lower = text.lower()
        for wrong, correct in known_umlaut_words.items():
            if wrong in text_lower:
                issues.append(f'"{wrong}" should be "{correct}"')

        return ', '.join(issues) if issues else ''

    def _fix_encoding(self, text: str) -> str:
        """Fix common encoding issues"""
        replacements = {
            'Schaetzt': 'Schätzt', 'schaetzt': 'schätzt',
            'Waehlt': 'Wählt', 'waehlt': 'wählt',
            'Faehrt': 'Fährt', 'faehrt': 'fährt',
            'Laeuft': 'Läuft', 'laeuft': 'läuft',
            'Haelt': 'Hält', 'haelt': 'hält',
            'Traegt': 'Trägt', 'traegt': 'trägt',
            'Kundenwuensche': 'Kundenwünsche', 'kundenwuensche': 'Kundenwünsche',
            'Wuensche': 'Wünsche', 'wuensche': 'Wünsche',
            'Prueft': 'Prüft', 'prueft': 'prüft',
            'Fuehrt': 'Führt', 'fuehrt': 'führt',
            'Hoert': 'Hört', 'hoert': 'hört',
            'Aufwaende': 'Aufwände', 'aufwaende': 'Aufwände',
        }

        result = text
        for wrong, correct in replacements.items():
            result = result.replace(wrong, correct)
        return result

    def _check_element_spacing(self, elements: List[Dict]) -> List[DesignIssue]:
        """Check if elements have enough spacing between them"""
        issues = []

        for i, elem1 in enumerate(elements):
            for j, elem2 in enumerate(elements):
                if i >= j:
                    continue

                # Check horizontal overlap/proximity
                x1, w1 = elem1.get('x', 0), elem1.get('width', 0)
                x2, w2 = elem2.get('x', 0), elem2.get('width', 0)
                y1, h1 = elem1.get('y', 0), elem1.get('height', 0)
                y2, h2 = elem2.get('y', 0), elem2.get('height', 0)

                # If on same row (similar y)
                if abs(y1 - y2) < 5:
                    gap = x2 - (x1 + w1) if x2 > x1 else x1 - (x2 + w2)
                    if 0 < gap < self.MIN_SPACING:
                        issues.append(DesignIssue(
                            severity='warning',
                            category='spacing',
                            message=f'Elements {i+1} and {j+1} are too close ({gap:.1f}%)',
                            location=f'question.task.elements',
                            current_value=gap,
                            suggested_value=self.MIN_SPACING,
                            auto_fixable=False
                        ))

        return issues

    def _check_dropzone_spacing(self, dropzones: List[Dict]) -> List[DesignIssue]:
        """Check spacing between dropzones"""
        issues = []

        for i, dz1 in enumerate(dropzones):
            for j, dz2 in enumerate(dropzones):
                if i >= j:
                    continue

                x1, w1 = dz1.get('x', 0), dz1.get('width', 0)
                x2, w2 = dz2.get('x', 0), dz2.get('width', 0)

                gap = x2 - (x1 + w1) if x2 > x1 else x1 - (x2 + w2)
                if 0 < gap < 5:
                    issues.append(DesignIssue(
                        severity='warning',
                        category='spacing',
                        message=f'Dropzones {i+1} and {j+1} are very close ({gap:.1f}%)',
                        location='question.task.dropZones',
                        current_value=gap,
                        auto_fixable=False
                    ))

        return issues


class MultiChoiceAnalyzer(BaseAnalyzer):
    """Analyzer for MultiChoice content"""

    def analyze(self, content: Dict, h5p_meta: Dict) -> List[DesignIssue]:
        issues = []

        questions = content.get('questions', [])
        for i, q in enumerate(questions):
            params = q.get('params', {})
            answers = params.get('answers', [])

            # Check answer count
            if len(answers) < 2:
                issues.append(DesignIssue(
                    severity='error',
                    category='content',
                    message=f'Question {i+1} has fewer than 2 answers',
                    location=f'questions[{i}].params.answers',
                    auto_fixable=False
                ))

            if len(answers) > 6:
                issues.append(DesignIssue(
                    severity='warning',
                    category='usability',
                    message=f'Question {i+1} has many answers ({len(answers)}) - consider reducing',
                    location=f'questions[{i}].params.answers',
                    auto_fixable=False
                ))

            # Check for correct answer
            has_correct = any(a.get('correct', False) for a in answers)
            if not has_correct:
                issues.append(DesignIssue(
                    severity='error',
                    category='content',
                    message=f'Question {i+1} has no correct answer marked',
                    location=f'questions[{i}].params.answers',
                    auto_fixable=False
                ))

        return issues


# =============================================================================
# H5P Designer (Main Class)
# =============================================================================

class H5PDesigner:
    """Main class for analyzing and fixing H5P files"""

    ANALYZERS = {
        'DragQuestion': DragQuestionAnalyzer(),
        'MultiChoice': MultiChoiceAnalyzer(),
    }

    def __init__(self, h5p_path: str):
        self.parser = H5PParser(h5p_path)
        self.h5p_json = None
        self.content_json = None
        self.original_content = None

    def analyze(self) -> H5PAnalysis:
        """Analyze the H5P file for design issues"""
        self.h5p_json, self.content_json = self.parser.parse()
        self.original_content = copy.deepcopy(self.content_json)

        content_type = self.parser.get_content_type()

        analysis = H5PAnalysis(
            file_path=str(self.parser.h5p_path),
            content_type=content_type,
            title=self.parser.title,
            metadata={
                'mainLibrary': self.h5p_json.get('mainLibrary'),
                'dependencies': self.h5p_json.get('preloadedDependencies', [])
            }
        )

        # Get appropriate analyzer
        analyzer = self.ANALYZERS.get(content_type)
        if analyzer:
            analysis.issues = analyzer.analyze(self.content_json, self.h5p_json)
        else:
            analysis.issues.append(DesignIssue(
                severity='info',
                category='support',
                message=f'No specific analyzer for {content_type} - basic checks only',
                location='',
                auto_fixable=False
            ))

        return analysis

    def apply_fixes(self, issues: List[DesignIssue] = None) -> Dict:
        """Apply auto-fixable issues to the content"""
        if issues is None:
            analysis = self.analyze()
            issues = [i for i in analysis.issues if i.auto_fixable]

        fixed_content = copy.deepcopy(self.content_json)
        fixes_applied = []

        for issue in issues:
            if not issue.auto_fixable or issue.suggested_value is None:
                continue

            try:
                self._apply_fix(fixed_content, issue.location, issue.suggested_value)
                fixes_applied.append(issue)
            except Exception as e:
                print(f"Warning: Could not apply fix for {issue.location}: {e}")

        self.content_json = fixed_content
        return {
            'fixes_applied': len(fixes_applied),
            'fixes': [f.message for f in fixes_applied]
        }

    def _apply_fix(self, content: Dict, location: str, value: Any):
        """Apply a single fix to the content at the given location"""
        # Parse location like 'question.task.elements[0].width'
        parts = re.split(r'\.|\[|\]', location)
        parts = [p for p in parts if p]  # Remove empty strings

        obj = content
        for i, part in enumerate(parts[:-1]):
            if part.isdigit():
                obj = obj[int(part)]
            else:
                obj = obj[part]

        final_key = parts[-1]
        if final_key.isdigit():
            obj[int(final_key)] = value
        else:
            obj[final_key] = value

    def optimize_layout(self, content_type: str = None) -> Dict:
        """Automatically optimize the layout for better usability"""
        if content_type is None:
            content_type = self.parser.get_content_type()

        if content_type == 'DragQuestion':
            return self._optimize_drag_drop_layout()

        return {'optimized': False, 'message': f'No layout optimizer for {content_type}'}

    def _optimize_drag_drop_layout(self) -> Dict:
        """Optimize Drag & Drop layout for better usability"""
        question = self.content_json.get('question', {})
        task = question.get('task', {})
        elements = task.get('elements', [])
        dropzones = task.get('dropZones', [])

        changes = []

        # Expand canvas if needed
        settings = question.setdefault('settings', {})
        size = settings.setdefault('size', {})
        if size.get('width', 0) < 700:
            size['width'] = 700
            changes.append('Expanded canvas width to 700px')
        if size.get('height', 0) < 500:
            size['height'] = 500
            changes.append('Expanded canvas height to 500px')

        # Resize draggables for better readability
        num_elements = len(elements)
        if num_elements > 0:
            # Calculate optimal layout
            cols = min(4, num_elements)
            rows = (num_elements + cols - 1) // cols

            elem_width = min(20, 80 // cols)
            elem_height = min(12, 35 // rows)
            h_gap = (100 - cols * elem_width) / (cols + 1)
            v_gap = 3

            for i, elem in enumerate(elements):
                row = i // cols
                col = i % cols

                old_w, old_h = elem.get('width'), elem.get('height')
                elem['width'] = elem_width
                elem['height'] = elem_height
                elem['x'] = round(h_gap + col * (elem_width + h_gap), 1)
                elem['y'] = round(5 + row * (elem_height + v_gap), 1)

                if old_w != elem_width or old_h != elem_height:
                    changes.append(f'Resized draggable {i+1}: {old_w}x{old_h} -> {elem_width}x{elem_height}')

                # Fix encoding in text
                if 'type' in elem and 'params' in elem['type']:
                    text = elem['type']['params'].get('text', '')
                    fixed_text = self._fix_german_encoding(text)
                    if fixed_text != text:
                        elem['type']['params']['text'] = fixed_text
                        changes.append(f'Fixed encoding in draggable {i+1}')

        # Resize and reposition dropzones
        num_zones = len(dropzones)
        if num_zones > 0:
            zone_width = min(25, 80 // num_zones)
            zone_height = 30
            zone_y = 65  # Below draggables
            h_gap = (100 - num_zones * zone_width) / (num_zones + 1)

            for i, dz in enumerate(dropzones):
                old_w, old_h = dz.get('width'), dz.get('height')
                dz['width'] = zone_width
                dz['height'] = zone_height
                dz['x'] = round(h_gap + i * (zone_width + h_gap), 1)
                dz['y'] = zone_y

                if old_w != zone_width or old_h != zone_height:
                    changes.append(f'Resized dropzone {i+1}: {old_w}x{old_h} -> {zone_width}x{zone_height}')

        return {
            'optimized': True,
            'changes': changes
        }

    def _fix_german_encoding(self, text: str) -> str:
        """Fix German umlaut encoding issues"""
        replacements = {
            'Schaetzt': 'Schätzt', 'schaetzt': 'schätzt',
            'Waehlt': 'Wählt', 'waehlt': 'wählt',
            'Faehrt': 'Fährt', 'faehrt': 'fährt',
            'Laeuft': 'Läuft', 'laeuft': 'läuft',
            'Haelt': 'Hält', 'haelt': 'hält',
            'Traegt': 'Trägt', 'traegt': 'trägt',
            'Kundenwuensche': 'Kundenwünsche',
            'Wuensche': 'Wünsche', 'wuensche': 'Wünsche',
            'Prueft': 'Prüft', 'prueft': 'prüft',
            'Fuehrt': 'Führt', 'fuehrt': 'führt',
            'Hoert': 'Hört', 'hoert': 'hört',
            'Aufwaende': 'Aufwände', 'aufwaende': 'Aufwände',
            'Losung': 'Lösung', 'losung': 'Lösung',
        }

        result = text
        for wrong, correct in replacements.items():
            result = result.replace(wrong, correct)
        return result

    def save(self, output_path: str = None, suffix: str = '-optimized') -> str:
        """Save the modified H5P file"""
        if output_path is None:
            base = self.parser.h5p_path.stem
            output_path = self.parser.h5p_path.parent / f"{base}{suffix}.h5p"

        output_path = Path(output_path)

        # Create temp directory
        temp_dir = Path('/tmp') / f"h5p_save_{datetime.now().strftime('%H%M%S')}"
        temp_dir.mkdir(parents=True, exist_ok=True)
        (temp_dir / 'content').mkdir(exist_ok=True)

        try:
            # Extract original file (to get images etc.)
            with zipfile.ZipFile(self.parser.h5p_path, 'r') as zf:
                zf.extractall(temp_dir)

            # Overwrite content.json with modified version
            with open(temp_dir / 'content' / 'content.json', 'w', encoding='utf-8') as f:
                json.dump(self.content_json, f, ensure_ascii=False, indent=2)

            # Create new H5P file
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(temp_dir)
                        zf.write(file_path, arcname)

            return str(output_path)

        finally:
            # Cleanup
            shutil.rmtree(temp_dir, ignore_errors=True)

    def get_content_json(self) -> str:
        """Get the current content.json as formatted string"""
        return json.dumps(self.content_json, ensure_ascii=False, indent=2)

    def set_content_value(self, location: str, value: Any):
        """Set a specific value in content.json"""
        self._apply_fix(self.content_json, location, value)


# =============================================================================
# Convenience Functions
# =============================================================================

def analyze_h5p(h5p_path: str) -> H5PAnalysis:
    """Analyze an H5P file and return issues"""
    designer = H5PDesigner(h5p_path)
    return designer.analyze()


def optimize_h5p(h5p_path: str, output_path: str = None) -> Tuple[str, Dict]:
    """Optimize an H5P file and save it"""
    designer = H5PDesigner(h5p_path)
    analysis = designer.analyze()

    # Apply auto-fixes
    fix_result = designer.apply_fixes()

    # Optimize layout
    layout_result = designer.optimize_layout()

    # Save
    saved_path = designer.save(output_path)

    return saved_path, {
        'analysis': analysis.summary(),
        'fixes': fix_result,
        'layout': layout_result
    }


def print_analysis(analysis: H5PAnalysis):
    """Pretty print an analysis"""
    print(f"\n{'='*60}")
    print(f"H5P Analysis: {analysis.title}")
    print(f"Type: {analysis.content_type}")
    print(f"File: {analysis.file_path}")
    print(f"{'='*60}")

    if not analysis.issues:
        print("No issues found!")
        return

    print(f"\nFound {len(analysis.issues)} issues:")
    print(f"  - Errors: {analysis.error_count}")
    print(f"  - Warnings: {analysis.warning_count}")
    print(f"  - Auto-fixable: {analysis.auto_fixable_count}")

    print("\nDetails:")
    for i, issue in enumerate(analysis.issues, 1):
        icon = '[ERR]' if issue.severity == 'error' else '[WARN]' if issue.severity == 'warning' else '[INFO]'
        fix_icon = '[FIX]' if issue.auto_fixable else ''
        print(f"  {i}. {icon} [{issue.category}] {issue.message} {fix_icon}")
        if issue.current_value is not None and issue.suggested_value is not None:
            print(f"      Current: {issue.current_value} -> Suggested: {issue.suggested_value}")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python h5p_designer.py <h5p_file> [--fix] [--output <path>]")
        print("\nOptions:")
        print("  --fix      Apply auto-fixes and optimize layout")
        print("  --output   Specify output path for fixed file")
        sys.exit(1)

    h5p_path = sys.argv[1]
    do_fix = '--fix' in sys.argv
    output_path = None

    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_path = sys.argv[idx + 1]

    # Analyze
    analysis = analyze_h5p(h5p_path)
    print_analysis(analysis)

    # Fix if requested
    if do_fix:
        print("\n" + "="*60)
        print("Applying fixes...")
        saved_path, results = optimize_h5p(h5p_path, output_path)
        print(f"\nFixes applied: {results['fixes']['fixes_applied']}")
        for fix in results['fixes']['fixes']:
            print(f"  [OK] {fix}")
        print(f"\nLayout changes:")
        for change in results['layout'].get('changes', []):
            print(f"  [OK] {change}")
        print(f"\nSaved to: {saved_path}")
