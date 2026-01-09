# H5P + WordPress: Interaktive Lernmodule in 10 Minuten
## Ein Praxis-Guide für tech-affine Lehrkräfte

## Der Moment, der alles änderte

Letzte Woche habe ich in 10 Minuten ein interaktives Lernmodul erstellt, das meine Schüler 3x länger beschäftigt hat als ein klassisches Arbeitsblatt. Keine Programmierung. Keine komplexe Software. Nur H5P und WordPress.

Während meine Kolleg:innen noch PDFs verschicken und PowerPoints hochladen, erstelle ich interaktive Module, die:
- **Sofortiges Feedback** geben
- **Engagement tracken** (wer hat was bearbeitet?)
- **Auf allen Geräten** funktionieren (Handy, Tablet, Laptop)
- **Wiederverwendbar** sind (einmal erstellen, immer nutzen)

Und das Beste: Der technische Aufwand ist minimal.

## Das Problem mit klassischen Materialien

Wir alle kennen es:

**PDF-Arbeitsblätter** → Schüler drucken aus (oder nicht), füllen aus (oder nicht), scannen ein (oder vergessen es)

**YouTube-Videos** → Passives Konsumieren, kein Feedback, keine Kontrolle ob wirklich geschaut

**PowerPoint-Präsentationen** → Statisch, keine Interaktion, kein Verständnis-Check

**LMS (Moodle, etc.)** → Zu komplex für schnelle Module, Einarbeitung kostet Stunden

Was fehlt? **Interaktivität + Einfachheit**

## Enter: H5P

H5P ist wie das WordPress der interaktiven Lernmodule. Open Source, browserbasiert, keine Installation nötig.

**Was ist H5P?**
- HTML5-basierte interaktive Inhalte
- 50+ Content-Types (Quizze, Videos, Präsentationen, etc.)
- Export als einzelne .h5p Datei
- Import in jedes LMS oder WordPress

**Warum ich es täglich nutze:**
- ✅ **10 Minuten** von Idee zu fertigem Modul
- ✅ **Kein Coding** nötig (aber möglich für Power-User)
- ✅ **Mobile-first** – funktioniert auf allen Geräten
- ✅ **Wiederverwendbar** – einmal erstellen, überall nutzen
- ✅ **Analytics** – sehe wer was bearbeitet hat

## Meine 3 Lieblings-Content-Types

Nach hunderten erstellten Modulen habe ich meine Go-To-Formate gefunden:

### 1. Course Presentation – Die strukturierte Lektion

**Wofür ich es nutze:**
- Einführung in neue Themen
- Schritt-für-Schritt-Anleitungen
- Selbstlern-Module

**Warum es funktioniert:**
- Slides wie PowerPoint, aber interaktiv
- Eingebettete Quizze zwischen Slides
- Schüler arbeiten in eigenem Tempo
- Navigation + Bookmarks

**Beispiel aus meinem Unterricht:**
"VG im Kopf vorbereiten" – Ein Modul zur Vorbereitung auf Vorstellungsgespräche. Schüler durchlaufen strukturiert:
1. Intro-Slide: Warum Vorbereitung wichtig ist
2. Selbstreflexion: "Was sind meine Stärken?" (Fill-in-the-blanks)
3. Typische Fragen + Musterlösungen
4. Quiz: Selbst-Check
5. Action Steps: Konkrete Aufgaben

**Ergebnis:** 90% Completion-Rate (vs. 60% bei PDF-Arbeitsblättern)

### 2. Multiple Choice – Der schnelle Wissens-Check

**Wofür ich es nutze:**
- Hausaufgaben-Checks
- Vorwissens-Tests
- Lernziel-Kontrollen

**Warum es funktioniert:**
- Sofortiges Feedback
- Mehrfach-Versuche möglich
- Randomisierte Fragen
- Feedback zu falschen Antworten

**Setup-Zeit:** 5-7 Minuten für 10 Fragen

**Pro-Tipp:** Ich erstelle Question-Banks und randomisiere, sodass jeder Schüler andere Fragen bekommt.

### 3. Interactive Video – Videos, die tatsächlich geschaut werden

**Wofür ich es nutze:**
- Erklärvideos mit Checkpoints
- Dokumentationen mit Verständnis-Checks
- Tutorials mit Pause-und-Übung

