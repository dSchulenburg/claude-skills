---
name: blog-article-workflow
description: Complete workflow for creating and publishing blog articles with Claude AI and WordPress MCP integration. Use when creating educational blog posts, tutorial articles, or documentation that needs to be published to WordPress.
license: MIT
---

# Blog Article Creation Workflow

Step-by-step workflow for creating high-quality blog articles from concept to publication, with WordPress automation via MCP.

## MCP Integration (WICHTIG)

**Dieser Skill nutzt den WordPress MCP Server direkt. Verwende immer diese Tools:**

| Tool | Zweck |
|------|-------|
| `wp_upload_media_from_url` | Bild von URL hochladen, gibt Media-ID zurück |
| `wp_upload_media_base64` | Optimiertes Bild (Base64) hochladen (WebP, Resize) |
| `wp_create_post` | Neuen Beitrag erstellen (mit `featuredMediaId`) |
| `wp_update_post` | Bestehenden Beitrag aktualisieren |
| `wp_list_posts` | Beiträge auflisten |
| `wp_list_media` | Medien in Bibliothek auflisten |

**Standard-Workflow (MCP):**
```
1. wp_upload_media_from_url → Media-ID erhalten
2. wp_create_post mit featuredMediaId → Draft erstellen
3. User reviewed in WordPress → Publish
```

**Empfohlen: CLI mit `wp-post-v2.py`** (Pexels + Auto-Image + Optimierung integriert, siehe nächster Abschnitt)

**NIEMALS SSH oder manuelle API-Calls verwenden - immer MCP-Tools oder wp-post-v2.py nutzen!**

---

## Schnellstart mit wp-post-v2.py (empfohlen)

**One-Command Publishing** mit automatischem Featured Image:

```bash
python tools/wp-post-v2.py create \
  --title "Mein Artikel" --file artikel.md \
  --auto-image "keyword1 keyword2 kontext" \
  --status publish
```

**Setup:**
```bash
# Pexels API Key (kostenlos): https://www.pexels.com/api/
# In .env oder als Environment Variable:
PEXELS_API_KEY=your-key-here

# Dependencies
pip install Pillow requests python-dotenv
```

**Alle Befehle:**

| Befehl | Funktion |
|--------|----------|
| `create` | Post erstellen (+ `--auto-image`, `--image`, `--file`) |
| `update` | Post aktualisieren (`--id`, `--auto-image`, `--status`) |
| `find-image` | Pexels-Bildsuche mit Preview (`--download`) |
| `upload-image` | Einzelbild hochladen (`--optimize` für WebP) |
| `batch-upload` | Ordner-Upload (`--folder`, `--optimize`) |
| `list` | Posts auflisten (`--search`, `--status`) |

**Query-Optimierung für bessere Bilder:**
- Spezifisch: `"coffee laptop workspace"` statt `"work"`
- Kontext: `"classroom students learning"` statt `"education"`
- Adjektive: `"modern office bright"` statt `"office"`
- Englisch bevorzugt (größere Pexels-Datenbank)

---

## When to Use This Skill

Use this skill when:
- Creating educational blog posts or tutorials
- Writing technical documentation for publication
- Producing content series for a blog
- Automating WordPress publishing workflows
- Converting ideas/audio/notes into structured articles

## Workflow Overview

### Phase 1: Concept & Structure (5-10 min)
1. Define topic and audience
2. Identify key message/takeaway
3. Create article structure
4. Gather examples/resources

### Phase 2: Content Creation (20-40 min)
1. Write hook/introduction
2. Develop main sections
3. Add practical examples
4. Include visuals/illustrations
5. Write conclusion/call-to-action

### Phase 3: Formatting (5-10 min)
1. Convert to WordPress-compatible HTML
2. Add proper heading hierarchy
3. Format lists, quotes, code blocks
4. Optimize for readability

### Phase 4: Publishing (1-2 min)
1. `wp-post-v2.py create --auto-image` (Bild + Post in einem Befehl)
2. Preview and publish

**Total Time:** 25-50 minutes per article

## Phase 1: Concept & Structure

### Step 1.1: Define Topic and Audience

**Questions to answer:**
- Who is reading this? (beginners, advanced users, peers?)
- What do they need to know?
- What problem does this solve?
- What action should they take after reading?

**Example:**
```
Topic: "H5P + WordPress Tutorial"
Audience: Tech-savvy teachers
Problem: Creating interactive content is time-consuming
Action: Create first H5P module in 10 minutes
```

### Step 1.2: Create Article Structure

**Standard structure for educational/tutorial articles:**

