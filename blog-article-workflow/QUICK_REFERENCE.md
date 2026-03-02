# Blog Article with Images - Quick Reference

**Schnell-Anleitung für Blog-Artikel mit Pexels, undraw.co, Screenshots und Emoji**

---

## 🎨 Vor dem Schreiben: Visuals planen

### Checkliste

- [ ] **Featured Image** via Pexels (`--auto-image`) oder undraw.co
- [ ] **1-3 Inline Illustrationen** (Pexels oder undraw.co)
- [ ] **Screenshots** gemacht (falls Tutorial)
- [ ] **Emoji-Set** definiert
- [ ] **Alt-Texte** vorbereitet

---

## 1️⃣ Bild-Workflow: Pexels (30 Sekunden)

**Empfohlen: Automatisch via wp-post-v2.py**
```bash
# Bild suchen, optimieren, hochladen - alles in einem Befehl
python tools/wp-post-v2.py create \
  --title "Mein Artikel" --file artikel.md \
  --auto-image "coffee laptop workspace" \
  --status draft
```

**Nur Bild suchen (Preview):**
```bash
python tools/wp-post-v2.py find-image "classroom education modern" --limit 5
```

**Query-Tipps:** Englisch, spezifisch + Kontext + Adjektive
```
Gut:    "modern office bright workspace"
Schlecht: "work"
```

**undraw.co** bleibt Option für abstrakte Inline-Illustrationen:
```
1. Gehe zu https://undraw.co/illustrations
2. Suche nach Keyword (z.B. "education", "coding")
3. Download PNG oder SVG
4. Umbenennen: article-slug-purpose.png
```

---

## 2️⃣ Publishing-Befehle

### wp-post-v2.py (empfohlen)

```bash
# Neuer Post mit Auto-Image
python tools/wp-post-v2.py create \
  --title "Titel" --file artikel.md \
  --auto-image "suchbegriffe" --status draft

# Post aktualisieren + Bild nachträglich
python tools/wp-post-v2.py update \
  --id 456 --auto-image "neue suchbegriffe" --status publish

# Einzelbild hochladen (mit Optimierung)
python tools/wp-post-v2.py upload-image --file foto.jpg --optimize

# Batch-Upload ganzer Ordner
python tools/wp-post-v2.py batch-upload --folder ./bilder/ --optimize

# Posts auflisten
python tools/wp-post-v2.py list --search "Tutorial" --status draft
```

### MCP-Tools (Alternative)

```javascript
// Featured Image hochladen
const media = await wp_upload_media_from_url({
  fileUrl: "https://example.com/hero.png",
  title: "Article Title - Hero Image",
  altText: "Description for accessibility and SEO"
});

// Post mit Featured Image erstellen
await wp_create_post({
  title: "Article Title",
  content: articleHtml,
  status: "draft",
  featuredMediaId: media.id  // Featured Image wird automatisch gesetzt!
});
```

---

## 3️⃣ WordPress HTML Embedding

### Featured Image
```javascript
// featuredMediaId funktioniert in wp_create_post UND wp_update_post:
wp_create_post({ ..., featuredMediaId: 123 });
wp_update_post({ id: 456, featuredMediaId: 123 });
```

### Inline Illustration (Zentriert)
```html
<!-- wp:image {"align":"center","id":123,"sizeSlug":"large"} -->
<figure class="wp-block-image aligncenter size-large">
  <img src="[URL]" alt="[ALT TEXT]" class="wp-image-123"/>
  <figcaption class="wp-element-caption">Beschreibung</figcaption>
</figure>
<!-- /wp:image -->
```

### Screenshot mit Kontext
```html
<!-- wp:paragraph -->
<p><strong>Schritt 2:</strong> Klicke auf "Start"</p>
<!-- /wp:paragraph -->

<!-- wp:image {"id":124,"sizeSlug":"large"} -->
<figure class="wp-block-image size-large">
  <img src="[URL]" alt="Screenshot showing..." class="wp-image-124"/>
  <figcaption class="wp-element-caption">Der Start-Button</figcaption>
</figure>
<!-- /wp:image -->

<!-- wp:paragraph -->
<p>Das öffnet...</p>
<!-- /wp:paragraph -->
```

---

## 4️⃣ Emoji Guide

### Häufig genutzt

**Erfolg/Positiv:**
```
✅ Checklisten, Bestätigung
🎉 Erfolg, Abschluss
⭐ Highlights
💯 Perfektion
```

**Aktion/Prozess:**
```
🚀 Start, Deployment, Schnell
⚡ Quick Win, Energie
🔥 Hot Topic, Wichtig
💡 Idee, Tipp
🎯 Ziel, Fokus
⚙️ Einstellung, Konfiguration
```

**Lernen/Info:**
```
📚 Dokumentation, Lernen
📊 Daten, Analytics
📈 Wachstum, Fortschritt
🧠 Verstehen, Konzept
💻 Code, Development
```

**Zeit:**
```
⏱️ Schnell, Zeitbasiert
⏰ Deadline, Erinnerung
📅 Datum, Zeitplan
```

**Warnung:**
```
⚠️ Vorsicht, Wichtig
❗ Achtung
🔴 Stop, Fehler
```