**Warum es funktioniert:**
- Video pausiert automatisch bei Fragen
- Schüler müssen antworten um weiterzuschauen
- Bookmarks für Navigation
- Ergebnisse trackbar

**Beispiel aus meinem Unterricht:**
"Die Recherche, mach dich schlau" – Ein 8-Minuten-Video über Recherche-Methoden mit:
- 3 eingebetteten Quizze
- Text-Overlays mit Definitionen
- Bookmarks für Sprungmarken
- Zusammenfassung am Ende

**Ergebnis:** 95% schauen das Video bis zum Ende (vs. 40% bei normalem YouTube-Video)

## Der 10-Minuten-Workflow

So erstelle ich ein H5P-Modul von Null:

### Option A: Schnell-Workflow (H5P.com)

**Minute 1-2:** Konzept skizzieren
- Was sollen Schüler lernen?
- Welcher Content-Type passt?

**Minute 3-7:** Erstellen auf H5P.com
1. Gehe zu h5p.com
2. "Create New Content"
3. Wähle Content-Type (z.B. Course Presentation)
4. Füge Slides hinzu
5. Füge Quizze/Bilder/Text hinzu

**Minute 8:** Exportieren
- "Download" → .h5p Datei

**Minute 9:** Upload zu WordPress
- Media → Add New
- .h5p hochladen

**Minute 10:** Einbetten
- Im Beitrag: `[h5p id="123"]`
- Fertig!

### Option B: Power-User-Workflow (mit MCP)

Wenn du meinen WordPress-MCP-Server nutzt:

**Minute 1-7:** H5P erstellen (wie oben)

**Minute 8:** Datei in Cloud speichern (Nextcloud/Dropbox)

**Minute 9-10:** Claude sagen:
```
"Erstelle einen Artikel über [Thema],
lade diese H5P-Datei hoch: [URL],
bette sie ein und publiziere als Draft"
```

**Claude macht automatisch:**
- Upload zu WordPress
- Artikel-Grundstruktur
- H5P eingebettet
- Draft erstellt

**Ich mache:** Review & Publish (2 Minuten)

**Gesamt:** 10 Minuten

## Tech-Setup für Kolleg:innen

### Variante 1: Minimal Setup (Empfohlen für Start)

**Was du brauchst:**
- Account auf h5p.com (kostenlos)
- WordPress-Zugang mit H5P-Plugin

**Setup:**
1. H5P Plugin in WordPress installieren
2. Account auf h5p.com erstellen
3. Erstes Modul erstellen
4. Fertig!

**Kosten:** 0€ (für Grundfunktionen)

### Variante 2: Selbst-Hosting

**Was du brauchst:**
- WordPress mit H5P Plugin
- Oder Moodle mit H5P-Aktivität

**Vorteil:**
- Volle Kontrolle
- Keine Datenschutz-Bedenken
- Unbegrenzt Content

**Setup:**
1. WordPress → Plugins → H5P installieren
2. Aktivieren
3. Content direkt in WordPress erstellen

### Variante 3: Power-User (wie ich)

**Setup:**
- WordPress mit H5P Plugin
- MCP-Server für Automation
- n8n für Workflows
- Nextcloud für File-Storage

**Vorteil:**
- Komplette Automatisierung
- API-basierte Workflows
- Batch-Upload möglich

**Aufwand:** ~2-3 Stunden Initial-Setup
**ROI:** Nach 20-30 Modulen break-even

## Best Practices aus 2+ Jahren H5P

### Was funktioniert ✅

**1. Klein anfangen**
Erstes Modul: 5 Slides, 2 Quizze. Nicht gleich Interactive Book mit 30 Seiten.

**2. Sofortiges Feedback**
Schüler lieben es, sofort zu wissen ob richtig/falsch. Nutze das!

**3. Mobile-First denken**
80% meiner Schüler bearbeiten auf dem Handy. Teste immer mobil!

**4. Wiederverwendung planen**
Erstelle Module als Building Blocks. "Einführung Recherche" nutze ich in 5 verschiedenen Kontexten.

**5. Analytics nutzen**
H5P trackt wer was bearbeitet hat. Nutze es für Hausaufgaben-Kontrolle.

### Was NICHT funktioniert ❌

**1. Zu komplex starten**
Erste Versuche mit Interactive Book → Überwältigung. Start simple!

