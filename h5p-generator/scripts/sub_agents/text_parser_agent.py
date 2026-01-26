"""
Text Parser Agent - Parst Freitext-Fragen in strukturierte Quiz-Formate

Unterstuetzte Input-Formate:
1. Simple Question: "Nenne 3 Merkmale..."
2. With Answers: "Was ist X? - Option A - Option B [correct]"
3. Batch TF: "--- Q: Aussage A: wahr ---"
"""

import re
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class QuestionType(Enum):
    """Erkannter Fragetyp"""
    TRUE_FALSE = "true_false"
    MULTI_CHOICE = "multi_choice"
    SINGLE_CHOICE = "single_choice"
    OPEN = "open"  # Kann zu TF-Aussagen konvertiert werden


class InputFormat(Enum):
    """Erkanntes Eingabeformat"""
    SIMPLE = "simple"           # Einzelne Frage ohne Antworten
    WITH_ANSWERS = "with_answers"  # Frage mit Antwortoptionen
    BATCH_TF = "batch_tf"       # Batch True/False mit --- Separatoren
    UNKNOWN = "unknown"


@dataclass
class ParsedQuestion:
    """Eine geparste Frage"""
    question_text: str
    question_type: QuestionType
    answers: Optional[list[dict]] = None  # [{"text": str, "correct": bool}]
    correct_answer: Optional[bool] = None  # Fuer TF-Fragen
    bloom_operator: Optional[str] = None
    confidence: float = 1.0
    raw_input: str = ""

    def to_true_false(self) -> dict:
        """Konvertiert zu True/False Format"""
        return {
            "text": self.question_text,
            "correct": self.correct_answer if self.correct_answer is not None else True
        }

    def to_multi_choice(self) -> dict:
        """Konvertiert zu Multiple Choice Format"""
        return {
            "question": self.question_text,
            "answers": self.answers or []
        }


@dataclass
class ParseResult:
    """Ergebnis des Parsens"""
    success: bool
    questions: list[ParsedQuestion] = field(default_factory=list)
    detected_format: InputFormat = InputFormat.UNKNOWN
    detected_type: QuestionType = QuestionType.TRUE_FALSE
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def question_count(self) -> int:
        return len(self.questions)

    def to_true_false_list(self) -> list[dict]:
        """Alle Fragen als True/False Liste"""
        return [q.to_true_false() for q in self.questions]

    def to_multi_choice_list(self) -> list[dict]:
        """Alle Fragen als Multiple Choice Liste"""
        return [q.to_multi_choice() for q in self.questions]


