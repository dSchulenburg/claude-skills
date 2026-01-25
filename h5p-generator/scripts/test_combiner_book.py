#!/usr/bin/env python3
"""
Test: Combiner Agent mit Interactive Book

Testet ob der Combiner:
1. Kompatible Typen (MultiChoice, TrueFalse, Dialogcards, DragText) einbettet
2. Inkompatible Typen (Blanks, DragQuestion) als Text darstellt
"""

import sys
import json
import zipfile
from pathlib import Path

# Pfade einrichten
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))
sys.path.insert(0, str(script_dir / 'sub_agents'))

from h5p_generator import (
    H5PResult,
    create_multi_choice,
    create_true_false,
    create_flashcards,
    create_drag_text,
    create_fill_blanks
)
from sub_agents.base_agent import AgentResult, AgentStatus
from sub_agents.combiner_agent import CombinerAgent, ContainerType

# Output-Verzeichnis (lokal oder Docker)
if Path('/home/claude').exists():
    output_dir = Path('/home/claude/h5p-output')
else:
    output_dir = Path(__file__).parent.parent / 'test-output'
output_dir.mkdir(parents=True, exist_ok=True)

print("=" * 60)
print("Test: Combiner mit Interactive Book")
print("=" * 60)
print(f"Output: {output_dir}")

# 1. Mock-Elemente erstellen (echte H5P-Dateien)
print("\n1. Erstelle Mock-Elemente...")

# MultiChoice (kompatibel)
mc_result = create_multi_choice(
    title="Sprint-Dauer",
    questions=[{
        "question": "Wie lange dauert ein Sprint maximal?",
        "answers": [
            {"text": "1 Woche", "correct": False},
            {"text": "4 Wochen", "correct": True},
            {"text": "3 Monate", "correct": False}
        ]
    }]
)
print(f"  - MultiChoice: {mc_result.success}")

# TrueFalse (kompatibel)
tf_result = create_true_false(
    title="PO-Verantwortung",
    questions=[{
        "question": "Der Product Owner ist fuer das Backlog verantwortlich.",
        "correct": True
    }]
)
print(f"  - TrueFalse: {tf_result.success}")

# Flashcards (kompatibel)
fc_result = create_flashcards(
    title="Scrum-Begriffe",
    cards=[
        {"front": "Sprint", "back": "Zeitbox von 2-4 Wochen"},
        {"front": "Product Owner", "back": "Verwaltet das Product Backlog"},
        {"front": "Scrum Master", "back": "Coacht das Team"}
    ]
)
print(f"  - Flashcards: {fc_result.success}")

# DragText (kompatibel)
dt_result = create_drag_text(
    title="Drag-Text",
    text="Ein *Sprint* dauert maximal *vier* Wochen. Der *Product Owner* priorisiert das Backlog."
)
print(f"  - DragText: {dt_result.success}")

# Fill in Blanks (INKOMPATIBEL - sollte als Text dargestellt werden)
blanks_result = create_fill_blanks(
    title="Lueckentext",
    text="Der *Scrum Master* hilft dem Team bei *Hindernissen*."
)
print(f"  - FillBlanks: {blanks_result.success} (INKOMPATIBEL)")

# 2. AgentResults erstellen
print("\n2. Erstelle AgentResults...")

agent_results = [
    AgentResult(
        status=AgentStatus.SUCCESS,
        h5p_result=mc_result,
        original_type='multi_choice',
        final_type='multi_choice'
    ),
    AgentResult(
        status=AgentStatus.SUCCESS,
        h5p_result=tf_result,
        original_type='true_false',
        final_type='true_false'
    ),
    AgentResult(
        status=AgentStatus.SUCCESS,
        h5p_result=fc_result,
        original_type='flashcards',
        final_type='flashcards'
    ),
    AgentResult(
        status=AgentStatus.SUCCESS,
        h5p_result=dt_result,
        original_type='drag_text',
        final_type='drag_text'
    ),
    AgentResult(
        status=AgentStatus.SUCCESS,
        h5p_result=blanks_result,
        original_type='fill_blanks',
        final_type='fill_blanks'
    ),
]

print(f"  {len(agent_results)} AgentResults erstellt")

# 3. Combiner aufrufen
print("\n3. Starte Combiner mit INTERACTIVE_BOOK...")

combiner = CombinerAgent(output_dir=output_dir)
result = combiner.combine(
    elements=agent_results,
    container_type=ContainerType.INTERACTIVE_BOOK,
    title="Scrum Grundlagen - Combiner Test"
)

print(f"\n4. Ergebnis:")
print(f"  Success: {result.success}")
print(f"  Container: {result.container_type}")
print(f"  Elemente: {result.elements_combined}")

if result.errors:
    print(f"  Errors: {result.errors}")

if result.h5p_result and result.h5p_result.success:
    print(f"  Output: {result.h5p_result.path}")

    # H5P-Datei analysieren
    print("\n5. H5P-Analyse:")
    with zipfile.ZipFile(result.h5p_result.path, 'r') as zf:
        content = json.loads(zf.read('content/content.json'))
        h5p_meta = json.loads(zf.read('h5p.json'))

        print(f"  Titel: {h5p_meta.get('title')}")
        print(f"  Kapitel: {len(content.get('chapters', []))}")

        for i, chapter in enumerate(content.get('chapters', [])):
            title = chapter.get('title', 'Unbekannt')
            elements = chapter.get('params', {}).get('content', [])
            libs = [e.get('content', {}).get('library', '?') for e in elements]
            print(f"    {i+1}. {title}: {libs}")

        print(f"\n  Dependencies:")
        for dep in h5p_meta.get('preloadedDependencies', []):
            print(f"    - {dep['machineName']} {dep['majorVersion']}.{dep['minorVersion']}")

print("\n" + "=" * 60)
print("Test abgeschlossen!")
print("=" * 60)
