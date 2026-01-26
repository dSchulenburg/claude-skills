"""
Distractor Generator - Generiert plausible falsche Antworten fuer Quiz-Fragen

Strategien:
1. Rule-based: Negation, Variation, Antonym
2. Domain-based: Vordefinierte Konzepte fuer Fachbereiche
3. Pattern-based: Aehnlich klingende Begriffe
"""

import re
import random
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DistractorResult:
    """Ergebnis der Distractor-Generierung"""
    distractors: list[str]
    strategy_used: str
    confidence: float = 0.8
    warnings: list[str] = field(default_factory=list)


class DistractorGenerator:
    """
    Generiert plausible falsche Antworten (Distraktoren) fuer Quiz-Fragen.

    Strategien:
    - Rule-based: Negation, Zahlen-Variation, Antonym
    - Domain-based: Fachbereichsspezifische Konzepte
    - Pattern-based: Syntaktische Variationen

    Beispiel:
        generator = DistractorGenerator()
        result = generator.generate(
            correct_answer="Debitor",
            question="Was beschreibt einen Kunden, der uns Geld schuldet?",
            domain="accounting",
            count=3
        )
        # -> ["Kreditor", "Lieferant", "Glaeubiger"]
    """

    # Domain-Templates fuer BS:WI-relevante Bereiche
    DOMAIN_CONCEPTS = {
        # Buchfuehrung/Rechnungswesen
        'accounting': {
            'debitor': ['Kreditor', 'Lieferant', 'Glaeubiger', 'Schuldner', 'Kunde'],
            'kreditor': ['Debitor', 'Kunde', 'Abnehmer', 'Schuldner', 'Kaeufer'],
            'aktiva': ['Passiva', 'Eigenkapital', 'Fremdkapital', 'Verbindlichkeiten'],
            'passiva': ['Aktiva', 'Anlagevermoegen', 'Umlaufvermoegen', 'Forderungen'],
            'soll': ['Haben', 'Kredit', 'Passiv', 'Minus'],
            'haben': ['Soll', 'Debit', 'Aktiv', 'Plus'],
            'bilanz': ['GuV', 'Kassenbuch', 'Inventar', 'Jahresabschluss'],
            'aufwand': ['Ertrag', 'Einnahme', 'Gewinn', 'Umsatz'],
            'ertrag': ['Aufwand', 'Ausgabe', 'Verlust', 'Kosten'],
            'eigenkapital': ['Fremdkapital', 'Verbindlichkeiten', 'Schulden', 'Darlehen'],
            'fremdkapital': ['Eigenkapital', 'Ruecklagen', 'Gewinnvortrag', 'Stammkapital'],
            'inventur': ['Inventar', 'Bilanz', 'Bestandsaufnahme', 'Pruefung'],
            'inventar': ['Inventur', 'Bilanz', 'Verzeichnis', 'Liste'],
            '_generic': ['Debitor', 'Kreditor', 'Aktiva', 'Passiva', 'Soll', 'Haben', 'Bilanz', 'GuV']
        },

        # Scrum/Agile
        'scrum': {
            'product owner': ['Scrum Master', 'Developer', 'Stakeholder', 'Team Lead'],
            'scrum master': ['Product Owner', 'Developer', 'Project Manager', 'Team Lead'],
            'developer': ['Product Owner', 'Scrum Master', 'Stakeholder', 'Tester'],
            'sprint': ['Release', 'Iteration', 'Phase', 'Meilenstein'],
            'backlog': ['Sprint', 'Kanban', 'Roadmap', 'Anforderungsliste'],
            'daily': ['Weekly', 'Monthly', 'Sprint Planning', 'Review'],
            'retrospektive': ['Review', 'Planning', 'Daily', 'Refinement'],
            'user story': ['Epic', 'Task', 'Feature', 'Requirement'],
            '_generic': ['Product Owner', 'Scrum Master', 'Developer', 'Sprint', 'Backlog', 'Daily', 'Review']
        },

        # IT-Grundlagen
        'it': {
            'cpu': ['GPU', 'RAM', 'SSD', 'Mainboard'],
            'ram': ['CPU', 'HDD', 'Cache', 'VRAM'],
            'ssd': ['HDD', 'RAM', 'CPU', 'USB'],
            'lan': ['WAN', 'WLAN', 'MAN', 'PAN'],
            'http': ['HTTPS', 'FTP', 'SMTP', 'TCP'],
            'ip-adresse': ['MAC-Adresse', 'URL', 'DNS', 'Port'],
            'datenbank': ['Dateisystem', 'Speicher', 'Server', 'Cache'],
            '_generic': ['Server', 'Client', 'Netzwerk', 'Datenbank', 'Protokoll', 'Hardware', 'Software']
        },

        # Allgemeine Wirtschaft
        'business': {
            'angebot': ['Nachfrage', 'Preis', 'Menge', 'Markt'],
            'nachfrage': ['Angebot', 'Preis', 'Bedarf', 'Konsum'],
            'gewinn': ['Verlust', 'Umsatz', 'Kosten', 'Aufwand'],
            'verlust': ['Gewinn', 'Ertrag', 'Einnahme', 'Umsatz'],
            'kosten': ['Ertrag', 'Gewinn', 'Umsatz', 'Einnahme'],
            '_generic': ['Angebot', 'Nachfrage', 'Preis', 'Menge', 'Markt', 'Gewinn', 'Verlust']
        }
    }

    # Negations-Patterns
    NEGATION_PREFIXES = ['nicht', 'kein', 'un-', 'miss-', 'anti-']
    NEGATION_WORDS = {
        'ja': 'nein', 'nein': 'ja',
        'wahr': 'falsch', 'falsch': 'wahr',
        'richtig': 'falsch', 'falsch': 'richtig',
        'positiv': 'negativ', 'negativ': 'positiv',
        'gross': 'klein', 'klein': 'gross',
        'hoch': 'niedrig', 'niedrig': 'hoch',
        'mehr': 'weniger', 'weniger': 'mehr',
        'steigt': 'sinkt', 'sinkt': 'steigt',
        'erhoeht': 'senkt', 'senkt': 'erhoeht',
    }

    # Zahlen-Variationen
    NUMBER_VARIATIONS = {
        '1': ['2', '3', '0'],
        '2': ['1', '3', '4'],
        '3': ['2', '4', '5'],
        '4': ['3', '5', '6'],
        '5': ['4', '6', '7'],
        '10': ['5', '15', '20'],
        '100': ['50', '150', '200'],
    }

    def __init__(self):
        """Initialisiert den Generator"""
        pass

    def generate(
        self,
        correct_answer: str,
        question: str = "",
        domain: Optional[str] = None,
        count: int = 3,
        exclude: list[str] = None
    ) -> DistractorResult:
        """
        Generiert Distraktoren fuer eine korrekte Antwort.

        Args:
            correct_answer: Die korrekte Antwort
            question: Die Frage (fuer Kontext)
            domain: Fachbereich ('accounting', 'scrum', 'it', 'business')
            count: Anzahl zu generierender Distraktoren
            exclude: Liste von Begriffen, die nicht verwendet werden sollen

        Returns:
            DistractorResult mit Distraktoren
        """
        exclude = exclude or []
        exclude.append(correct_answer.lower())
        distractors = []
        warnings = []
        strategy = "mixed"

        # 1. Domain-basierte Distraktoren (beste Qualitaet)
        if domain and domain in self.DOMAIN_CONCEPTS:
            domain_results = self._generate_from_domain(correct_answer, domain, exclude)
            distractors.extend(domain_results)

        # 2. Automatische Domain-Erkennung aus Frage
        if not domain and question:
            detected_domain = self._detect_domain(question + " " + correct_answer)
            if detected_domain:
                domain_results = self._generate_from_domain(correct_answer, detected_domain, exclude + distractors)
                distractors.extend(domain_results)
                strategy = f"auto_domain:{detected_domain}"

        # 3. Rule-based Fallback
        if len(distractors) < count:
            rule_results = self._generate_rule_based(correct_answer, question, exclude + distractors)
            distractors.extend(rule_results)

        # 4. Generic Fallback
        if len(distractors) < count:
            generic_results = self._generate_generic(correct_answer, question, count - len(distractors), exclude + distractors)
            distractors.extend(generic_results)
            if generic_results:
                warnings.append("Einige Distraktoren sind generisch und sollten manuell geprueft werden")

        # Auf count begrenzen und deduplizieren
        seen = set()
        unique_distractors = []
        for d in distractors:
            d_lower = d.lower()
            if d_lower not in seen and d_lower not in [e.lower() for e in exclude]:
                seen.add(d_lower)
                unique_distractors.append(d)
                if len(unique_distractors) >= count:
                    break

        # Confidence basierend auf Strategie
        confidence = 0.9 if domain else 0.7

        return DistractorResult(
            distractors=unique_distractors,
            strategy_used=strategy,
            confidence=confidence,
            warnings=warnings
        )

    def _detect_domain(self, text: str) -> Optional[str]:
        """Erkennt Domain aus Text"""
        text_lower = text.lower()

        # Domain-Indikatoren
        domain_indicators = {
            'accounting': ['debitor', 'kreditor', 'bilanz', 'buchung', 'konto', 'soll', 'haben', 'aktiv', 'passiv', 'buchfuehrung', 'rechnungswesen'],
            'scrum': ['scrum', 'sprint', 'backlog', 'product owner', 'agile', 'kanban', 'retrospektive', 'daily'],
            'it': ['server', 'client', 'netzwerk', 'datenbank', 'protokoll', 'ip', 'http', 'software', 'hardware', 'programmierung'],
            'business': ['angebot', 'nachfrage', 'markt', 'preis', 'kosten', 'gewinn', 'verlust', 'wirtschaft']
        }

        for domain, indicators in domain_indicators.items():
            matches = sum(1 for ind in indicators if ind in text_lower)
            if matches >= 1:
                return domain

        return None

    def _generate_from_domain(self, answer: str, domain: str, exclude: list[str]) -> list[str]:
        """Generiert Distraktoren aus Domain-Wissen"""
        distractors = []
        concepts = self.DOMAIN_CONCEPTS.get(domain, {})
        answer_lower = answer.lower()

        # Exakte Match suchen
        if answer_lower in concepts:
            candidates = concepts[answer_lower]
            for c in candidates:
                if c.lower() not in [e.lower() for e in exclude]:
                    distractors.append(c)

        # Generische Domain-Begriffe als Fallback
        if len(distractors) < 3 and '_generic' in concepts:
            for c in concepts['_generic']:
                if c.lower() not in [e.lower() for e in exclude] and c.lower() not in [d.lower() for d in distractors]:
                    distractors.append(c)

        return distractors[:4]  # Max 4 zurueckgeben

    def _generate_rule_based(self, answer: str, question: str, exclude: list[str]) -> list[str]:
        """Generiert Distraktoren mit Regeln"""
        distractors = []
        answer_lower = answer.lower()

        # 1. Negation/Antonym
        for word, antonym in self.NEGATION_WORDS.items():
            if word in answer_lower:
                negated = answer_lower.replace(word, antonym)
                # Kapitalisierung wiederherstellen
                if answer[0].isupper():
                    negated = negated.capitalize()
                if negated.lower() not in [e.lower() for e in exclude]:
                    distractors.append(negated)
                break

        # 2. Zahlen-Variation
        numbers = re.findall(r'\d+', answer)
        for num in numbers:
            if num in self.NUMBER_VARIATIONS:
                for var in self.NUMBER_VARIATIONS[num]:
                    varied = answer.replace(num, var)
                    if varied.lower() not in [e.lower() for e in exclude + distractors]:
                        distractors.append(varied)
                        break

        # 3. Wortreihenfolge aendern (bei mehreren Woertern)
        words = answer.split()
        if len(words) >= 2:
            # Reversed
            reversed_answer = ' '.join(reversed(words))
            if reversed_answer.lower() not in [e.lower() for e in exclude + distractors] and reversed_answer != answer:
                distractors.append(reversed_answer)

        return distractors

    def _generate_generic(self, answer: str, question: str, count: int, exclude: list[str]) -> list[str]:
        """Generiert generische Distraktoren als Fallback"""
        distractors = []

        # Generische Antworten basierend auf Fragemuster
        generic_options = [
            "Keine der Antworten",
            "Alle Antworten sind korrekt",
            "Kann nicht bestimmt werden",
        ]

        # Laengenbasierte Generierung
        answer_len = len(answer)
        if answer_len < 10:
            generic_options.extend(["Option A", "Option B", "Option C", "Variante X"])
        else:
            generic_options.extend([
                "Das Gegenteil ist der Fall",
                "Dies trifft nicht zu",
                "Eine andere Definition gilt",
            ])

        for opt in generic_options:
            if opt.lower() not in [e.lower() for e in exclude + distractors]:
                distractors.append(opt)
                if len(distractors) >= count:
                    break

        return distractors

    def generate_true_false_variants(
        self,
        statement: str,
        correct: bool = True,
        count: int = 3
    ) -> list[dict]:
        """
        Generiert True/False Varianten aus einer Aussage.

        Args:
            statement: Die urspruengliche Aussage
            correct: Ob die urspruengliche Aussage wahr ist
            count: Anzahl Varianten (inkl. Original)

        Returns:
            Liste von {"text": str, "correct": bool}
        """
        variants = [{"text": statement, "correct": correct}]

        # Negierte Version
        negated = self._negate_statement(statement)
        if negated != statement:
            variants.append({"text": negated, "correct": not correct})

        # Variationen durch Wortaustausch
        for word, antonym in self.NEGATION_WORDS.items():
            if word in statement.lower():
                # Einfacher Replace
                varied = statement
                # Case-insensitive replace mit Erhaltung der Gross-/Kleinschreibung
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                varied = pattern.sub(antonym, varied)
                if varied not in [v["text"] for v in variants]:
                    variants.append({"text": varied, "correct": not correct})
                break

        return variants[:count]

    def _negate_statement(self, statement: str) -> str:
        """Negiert eine Aussage"""
        # Einfache Negation durch Einfuegen von "nicht"
        words = statement.split()

        # "ist" -> "ist nicht"
        if 'ist' in words:
            idx = words.index('ist')
            if idx + 1 < len(words) and words[idx + 1] != 'nicht':
                words.insert(idx + 1, 'nicht')
                return ' '.join(words)

        # "sind" -> "sind nicht"
        if 'sind' in words:
            idx = words.index('sind')
            if idx + 1 < len(words) and words[idx + 1] != 'nicht':
                words.insert(idx + 1, 'nicht')
                return ' '.join(words)

        # Fallback: "nicht" am Ende
        if 'nicht' not in words:
            return statement + " nicht"

        return statement

    def get_domain_concepts(self, domain: str) -> list[str]:
        """Gibt alle Konzepte einer Domain zurueck"""
        if domain not in self.DOMAIN_CONCEPTS:
            return []

        concepts = []
        for key, values in self.DOMAIN_CONCEPTS[domain].items():
            if key != '_generic':
                concepts.append(key)
                concepts.extend(values)
        return list(set(concepts))