class TextParserAgent:
    """
    Parst Freitext-Fragen in strukturierte Quiz-Formate.

    Workflow:
    1. detect_format() - Erkennt das Eingabeformat
    2. parse() - Parst den Text basierend auf erkanntem Format
    3. Optionale: detect_operator() - Erkennt Bloom-Operatoren

    Beispiel:
        parser = TextParserAgent()
        result = parser.parse('''
            Was ist ein Debitor?
            - Ein Schuldner
            - Ein Glaeubiger [correct]
            - Ein Lieferant
        ''')
    """

    # Bloom-Operatoren und ihre Indikatoren
    BLOOM_OPERATORS = {
        'nennen': ['nenne', 'nennen', 'liste', 'zaehle', 'zaehl'],
        'beschreiben': ['beschreibe', 'beschreiben', 'erklaere', 'schildere'],
        'erklaeren': ['erklaere', 'erklaeren', 'erlaeutere', 'erlaeutern'],
        'zuordnen': ['ordne zu', 'zuordnen', 'kategorisiere', 'klassifiziere'],
        'bewerten': ['bewerte', 'bewerten', 'beurteile', 'analysiere'],
        'anwenden': ['wende an', 'anwenden', 'berechne', 'loeuse'],
        'definieren': ['definiere', 'definieren', 'was ist', 'was bedeutet'],
    }

    # TF-Antwort-Mapping
    TF_TRUE_INDICATORS = ['wahr', 'richtig', 'true', 'ja', 'korrekt', 'stimmt', 'w', 'r', 't']
    TF_FALSE_INDICATORS = ['falsch', 'unwahr', 'false', 'nein', 'inkorrekt', 'f', 'n']

    def __init__(self):
        """Initialisiert den Parser"""
        pass

    def detect_format(self, text: str) -> InputFormat:
        """
        Erkennt das Eingabeformat des Textes.

        Args:
            text: Der zu analysierende Text

        Returns:
            InputFormat Enum
        """
        text_stripped = text.strip()

        # Batch TF Format: Verwendet --- Separatoren und Q:/A: Pattern
        if '---' in text_stripped and re.search(r'Q:|A:', text_stripped, re.IGNORECASE):
            return InputFormat.BATCH_TF

        # With Answers Format: Hat Antwortoptionen mit - oder [correct]
        lines = text_stripped.split('\n')
        has_answer_markers = any(
            line.strip().startswith('-') and len(line.strip()) > 2
            for line in lines[1:]  # Erste Zeile ist meist die Frage
        )
        has_correct_marker = '[correct]' in text_stripped.lower() or '[korrekt]' in text_stripped.lower()

        if has_answer_markers and (has_correct_marker or len([l for l in lines if l.strip().startswith('-')]) >= 2):
            return InputFormat.WITH_ANSWERS

        # Simple Format: Einzelne Frage/Aussage
        if len(text_stripped) > 5:
            return InputFormat.SIMPLE

        return InputFormat.UNKNOWN

    def detect_operator(self, text: str) -> Optional[str]:
        """
        Erkennt Bloom-Operator in einem Text.

        Args:
            text: Der zu analysierende Text (meist eine Frage)

        Returns:
            Erkannter Operator oder None
        """
        text_lower = text.lower()

        for operator, indicators in self.BLOOM_OPERATORS.items():
            for indicator in indicators:
                # Wortgrenzen pruefen
                pattern = r'\b' + re.escape(indicator) + r'\b'
                if re.search(pattern, text_lower):
                    return operator

        return None

    def parse(self, text: str, force_type: Optional[str] = None) -> ParseResult:
        """
        Parst Freitext in strukturierte Fragen.

        Args:
            text: Der zu parsende Text
            force_type: Optional, erzwingt bestimmten Fragetyp ('true_false', 'multi_choice')

        Returns:
            ParseResult mit geparsten Fragen
        """
        text = text.strip()
        if not text:
            return ParseResult(
                success=False,
                errors=["Leerer Text uebergeben"]
            )

        detected_format = self.detect_format(text)

        # Parse basierend auf Format
        if detected_format == InputFormat.BATCH_TF:
            return self._parse_batch_tf(text)
        elif detected_format == InputFormat.WITH_ANSWERS:
            return self._parse_with_answers(text, force_type)
        elif detected_format == InputFormat.SIMPLE:
            return self._parse_simple(text, force_type)
        else:
            return ParseResult(
                success=False,
                detected_format=detected_format,
                errors=["Format konnte nicht erkannt werden"]
            )

    def _parse_batch_tf(self, text: str) -> ParseResult:
        """Parst Batch True/False Format"""
        questions = []
        errors = []
        warnings = []

        # Blöcke trennen (durch --- oder mehrere Newlines)
        blocks = re.split(r'---+|\n{2,}', text)

        for i, block in enumerate(blocks):
            block = block.strip()
            if not block:
                continue

            # Q:/A: Pattern extrahieren
            q_match = re.search(r'Q:\s*(.+?)(?=A:|$)', block, re.IGNORECASE | re.DOTALL)
            a_match = re.search(r'A:\s*(.+?)$', block, re.IGNORECASE | re.DOTALL)

            if q_match:
                question_text = q_match.group(1).strip()

                # Antwort auswerten
                correct_answer = True  # Default
                if a_match:
                    answer_text = a_match.group(1).strip().lower()
                    if any(ind in answer_text for ind in self.TF_FALSE_INDICATORS):
                        correct_answer = False
                    elif any(ind in answer_text for ind in self.TF_TRUE_INDICATORS):
                        correct_answer = True
                    else:
                        warnings.append(f"Block {i+1}: Antwort '{answer_text}' nicht eindeutig, default: wahr")

                questions.append(ParsedQuestion(
                    question_text=question_text,
                    question_type=QuestionType.TRUE_FALSE,
                    correct_answer=correct_answer,
                    bloom_operator=self.detect_operator(question_text),
                    raw_input=block
                ))
            elif block.strip():
                # Block ohne Q: Pattern - als einfache Aussage behandeln
                if len(block) > 10:  # Mindestlaenge
                    questions.append(ParsedQuestion(
                        question_text=block,
                        question_type=QuestionType.TRUE_FALSE,
                        correct_answer=True,
                        bloom_operator=self.detect_operator(block),
                        raw_input=block
                    ))

        return ParseResult(
            success=len(questions) > 0,
            questions=questions,
            detected_format=InputFormat.BATCH_TF,
            detected_type=QuestionType.TRUE_FALSE,
            errors=errors,
            warnings=warnings
        )

    def _parse_with_answers(self, text: str, force_type: Optional[str] = None) -> ParseResult:
        """Parst Format mit Antwortoptionen"""
        questions = []
        errors = []
        warnings = []

        # Mehrere Fragen trennen (doppelte Newlines oder Nummerierung)
        question_blocks = re.split(r'\n\s*\n|\n\d+\.\s+', text)

        for block in question_blocks:
            block = block.strip()
            if not block:
                continue

            lines = block.split('\n')
            if not lines:
                continue

            # Erste Nicht-Antwort-Zeile ist die Frage
            question_text = ""
            answers = []

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Antwortzeile (beginnt mit - oder * oder ist nummeriert)
                if re.match(r'^[-*]\s+|^\d+[\.\)]\s+|^[a-d][\.\)]\s+', line, re.IGNORECASE):
                    # Antwort extrahieren
                    answer_text = re.sub(r'^[-*\d\.a-d\)]+\s*', '', line, flags=re.IGNORECASE)
                    is_correct = False

                    # [correct] oder [korrekt] Marker prufen
                    if re.search(r'\[correct\]|\[korrekt\]|\[richtig\]|\[x\]', answer_text, re.IGNORECASE):
                        is_correct = True
                        answer_text = re.sub(r'\s*\[correct\]|\[korrekt\]|\[richtig\]|\[x\]\s*', '', answer_text, flags=re.IGNORECASE)

                    answer_text = answer_text.strip()
                    if answer_text:
                        answers.append({"text": answer_text, "correct": is_correct})
                else:
                    # Fragentext
                    if not question_text:
                        question_text = line
                    else:
                        question_text += " " + line

            if question_text:
                # Typ bestimmen
                if force_type == 'true_false':
                    q_type = QuestionType.TRUE_FALSE
                elif force_type == 'multi_choice' or len(answers) > 0:
                    q_type = QuestionType.MULTI_CHOICE
                else:
                    q_type = QuestionType.OPEN

                # Pruefen ob mindestens eine korrekte Antwort
                if answers and not any(a['correct'] for a in answers):
                    warnings.append(f"Keine korrekte Antwort markiert bei: {question_text[:40]}...")
                    # Erste Antwort als korrekt markieren
                    if answers:
                        answers[0]['correct'] = True

                questions.append(ParsedQuestion(
                    question_text=question_text,
                    question_type=q_type,
                    answers=answers if answers else None,
                    bloom_operator=self.detect_operator(question_text),
                    raw_input=block
                ))

        # Typ fuer alle bestimmen
        final_type = QuestionType.MULTI_CHOICE if any(q.answers for q in questions) else QuestionType.OPEN

        return ParseResult(
            success=len(questions) > 0,
            questions=questions,
            detected_format=InputFormat.WITH_ANSWERS,
            detected_type=final_type,
            errors=errors,
            warnings=warnings
        )

    def _parse_simple(self, text: str, force_type: Optional[str] = None) -> ParseResult:
        """Parst einfache Frage/Aussage"""
        questions = []
        warnings = []

        # Mehrere Aussagen trennen (Zeilenweise)
        lines = [l.strip() for l in text.split('\n') if l.strip()]

        for line in lines:
            # Listenpunkte entfernen
            line = re.sub(r'^[-*\d\.]+\s*', '', line).strip()
            if len(line) < 5:  # Zu kurz
                continue

            # Operator erkennen
            operator = self.detect_operator(line)

            # Typ basierend auf Operator
            if force_type == 'multi_choice':
                q_type = QuestionType.MULTI_CHOICE
            elif force_type == 'true_false':
                q_type = QuestionType.TRUE_FALSE
            elif operator in ['nennen', 'beschreiben', 'definieren']:
                # Diese Operatoren brauchen generierte Antworten -> OPEN
                q_type = QuestionType.OPEN
                warnings.append(f"Offene Frage erkannt, Distraktoren muessen generiert werden: {line[:40]}...")
            else:
                q_type = QuestionType.TRUE_FALSE

            questions.append(ParsedQuestion(
                question_text=line,
                question_type=q_type,
                bloom_operator=operator,
                correct_answer=True,  # Default fuer TF
                raw_input=line
            ))

        return ParseResult(
            success=len(questions) > 0,
            questions=questions,
            detected_format=InputFormat.SIMPLE,
            detected_type=QuestionType.TRUE_FALSE if not any(q.question_type == QuestionType.OPEN for q in questions) else QuestionType.OPEN,
            warnings=warnings
        )

    def extract_key_concepts(self, text: str) -> list[str]:
        """
        Extrahiert Schluesselkonzepte aus einem Text.
        Nuetzlich fuer Distractor-Generierung.

        Args:
            text: Der zu analysierende Text

        Returns:
            Liste von Schluesselkonzepten
        """
        concepts = []

        # Fachbegriffe in Anfuehrungszeichen
        quoted = re.findall(r'"([^"]+)"', text)
        concepts.extend(quoted)

        # Begriffe nach "ist ein/eine"
        is_a = re.findall(r'ist (?:ein|eine) ([A-Z][a-z]+)', text)
        concepts.extend(is_a)

        # Grossgeschriebene Woerter (potenzielle Fachbegriffe)
        caps = re.findall(r'\b([A-Z][a-z]{3,})\b', text)
        # Filtern: Nicht am Satzanfang
        for cap in caps:
            if cap not in concepts:
                concepts.append(cap)

        return list(set(concepts))