### Verwendung

**Feature Lists:**
```html
<!-- wp:list -->
<ul class="wp-block-list">
<li>✅ Feature 1</li>
<li>🚀 Feature 2</li>
<li>📊 Feature 3</li>
</ul>
<!-- /wp:list -->
```

**Headings:**
```html
<!-- wp:heading -->
<h2 class="wp-block-heading">🎯 Getting Started</h2>
<!-- /wp:heading -->
```

---

## 5️⃣ Best Practices

### Anzahl Visuals

**Artikel-Länge → Anzahl Illustrationen:**
```
800-1200 Wörter:   1-2 Illustrationen + Emoji
1200-2000 Wörter:  2-3 Illustrationen + Emoji
2000+ Wörter:      3-5 Illustrationen + Emoji
```

### Alt Text Formeln

**Illustrationen:**
```
"Illustration showing [main concept/action]"
"Diagram of [process/workflow]"
```

**Screenshots:**
```
"Screenshot of [tool/interface] with [key element] highlighted"
```

### Dateibenennung

```
article-slug-hero.webp         # Featured Image (WebP, optimiert)
article-slug-workflow.png      # Inline Illustration
article-slug-screenshot-1.png  # Screenshot 1
```

---

## 6️⃣ Kompletter Workflow (~10 Min)

```
Minute 1-3:   Artikel-Struktur & Content schreiben (Markdown)
Minute 4-6:   Weitere Inhalte, Beispiele, Screenshots
Minute 7-8:   Optional: undraw.co Inline-Illustrationen
Minute 9:     wp-post-v2.py create --auto-image (30 Sek)
Minute 10:    Preview in WordPress, ggf. Feintuning
```

**Bildworkflow-Vergleich:**
| Schritt | Alt (v1, ~15 Min) | Neu (v2, ~30 Sek) |
|---------|--------------------|--------------------|
| Bild suchen | undraw.co manuell | Pexels automatisch |
| Optimieren | TinyPNG manuell | WebP automatisch |
| Hochladen | MCP/manuell | Integriert |
| Featured setzen | Manuell in WP | featuredMediaId |

---

## 7️⃣ Vollautomatisierung mit wp-post-v2.py

**Einzelner Artikel:**
```bash
python tools/wp-post-v2.py create \
  --title "Docker & n8n: Automation Setup" \
  --file docker-n8n-artikel.md \
  --auto-image "docker container automation server" \
  --status publish
```

**Artikel-Serie (Batch):**
```bash
for f in teil-1.md teil-2.md teil-3.md; do
  python tools/wp-post-v2.py create \
    --title "Tutorial $(basename ${f%.md})" \
    --file "$f" \
    --auto-image "tutorial education technology" \
    --status draft
done
```

**Nachträglich Bild hinzufügen:**
```bash
python tools/wp-post-v2.py update --id 456 \
  --auto-image "office workspace productivity"
```

---

## 8️⃣ Troubleshooting

**Problem:** Pexels findet keine passenden Bilder
```
✓ Englische Suchbegriffe verwenden
✓ Spezifischer suchen: "coffee laptop" statt "work"
✓ Adjektive hinzufügen: "modern bright office"
→ Fallback: undraw.co oder manueller Upload
```

**Problem:** Bild-Upload schlägt fehl
```
✓ PEXELS_API_KEY in .env gesetzt?
✓ Pillow installiert? (pip install Pillow)
✓ WordPress upload_max_filesize erhöht?
→ Fallback: wp_upload_media_from_url via MCP
```

**Problem:** Bild wird nicht angezeigt
```
✓ Media ID korrekt?
✓ Image Upload erfolgreich? (Check WP Media Library)
✓ WordPress Block Syntax korrekt?
→ Test in WP Preview Mode
```

---

## 9️⃣ Checkliste vor Publish

- [ ] Featured Image gesetzt (via `--auto-image` oder MCP)
- [ ] Alle inline images haben Alt Text
- [ ] Images sind optimiert (automatisch via wp-post-v2.py)
- [ ] Emoji konsistent verwendet
- [ ] Captions bei allen wichtigen Images
- [ ] Mobile Preview gecheckt
- [ ] Links funktionieren
- [ ] Code-Blocks richtig formatiert

---

## 🔟 Ressourcen

**Tools:**
```
Bilder (primär):  Pexels API (kostenlos, via wp-post-v2.py)
Illustrationen:   undraw.co (kostenlos, open source)
Komprimierung:    Automatisch via wp-post-v2.py (WebP)
                  TinyPNG.com (optional, für manuelle Optimierung)
Screenshots:      Win+Shift+S (Windows), Cmd+Shift+4 (Mac)
Annotation:       Photopea.com (kostenlos), Snagit (paid)
Emoji:            emojipedia.org (Referenz)
```

**Dokumentation:**
```
Skills:          blog-article-workflow/SKILL.md
                 blog-article-workflow/workflows/images-and-media.md
CLI-Tool:        tools/wp-post-v2.py (--help für alle Optionen)
MCP Server:      wp-mcp/README.md
```

---

*Zuletzt aktualisiert: 15.02.2026*
*Version: 2.0 - Pexels API + Auto-Image Integration*
