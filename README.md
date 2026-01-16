# Claude Skills - Installation & Testing Guide

Deine Custom Skills für Claude Desktop - bereit zum Einsatz! 🚀

## 📦 Verfügbare Skills

### 1. blog-article-workflow
**Was es macht:**
- Erstellt strukturierte Blog-Artikel
- WordPress HTML Formatting
- undraw.co Illustrationen Integration
- Emoji für bessere Scanbarkeit
- MCP WordPress Publishing

**Wann wird es aktiviert:**
- "Erstelle einen Blog-Artikel über [THEMA]"
- "Schreibe einen Tutorial-Post über [THEMA]"
- "Ich möchte einen Artikel schreiben über [THEMA]"

---

### 2. h5p-wordpress-workflow
**Was es macht:**
- H5P Content-Erstellung (manuell)
- WordPress Integration
- MCP Automation
- Best Practices für interaktive Inhalte

**Wann wird es aktiviert:**
- "Wie erstelle ich H5P Content?"
- "H5P in WordPress einbinden"
- "Interactive Video mit H5P"

---

### 3. h5p-generator ⭐ NEU
**Was es macht:**
- Erstellt .h5p-Dateien **direkt aus Python** ohne Web-Editor
- Unterstützt: True/False, Multiple Choice, Fill in Blanks, Drag & Drop
- Batch-Erstellung mehrerer H5P-Dateien
- Export für Moodle, WordPress oder andere LMS

**Wann wird es aktiviert:**
- "Erstelle H5P Dateien für mein Quiz"
- "Generiere ein Multiple Choice H5P"
- "H5P Lückentext programmatisch erstellen"
- "Drag and Drop H5P generieren"

**Unterstützte Content-Types:**

| Typ | Funktion | Beispiel |
|-----|----------|----------|
| True/False | `create_true_false()` | Wahr/Falsch Quizze |
| Multiple Choice | `create_multi_choice()` | MC-Fragen mit 4+ Optionen |
| Fill in Blanks | `create_fill_blanks()` | Lückentexte mit `*Lücke*` |
| Drag & Drop | `create_drag_drop()` | Zuordnungsaufgaben |

**Quick Start:**
```python
from h5p_generator import create_true_false

questions = [
    {
        "text": "Python ist eine Programmiersprache.",
        "correct": True,
        "feedback_correct": "Richtig!",
        "feedback_wrong": "Doch, ist es!"
    }
]
create_true_false("Mein Quiz", questions, "quiz-name")
# → Erstellt: /home/claude/h5p-output/quiz-name.h5p
```

---

### 4. recherche-workflow
**Was es macht:**
- Strukturierte Web-Recherche
- Quellensammlung und -bewertung
- Zusammenfassung von Recherche-Ergebnissen

**Wann wird es aktiviert:**
- "Recherchiere zu [THEMA]"
- "Finde Quellen über [THEMA]"

---

### 5. bswi-infobrief
**Was es macht:**
- Schulspezifische Formatierung
- Infobrief-Erstellung für BSWI

**Wann wird es aktiviert:**
- Schulspezifische Anfragen

---

## 🚀 Installation

### Schritt 1: Script ausführen

**Option A: Doppelklick**
```
1. Navigiere zu: C:\Users\mail\entwicklung\docker\claude-skills
2. Doppelklick auf: install-skills.bat
3. Script führt automatisch Installation durch
```

**Option B: Command Line**
```cmd
cd C:\Users\mail\entwicklung\docker\claude-skills
install-skills.bat
```

### Schritt 2: Claude Desktop neu starten

⚠️ **WICHTIG:** Claude Desktop muss KOMPLETT geschlossen werden!

```
1. Claude Desktop schließen
2. System Tray checken (unten rechts in der Taskleiste)
3. Falls Claude-Icon vorhanden → Rechtsklick → "Beenden"
4. Claude Desktop neu öffnen
```

### Schritt 3: Testen!

Öffne Claude Desktop und teste mit einem dieser Prompts:

---

## 🧪 Test-Prompts

### Test 1: Blog-Artikel erstellen

```
Erstelle einen Blog-Artikel über "Git Workflow für Lehrer"
```

**Erwartetes Verhalten:**
- ✅ Claude nutzt automatisch blog-article-workflow
- ✅ Erstellt strukturierten Artikel
- ✅ Nutzt Emoji für Scanbarkeit
- ✅ Generiert WordPress-kompatibles HTML

---

### Test 2: H5P Content (manuell)

```
Wie erstelle ich ein Interactive Video mit H5P?
```

**Erwartetes Verhalten:**
- ✅ Claude nutzt automatisch h5p-wordpress-workflow
- ✅ Erklärt H5P Content-Types
- ✅ Zeigt WordPress Integration

---

### Test 3: H5P Generator (automatisch) ⭐

```
Erstelle ein True/False Quiz über Deutschland mit 5 Fragen als H5P-Datei
```

**Erwartetes Verhalten:**
- ✅ Claude nutzt h5p-generator Skill
- ✅ Generiert Python-Code mit h5p_generator.py
- ✅ Erstellt .h5p-Datei im Output-Ordner
- ✅ Datei kann direkt in Moodle/WordPress importiert werden

---

