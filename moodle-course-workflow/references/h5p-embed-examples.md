# H5P Embedding Examples

Code snippets for embedding H5P content from WordPress into Moodle.

## WordPress H5P Embed URL

The standard H5P embed URL format:

```
https://YOUR-WORDPRESS-URL/wp-admin/admin-ajax.php?action=h5p_embed&id=H5P_ID
```

Example:
```
https://www.dirk-schulenburg.net/wp-admin/admin-ajax.php?action=h5p_embed&id=12
```

## Basic iframe Embed

Minimal iframe for Moodle pages:

```html
<iframe
  src="https://www.dirk-schulenburg.net/wp-admin/admin-ajax.php?action=h5p_embed&id=12"
  width="100%"
  height="600"
  frameborder="0"
  allowfullscreen>
</iframe>
```

## Responsive iframe Embed

Better for mobile devices:

```html
<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden;">
  <iframe
    src="https://www.dirk-schulenburg.net/wp-admin/admin-ajax.php?action=h5p_embed&id=12"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
    frameborder="0"
    allowfullscreen>
  </iframe>
</div>
```

## Styled Embed with Context

Full embed with title and description:

```html
<div style="border: 1px solid #ddd; border-radius: 8px; padding: 16px; margin: 16px 0;">
  <h4 style="margin-top: 0;">Interactive Quiz: Compliance Check</h4>
  <p style="color: #666;">Test your knowledge of legal requirements. You need 80% to pass.</p>
  <iframe
    src="https://www.dirk-schulenburg.net/wp-admin/admin-ajax.php?action=h5p_embed&id=12"
    width="100%"
    height="500"
    frameborder="0"
    allowfullscreen
    style="border: none; border-radius: 4px;">
  </iframe>
  <p style="font-size: 12px; color: #999; margin-bottom: 0;">
    Content provided by H5P Interactive Content
  </p>
</div>
```

## H5P Content Type Specific Heights

Recommended iframe heights by content type:

| H5P Type | Height | Notes |
|----------|--------|-------|
| QuestionSet | 500-600px | Depends on question complexity |
| InteractiveVideo | 400-500px | 16:9 aspect ratio |
| CoursePresentation | 600-700px | Slides need space |
| InteractiveBook | 700-800px | Multi-page content |
| DragQuestion | 400-500px | Depends on drop zone layout |
| FillInTheBlanks | 300-400px | Usually shorter |
| Timeline | 500-600px | Horizontal scroll needs height |
| ImageHotspots | 400-500px | Depends on image size |

## Moodle Page Examples

### Example 1: Quiz Page

```javascript
await moodle_create_page({
  courseId: 123,
  sectionNum: 1,
  pageName: "Module 1 Quiz: Legal Basics",
  content: `
    <h3>Knowledge Check</h3>
    <p>Complete this quiz to verify your understanding of the legal framework.</p>
    <p><strong>Requirements:</strong> Score at least 80% to proceed to the next module.</p>

    <iframe
      src="https://www.dirk-schulenburg.net/wp-admin/admin-ajax.php?action=h5p_embed&id=15"
      width="100%"
      height="550"
      frameborder="0"
      allowfullscreen>
    </iframe>

    <p style="margin-top: 16px;">
      <em>If you don't pass, review the materials and try again.</em>
    </p>
  `
});
```

### Example 2: Interactive Lesson

```javascript
await moodle_create_page({
  courseId: 123,
  sectionNum: 2,
  pageName: "Plant Development Stages",
  content: `
    <h3>Understanding Growth Phases</h3>
    <p>Explore the different stages of plant development in this interactive presentation.</p>

    <iframe
      src="https://www.dirk-schulenburg.net/wp-admin/admin-ajax.php?action=h5p_embed&id=16"
      width="100%"
      height="650"
      frameborder="0"
      allowfullscreen>
    </iframe>

    <h4>Key Takeaways</h4>
    <ul>
      <li>Seedling stage: 1-2 weeks</li>
      <li>Vegetative stage: 3-8 weeks</li>
      <li>Flowering stage: 6-12 weeks</li>
    </ul>
  `
});
```

