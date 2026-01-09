# Images & Media Workflow for Blog Articles

Complete guide for integrating visual assets (undraw.co illustrations, screenshots, icons) into WordPress blog articles.

## Overview

**Visual Types Used:**
- 🎨 **undraw.co illustrations** - Conceptual visuals, hero images
- 📸 **Screenshots** - Tutorial steps, UI demonstrations  
- 🎯 **Icons/Emoji** - Feature lists, quick visual markers

**Integration Methods:**
- Manual upload to WordPress Media Library
- Automated upload via MCP (`wp_upload_media_from_url`)
- Direct embedding in article HTML

---

## Quick Reference: Emoji Guide

**Recommended emoji for educational content:**
```
Success/Positive: ✅ ✔️ 🎉 👍 💯 ⭐
Action/Process: 🚀 ⚡ 🔥 💡 🎯 ⚙️
Learning: 📚 📖 🎓 📊 📈 🧠
Time: ⏱️ ⏰ 📅 🕐
Warning/Important: ⚠️ ❗ 💥 🔴
Tools: 🛠️ 🔧 💻 📱 🖥️
```

---

## Workflow 1: undraw.co Illustrations

### Finding the Right Illustration

**Step 1: Search on undraw.co**
```
1. Visit https://undraw.co/illustrations
2. Search for topic (e.g., "education", "coding", "workflow")
3. Browse results
4. Select illustration
```

**Popular searches for educational content:**
```
Learning: education, studying, online_learning, teacher, graduation
Technical: coding, programming, developer_activity, server, data
Workflow: working, collaboration, process, setup_wizard, timeline
Productivity: task_list, time_management, checklist, organize
Success: celebration, feeling_proud, achievement, team_spirit
```

**Step 2: Customize & Download**
```
1. Click on selected illustration
2. (Optional) Change primary color to match brand
3. Download as PNG or SVG
4. Rename file: article-slug-purpose.png
   Example: h5p-tutorial-hero.png
```

### WordPress Integration

**Option A: Manual Upload**
```
1. WordPress Admin → Media → Add New
2. Upload image file
3. Fill in metadata:
   - Title: "H5P Tutorial - Hero Image"
   - Alt Text: "Illustration showing interactive learning workflow"
4. Note the Media ID
```

**Option B: MCP Upload (from URL)**
```javascript
const result = await MyWordPressMCP:wp_upload_media_from_url({
  fileUrl: "https://undraw.co/download/education.png",
  title: "H5P Tutorial Hero Image",
  altText: "Illustration of online education with interactive elements"
});
// Returns: { id: 123, source_url: "...", mime_type: "..." }
```

### Embedding in Article

**As Featured Image:**
```javascript
// Step 1: Upload the image first
const media = await MyWordPressMCP:wp_upload_media_from_url({
  fileUrl: "https://undraw.co/download/education.png",
  title: "Article Featured Image",
  altText: "Description for accessibility and SEO"
});
// Returns: { id: 123, source_url: "...", mime_type: "..." }

// Step 2: Create post with featured image
await MyWordPressMCP:wp_create_post({
  title: "Article Title",
  content: articleHtml,
  status: "draft",
  featuredMediaId: media.id  // Sets the Featured Image automatically!
});
```

**As Inline Image (Centered):**
```html
<!-- wp:image {"align":"center","id":123,"sizeSlug":"large"} -->
<figure class="wp-block-image aligncenter size-large">
  <img src="https://yoursite.com/wp-content/uploads/2026/01/education.png" 
       alt="Illustration showing interactive learning workflow" 
       class="wp-image-123"/>
  <figcaption class="wp-element-caption">H5P makes interactive content simple</figcaption>
</figure>
<!-- /wp:image -->
```

**As Inline Image (Full Width):**
```html
<!-- wp:image {"id":124,"sizeSlug":"full"} -->
<figure class="wp-block-image size-full">
  <img src="https://yoursite.com/wp-content/uploads/2026/01/workflow.png" 
       alt="Workflow diagram from creation to publishing" 
       class="wp-image-124"/>
</figure>
<!-- /wp:image -->
```

---

## Workflow 2: Screenshots

### Capturing Screenshots

**Tools:**
- **Windows:** Win + Shift + S (Snipping Tool)
- **Mac:** Cmd + Shift + 4
- **Professional:** Snagit, Greenshot, ShareX