# =============================================================================
# CLI / Test
# =============================================================================

if __name__ == "__main__":
    parser = TextParserAgent()

    # Test 1: Simple Question
    print("=" * 60)
    print("Test 1: Simple Question")
    result = parser.parse("Nenne 3 Merkmale einer ordnungsgemaessen Buchfuehrung.")
    print(f"Format: {result.detected_format.value}")
    print(f"Type: {result.detected_type.value}")
    print(f"Questions: {result.question_count}")
    for q in result.questions:
        print(f"  - {q.question_text[:50]}... (Operator: {q.bloom_operator})")

    # Test 2: Multiple Choice
    print("\n" + "=" * 60)
    print("Test 2: Multiple Choice")
    result = parser.parse("""
Was ist ein Debitor?
- Ein Kunde, dem wir Geld schulden
- Ein Kunde, der uns Geld schuldet [correct]
- Ein Lieferant
- Die Bank
    """)
    print(f"Format: {result.detected_format.value}")
    print(f"Type: {result.detected_type.value}")
    for q in result.questions:
        print(f"  Frage: {q.question_text}")
        if q.answers:
            for a in q.answers:
                marker = "[X]" if a['correct'] else "[ ]"
                print(f"    {marker} {a['text']}")

    # Test 3: Batch True/False
    print("\n" + "=" * 60)
    print("Test 3: Batch True/False")
    result = parser.parse("""
---
Q: Ein Debitor ist ein Schuldner des Unternehmens.
A: wahr
---
Q: Kreditoren erscheinen auf der Aktivseite.
A: falsch
---
Q: Die Bilanz zeigt Vermoegen und Kapital.
A: richtig
    """)
    print(f"Format: {result.detected_format.value}")
    print(f"Questions: {result.question_count}")
    for q in result.questions:
        answer = "WAHR" if q.correct_answer else "FALSCH"
        print(f"  [{answer}] {q.question_text}")

    print("\n" + "=" * 60)
    print("Tests abgeschlossen!")