```markdown
1. Hook (personal story or surprising fact)
2. Problem statement
3. Solution overview
4. Detailed explanation (3-5 main points)
5. Practical examples
6. Step-by-step workflow
7. Best practices
8. Common mistakes
9. Next steps
10. Resources
```

**Pro tip:** Use this as a template, adapt as needed

### Step 1.3: Gather Resources

Before writing, collect:
- Screenshots/images
- Code examples
- Links to references
- Real-world examples
- Data/statistics (if applicable)

**Time-saver:** Create a "drafts" folder with all assets before writing

## Phase 2: Content Creation

### Visual Assets Strategy

**Before writing, plan your visuals:**

**Types of visuals to include:**

1. **Featured Image (Hero Image)**
   - **Primär:** Pexels API via `--auto-image` (automatisch optimiert)
   - Size: 1200x630px (automatisch via wp-post-v2.py)
   - Format: WebP, ~52KB (95.9% Kompression)
   - Alternativ: undraw.co Illustrationen für abstraktere Themen

2. **Inline Illustrations**
   - Use undraw.co for concepts/workflows
   - Example topics: collaboration, coding, learning, data
   - Place every 300-500 words for visual breaks
   - Always include alt text for accessibility

3. **Screenshots (for tutorials)**
   - Annotate with arrows/boxes/highlights
   - Use consistent border/shadow style
   - Crop to relevant UI sections only
   - Include captions explaining what's shown

4. **Icons**
   - Use for feature lists, benefits, steps
   - Sources: Font Awesome, Heroicons, Lucide, emoji
   - Keep consistent style throughout article
   - Consider using emoji as lightweight alternative (✅ 🚀 📊 💡 ⚡)

**Visual placement guide:**
```
[Hero Image - Featured]
Introduction (200-300 words)
[Illustration 1 - Concept overview]
Main Section 1 (300-400 words)
[Screenshot 1 - Step demonstration]
Main Section 2 (300-400 words)
[Illustration 2 - Workflow diagram]
Main Section 3 (300-400 words)
[Screenshot 2 - Result]
Conclusion (200-300 words)
```

**Asset preparation checklist:**
- [ ] Featured image via Pexels (`--auto-image`) oder undraw.co
- [ ] Inline illustrations (undraw.co oder Pexels)
- [ ] Screenshots taken and annotated
- [ ] Icons identified (emoji or icon library)
- [ ] Bilder optimiert (automatisch via wp-post-v2.py, ~52KB WebP)
- [ ] Alt text written for each image

### Undraw.co Workflow (für Inline-Illustrationen)

**Finding the right illustration:**
1. Go to https://undraw.co/illustrations
2. Search for topic keywords (e.g., "education", "coding", "workflow")
3. Customize color to match brand (optional)
4. Download as SVG or PNG
5. Rename descriptively (e.g., `h5p-workflow-illustration.svg`)

**Popular undraw.co topics for educational content:**
- **Learning:** education, studying, online_learning, teacher
- **Technical:** coding, programming, developer, data
- **Workflow:** working, collaboration, process, timeline
- **Success:** celebration, feeling_proud, goals, growth

**Pro tip:** Download 3-4 illustrations at once, then pick the best 1-2 during writing

### Writing Principles

**1. Start with the hook**
- Personal anecdote
- Surprising statistic
- Provocative question
- Common pain point

**Bad:** "In this article, I will explain H5P..."
**Good:** "Last week I created an interactive module in 10 minutes that kept students engaged 3x longer than a PDF worksheet."

**2. Show, don't just tell**
- Use concrete examples
- Include real numbers/data
- Reference actual projects
- Share screenshots/visuals

**3. Write conversationally**
- Use "you" and "I"
- Short paragraphs (2-4 sentences)
- Varied sentence length
- Active voice

**4. Structure for scanning**
- Clear headings (H2, H3)
- Bulleted lists for key points
- Bold for emphasis (sparingly)
- Code blocks for technical content

### Section Templates

**Introduction Template:**
```markdown
[Hook - personal story or surprising fact]

[Problem statement - what frustrates readers]

[Solution preview - what this article delivers]

[Credibility - why you're qualified to write this]
```

**Main Section Template:**
```markdown
## [Clear, benefit-focused heading]

[Brief explanation - what and why]

**[Sub-concept]:** [Explanation]
- Bullet point 1
- Bullet point 2
- Bullet point 3

**Example from my practice:**
[Concrete example with details]

**Result:** [Outcome, ideally with numbers]
```

**Workflow Section Template:**
```markdown
## The [X]-Minute Workflow

### Option A: [Simple approach]

**Minute 1-2:** [Step name]
- Action 1
- Action 2

**Minute 3-5:** [Step name]
- Action 1
- Action 2

**Minute 6:** [Final step]
- Result achieved

### Option B: [Advanced approach]

[Same format but for power users]
```

