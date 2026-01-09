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
- H5P Content-Erstellung
- WordPress Integration
- MCP Automation
- Best Practices für interaktive Inhalte

**Wann wird es aktiviert:**
- "Wie erstelle ich H5P Content?"
- "H5P in WordPress einbinden"
- "Interactive Video mit H5P"

---

## 🚀 Installation

### Schritt 1: Script ausführen

**Option A: Doppelklick**
```
1. Navigiere zu: C:\Users\mail\OneDrive\Dokumente\EigeneProjekte\dev\claude-skills
2. Doppelklick auf: install-skills.bat
3. Script führt automatisch Installation durch
```

**Option B: Command Line**
```cmd
cd C:\Users\mail\OneDrive\Dokumente\EigeneProjekte\dev\claude-skills
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
- ✅ Schlägt undraw.co Illustrationen vor

---

### Test 2: H5P Content

```
Wie erstelle ich ein Interactive Video mit H5P?
```

**Erwartetes Verhalten:**
- ✅ Claude nutzt automatisch h5p-wordpress-workflow
- ✅ Erklärt H5P Content-Types
- ✅ Zeigt WordPress Integration
- ✅ Bietet MCP Automation an

---

### Test 3: Artikel mit MCP publizieren

```
Erstelle einen Artikel über "Docker Basics" und publiziere ihn als Draft zu WordPress
```

**Erwartetes Verhalten:**
- ✅ Erstellt Artikel-Struktur
- ✅ Nutzt WordPress HTML Blöcke
- ✅ Ruft MyWordPressMCP:wp_create_post auf
- ✅ Erstellt Draft in WordPress

---

## 📁 Skills-Verzeichnis Struktur

Nach Installation sollte das Verzeichnis so aussehen:

```
%APPDATA%\Claude\skills\
├── blog-article-workflow\
│   ├── SKILL.md                    # Haupt-Skill Dokumentation
│   ├── QUICK_REFERENCE.md          # Schnell-Referenz
│   ├── workflows\
│   │   └── images-and-media.md     # Bild-Integration Guide
│   └── examples\
│       └── docker-n8n-article-test.md
└── h5p-wordpress-workflow\
    └── SKILL.md                     # H5P Skill Dokumentation
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
4. ✅ Prompt triggert Skill-Keywords? (z.B. "Blog-Artikel", "H5P")

**Check-Command:**
```cmd
dir "%APPDATA%\Claude\skills\blog-article-workflow"
```

Sollte zeigen:
```
SKILL.md
QUICK_REFERENCE.md
workflows\
examples\
```

---

### Problem: MCP WordPress Tools nicht verfügbar

**Symptom:**
Claude kann Artikel erstellen, aber nicht zu WordPress publizieren

**Lösung:**
1. ✅ MCP Server läuft? (Docker Desktop → Containers → wp-mcp)
2. ✅ MCP in Claude Desktop konfiguriert?
3. ✅ Test: `docker ps` zeigt wp-mcp Container?

---

### Problem: undraw.co Bilder werden nicht gefunden

**Symptom:**
Skill schlägt Illustrationen vor, aber Upload schlägt fehl

**Lösung:**
Das ist normal! undraw.co CDN ist manchmal nicht verfügbar.

**Workaround:**
```
1. Gehe manuell zu https://undraw.co/illustrations
2. Suche + Download Illustrationen
3. Upload via WordPress Media Library
4. Oder: wp_upload_media_from_url mit eigener URL
```

---

## 🎯 Nächste Schritte

### Diese Woche:
- [ ] Skills installiert & getestet
- [ ] Ersten Artikel mit Skill erstellt
- [ ] MCP Publishing getestet

### Nächste Woche:
- [ ] Skills erweitern (neue Workflows)
- [ ] Eigene Templates erstellen
- [ ] Weitere Skills hinzufügen

### Langfristig:
- [ ] Skills für andere Projekte anpassen
- [ ] Skill-Creator nutzen für neue Skills
- [ ] Skills mit Team teilen

---

## 📝 Skills aktualisieren

**Bei Änderungen an den Skills:**

```cmd
# Skills neu installieren
cd C:\Users\mail\OneDrive\Dokumente\EigeneProjekte\dev\claude-skills
install-skills.bat

# Claude Desktop neu starten
# (komplett beenden + neu öffnen)
```

**Automatisches Update (geplant):**
- Git-Repository mit Skills
- Auto-Sync bei Änderungen
- Version Control

---

## 💡 Pro-Tips

### Tip 1: Kombiniere Skills
```
Erstelle einen H5P Tutorial-Artikel über Interactive Videos
```
→ Nutzt BEIDE Skills zusammen!

### Tip 2: Explizite Skill-Auswahl
```
Nutze den blog-article-workflow Skill um einen Artikel über Python zu erstellen
```
→ Forciert spezifischen Skill

### Tip 3: Quick Reference nutzen
```
Zeige mir die undraw.co Workflow Quick Reference
```
→ Lädt QUICK_REFERENCE.md

---

## 📚 Dokumentation

**Alle Skills dokumentiert in:**
```
C:\Users\mail\OneDrive\Dokumente\EigeneProjekte\dev\claude-skills\

blog-article-workflow\
├── SKILL.md              → Kompletter Workflow
├── QUICK_REFERENCE.md    → Schnell-Referenz
└── workflows\
    └── images-and-media.md → Bild-Integration

h5p-wordpress-workflow\
└── SKILL.md              → H5P Workflow
```

---

## ✅ Installation Checklist

- [ ] install-skills.bat ausgeführt
- [ ] Claude Desktop neu gestartet (KOMPLETT!)
- [ ] Test-Prompt ausgeführt
- [ ] blog-article-workflow triggert
- [ ] h5p-wordpress-workflow triggert
- [ ] MCP WordPress Tools verfügbar
- [ ] Ersten Artikel erstellt

**Alles ✅? Glückwunsch! Skills sind aktiv! 🎉**

---

## 🆘 Support

**Fragen? Probleme?**
1. Check Troubleshooting-Sektion oben
2. Überprüfe Skills-Verzeichnis
3. Test mit einfachem Prompt

**Feedback:**
Skills funktionieren gut? Verbesserungsvorschläge?
→ Dokumentiere in claude-skills/FEEDBACK.md

---

*Zuletzt aktualisiert: 03.01.2026*
*Version: 1.0*