# =============================================================================
# CLI / Test
# =============================================================================

if __name__ == "__main__":
    generator = DistractorGenerator()

    print("=" * 60)
    print("Distractor Generator - Tests")
    print("=" * 60)

    # Test 1: Domain-basiert (Accounting)
    print("\nTest 1: Accounting Domain")
    result = generator.generate(
        correct_answer="Debitor",
        question="Was beschreibt einen Kunden, der uns Geld schuldet?",
        domain="accounting",
        count=3
    )
    print(f"Korrekte Antwort: Debitor")
    print(f"Distraktoren: {result.distractors}")
    print(f"Strategie: {result.strategy_used}")

    # Test 2: Domain-basiert (Scrum)
    print("\n" + "-" * 40)
    print("Test 2: Scrum Domain")
    result = generator.generate(
        correct_answer="Product Owner",
        question="Wer priorisiert das Backlog?",
        domain="scrum",
        count=3
    )
    print(f"Korrekte Antwort: Product Owner")
    print(f"Distraktoren: {result.distractors}")

    # Test 3: Auto-Domain-Erkennung
    print("\n" + "-" * 40)
    print("Test 3: Auto Domain Detection")
    result = generator.generate(
        correct_answer="Haben",
        question="Auf welcher Seite werden Ertraege gebucht?",
        count=3
    )
    print(f"Korrekte Antwort: Haben")
    print(f"Distraktoren: {result.distractors}")
    print(f"Strategie: {result.strategy_used}")

    # Test 4: True/False Varianten
    print("\n" + "-" * 40)
    print("Test 4: True/False Varianten")
    variants = generator.generate_true_false_variants(
        "Ein Debitor ist ein Kunde, der uns Geld schuldet.",
        correct=True,
        count=4
    )
    for v in variants:
        marker = "[WAHR]" if v["correct"] else "[FALSCH]"
        print(f"  {marker} {v['text']}")

    # Test 5: Zahlen-Variation
    print("\n" + "-" * 40)
    print("Test 5: Zahlen-Variation")
    result = generator.generate(
        correct_answer="3 Scrum-Rollen",
        question="Wie viele Rollen gibt es in Scrum?",
        count=3
    )
    print(f"Korrekte Antwort: 3 Scrum-Rollen")
    print(f"Distraktoren: {result.distractors}")

    print("\n" + "=" * 60)
    print("Tests abgeschlossen!")
