---
name: h5p-wordpress-workflow
description: Complete workflow for creating and publishing H5P interactive content to WordPress. Use when users want to create interactive educational content (quizzes, videos, presentations), integrate H5P with WordPress, or automate H5P content publishing workflows with MCP servers.
license: MIT
---

# H5P + WordPress Workflow

Complete workflow for creating interactive educational content with H5P and publishing to WordPress, with optional MCP automation.

## When to Use This Skill

Use this skill when:
- Creating interactive educational content (quizzes, interactive videos, timelines, etc.)
- Publishing H5P content to WordPress
- Automating H5P workflows with MCP servers
- Setting up H5P for educational institutions
- Migrating H5P content between platforms

## Quick Start

### Basic Workflow (Manual)
1. Create H5P content on H5P.com or locally
2. Export as .h5p file
3. Upload to WordPress via Media Library
4. Embed using shortcode: `[h5p id="123"]`

### Advanced Workflow (MCP Automation)
1. Create H5P content
2. Store .h5p file in accessible location (URL)
3. Use MCP to upload and publish automatically

## H5P Content Types Overview

### Most Popular for Education

**Interactive Video** - Videos with embedded questions, popups, and navigation
- Use case: Flipped classroom, video lessons with comprehension checks
- Engagement: ★★★★★

**Quiz (Question Set)** - Multiple question types in sequence
- Use case: Assessments, self-checks, homework
- Engagement: ★★★★☆

**Course Presentation** - Slide-based presentations with interactive elements
- Use case: Lessons, tutorials, presentations
- Engagement: ★★★★☆

**Interactive Book** - Multi-page content with various H5P elements
- Use case: Digital textbooks, comprehensive learning modules
- Engagement: ★★★★★

**Timeline** - Interactive chronological presentations
- Use case: History, processes, project planning
- Engagement: ★★★☆☆

**Drag and Drop** - Visual categorization and matching
- Use case: Vocabulary, categorization, labeling
- Engagement: ★★★★☆

### Also Useful

- **Accordion** - Expandable text sections
- **Dialog Cards** - Flashcards with flip animation
- **Fill in the Blanks** - Cloze tests
- **Mark the Words** - Text highlighting exercises
- **Memory Game** - Card matching
- **Multiple Choice** - Single question quizzes
- **Summary** - End-of-content summaries with statements

## WordPress Integration

### Requirements
- WordPress 5.0+
- H5P plugin installed and activated
- Sufficient upload size limit (typically 64MB+)

### Manual Upload Process
```
1. Go to WordPress Admin → Media → Add New
2. Upload .h5p file
3. Copy Media ID or URL
4. In post/page, add shortcode: [h5p id="123"]
   OR use Gutenberg H5P block
```

### MCP Automation Process
```
Prerequisites:
- MCP Server with wp_upload_h5p_from_url tool
- .h5p file accessible via URL (Nextcloud, GitHub, etc.)

Process:
1. Use MCP tool: wp_upload_h5p_from_url
   Input: fileUrl, title (optional)
   Output: Media ID

2. Use MCP tool: wp_create_post or wp_update_post
   Include H5P shortcode with returned Media ID
```

## Workflow Patterns

### Pattern 1: Simple Content Creation

**Context:** Single H5P element for a blog post or lesson

**Steps:**
1. Create H5P content on H5P.com or H5P.org
2. Export as .h5p
3. Upload to WordPress
4. Embed in post

**Time:** ~10-15 minutes

### Pattern 2: Course Module with Multiple H5P Elements

**Context:** Complete lesson with multiple interactive elements

**Steps:**
1. Plan content structure
2. Create multiple H5P elements:
   - Opening video (Interactive Video)
   - Mid-lesson quiz (Question Set)
   - Summary (Course Presentation)
3. Upload all to WordPress
4. Create structured post with all elements
5. Add navigation between elements

**Time:** ~30-60 minutes

### Pattern 3: Automated Publishing (with MCP)

**Context:** Regular content updates, batch publishing

**Steps:**
1. Create H5P content
2. Store in cloud (Nextcloud, Dropbox) with public link
3. Create article content
4. Use MCP to:
   - Upload H5P automatically
   - Create WordPress post
   - Embed H5P with ID
