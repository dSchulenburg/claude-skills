#!/usr/bin/env python3
"""Generiert ein interaktives Buch: KI fuer Lehrerinnen und Lehrer"""
import sys
sys.path.insert(0, '.')
from h5p_containers import create_interactive_book

chapters = [
    {
        'title': 'Kapitel 1: Was ist KI?',
        'elements': [
            {
                'library': 'H5P.AdvancedText 1.1',
                'params': {'text': '<h2>Was ist K&uuml;nstliche Intelligenz?</h2><p>KI ist ein Teilgebiet der Informatik, das Systeme entwickelt, die Aufgaben ausf&uuml;hren, die normalerweise menschliche Intelligenz erfordern: Sprachverarbeitung, Bilderkennung, Entscheidungsfindung und Lernen aus Daten.</p><p>In diesem Buch lernen Sie, wie KI Ihren Unterricht bereichern kann.</p>'}
            },
            {
                'library': 'H5P.TrueFalse 1.8',
                'params': {
                    'question': '<p>KI kann selbstst&auml;ndig denken und f&uuml;hlen wie ein Mensch.</p>',
                    'correct': 'false',
                    'l10n': {'trueText': 'Wahr', 'falseText': 'Falsch'},
                    'behaviour': {'enableRetry': True, 'enableSolutionsButton': True, 'confirmCheckDialog': False, 'confirmRetryDialog': False},
                    'feedbackOnCorrect': 'Richtig! KI simuliert intelligentes Verhalten, denkt oder f&uuml;hlt aber nicht.',
                    'feedbackOnWrong': 'Falsch. KI simuliert intelligentes Verhalten, kann aber nicht wirklich denken.'
                }
            },
            {
                'library': 'H5P.MultiChoice 1.16',
                'params': {
                    'question': '<p>Welche Technologien basieren auf KI?</p>',
                    'answers': [
                        {'text': '<p>Sprachassistenten (Siri, Alexa)</p>', 'correct': True, 'tpiMessage': 'Richtig! Sprachassistenten nutzen Natural Language Processing.'},
                        {'text': '<p>Taschenrechner</p>', 'correct': False, 'tpiMessage': 'Ein Taschenrechner folgt festen Regeln, keine KI.'},
                        {'text': '<p>ChatGPT / Claude</p>', 'correct': True, 'tpiMessage': 'Richtig! Chatbots sind generative KI.'},
                        {'text': '<p>Excel-Formeln</p>', 'correct': False, 'tpiMessage': 'Excel-Formeln sind regelbasiert.'},
                        {'text': '<p>DeepL &Uuml;bersetzung</p>', 'correct': True, 'tpiMessage': 'Richtig! DeepL nutzt neuronale Netze.'}
                    ],
                    'behaviour': {'enableRetry': True, 'enableSolutionsButton': True, 'enableCheckButton': True, 'type': 'auto', 'singlePoint': False},
                    'UI': {'checkAnswerButton': 'Pr&uuml;fen', 'showSolutionButton': 'L&ouml;sung', 'tryAgainButton': 'Nochmal', 'correctText': 'Richtig!', 'incorrectText': 'Falsch!', 'shouldCheck': 'H&auml;tte gew&auml;hlt werden m&uuml;ssen', 'shouldNotCheck': 'H&auml;tte nicht gew&auml;hlt werden sollen', 'noInput': 'Bitte antworten'}
                }
            },
            {
                'library': 'H5P.Accordion 1.0',
                'params': {
                    'panels': [
                        {'title': 'Maschinelles Lernen', 'content': {'params': {'text': '<p>Algorithmen lernen aus Daten, ohne explizit programmiert zu werden. Beispiel: Spam-Filter lernt aus markierten E-Mails.</p>'}, 'library': 'H5P.AdvancedText 1.1', 'subContentId': 'acc-1', 'metadata': {'contentType': 'Text', 'license': 'U', 'title': 'ML'}}},
                        {'title': 'Neuronales Netz', 'content': {'params': {'text': '<p>Mathematisches Modell nach Vorbild des Gehirns. Neuronen in Schichten verarbeiten Informationen. Grundlage f&uuml;r Deep Learning und ChatGPT.</p>'}, 'library': 'H5P.AdvancedText 1.1', 'subContentId': 'acc-2', 'metadata': {'contentType': 'Text', 'license': 'U', 'title': 'NN'}}},
                        {'title': 'Generative KI', 'content': {'params': {'text': '<p>KI-Systeme die neue Inhalte erzeugen: Texte (ChatGPT, Claude), Bilder (DALL-E, Midjourney), Code, Musik. Seit 2022 der gr&ouml;&szlig;te KI-Durchbruch.</p>'}, 'library': 'H5P.AdvancedText 1.1', 'subContentId': 'acc-3', 'metadata': {'contentType': 'Text', 'license': 'U', 'title': 'GenAI'}}},
                        {'title': 'Prompt', 'content': {'params': {'text': '<p>Die Eingabe (Anweisung) an ein KI-System. Je pr&auml;ziser der Prompt, desto besser das Ergebnis. Prompt Engineering ist die Kunst, gute Anweisungen zu formulieren.</p>'}, 'library': 'H5P.AdvancedText 1.1', 'subContentId': 'acc-4', 'metadata': {'contentType': 'Text', 'license': 'U', 'title': 'Prompt'}}},
                        {'title': 'Halluzination', 'content': {'params': {'text': '<p>Wenn KI plausibel klingende, aber falsche Informationen generiert. KI &quot;erfindet&quot; Quellen und Fakten. Daher ist Faktencheck immer Pflicht!</p>'}, 'library': 'H5P.AdvancedText 1.1', 'subContentId': 'acc-5', 'metadata': {'contentType': 'Text', 'license': 'U', 'title': 'Halluzination'}}}
                    ],
                    'hTag': 'h3'
                }
            }
        ]
    },
    {
        'title': 'Kapitel 2: KI-Tools im &Uuml;berblick',
        'elements': [
            {'library': 'H5P.AdvancedText 1.1', 'params': {'text': '<h2>KI-Tools f&uuml;r den Unterricht</h2><p>Hunderte KI-Tools sind f&uuml;r Lehrkr&auml;fte relevant. Hier die wichtigsten Kategorien.</p>'}},
            {
                'library': 'H5P.DragText 1.10',
                'params': {
                    'textField': 'F&uuml;r Textgenerierung nutze ich *ChatGPT* oder *Claude*.\nBilder erzeuge ich mit *DALL-E* oder *Midjourney*.\nF&uuml;r &Uuml;bersetzungen eignet sich *DeepL* besonders gut.\nPr&auml;sentationen erstelle ich mit *Gamma*.',
                    'taskDescription': '<p>Ziehe die KI-Tools an die richtige Stelle.</p>',
                    'checkAnswer': 'Pr&uuml;fen', 'tryAgain': 'Nochmal', 'showSolution': 'L&ouml;sung',
                    'behaviour': {'enableRetry': True, 'enableSolutionsButton': True, 'enableCheckButton': True, 'instantFeedback': False}
                }
            },
            {
                'library': 'H5P.Dialogcards 1.9',
                'params': {
                    'title': '<p>KI-Tool-Steckbriefe</p>', 'mode': 'normal',
                    'description': '<p>Lernen Sie die wichtigsten KI-Tools kennen.</p>',
                    'dialogs': [
                        {'text': '<p>ChatGPT</p>', 'answer': '<p>Chatbot von OpenAI. Texte, Fragen, Code. Kostenlos (GPT-3.5) und Plus (GPT-4). Seit November 2022.</p>'},
                        {'text': '<p>Claude</p>', 'answer': '<p>Chatbot von Anthropic. Stark bei langen Texten, Analyse, Programmierung. Sorgf&auml;ltige Antworten.</p>'},
                        {'text': '<p>DeepL</p>', 'answer': '<p>KI-&Uuml;bersetzer aus Deutschland. 30+ Sprachen. DeepL Write korrigiert Texte. Datenschutzkonform.</p>'},
                        {'text': '<p>Perplexity</p>', 'answer': '<p>KI-Suchmaschine mit Quellenangabe. Ideal f&uuml;r Recherche.</p>'},
                        {'text': '<p>SchulKI</p>', 'answer': '<p>Deutsche KI-Plattform f&uuml;r Schulen. DSGVO-konform. Keine SuS-Registrierung n&ouml;tig.</p>'}
                    ],
                    'behaviour': {'enableRetry': True, 'disableBackwardsNavigation': False, 'randomCards': False}
                }
            },
            {
                'library': 'H5P.MarkTheWords 1.11',
                'params': {
                    'taskDescription': '<p>Markiere alle W&ouml;rter, die KI-bezogene Risiken beschreiben.</p>',
                    'textField': 'Beim KI-Einsatz muss man auf *Halluzinationen* achten. Der *Datenschutz* ist wichtig bei *Sch&uuml;lerdaten*. Es droht *Abh&auml;ngigkeit* und *Plagiat*. *Bias* f&uuml;hrt zu *Diskriminierung*.',
                    'behaviour': {'enableRetry': True, 'enableSolutionsButton': True, 'enableCheckButton': True},
                    'checkAnswerButton': 'Pr&uuml;fen', 'tryAgainButton': 'Nochmal', 'showSolutionButton': 'L&ouml;sung'
                }
            }
        ]
    },
    {
        'title': 'Kapitel 3: Prompt Engineering',
        'elements': [
            {'library': 'H5P.AdvancedText 1.1', 'params': {'text': '<h2>Prompt Engineering f&uuml;r Lehrkr&auml;fte</h2><p>Die 5 Elemente eines guten Prompts:</p><ol><li><strong>Rolle:</strong> Wer soll die KI sein?</li><li><strong>Aufgabe:</strong> Was soll getan werden?</li><li><strong>Kontext:</strong> F&uuml;r wen? Welches Niveau?</li><li><strong>Format:</strong> Wie soll die Ausgabe aussehen?</li><li><strong>Einschr&auml;nkungen:</strong> Was soll vermieden werden?</li></ol>'}},
            {
                'library': 'H5P.SortParagraphs 0.11',
                'params': {
                    'taskDescription': '<p>Bringe die Prompt-Elemente in die empfohlene Reihenfolge.</p>',
                    'paragraphs': [
                        {'text': '<p><strong>1. Rolle:</strong> &quot;Du bist ein erfahrener Berufsschullehrer.&quot;</p>'},
                        {'text': '<p><strong>2. Aufgabe:</strong> &quot;Erstelle ein Arbeitsblatt zum Thema Angebot und Nachfrage.&quot;</p>'},
                        {'text': '<p><strong>3. Kontext:</strong> &quot;1. Ausbildungsjahr, Kaufleute im Einzelhandel.&quot;</p>'},
                        {'text': '<p><strong>4. Format:</strong> &quot;5 MC-Fragen und 3 offene Fragen.&quot;</p>'},
                        {'text': '<p><strong>5. Einschr&auml;nkungen:</strong> &quot;Einfache Sprache, maximal 2 Seiten.&quot;</p>'}
                    ],
                    'behaviour': {'enableRetry': True, 'enableSolutionsButton': True, 'scoringMode': 'positions'},
                    'l10n': {'checkAnswer': 'Pr&uuml;fen', 'tryAgain': 'Nochmal', 'showSolution': 'L&ouml;sung', 'up': 'Hoch', 'down': 'Runter', 'correctAnswer': 'Richtig', 'wrongAnswer': 'Falsch', 'yourResult': '@score von @total Punkten'}
                }
            },
            {
                'library': 'H5P.Essay 1.5',
                'params': {
                    'media': {'type': {'params': {}}, 'disableImageZooming': False},
                    'taskDescription': '<p>Schreiben Sie einen Prompt f&uuml;r ein Arbeitsblatt. Nutzen Sie alle 5 Elemente (Rolle, Aufgabe, Kontext, Format, Einschr&auml;nkungen).</p>',
                    'solution': {'introduction': '<p>Beispiel-Prompt:</p>', 'sample': '<p>Du bist ein Berufsschullehrer f&uuml;r Wirtschaft. Erstelle ein Arbeitsblatt zu Kaufvertragsst&ouml;rungen. 2. Ausbildungsjahr, Gro&szlig;handelskaufleute. Ein Fallbeispiel + 3 Fragen + Zuordnungsaufgabe. Einfache Sprache, max. 2 Seiten.</p>'},
                    'keywords': [
                        {'keyword': 'Rolle', 'alternatives': ['Du bist', 'Agiere als'], 'options': {'points': 1, 'forgiveMistakes': True, 'caseSensitive': False}},
                        {'keyword': 'Erstelle', 'alternatives': ['Schreibe', 'Generiere', 'Entwirf'], 'options': {'points': 1, 'forgiveMistakes': True, 'caseSensitive': False}},
                        {'keyword': 'Klasse', 'alternatives': ['Jahrgang', 'Ausbildungsjahr', 'Schueler'], 'options': {'points': 1, 'forgiveMistakes': True, 'caseSensitive': False}},
                        {'keyword': 'Format', 'alternatives': ['Tabelle', 'Fragen', 'Aufgaben', 'Seiten'], 'options': {'points': 1, 'forgiveMistakes': True, 'caseSensitive': False}},
                        {'keyword': 'maximal', 'alternatives': ['nicht', 'kein', 'vermeiden', 'einfach'], 'options': {'points': 1, 'forgiveMistakes': True, 'caseSensitive': False}}
                    ],
                    'overallFeedback': [{'from': 0, 'to': 40, 'feedback': 'Versuche, mehr der 5 Elemente einzubauen.'}, {'from': 41, 'to': 70, 'feedback': 'Guter Ansatz!'}, {'from': 71, 'to': 100, 'feedback': 'Hervorragend!'}],
                    'behaviour': {'minimumLength': 50, 'inputFieldSize': 10, 'enableRetry': True, 'enableSolutionsButton': True, 'ignoreScoring': False, 'pointsHost': 1},
                    'checkAnswer': 'Pr&uuml;fen', 'tryAgain': 'Nochmal', 'showSolution': 'L&ouml;sung',
                    'feedbackHeader': 'Feedback', 'solutionTitle': 'Beispiel',
                    'remainingChars': 'Verbleibend: @chars', 'notEnoughChars': 'Mind. @chars Zeichen!',
                    'ariaYourResult': '@score von @total'
                }
            },
            {
                'library': 'H5P.Summary 1.10',
                'params': {
                    'intro': '<p>W&auml;hle jeweils die richtige Aussage.</p>',
                    'summaries': [
                        {'summary': [{'text': '<p>Ein guter Prompt enth&auml;lt Rolle, Aufgabe, Kontext, Format und Einschr&auml;nkungen.</p>', 'correct': True}, {'text': '<p>Je k&uuml;rzer, desto besser.</p>', 'correct': False}, {'text': '<p>Reihenfolge ist egal.</p>', 'correct': False}]},
                        {'summary': [{'text': '<p>Iteratives Prompting verbessert das Ergebnis schrittweise.</p>', 'correct': True}, {'text': '<p>Immer nur einen Prompt verwenden.</p>', 'correct': False}, {'text': '<p>KI versteht jeden Prompt gleich gut.</p>', 'correct': False}]},
                        {'summary': [{'text': '<p>Few-Shot Beispiele verbessern die Qualit&auml;t.</p>', 'correct': True}, {'text': '<p>Beispiele verwirren die KI.</p>', 'correct': False}, {'text': '<p>Few-Shot nur bei ChatGPT.</p>', 'correct': False}]}
                    ],
                    'solvedLabel': 'Gel&ouml;st:', 'scoreLabel': 'Fehler:', 'resultLabel': 'Ergebnis', 'labelCorrect': 'Richtig!', 'labelIncorrect': 'Falsch!', 'tipButtonLabel': 'Tipp'
                }
            }
        ]
    },
    {
        'title': 'Kapitel 4: Unterrichtsvorbereitung mit KI',
        'elements': [
            {'library': 'H5P.AdvancedText 1.1', 'params': {'text': '<h2>KI in der Unterrichtsvorbereitung</h2><p>Unterrichtsvorbereitung ist der Bereich, in dem KI am meisten Zeit spart.</p>'}},
            {
                'library': 'H5P.SingleChoiceSet 1.11',
                'params': {
                    'choices': [
                        {'question': '<p>Bestes Tool f&uuml;r differenzierte Arbeitsbl&auml;tter?</p>', 'answers': ['<p>ChatGPT / Claude</p>', '<p>DALL-E</p>', '<p>DeepL</p>']},
                        {'question': '<p>Was bei KI-Material IMMER tun?</p>', 'answers': ['<p>Fachlich pr&uuml;fen und anpassen</p>', '<p>Unver&auml;ndert nutzen</p>', '<p>Sofort verteilen</p>']},
                        {'question': '<p>Wie hilft KI bei Differenzierung?</p>', 'answers': ['<p>Verschiedene Schwierigkeitsstufen</p>', '<p>Automatische Gruppeneinteilung</p>', '<p>Noten vergeben</p>']},
                        {'question': '<p>Prompt-Technik f&uuml;r Klausuren?</p>', 'answers': ['<p>Bloom-Operatoren nutzen</p>', '<p>Nur &quot;Schreibe Klausur&quot;</p>', '<p>Alte Klausuren fotografieren</p>']}
                    ],
                    'behaviour': {'autoContinue': True, 'timeoutCorrect': 2000, 'timeoutWrong': 3000, 'enableRetry': True, 'enableSolutionsButton': True},
                    'l10n': {'nextButtonLabel': 'Weiter', 'showSolutionButtonLabel': 'L&ouml;sung', 'retryButtonLabel': 'Nochmal', 'correctText': 'Richtig!', 'incorrectText': 'Falsch!', 'slideOfTotal': '@current von @total', 'scoreBarLabel': '@score von @total'}
                }
            },
            {
                'library': 'H5P.Blanks 1.14',
                'params': {
                    'text': '<p>KI hilft bei der *Differenzierung*, indem sie Material in verschiedenen *Schwierigkeitsstufen* erstellt.</p><p>Mit *Few-Shot* Prompting gibt man der KI *Beispiele* f&uuml;r das gew&uuml;nschte *Format*.</p><p>Generierte Inhalte m&uuml;ssen fachlich *gepr&uuml;ft* werden, um *Halluzinationen* auszuschlie&szlig;en.</p>',
                    'showSolutions': 'L&ouml;sung', 'tryAgain': 'Nochmal', 'checkAnswer': 'Pr&uuml;fen',
                    'notFilledOut': 'Bitte alles ausf&uuml;llen!', 'answerIsCorrect': 'Richtig!', 'answerIsWrong': 'Falsch!',
                    'behaviour': {'enableRetry': True, 'enableSolutionsButton': True, 'enableCheckButton': True, 'caseSensitive': False, 'acceptSpellingErrors': True}
                }
            }
        ]
    },
    {
        'title': 'Kapitel 5: Ethik und Datenschutz',
        'elements': [
            {'library': 'H5P.AdvancedText 1.1', 'params': {'text': '<h2>Ethik, Datenschutz und kritischer Umgang</h2><p>KI im Bildungsbereich wirft wichtige ethische und rechtliche Fragen auf.</p>'}},
            {
                'library': 'H5P.BranchingScenario 1.8',
                'params': {
                    'branchingScenario': {
                        'content': [
                            {'type': {'library': 'H5P.AdvancedText 1.1', 'params': {'text': '<h3>Szenario: KI im Klassenzimmer</h3><p>Ein Sch&uuml;ler gibt einen sprachlich auffallend guten Aufsatz ab. Sie vermuten ChatGPT-Nutzung.</p>'}, 'subContentId': 'bs-0', 'metadata': {'contentType': 'Text', 'license': 'U', 'title': 'Intro'}}, 'showContentTitle': True, 'contentTitle': 'Die Situation', 'nextContentId': 1, 'forceContentFinished': False},
                            {'type': {'library': 'H5P.BranchingQuestion 1.0', 'params': {'branchingQuestion': {'question': '<p>Wie reagieren Sie?</p>', 'alternatives': [{'text': 'Direkt konfrontieren, Note 6', 'nextContentId': 2}, {'text': 'Gespr&auml;ch unter vier Augen', 'nextContentId': 3}, {'text': 'Nichts unternehmen', 'nextContentId': 4}]}}, 'subContentId': 'bs-1', 'metadata': {'contentType': 'Branching Question', 'license': 'U', 'title': 'Entscheidung'}}, 'showContentTitle': False, 'forceContentFinished': False},
                            {'type': {'library': 'H5P.AdvancedText 1.1', 'params': {'text': '<h3>Problematisch</h3><p>KI-Nutzung l&auml;sst sich nicht beweisen. Ein Verbot signalisiert, dass KI grunds&auml;tzlich schlecht ist. Besser: Gespr&auml;ch suchen und gemeinsam Regeln kl&auml;ren.</p>'}, 'subContentId': 'bs-2', 'metadata': {'contentType': 'Text', 'license': 'U', 'title': 'Konfrontation'}}, 'showContentTitle': True, 'contentTitle': 'Konfrontation', 'nextContentId': -1, 'forceContentFinished': False},
                            {'type': {'library': 'H5P.AdvancedText 1.1', 'params': {'text': '<h3>Gute Wahl!</h3><p>Im Gespr&auml;ch k&ouml;nnen Sie: den Prozess besprechen, Regeln erarbeiten, &uuml;ber den Lerneffekt reflektieren und KI als Werkzeug einordnen.</p>'}, 'subContentId': 'bs-3', 'metadata': {'contentType': 'Text', 'license': 'U', 'title': 'Gespraech'}}, 'showContentTitle': True, 'contentTitle': 'Das Gespr&auml;ch', 'nextContentId': -1, 'forceContentFinished': False},
                            {'type': {'library': 'H5P.AdvancedText 1.1', 'params': {'text': '<h3>Nicht ideal</h3><p>Ohne Regeln entsteht Unsicherheit. Andere f&uuml;hlen sich benachteiligt, der Lerneffekt geht verloren. Erarbeiten Sie gemeinsam KI-Regeln.</p>'}, 'subContentId': 'bs-4', 'metadata': {'contentType': 'Text', 'license': 'U', 'title': 'Ignorieren'}}, 'showContentTitle': True, 'contentTitle': 'Nichts tun', 'nextContentId': -1, 'forceContentFinished': False}
                        ],
                        'startScreen': {'startScreenTitle': 'KI im Klassenzimmer', 'startScreenSubtitle': 'Eine ethische Entscheidung'},
                        'endScreens': [{'endScreenTitle': 'Ende', 'endScreenSubtitle': '', 'contentId': -1, 'endScreenScore': 0}],
                        'scoringOptionGroup': {'scoringOption': 'no-score'},
                        'l10n': {'startScreenButtonText': 'Starten', 'endScreenButtonText': 'Neustart', 'backButtonText': 'Zur&uuml;ck', 'proceedButtonText': 'Weiter', 'disableProceedButtonText': 'Bitte antworten.', 'scoreText': 'Ergebnis:', 'fullscreenAria': 'Vollbild'}
                    }
                }
            },
            {
                'library': 'H5P.MultiChoice 1.16',
                'params': {
                    'question': '<p>Welche Daten d&uuml;rfen NICHT in ChatGPT eingegeben werden?</p>',
                    'answers': [
                        {'text': '<p>Namen und Noten von Sch&uuml;lern</p>', 'correct': True, 'tpiMessage': 'Richtig! Personenbezogene Daten nicht in Cloud-KI.'},
                        {'text': '<p>Allgemeine Themen</p>', 'correct': False, 'tpiMessage': 'Fachliche Anfragen sind unproblematisch.'},
                        {'text': '<p>F&ouml;rderpl&auml;ne mit Namen</p>', 'correct': True, 'tpiMessage': 'Richtig! Hochsensible Daten.'},
                        {'text': '<p>Anonymisierte Aufgaben</p>', 'correct': False, 'tpiMessage': 'Anonymisiert ist ok.'},
                        {'text': '<p>Fotos mit erkennbaren SuS</p>', 'correct': True, 'tpiMessage': 'Richtig! Besonders sch&uuml;tzenswert.'}
                    ],
                    'behaviour': {'enableRetry': True, 'enableSolutionsButton': True, 'enableCheckButton': True, 'type': 'auto', 'singlePoint': False},
                    'UI': {'checkAnswerButton': 'Pr&uuml;fen', 'showSolutionButton': 'L&ouml;sung', 'tryAgainButton': 'Nochmal', 'correctText': 'Richtig!', 'incorrectText': 'Falsch!', 'shouldCheck': 'W&auml;hlen', 'shouldNotCheck': 'Nicht w&auml;hlen', 'noInput': 'Bitte antworten'}
                }
            }
        ]
    },
    {
        'title': 'Kapitel 6: Checkliste und Abschlussquiz',
        'elements': [
            {'library': 'H5P.AdvancedText 1.1', 'params': {'text': '<h2>Ihre KI-Checkliste</h2><h3>Sofort</h3><ul><li>ChatGPT oder Claude Account erstellen</li><li>5 Prompt-Elemente nutzen</li><li>Inhalte IMMER pr&uuml;fen</li><li>Keine personenbezogenen Daten</li></ul><h3>Diese Woche</h3><ul><li>Ein Arbeitsblatt mit KI erstellen</li><li>Mit Kolleg*innen austauschen</li><li>KI-Regeln f&uuml;r die Klasse</li></ul><h3>Diesen Monat</h3><ul><li>3 KI-Tools ausprobieren</li><li>Unterrichtseinheit mit KI planen</li><li>SuS KI-Kompetenz vermitteln</li></ul>'}},
            {
                'library': 'H5P.TrueFalse 1.8',
                'params': {
                    'question': '<p>KI-generierte Materialien d&uuml;rfen ungepr&uuml;ft im Unterricht eingesetzt werden.</p>',
                    'correct': 'false',
                    'l10n': {'trueText': 'Wahr', 'falseText': 'Falsch'},
                    'behaviour': {'enableRetry': True, 'enableSolutionsButton': True, 'confirmCheckDialog': False, 'confirmRetryDialog': False},
                    'feedbackOnCorrect': 'Richtig! Faktencheck ist Pflicht.',
                    'feedbackOnWrong': 'Falsch! KI kann halluzinieren.'
                }
            },
            {
                'library': 'H5P.TrueFalse 1.8',
                'params': {
                    'question': '<p>Sch&uuml;lernamen und Noten geh&ouml;ren nicht in Cloud-KI-Tools.</p>',
                    'correct': 'true',
                    'l10n': {'trueText': 'Wahr', 'falseText': 'Falsch'},
                    'behaviour': {'enableRetry': True, 'enableSolutionsButton': True, 'confirmCheckDialog': False, 'confirmRetryDialog': False},
                    'feedbackOnCorrect': 'Richtig! Datenschutz beachten.',
                    'feedbackOnWrong': 'Falsch! Das w&auml;re ein Versto&szlig;.'
                }
            },
            {
                'library': 'H5P.TrueFalse 1.8',
                'params': {
                    'question': '<p>Ein guter Prompt enth&auml;lt Rolle, Aufgabe, Kontext, Format und Einschr&auml;nkungen.</p>',
                    'correct': 'true',
                    'l10n': {'trueText': 'Wahr', 'falseText': 'Falsch'},
                    'behaviour': {'enableRetry': True, 'enableSolutionsButton': True, 'confirmCheckDialog': False, 'confirmRetryDialog': False},
                    'feedbackOnCorrect': 'Richtig! Die 5 Prompt-Elemente.',
                    'feedbackOnWrong': 'Doch! Diese 5 Elemente sind der Schl&uuml;ssel.'
                }
            },
            {'library': 'H5P.AdvancedText 1.1', 'params': {'text': '<hr><h3>Herzlichen Gl&uuml;ckwunsch!</h3><blockquote><p><em>KI ersetzt keine Lehrkraft &ndash; aber eine Lehrkraft, die KI nutzt, wird diejenige ersetzen, die es nicht tut.</em></p></blockquote><p>Starten Sie klein, experimentieren Sie, und teilen Sie Ihre Erfahrungen!</p>'}}
        ]
    }
]

