---
name: moodle-course-workflow
description: Complete workflow for creating Moodle courses with H5P content integration from WordPress. Use when creating educational courses, adding interactive H5P modules to Moodle, or automating course deployment.
license: MIT
---

# Moodle Course Creation Workflow

Complete workflow for creating Moodle courses with sections, activities, and H5P content integration from WordPress.

## When to Use This Skill

Use this skill when:
- Creating new Moodle courses programmatically
- Adding H5P interactive content from WordPress to Moodle
- Building structured learning modules with multiple sections
- Automating course deployment workflows
- Setting up courses based on course templates/concepts

## Prerequisites

### Required MCP Servers
1. **moodle-mcp** - Moodle course management
   - Tools: `moodle_create_course`, `moodle_create_section`, `moodle_create_url`, `moodle_create_page`, `moodle_create_label`

2. **wp-mcp** - WordPress/H5P management (for H5P integration)
   - Tools: `wp_import_h5p`, `wp_list_h5p_contents`, `wp_create_post`

### Required Moodle Plugins
- `local_wsmanagesections` - For section management
- `local_sync_service` or `local_course` - For module creation via API

### WordPress Setup
- H5P Plugin installed and active
- h5p-rest-import Plugin for REST API imports

## Quick Start

### Basic Course Creation

```
1. Create course: moodle_create_course
   - fullname, shortname, categoryid, numsections

2. Add sections: moodle_create_section (repeat for each module)
   - courseId, position, name, summary

3. Add content: moodle_create_url / moodle_create_page / moodle_create_label
   - courseId, sectionNum, name/content
```

### Course with H5P Integration

```
1. Import H5P to WordPress: wp_import_h5p
   - Get H5P ID

2. Create Moodle course and sections

3. Embed H5P in Moodle section:
   - Option A: moodle_create_url (link to WordPress H5P)
   - Option B: moodle_create_page with iframe embed
```

## H5P Integration Methods

### Method 1: URL Resource (Simple)

Add H5P as clickable link in Moodle:

```javascript
moodle_create_url({
  courseId: 123,
  sectionNum: 1,
  name: "Interactive Quiz",
  url: "https://your-wordpress.com/?p=POST_ID_WITH_H5P"
})
```

**Pros:** Simple, opens in new tab
**Cons:** Leaves Moodle context

### Method 2: Page with iFrame (Embedded)

Embed H5P directly in Moodle page:

```javascript
moodle_create_page({
  courseId: 123,
  sectionNum: 1,
  pageName: "Interactive Quiz",
  content: `
    <p>Complete the following interactive quiz:</p>
    <iframe
      src="https://your-wordpress.com/wp-admin/admin-ajax.php?action=h5p_embed&id=H5P_ID"
      width="100%"
      height="600"
      frameborder="0"
      allowfullscreen>
    </iframe>
  `
})
```

**Pros:** Stays in Moodle, seamless experience
**Cons:** Requires iframe permissions

### Method 3: Label with Embed (Inline)

Add H5P inline within a section:

```javascript
moodle_create_label({
  courseId: 123,
  sectionNum: 1,
  labelText: `
    <h4>Practice Exercise</h4>
    <iframe
      src="https://your-wordpress.com/wp-admin/admin-ajax.php?action=h5p_embed&id=H5P_ID"
      width="100%"
      height="500"
      frameborder="0">
    </iframe>
  `
})
```

**Pros:** No extra click needed, inline content
**Cons:** May clutter section view

## H5P Embed URL Format

WordPress H5P can be embedded via:

```
https://YOUR-WORDPRESS-URL/wp-admin/admin-ajax.php?action=h5p_embed&id=H5P_ID
```

Example:
```
https://www.dirk-schulenburg.net/wp-admin/admin-ajax.php?action=h5p_embed&id=12
```

## Complete Course Creation Workflow

### Step 1: Prepare Content

1. **Define course structure** (modules, sections)
2. **Create/import H5P content** to WordPress
3. **Document H5P IDs** for embedding

### Step 2: Create Moodle Course