5. Review and publish

**Time:** ~5-10 minutes (mostly content creation)

### Pattern 4: Reusable Content Library

**Context:** Building a library of reusable H5P modules

**Steps:**
1. Create H5P modules by topic/type
2. Upload all to WordPress Media Library
3. Document Media IDs in spreadsheet/notes
4. Reuse via shortcode in multiple posts
5. Update once, affects all instances

**Time:** Initial setup ~2-3 hours, then instant reuse

## Best Practices

### Content Creation
- Start simple, add complexity gradually
- Test on target device types (mobile, tablet, desktop)
- Include clear instructions within H5P content
- Provide feedback for all answer types
- Use multimedia strategically (not for decoration)

### WordPress Integration
- Use descriptive titles when uploading H5P files
- Add H5P content early in post (don't bury it)
- Provide context before and after H5P element
- Test all interactions after publishing
- Check mobile responsiveness

### Performance
- Keep H5P files under 50MB when possible
- Optimize images/videos before including in H5P
- Use H5P's built-in compression options
- Cache H5P content when possible
- Consider CDN for high-traffic sites

### Pedagogy
- One learning objective per H5P element
- Immediate feedback is more engaging
- Allow multiple attempts for formative assessment
- Provide hints for complex questions
- Track analytics if assessment is critical

## Common Issues & Solutions

### Issue: H5P upload fails
**Solutions:**
- Check file size limit: WordPress Settings → Media
- Increase PHP upload_max_filesize and post_max_size
- Verify .h5p file isn't corrupted (re-export)

### Issue: H5P content doesn't display
**Solutions:**
- Clear browser cache
- Check if H5P plugin is activated
- Verify shortcode syntax: [h5p id="123"]
- Check console for JavaScript errors

### Issue: Interactive elements don't work
**Solutions:**
- Check for JavaScript conflicts with theme/plugins
- Disable other plugins temporarily to isolate
- Update H5P plugin to latest version
- Test in different browser

### Issue: Content looks different than in H5P editor
**Solutions:**
- Check WordPress theme CSS conflicts
- Use H5P's preview mode before exporting
- Test on actual site before publishing
- Adjust H5P styling if needed

## MCP Integration Details

### Tool: wp_upload_h5p_from_url
```javascript
Input:
{
  fileUrl: "https://example.com/content.h5p",
  title: "Interactive Quiz - Chapter 1"  // optional
}

Output:
{
  id: 123,
  source_url: "https://yoursite.com/wp-content/uploads/h5p/content.h5p",
  mime_type: "application/zip"
}
```

### Tool: wp_create_post (with H5P)
```javascript
Input:
{
  title: "Lesson: Introduction to Photosynthesis",
  content: "<p>Watch this interactive video...</p>",
  h5pId: "123",  // Appends [h5p id="123"] automatically
  status: "draft"
}

Output:
{
  id: 456,
  link: "https://yoursite.com/lesson-photosynthesis",
  status: "draft"
}
```

## Reference Files

For detailed information, see:
- `references/h5p-content-types.md` - Complete list of H5P content types with examples
- `references/mcp-automation-examples.md` - Full MCP workflow examples with code

## Next Steps

After creating H5P content:
1. Consider analytics: H5P can track user interactions
2. Gather feedback: Ask learners what works
3. Iterate: Improve based on usage data
4. Share: H5P content can be shared across sites
5. Scale: Use MCP automation for regular content

## Real-World Example

**Teacher's Workflow (Dirk's Setup):**
1. Creates H5P Interactive Video in H5P.com
2. Exports as .h5p file
3. Stores in Nextcloud with share link
4. Opens Claude Desktop
5. Says: "Create a blog post about [topic], upload this H5P: [link], and embed it"
6. Claude uses MCP to:
   - Upload H5P to WordPress
   - Generate article content
   - Embed H5P with correct ID
   - Create draft post
7. Teacher reviews, adjusts, publishes
8. Total time: ~10 minutes

**Before automation:** 30-45 minutes (manual upload, formatting, embedding)
**After automation:** ~10 minutes (mostly content review)

---

*This skill is based on real-world usage by educators using H5P daily in classroom settings.*