**Conclusion Template:**
```markdown
## Your Next Steps

### Week 1: [First milestone]
1. Action item 1
2. Action item 2

### Week 2: [Second milestone]
1. Action item 1
2. Action item 2

### Long-term: [Vision]
[Bigger picture goals]

## Resources

[Links to tools, docs, examples]

---

**Questions? Feedback?** [Call to action]

---

*[Closing note about authenticity/experience]*
```

## Phase 3: WordPress Formatting

### HTML Conversion Rules

**Headings:**
```html
# Title → Not used (WordPress post title)
## Section → <h2 class="wp-block-heading">
### Subsection → <h3 class="wp-block-heading">
```

**Paragraphs:**
```html
<!-- wp:paragraph -->
<p>Text here</p>
<!-- /wp:paragraph -->
```

**Lists:**
```html
<!-- wp:list -->
<ul class="wp-block-list">
<li>Item 1</li>
<li>Item 2</li>
</ul>
<!-- /wp:list -->
```

**Quotes:**
```html
<!-- wp:quote -->
<blockquote class="wp-block-quote">
<p>Quote text</p>
</blockquote>
<!-- /wp:quote -->
```

**Code blocks:**
```html
<!-- wp:code -->
<pre class="wp-block-code"><code>code here</code></pre>
<!-- /wp:code -->
```

**Separators:**
```html
<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->
```

### Formatting Checklist

