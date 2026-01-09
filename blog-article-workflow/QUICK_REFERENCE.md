# Blog Article with Images - Quick Reference

**Schnell-Anleitung für Blog-Artikel mit undraw.co, Screenshots und Emoji**

---

## 🎨 Vor dem Schreiben: Visuals planen

### Checkliste

- [ ] **Featured Image** ausgewählt (undraw.co)
- [ ] **1-3 Inline Illustrationen** heruntergeladen
- [ ] **Screenshots** gemacht (falls Tutorial)
- [ ] **Emoji-Set** definiert
- [ ] **Alt-Texte** vorbereitet

---

## 1️⃣ undraw.co Workflow (2 Minuten)

```
1. Gehe zu https://undraw.co/illustrations
2. Suche nach Keyword (z.B. "education", "coding")
3. Download PNG oder SVG
4. Umbenennen: article-slug-purpose.png
5. Optional: Komprimieren mit TinyPNG.com
```

**Beliebte Suchbegriffe:**
```
Lernen:     education, studying, online_learning
Tech:       coding, programming, server, data
Workflow:   working, collaboration, setup_wizard
Erfolg:     celebration, feeling_proud, achievement
```

---

## 2️⃣ MCP Upload (30 Sekunden pro Bild)

```javascript
// Featured Image
const hero = await MyWordPressMCP:wp_upload_media_from_url({
  fileUrl: "https://example.com/hero.png",
  title: "Article Title - Hero Image",
  altText: "Illustration showing [describe what's in image]"
});
// Merke dir: hero.id

// Inline Illustrationen
const img1 = await MyWordPressMCP:wp_upload_media_from_url({
  fileUrl: "https://example.com/workflow.png",
  title: "Workflow Illustration",
  altText: "Diagram of workflow from A to B"
});
// Merke dir: img1.id, img1.source_url
```

---

## 3️⃣ WordPress HTML Embedding

### Featured Image
```javascript
// In wp_create_post / wp_update_post
// Note: Featured image muss aktuell noch manuell in WP gesetzt werden
// featuredImageId parameter noch nicht verfügbar
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

**Step-by-Step:**
```html
<!-- wp:paragraph -->
<p><strong>Schritt 1:</strong> 🎯 Definiere Ziel</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Schritt 2:</strong> ✏️ Schreibe Content</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Schritt 3:</strong> 🚀 Publiziere</p>
<!-- /wp:paragraph -->
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

**Placement:**
```
[Hero Image]
Intro (200-300w)
[Illustration 1]
Section (300-400w)
[Screenshot 1]
Section (300-400w)
[Illustration 2]
Conclusion (200-300w)
```

### Alt Text Formeln

**Illustrationen:**
```
"Illustration showing [main concept/action]"
"Diagram of [process/workflow]"
"Conceptual illustration depicting [idea]"
```

**Screenshots:**
```
"Screenshot of [tool/interface] with [key element] highlighted"
"Screenshot showing [step/action] in [tool]"
```

### Dateibenennung

```
article-slug-hero.png          # Featured Image
article-slug-workflow.png      # Inline Illustration
article-slug-screenshot-1.png  # Screenshot 1
article-slug-screenshot-2.png  # Screenshot 2
```

---

## 6️⃣ Kompletter Workflow (15 Min)

```
Minute 1-3:   Artikel-Struktur schreiben
Minute 4-5:   undraw.co Illustrationen suchen & downloaden
Minute 6-7:   Screenshots machen (falls Tutorial)
Minute 8-10:  Artikel-Content schreiben
Minute 11-12: Bilder via MCP uploaden
Minute 13-14: HTML mit embedded images erstellen
Minute 15:    Via MCP als Draft publizieren
```

---

## 7️⃣ MCP Vollautomatisierung

**Komplett-Script:**

```javascript
// 1. Bilder hochladen
const images = {
  hero: await MyWordPressMCP:wp_upload_media_from_url({
    fileUrl: "https://example.com/hero.png",
    title: "Docker Tutorial - Hero",
    altText: "Illustration of Docker container deployment"
  }),
  workflow: await MyWordPressMCP:wp_upload_media_from_url({
    fileUrl: "https://example.com/workflow.png",
    title: "Docker Workflow Diagram",
    altText: "Diagram showing Docker setup process"
  })
};

// 2. HTML mit images bauen
const articleHtml = `
<!-- wp:paragraph -->
<p>Intro text... 🚀</p>
<!-- /wp:paragraph -->

<!-- wp:image {"align":"center","id":${images.workflow.id}} -->
<figure class="wp-block-image aligncenter">
  <img src="${images.workflow.source_url}" 
       alt="${images.workflow.altText}" 
       class="wp-image-${images.workflow.id}"/>
  <figcaption class="wp-element-caption">Workflow overview</figcaption>
</figure>
<!-- /wp:image -->

<!-- More content... -->
`;

// 3. Artikel publizieren
await MyWordPressMCP:wp_create_post({
  title: "Docker & n8n: Automation Setup",
  content: articleHtml,
  status: "draft"
});
// Note: Featured image manuell setzen in WP Admin
```

---

## 8️⃣ Troubleshooting

**Problem:** Bild-Upload schlägt fehl
```
✓ URL öffentlich zugänglich?
✓ Datei <64MB?
✓ WordPress upload_max_filesize erhöht?
→ Fallback: Manueller Upload in WP Media Library
```

**Problem:** Bild wird nicht angezeigt
```
✓ Media ID korrekt?
✓ Image Upload erfolgreich? (Check WP Media Library)
✓ WordPress Block Syntax korrekt?
→ Test in WP Preview Mode
```

**Problem:** Emoji werden nicht angezeigt
```
✓ UTF-8 Encoding im HTML?
✓ WordPress charset richtig?
→ Emoji funktionieren normalerweise out-of-the-box
```

---

## 9️⃣ Checkliste vor Publish

- [ ] Featured Image gesetzt (manuell in WP)
- [ ] Alle inline images haben Alt Text
- [ ] Images sind komprimiert (<500KB)
- [ ] Emoji konsistent verwendet
- [ ] Captions bei allen wichtigen Images
- [ ] Mobile Preview gecheckt
- [ ] Links funktionieren
- [ ] Code-Blocks richtig formatiert

---

## 🔟 Ressourcen

**Tools:**
```
Illustrationen:  undraw.co (kostenlos, open source)
Komprimierung:   tinypng.com (kostenlos)
Screenshots:     Win+Shift+S (Windows), Cmd+Shift+4 (Mac)
Annotation:      Photopea.com (kostenlos), Snagit (paid)
Emoji:           emojipedia.org (Referenz)
```

**Dokumentation:**
```
Skills:          blog-article-workflow/SKILL.md
                 blog-article-workflow/workflows/images-and-media.md
Examples:        blog-article-workflow/examples/docker-n8n-article-test.md
MCP Server:      wp-mcp/README.md
```

---

*Zuletzt aktualisiert: 03.01.2026*
*Version: 1.0*