### Test 4: Batch H5P Erstellung

```
Erstelle für mein Modul "Botanik" folgende H5P-Dateien:
1. Ein True/False Quiz mit 3 Fragen
2. Einen Lückentext über Photosynthese
3. Ein Drag & Drop zur Pflanzenzuordnung
```

**Erwartetes Verhalten:**
- ✅ Erstellt 3 separate .h5p-Dateien
- ✅ Alle mit korrektem Content
- ✅ Bereit zum Import

---

## 📁 Skills-Verzeichnis Struktur

Nach Installation sollte das Verzeichnis so aussehen:

```
%APPDATA%\Claude\skills\
├── blog-article-workflow\
│   ├── SKILL.md
│   ├── QUICK_REFERENCE.md
│   ├── workflows\
│   └── examples\
├── h5p-wordpress-workflow\
│   ├── SKILL.md
│   └── references\
├── h5p-generator\                    # ⭐ NEU
│   ├── SKILL.md
│   ├── scripts\
│   │   └── h5p_generator.py
│   └── references\
│       └── h5p-json-structure.md
├── recherche-workflow\
│   └── SKILL.md
└── bswi-infobrief\
    └── SKILL.md
```

**Voller Pfad (Windows):**
```
C:\Users\mail\AppData\Roaming\Claude\skills\
```

---

## 🔍 Troubleshooting

### Problem: Skills werden nicht aktiviert

**Lösung:**
1. ✅ Claude Desktop KOMPLETT neu gestartet?
2. ✅ Skills-Verzeichnis existiert: `%APPDATA%\Claude\skills\`
3. ✅ SKILL.md Dateien vorhanden in Unterordnern?
4. ✅ Prompt triggert Skill-Keywords?

**Check-Command:**
```cmd
dir "%APPDATA%\Claude\skills\"
```

---

### Problem: h5p-generator erstellt keine Dateien

**Symptom:**
Claude beschreibt den Code, aber erstellt keine .h5p-Datei

**Lösung:**
1. ✅ Skill muss in Claude.ai mit Computer-Nutzung laufen (nicht Claude Desktop)
2. ✅ Oder: Code manuell in Python ausführen
3. ✅ Output-Verzeichnis prüfen: `/home/claude/h5p-output/`

---

### Problem: MCP WordPress Tools nicht verfügbar

**Symptom:**
Claude kann Artikel erstellen, aber nicht zu WordPress publizieren

**Lösung:**
1. ✅ MCP Server läuft? (Docker Desktop → Containers)
2. ✅ MCP in Claude Desktop konfiguriert?
3. ✅ Test: `docker ps` zeigt MCP Container?

---

## 🎯 Skill-Kombinationen

### H5P Workflow komplett

```
1. Erstelle H5P-Dateien mit h5p-generator
2. Lade zu WordPress hoch mit h5p-wordpress-workflow
3. Erstelle Blog-Artikel mit blog-article-workflow
4. Bette H5P ein
```

**Beispiel-Prompt:**
```
Erstelle ein Quiz über Photosynthese als H5P-Datei und 
dann einen Blog-Artikel der das Quiz einbettet
```

---

## 💡 Pro-Tips

### Tip 1: Kombiniere Skills
```
Erstelle einen H5P Tutorial-Artikel über Interactive Videos
```
→ Nutzt BEIDE H5P-Skills zusammen!

### Tip 2: Batch-Erstellung
```
Erstelle für jeden Monat des Jahres ein True/False Quiz als H5P
```
→ Generator erstellt 12 Dateien automatisch

### Tip 3: Fill in Blanks Syntax
```
Lücken mit *Sternchen* markieren.
Mehrere Antworten: *Antwort1/Antwort2/Antwort3*
```

---

## 📚 Dokumentation pro Skill

| Skill | Hauptdatei | Referenzen |
|-------|------------|------------|
| blog-article-workflow | SKILL.md | workflows/, examples/ |
| h5p-wordpress-workflow | SKILL.md | references/h5p-content-types.md |
| h5p-generator | SKILL.md | scripts/h5p_generator.py, references/h5p-json-structure.md |
| recherche-workflow | SKILL.md | - |
| bswi-infobrief | SKILL.md | - |

---

## ✅ Installation Checklist

- [ ] install-skills.bat ausgeführt
- [ ] Claude Desktop neu gestartet (KOMPLETT!)
- [ ] Test-Prompt ausgeführt
- [ ] blog-article-workflow triggert
- [ ] h5p-wordpress-workflow triggert
- [ ] h5p-generator triggert ⭐
- [ ] MCP WordPress Tools verfügbar
- [ ] Ersten Artikel/H5P erstellt

**Alles ✅? Glückwunsch! Skills sind aktiv! 🎉**

---

## 🆕 Changelog

### 2026-01-10
- ⭐ **NEU:** h5p-generator Skill hinzugefügt
  - Erstellt .h5p-Dateien direkt aus Python
  - Unterstützt: True/False, Multiple Choice, Fill in Blanks, Drag & Drop
  - Batch-Erstellung möglich

### 2026-01-03
- Initial Release
- blog-article-workflow
- h5p-wordpress-workflow

---

*Zuletzt aktualisiert: 10.01.2026*
*Version: 1.1*