- [ ] All headings use proper hierarchy (H2 → H3 → H4)
- [ ] Paragraphs are wrapped in WordPress blocks
- [ ] Lists use proper Gutenberg formatting
- [ ] Links are absolute URLs (https://...)
- [ ] Images have alt text
- [ ] Code blocks use proper syntax
- [ ] Separators between major sections

## Phase 4: Publishing

### Empfohlen: wp-post-v2.py (One-Command)

**Einzelner Artikel mit Auto-Image:**
```bash
python tools/wp-post-v2.py create \
  --title "H5P + WordPress: Interactive Learning Modules in 10 Minutes" \
  --file artikel.md \
  --auto-image "interactive learning digital education" \
  --status draft
```

**Artikel nachträglich mit Bild versehen:**
```bash
python tools/wp-post-v2.py update \
  --id 456 \
  --auto-image "education technology classroom" \
  --status publish
```

**Batch-Publishing für Serien:**
```bash
# Artikel 1-4 erstellen
for f in teil-1.md teil-2.md teil-3.md teil-4.md; do
  python tools/wp-post-v2.py create \
    --title "Serie: ${f%.md}" --file "$f" \
    --auto-image "tutorial series learning" \
    --status draft
done
```

### Alternative: MCP-Tools

**Step 1: Upload image and get Media-ID**
```javascript
const media = await wp_upload_media_from_url({
  fileUrl: "https://example.com/image.png",
  title: "Article Featured Image",
  altText: "Description for SEO"
});
// Response includes: Media-ID: 123
```

**Step 2: Create post with Featured Image**
```javascript
wp_create_post({
  title: "Article Title",
  content: articleContent,
  status: "draft",
  featuredMediaId: media.id  // Sets Featured Image automatically!
});
```

**Step 3: Review and finalize**
- Check preview in WordPress
- Verify formatting
- Publish when ready

### Manual Publishing (Fallback)

```
1. Copy HTML content
2. WordPress → Posts → Add New
3. Paste into editor (code view)
4. Add featured image
5. Set categories/tags
6. Preview → Publish
```

## Real-World Example: Tutorial-Serie (4 Artikel)

**Projekt:** Claude AI Tutorial-Serie (14.02.2026)

**Phase 1: Konzept (10 min, 4 Artikel geplant)**
- Zielgruppe: Lehrer, Bildungsinteressierte
- Themen: Claude Grundlagen, Unterricht, Prompting, MCP
- Struktur pro Artikel: Problem → Lösung → Workflow → Beispiele

**Phase 2: Content (40 min, alle 4 Artikel)**
- Markdown in separaten Dateien geschrieben
- Praxis-Beispiele aus echtem Unterricht
- Code-Beispiele und Workflows

**Phase 3: Formatting (3 min)**
- wp-post-v2.py konvertiert Markdown automatisch zu WordPress-Blocks

**Phase 4: Publishing (10 min, alle 4 Artikel)**
```bash
# Pro Artikel: 1 Befehl, ~30 Sekunden
python tools/wp-post-v2.py create \
  --title "Claude AI Tutorial: Grundlagen" \
  --file tutorial-1.md \
  --auto-image "artificial intelligence education" \
  --status publish
```
- Pexels-Bild automatisch gefunden, optimiert (1.3MB → 52KB WebP), hochgeladen
- Featured Image automatisch gesetzt
- Direkt als Draft oder Published

**Total: 63 Minuten** für 4 fertige Artikel (statt ~4h mit altem Workflow)

**Zeitvergleich pro Artikel:**

| Schritt | Alt (v1) | Neu (v2) |
|---------|----------|----------|
| Bild suchen | 5-10 min (undraw.co, manuell) | 5 sek (Pexels, automatisch) |
| Bild optimieren | 3-5 min (TinyPNG, manuell) | 0 sek (automatisch, WebP) |
| Bild hochladen | 2-3 min (MCP/manuell) | 0 sek (integriert) |
| Featured Image setzen | 1-2 min (manuell in WP) | 0 sek (featuredMediaId) |
| **Gesamt Bildworkflow** | **11-20 min** | **~30 sek** |

## Bildoptimierung

### Automatische Pipeline (wp-post-v2.py)

```
Pexels API → Download Original → Resize 1200x630 → WebP 85% → Upload Base64
```

**Ergebnisse:**
- Kompression: ~95.9% (1.3MB Original → ~52KB WebP)
- Format: WebP mit 85% Qualität (gute Balance)
- Smart Crop: Automatischer Bildausschnitt auf 1200x630 (Fokus Mitte)
- EXIF: Orientierung wird korrigiert (Handy-Fotos)

**Dependencies:**
```bash
pip install Pillow requests python-dotenv
```

**Konfiguration** (in wp-post-v2.py):
```python
DEFAULT_FEATURED_SIZE = (1200, 630)  # WordPress Featured Image Standard
DEFAULT_QUALITY = 85                  # WebP Qualität
WEBP_ENABLED = True                   # WebP-Konvertierung
```

### Manuelle Optimierung (falls nötig)

```bash
# Einzelbild optimieren und hochladen
python tools/wp-post-v2.py upload-image --file foto.jpg --optimize

# Ganzen Ordner hochladen
python tools/wp-post-v2.py batch-upload --folder ./bilder/ --optimize
```

---

## Best Practices

### Content Quality

**Do:**
- Start with real examples
- Use concrete numbers/data
- Write conversationally
- Include next steps
- Provide resources

**Don't:**
- Use jargon without explanation
- Write walls of text
- Assume prior knowledge
- Skip the "why"
- Forget mobile readers

### SEO Basics

**Include:**
- Focus keyword in title
- Focus keyword in first paragraph
- Descriptive headings (not "Introduction")
- Internal links to other articles
- External links to authoritative sources
- Alt text for all images

### Engagement

**Increase readership:**
- Strong hook
- Scannable structure
- Visuals every 300-400 words
- Concrete examples
- Clear next steps

**Call to action:**
- Ask for feedback
- Encourage sharing
- Offer resources
- Invite questions

## Skill Integration

### Combine with Other Skills

**With h5p-wordpress-workflow:**
- Write articles about H5P
- Include .h5p file uploads
- Automate full publishing

**With frontend-design:**
- Create custom illustrations
- Design infographics
- Build interactive demos

**With canvas-design:**
- Create featured images
- Design diagrams
- Produce visual assets

## Common Issues

### Issue: Writer's block
**Solution:** Start with structure, fill in examples first, then write connecting text

### Issue: Too long/too short
**Solution:** Aim for 1500-2500 words for tutorials, adjust based on complexity

### Issue: Too technical/not technical enough
**Solution:** Define audience first, write for them specifically, have peer review

### Issue: Formatting breaks in WordPress
**Solution:** Use WordPress block comments consistently, test in preview

## Next Steps

1. **Today:** Create article structure for next post
2. **This week:** Write and publish first article using this workflow
3. **Next week:** Review analytics, iterate on what works
4. **Long-term:** Build article templates for common topics

---

## Logging

Bei Ausführung dieses Skills wird automatisch geloggt:

| Feld | Wert |
|------|------|
| **Agent** | personal |
| **Action** | blog:publish_article |
| **Context** | title, post_id, word_count, featured_image_id |
| **Result** | success/failure |

**Beispiel-Log:**
```json
{
  "agent": "personal",
  "action": "blog:publish_article",
  "context": "{\"title\": \"H5P + WordPress Tutorial\", \"post_id\": 456, \"word_count\": 2100, \"featured_image_id\": 123}",
  "result": "success"
}
```

---

*Version 2.0 - Pexels API + Auto-Image Integration (15.02.2026)*