**2. Zu viel Text**
H5P ist interaktiv, nicht ein digitales PDF. Kurze Texte + viel Interaktion!

**3. Keine mobil-Optimierung**
Drag & Drop mit winzigen Elementen? Auf dem Handy Disaster.

**4. Vergessen zu testen**
Immer selbst durchklicken vor Veröffentlichung. Immer!

**5. Perfektionismus**
"Quick & dirty" Module sind besser als perfekte Module die nie fertig werden.

## Häufige Fehler (und wie ich sie gelöst habe)

### Problem: Upload-Limit zu klein
**Symptom:** .h5p Datei ist 80MB, WordPress erlaubt nur 64MB

**Lösung:**
```php
// wp-config.php
@ini_set('upload_max_size', '128M');
@ini_set('post_max_size', '128M');
```

### Problem: H5P zeigt nicht an
**Symptom:** Shortcode wird als Text angezeigt

**Lösung:**
- H5P Plugin aktiviert?
- Cache geleert?
- Richtige ID? (nicht URL, nur Zahl!)

### Problem: Schüler sehen verschiedene Versionen
**Symptom:** Ich habe aktualisiert, Schüler sehen alte Version

**Lösung:**
- Browser-Cache leeren (oder Inkognito-Modus testen)
- WordPress-Cache-Plugin leeren
- H5P-Content im Editor "Re-save"

## Deine nächsten Schritte

### Woche 1: Erstes Modul
1. Gehe zu h5p.com
2. Erstelle Multiple Choice mit 5 Fragen
3. Exportiere als .h5p
4. Teste mit Kolleg:in oder Freund

### Woche 2: Im Unterricht testen
1. Erstelle Course Presentation (5 Slides)
2. Lade zu WordPress hoch
3. Teile Link mit einer Klasse
4. Sammle Feedback

### Woche 3: Iterieren & Skalieren
1. Analysiere: Was funktionierte?
2. Erstelle 2-3 weitere Module
3. Beginne Library aufzubauen
4. Teile mit Kolleg:innen

### Langfristig: Automatisierung
Wenn du 20+ Module hast:
- Überlege MCP-Setup
- n8n Workflows für Routine-Aufgaben
- Content-Library systematisieren

## Ressourcen

### Offizielle Quellen
- **H5P.org** – Dokumentation, Community
- **H5P.com** – Online-Editor (kostenlos starten)
- **Examples.h5p.org** – Beispiel-Module zum Ausprobieren

### Meine Setup-Guides (GitHub)
- WordPress MCP-Server – Automation-Setup
- H5P Workflow-Templates – Meine Standard-Module
- Best-Practice-Sammlung – Was ich gelernt habe

### Community
- H5P Forum – Fragen stellen, Hilfe bekommen
- Facebook: "H5P für Lehrer" (DACH)
- Twitter: #H5P (internationale Community)

### Beispiel-Module zum Download
- "Die Recherche, mach dich schlau" – Interactive Video
- "VG im Kopf vorbereiten" – Course Presentation

*(Diese Module stelle ich auf meinem Blog zur Verfügung)*

## Fazit: Einfach anfangen!

H5P hat meine Art zu unterrichten verändert. Nicht weil es revolutionär kompliziert ist, sondern weil es **einfach genug ist, um es tatsächlich zu nutzen**.

Der Unterschied zwischen einem passiven PDF und einem interaktiven H5P-Modul?
- **10 Minuten** mehr Aufwand
- **3x mehr** Engagement
- **Echtes** Feedback statt Rätselraten

**Mein Tipp:** Nimm dir heute Abend 10 Minuten. Gehe zu h5p.com. Erstelle ein Mini-Quiz zu deinem nächsten Thema. Teste es morgen.

Du wirst überrascht sein, wie viel Unterschied so wenig Aufwand macht.

---

**Fragen? Feedback?** Schreib mir oder – noch besser – **teile dein erstes H5P-Modul!** 

Das ist Stigmergy in Aktion: Du baust auf dem auf, was ich geteilt habe, und andere bauen auf dem auf, was du teilst. 🚀

---

*Dieser Artikel basiert auf 2+ Jahren täglicher H5P-Nutzung im Unterricht. Alle Beispiele sind real, alle Zeiten sind realistisch.*
