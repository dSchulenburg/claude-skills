# 🎯 Skills Quick Start Guide

**3 Schritte zum Einsatz deiner Custom Claude Skills**

---

## 📦 Schritt 1: Installieren

### Windows Batch Script (Empfohlen)

```
1. Öffne: C:\Users\mail\OneDrive\Dokumente\EigeneProjekte\dev\claude-skills
2. Doppelklick auf: install-skills.bat
3. Warte auf "Installation abgeschlossen!"
```

**Was passiert:**
```
✅ Erstellt %APPDATA%\Claude\skills\ Verzeichnis
✅ Kopiert blog-article-workflow
✅ Kopiert h5p-wordpress-workflow
✅ Zeigt Bestätigung
```

**Dauer:** ~5 Sekunden

---

## 🔄 Schritt 2: Claude Desktop neu starten

### WICHTIG: Komplett beenden!

```
1. Schließe alle Claude Desktop Fenster
2. Klicke auf Taskleiste (unten rechts)
3. Suche Claude-Icon im System Tray
4. Rechtsklick → "Beenden"
5. Öffne Claude Desktop neu
```

**Warum?**
Skills werden nur beim Start geladen!

---

## 🧪 Schritt 3: Testen

### Test-Prompt 1: Blog-Artikel

**In Claude Desktop eingeben:**
```
Erstelle einen Blog-Artikel über "Effektive Git Workflows"
```

**Erwartetes Verhalten:**
```
🎯 Claude startet mit blog-article-workflow
📝 Erstellt strukturierten Artikel
✨ Nutzt Emoji für Scanbarkeit  
🎨 Schlägt undraw.co Illustrationen vor
🌐 Generiert WordPress HTML
```

---

### Test-Prompt 2: H5P Content

**In Claude Desktop eingeben:**
```
Wie erstelle ich ein Interactive Video mit H5P und binde es in WordPress ein?
```

**Erwartetes Verhalten:**
```
🎯 Claude startet mit h5p-wordpress-workflow
📚 Erklärt H5P Content-Types
🔧 Zeigt WordPress Integration
⚡ Bietet MCP Automation an
```

---

### Test-Prompt 3: Vollautomatisch publizieren

**In Claude Desktop eingeben:**
```
Erstelle einen Artikel über "Docker für Einsteiger" und publiziere ihn als Draft zu WordPress
```

**Erwartetes Verhalten:**
```
📝 Erstellt Artikel-Struktur
🎨 Plant Illustrationen
🌐 Generiert WordPress HTML
🚀 Ruft MyWordPressMCP:wp_create_post auf
✅ Erstellt Draft in WordPress
📎 Liefert Link zum Artikel
```

---

## ✅ Erfolgs-Checkliste

Nach den 3 Schritten sollte folgendes funktionieren:

### Skills aktiv:
- [x] `blog-article-workflow` triggert bei "Erstelle einen Artikel"
- [x] `h5p-wordpress-workflow` triggert bei "H5P" Keywords
- [x] Skills nutzen undraw.co Workflows
- [x] Skills nutzen Emoji konsistent
- [x] WordPress HTML wird korrekt generiert

### MCP Integration:
- [x] MyWordPressMCP Tools verfügbar
- [x] wp_create_post funktioniert
- [x] wp_upload_media_from_url funktioniert
- [x] Artikel werden als Draft erstellt

### Workflow funktioniert:
- [x] Idee → Artikel-Struktur in Sekunden
- [x] Artikel → WordPress HTML automatisch
- [x] HTML → WordPress Draft via MCP
- [x] Draft → Manuell finalisieren & publizieren

---

## 🎨 Beispiel-Session

**Du:**
```
Erstelle einen Artikel über "n8n Workflows für Lehrer"
```

**Claude (mit Skills):**
```
Ich erstelle einen strukturierten Blog-Artikel über 
n8n Workflows für Lehrer!

[Nutzt blog-article-workflow automatisch]

📝 Artikel-Struktur:
- Hook: Reales Beispiel aus deinem Unterricht
- Problem: Zeitaufwendige Routineaufgaben
- Lösung: n8n Automation
- 15-Minuten Workflow
- Best Practices
- Next Steps

🎨 Geplante Visuals:
- Hero: undraw.co "automation" Illustration
- Workflow: undraw.co "setup_wizard"
- Success: undraw.co "celebration"

[Erstellt vollständigen Artikel mit WordPress HTML]

✨ Artikel fertig!

Möchtest du:
A) Als Draft zu WordPress publizieren
B) Erst durchlesen/anpassen
C) Illustrationen von undraw.co holen
```

**Du:**
```
A - publiziere als Draft
```

**Claude:**
```
🚀 Publiziere zu WordPress...

[Ruft MyWordPressMCP:wp_create_post auf]

✅ Artikel publiziert!

📎 Draft: https://www.dirk-schulenburg.net/?p=101

Nächste Schritte:
1. Featured Image in WordPress setzen
2. Kategorien/Tags hinzufügen  
3. Preview checken
4. Publizieren
```

---

## 🚀 Das war's!

**Skills sind aktiv und einsatzbereit!**

Starte einen neuen Chat in Claude Desktop und teste die Prompts! 🎉

---

**Probleme?** → Siehe README.md Troubleshooting

**Feedback?** → Erstelle FEEDBACK.md

**Fragen?** → Check die vollständige Dokumentation in README.md

---

*Quick Start Guide - 03.01.2026*
