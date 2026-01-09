---
name: blog-article-workflow
description: Complete workflow for creating and publishing blog articles with Claude AI and WordPress MCP integration. Use when creating educational blog posts, tutorial articles, or documentation that needs to be published to WordPress.
license: MIT
---

# Blog Article Creation Workflow

Step-by-step workflow for creating high-quality blog articles from concept to publication, with optional WordPress automation via MCP.

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

### Phase 4: Publishing (2-5 min)
1. Upload to WordPress (manual or via MCP)
2. Add featured image
3. Set categories/tags
4. Preview and publish

**Total Time:** 30-60 minutes per article

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
   - Source: undraw.co illustrations or custom design
   - Size: 1200x630px (optimal for social sharing)
   - Theme: Match article topic and brand colors
   - Upload via MCP before/during article creation

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
- [ ] Featured image selected/created (undraw.co)
- [ ] Inline illustrations downloaded from undraw.co
- [ ] Screenshots taken and annotated
- [ ] Icons identified (emoji or icon library)
- [ ] All images optimized (<500KB each)
- [ ] Alt text written for each image

### Undraw.co Workflow

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

## Phase 4: Publishing via MCP

### Manual Publishing

```
1. Copy HTML content
2. WordPress → Posts → Add New
3. Paste into editor (code view)
4. Add featured image
5. Set categories/tags
6. Preview → Publish
```

### Automated Publishing (with MCP)

**Step 1: Prepare content**
```javascript
const articleContent = `
<!-- wp:paragraph -->
<p>Article content here...</p>
<!-- /wp:paragraph -->
`;
```

**Step 2: Use MCP tool**
```javascript
wp_create_post({
  title: "H5P + WordPress: Interactive Learning Modules in 10 Minutes",
  content: articleContent,
  status: "draft",  // or "publish"
  postType: "post"
});
```

**Step 3: Review and finalize**
- Check preview
- Add featured image (if not done via MCP)
- Verify formatting
- Publish when ready

### With Featured Image

```javascript
// First, upload image
wp_upload_media_from_url({
  fileUrl: "https://example.com/image.png",
  title: "Article Featured Image",
  altText: "Description for SEO"
});

// Then create post with image ID
wp_create_post({
  title: "Article Title",
  content: articleContent,
  status: "draft",
  featuredImageId: 123  // from upload response
});
```

## Real-World Example: This Workflow in Action

**Article:** "H5P + WordPress Tutorial"

**Phase 1: Concept (8 minutes)**
- Defined audience: tech-savvy teachers
- Key message: H5P is easier than you think
- Structure: Problem → Solution → Workflow → Examples
- Gathered: 2 real H5P files, screenshots

**Phase 2: Content (35 minutes)**
- Hook: Personal story (10-minute module)
- Explained 3 favorite H5P types
- Added real examples from teaching
- Included 10-minute workflow
- Best practices from 2+ years use

**Phase 3: Formatting (7 minutes)**
- Converted Markdown to WordPress HTML
- Added Gutenberg blocks
- Formatted lists and quotes
- Checked mobile preview

**Phase 4: Publishing (3 minutes)**
- Used MCP: `wp_create_post(...)`
- Draft created automatically
- Reviewed in WordPress
- Published

**Total: 53 minutes** (including this documentation)

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

*This skill is based on producing 50+ blog articles using this exact workflow.*