### Example 3: Practice Exercise

```javascript
await moodle_create_page({
  courseId: 123,
  sectionNum: 3,
  pageName: "VPD Calculator Practice",
  content: `
    <h3>Calculate Vapor Pressure Deficit</h3>
    <p>Use this interactive tool to practice VPD calculations for optimal growing conditions.</p>

    <iframe
      src="https://www.dirk-schulenburg.net/wp-admin/admin-ajax.php?action=h5p_embed&id=17"
      width="100%"
      height="450"
      frameborder="0"
      allowfullscreen>
    </iframe>

    <div style="background: #f5f5f5; padding: 12px; border-radius: 4px; margin-top: 16px;">
      <strong>Tip:</strong> Optimal VPD ranges between 0.8-1.2 kPa for vegetative growth.
    </div>
  `
});
```

## Moodle Label Examples

### Example 1: Inline Quiz

```javascript
await moodle_create_label({
  courseId: 123,
  sectionNum: 1,
  labelText: `
    <div style="background: #e8f4fd; padding: 16px; border-radius: 8px; margin: 8px 0;">
      <h4 style="margin-top: 0;">Quick Check</h4>
      <iframe
        src="https://www.dirk-schulenburg.net/wp-admin/admin-ajax.php?action=h5p_embed&id=18"
        width="100%"
        height="350"
        frameborder="0">
      </iframe>
    </div>
  `
});
```

### Example 2: Section Introduction with H5P

```javascript
await moodle_create_label({
  courseId: 123,
  sectionNum: 2,
  labelText: `
    <div style="border-left: 4px solid #4CAF50; padding-left: 16px;">
      <h3>Welcome to Module 2</h3>
      <p>In this module, you'll learn about plant physiology.</p>
      <p>Start with this interactive overview:</p>
      <iframe
        src="https://www.dirk-schulenburg.net/wp-admin/admin-ajax.php?action=h5p_embed&id=19"
        width="100%"
        height="400"
        frameborder="0"
        allowfullscreen>
      </iframe>
    </div>
  `
});
```

## URL Resource Examples

When iframe embedding isn't possible or desired:

```javascript
// Link to WordPress post with H5P
await moodle_create_url({
  courseId: 123,
  sectionNum: 1,
  name: "Interactive Quiz (opens in new window)",
  url: "https://www.dirk-schulenburg.net/?p=147"
});

// Direct H5P embed page (if available)
await moodle_create_url({
  courseId: 123,
  sectionNum: 1,
  name: "Practice Exercise",
  url: "https://www.dirk-schulenburg.net/h5p-content/compliance-quiz/"
});
```

## Troubleshooting Embeds

### Problem: iframe blocked

**Cause:** X-Frame-Options or CSP headers blocking embed

**Solution:** Add to WordPress .htaccess or nginx config:
```
Header always unset X-Frame-Options
```

Or configure CSP to allow Moodle domain.

### Problem: H5P not loading

**Cause:** Mixed content (HTTPS/HTTP mismatch)

**Solution:** Ensure both Moodle and WordPress use HTTPS.

### Problem: iframe too small/large

**Solution:** Adjust height value or use responsive wrapper.

### Problem: H5P buttons cut off

**Solution:** Increase iframe height by 50-100px.

## Multiple H5P on One Page

When embedding multiple H5P elements:

```html
<h3>Learning Activities</h3>

<h4>Activity 1: Video Lesson</h4>
<iframe src="...&id=20" width="100%" height="400" frameborder="0"></iframe>

<hr style="margin: 24px 0;">

<h4>Activity 2: Practice Quiz</h4>
<iframe src="...&id=21" width="100%" height="450" frameborder="0"></iframe>

<hr style="margin: 24px 0;">

<h4>Activity 3: Summary</h4>
<iframe src="...&id=22" width="100%" height="300" frameborder="0"></iframe>
```

**Note:** Limit to 2-3 H5P elements per page for performance.

---

*Always test embeds in the actual Moodle environment before deploying to students.*