**Best Practices:**
```
✅ Do:
- Crop to relevant UI section only
- Use consistent window size for series
- Capture high resolution (then compress)
- Ensure text is readable
- Remove sensitive information

❌ Don't:
- Include unnecessary browser chrome
- Mix screenshot sizes in one article
- Upload without compression
- Forget to annotate important elements
```

### Annotating Screenshots

**Simple annotations:**
- Arrows pointing to key elements
- Boxes highlighting important sections
- Numbers for step-by-step sequences
- Text callouts for explanations

**Tools for annotation:**
- **Built-in:** Windows Snipping Tool, Mac Preview
- **Online:** Photopea.com (free Photoshop alternative)
- **Professional:** Snagit, CloudApp

### Optimization

**Before uploading:**
```
1. Crop to relevant section
2. Add annotations if needed
3. Compress with TinyPNG.com
4. Target: <300KB per screenshot
5. Rename: article-slug-screenshot-N.png
```

**Example naming:**
```
h5p-tutorial-screenshot-1-editor.png
h5p-tutorial-screenshot-2-settings.png
h5p-tutorial-screenshot-3-preview.png
```

### Embedding Screenshots

**With context (recommended):**
```html
<!-- wp:paragraph -->
<p><strong>Step 2:</strong> Select "Interactive Video" from the content type dropdown:</p>
<!-- /wp:paragraph -->

<!-- wp:image {"id":125,"sizeSlug":"large"} -->
<figure class="wp-block-image size-large">
  <img src="https://yoursite.com/wp-content/uploads/screenshot-1.png" 
       alt="Screenshot of H5P editor with Interactive Video selected" 
       class="wp-image-125"/>
  <figcaption class="wp-element-caption">Choose Interactive Video to begin</figcaption>
</figure>
<!-- /wp:image -->

<!-- wp:paragraph -->
<p>This opens the editor interface where you can...</p>
<!-- /wp:paragraph -->
```

---

## Workflow 3: Icons & Emoji

### Using Emoji (Fastest Method)

**Feature lists:**
```html
<!-- wp:list -->
<ul class="wp-block-list">
<li>✅ Easy to create</li>
<li>🚀 Fast deployment</li>
<li>📊 Built-in analytics</li>
<li>💡 Engaging for students</li>
</ul>
<!-- /wp:list -->
```

**Step-by-step guides:**
```html
<!-- wp:heading {"level":3} -->
<h3 class="wp-block-heading">⏱️ 10-Minute Workflow</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Minute 1-2:</strong> 🎯 Select content type</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Minute 3-5:</strong> ✏️ Add your content</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Minute 6-8:</strong> ⚙️ Configure settings</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Minute 9-10:</strong> 🚀 Export and publish</p>
<!-- /wp:paragraph -->
```

**Section headers:**
```html
<!-- wp:heading -->
<h2 class="wp-block-heading">🎯 Getting Started</h2>
<!-- /wp:heading -->

<!-- wp:heading -->
<h2 class="wp-block-heading">⚡ Quick Wins</h2>
<!-- /wp:heading -->

<!-- wp:heading -->
<h2 class="wp-block-heading">🚀 Next Steps</h2>
<!-- /wp:heading -->
```

### Using Icon Images (Advanced)

**When to use:**
- Need consistent brand styling
- Building infographics
- Creating feature comparison tables
- Professional documentation

**Icon sources:**
- Font Awesome: https://fontawesome.com/icons (free tier)
- Heroicons: https://heroicons.com (MIT license, free)
- Lucide: https://lucide.dev (ISC license, free)
- Feather: https://feathericons.com (MIT license, free)

---

## Complete Example: Article with Images

### Visual Inventory

**For article: "H5P + WordPress: Interactive Learning in 10 Minutes"**

```
📁 Visual assets:
├── 🎨 h5p-hero.png (undraw.co - Featured image)
├── 🎨 h5p-workflow.png (undraw.co - Inline illustration)
├── 📸 h5p-screenshot-1-editor.png (Screenshot of H5P editor)
├── 📸 h5p-screenshot-2-preview.png (Screenshot of preview)
└── 🎯 Emoji (✅, 🚀, ⏱️, 💡, etc.)
```

### Article Structure