```javascript
// 1. Create course
const course = await moodle_create_course({
  fullname: "Introduction to Cannabis Cultivation",
  shortname: "CANNABIS-101",
  categoryid: 1,
  summary: "Comprehensive course on professional cannabis cultivation",
  format: "topics",
  numsections: 12
});

// 2. Rename sections
await moodle_update_section({
  courseId: course.id,
  sectionNum: 1,
  name: "Module 1: Legal Framework",
  summary: "Understanding compliance and regulations"
});

// 3. Add H5P content as page
await moodle_create_page({
  courseId: course.id,
  sectionNum: 1,
  pageName: "Compliance Quiz",
  content: `
    <p>Test your knowledge of legal requirements:</p>
    <iframe src="https://your-wp.com/wp-admin/admin-ajax.php?action=h5p_embed&id=12"
            width="100%" height="600" frameborder="0" allowfullscreen></iframe>
  `
});

// 4. Add supporting materials
await moodle_create_url({
  courseId: course.id,
  sectionNum: 1,
  name: "Official Guidelines PDF",
  url: "https://example.com/guidelines.pdf"
});
```

### Step 3: Verify and Publish

1. Preview course in Moodle
2. Test H5P embeds
3. Set course visibility to public

## Workflow Patterns

### Pattern 1: Quick Module

**Use case:** Single H5P exercise in existing course

```
1. wp_list_h5p_contents → Find H5P ID
2. moodle_create_page → Embed in section
```

### Pattern 2: Full Course Build

**Use case:** Complete course from template

```
1. moodle_create_course → New course
2. Loop: moodle_create_section → Add modules
3. Loop: moodle_create_page/url/label → Add content
4. moodle_enrol_user → Add instructors
```

### Pattern 3: H5P First

**Use case:** Start with interactive content

```
1. wp_import_h5p → Import H5P from URL
2. moodle_create_course → New course
3. moodle_create_page → Embed H5P
```

## Best Practices

### Course Structure
- Keep section names concise (max 50 chars)
- Use consistent naming: "Module X: Topic"
- Include section summaries for navigation

### H5P Integration
- Test embed URLs before deployment
- Set appropriate iframe heights (400-800px)
- Include fallback text for accessibility

### Performance
- Don't embed too many H5Ps per page (max 2-3)
- Use URL links for large H5P content
- Consider load times on mobile

## Example: Cannabis Cultivation Course

Based on the Moodle-Grower-Kurs concept:

```
Course: "Professional Cannabis Cultivation (CEA)"
├── Module 1: Legal Framework & Compliance
│   ├── Label: Introduction text
│   ├── Page: Compliance Quiz [H5P ID: 15]
│   └── URL: Official Guidelines PDF
├── Module 2: Botany & Physiology
│   ├── Page: Development Stages [H5P Interactive Book]
│   └── Label: Glossary
├── Module 3: Light Technology
│   ├── Page: DLI Calculator [H5P]
│   └── URL: LED vs HPS Comparison
...
└── Module 12: SOPs & Audit Readiness
    ├── Page: SOP Template
    └── Assignment: Create your own SOP
```

## Troubleshooting

### Issue: H5P not displaying in Moodle

**Solutions:**
- Check iframe permissions in Moodle security settings
- Verify H5P embed URL is accessible (test in browser)
- Ensure WordPress has proper CORS headers

### Issue: Section creation fails

**Solutions:**
- Verify `local_wsmanagesections` plugin is installed
- Check API token permissions
- Use `moodle_get_site_info` to verify available functions

### Issue: Course not visible

**Solutions:**
- Set `visible: 1` when creating course
- Check category visibility
- Verify user has course view permissions

## API Reference

### WordPress H5P Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/wp-json/h5p-import/v1/import` | POST | Import H5P file |
| `/wp-json/h5p-import/v1/list` | GET | List H5P contents |
| `/wp-json/h5p-import/v1/status` | GET | Plugin status |

### Moodle Tools (via moodle-mcp)

| Tool | Description |
|------|-------------|
| `moodle_create_course` | Create new course |
| `moodle_create_section` | Add section to course |
| `moodle_update_section` | Rename/modify section |
| `moodle_create_url` | Add URL resource |
| `moodle_create_page` | Add page with content |
| `moodle_create_label` | Add inline text/HTML |
| `moodle_get_course_contents` | View course structure |

## Reference Files

- `references/course-templates.md` - Example course structures
- `references/h5p-embed-examples.md` - H5P embedding patterns

---

## Logging

Bei Ausführung dieses Skills wird automatisch geloggt:

| Feld | Wert |
|------|------|
| **Agent** | education |
| **Action** | moodle:create_course |
| **Context** | course_name, course_id, section_count, h5p_count |
| **Result** | success/failure |

**Beispiel-Log:**
```json
{
  "agent": "education",
  "action": "moodle:create_course",
  "context": "{\"course_name\": \"Cannabis Cultivation CEA\", \"course_id\": 15, \"section_count\": 12, \"h5p_count\": 5}",
  "result": "success"
}
```

---

*This skill combines moodle-mcp and wp-mcp for seamless course creation with interactive content.*