result = create_interactive_book(
    'KI f&uuml;r Lehrerinnen und Lehrer',
    chapters=chapters,
    output_name='ki-fuer-lehrkraefte',
    cover_description='Interaktives Lernbuch: K&uuml;nstliche Intelligenz im Schulalltag. 6 Kapitel, &uuml;ber 20 &Uuml;bungen.',
    base_color='#003366'
)

print(result)

import zipfile, json
with zipfile.ZipFile(str(result.path), 'r') as zf:
    content = json.loads(zf.read('content/content.json'))
    h5p = json.loads(zf.read('h5p.json'))
    ch = content['chapters']
    total = sum(len(c['params']['content']) for c in ch)
    print(f'\nKapitel: {len(ch)}')
    print(f'Elemente gesamt: {total}')
    print(f'Dependencies: {len(h5p["preloadedDependencies"])}')
    for i, c in enumerate(ch):
        elems = c['params']['content']
        libs = [e['content']['library'].split(' ')[0].replace('H5P.', '') for e in elems]
        print(f'  Kap {i+1} ({len(elems)}): {", ".join(libs)}')

    # Count unique types
    all_libs = set()
    for c in ch:
        for e in c['params']['content']:
            all_libs.add(e['content']['library'].split(' ')[0])
    print(f'\nVerwendete H5P-Typen: {len(all_libs)}')
    for lib in sorted(all_libs):
        print(f'  - {lib}')
    print(f'\nDatei: {result.path}')