```html
<!-- FEATURED IMAGE: Set manually in WordPress admin after creating draft -->

<!-- Introduction -->
<!-- wp:paragraph -->
<p>Last week I created an interactive module in 10 minutes that kept students engaged 3x longer than a PDF worksheet. 🎉</p>
<!-- /wp:paragraph -->

<!-- Section 1: Why H5P? -->
<!-- wp:heading -->
<h2 class="wp-block-heading">🎯 Why H5P?</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<li>✅ Free and open source</li>
<li>🚀 Quick to create</li>
<li>📊 Built-in analytics</li>
<li>💡 Engaging for students</li>
</ul>
<!-- /wp:list -->

<!-- ILLUSTRATION 1: Workflow overview -->
<!-- wp:image {"align":"center","id":201,"sizeSlug":"large"} -->
<figure class="wp-block-image aligncenter size-large">
  <img src="https://yoursite.com/wp-content/uploads/h5p-workflow.png" 
       alt="Illustration of H5P workflow from creation to student interaction" 
       class="wp-image-201"/>
  <figcaption class="wp-element-caption">The complete H5P workflow</figcaption>
</figure>
<!-- /wp:image -->

<!-- Section 2: 10-Minute Workflow -->
<!-- wp:heading -->
<h2 class="wp-block-heading">⏱️ The 10-Minute Workflow</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Minute 1-3:</strong> 🎯 Select "Interactive Video" in H5P editor</p>
<!-- /wp:paragraph -->

<!-- SCREENSHOT 1: Editor interface -->
<!-- wp:image {"id":202,"sizeSlug":"large"} -->
<figure class="wp-block-image size-large">
  <img src="https://yoursite.com/wp-content/uploads/screenshot-1-editor.png" 
       alt="Screenshot of H5P editor with Interactive Video content type selected" 
       class="wp-image-202"/>
  <figcaption class="wp-element-caption">Select Interactive Video to begin</figcaption>
</figure>
<!-- /wp:image -->

<!-- wp:paragraph -->
<p><strong>Minute 4-6:</strong> ✏️ Upload your video and add interactive elements</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Minute 7-9:</strong> ⚙️ Configure feedback and behavior settings</p>
<!-- /wp:paragraph -->

<!-- SCREENSHOT 2: Preview -->
<!-- wp:image {"id":203,"sizeSlug":"large"} -->
<figure class="wp-block-image size-large">
  <img src="https://yoursite.com/wp-content/uploads/screenshot-2-preview.png" 
       alt="Screenshot showing completed H5P interactive video module preview" 
       class="wp-image-203"/>
  <figcaption class="wp-element-caption">Preview your completed module</figcaption>
</figure>
<!-- /wp:image -->

<!-- wp:paragraph -->
<p><strong>Minute 10:</strong> 🚀 Export and publish to WordPress</p>
<!-- /wp:paragraph -->

<!-- Conclusion -->
<!-- wp:paragraph -->
<p>🎉 Congratulations! You've just created your first interactive learning module in 10 minutes!</p>
<!-- /wp:paragraph -->
```

---

## Best Practices

### Image Quality
- ✅ Compress all images (<500KB per image)
- ✅ Use PNG for screenshots (sharp text)
- ✅ Use SVG for icons when possible
- ✅ Optimize with TinyPNG.com before upload

### Accessibility
- ✅ Write descriptive alt text for every image
- ✅ Include captions when helpful
- ✅ Use emoji sparingly (not excessive)
- ❌ Don't leave alt text empty
- ❌ Don't use "image.png" as alt text

### Visual Consistency
- ✅ Use same undraw.co color theme across article
- ✅ Keep screenshot annotation style consistent
- ✅ Use emoji set consistently
- ✅ Maintain visual hierarchy

### Performance
- ✅ Lazy-load images (WordPress default)
- ✅ Use WordPress responsive image classes
- ❌ Don't hotlink from external sites
- ❌ Don't upload massive uncompressed files

---

## Troubleshooting

**Issue: Image upload fails**
- Check file size (<64MB WordPress default)
- Verify URL is publicly accessible (if using MCP)
- Try compressing image further
- Upload manually as fallback

**Issue: Images don't display**
- Verify image uploaded to Media Library
- Check media ID matches in HTML
- Test in WordPress preview mode
- Clear browser cache

**Issue: Images look bad on mobile**
- Use WordPress responsive classes (size-large, size-medium)
- Test on actual mobile device
- Ensure images aren't too wide
- Use mobile-friendly WordPress theme

---

## Next Steps

1. **Build visual library** - Download 10-15 undraw.co illustrations for common topics
2. **Screenshot workflow** - Set up annotation tool with consistent styling
3. **Emoji reference** - Create personal emoji guide for your style
4. **Test MCP automation** - Upload images via MCP and embed in article
5. **Measure engagement** - Compare article performance with/without visuals

---

*This workflow is based on creating 50+ blog articles with undraw.co illustrations, annotated screenshots, and strategic emoji use.*
