---
name: debug-agent
description: Specialized debugging agent with Playwright browser automation for end-to-end testing, visual verification, and interactive debugging of web applications and MCP tools.
license: MIT
---

# Debug Agent

Specialized sub-agent for the DevOps Agent that handles browser-based debugging, end-to-end testing, and visual verification using Playwright.

## When to Use This Skill

Use this skill when:
- Testing MCP tools that interact with web UIs (Moodle, WordPress, n8n)
- Debugging visual issues in web applications
- Verifying that API calls produce correct UI results
- Creating automated test scenarios
- Capturing evidence of bugs or successful fixes

## Core Capabilities

### 1. Playwright Browser Automation

Use the MCP browser tools (Playwright-based) for all browser interactions:

```javascript
// Available tools via MCP
browser_navigate     // Go to URL
browser_snapshot     // Get accessibility tree (preferred)
browser_click        // Click elements
browser_type         // Type text
browser_fill_form    // Fill multiple fields
browser_take_screenshot  // Visual capture
browser_wait_for     // Wait for text/conditions
browser_console_messages // Check for JS errors
browser_network_requests // Monitor API calls
```

## Workflow: Debug MCP Tool via UI

### Phase 1: Setup Test Environment

```markdown
## Debug Session Setup

**Tool Under Test:** moodle_create_quiz
**Target URL:** https://moodle.dirk-schulenburg.net
**Test Course:** LF4 Weinhandlung (ID: 8)
**Expected Outcome:** Quiz visible in section 1
```

### Phase 2: Manual Verification via Browser

```javascript
// 1. Navigate to Moodle course
browser_navigate({ url: "https://moodle.dirk-schulenburg.net/course/view.php?id=8" })

// 2. Get page structure
browser_snapshot()

// 3. Find the quiz element
browser_find({ query: "quiz", tabId: currentTab })

// 4. Take screenshot as evidence
browser_take_screenshot({ filename: "quiz-created.png" })
```

### Phase 3: Check for Errors

```javascript
// Check browser console for JS errors
browser_console_messages({ onlyErrors: true })

// Check network requests for failed API calls
browser_network_requests({ urlPattern: "webservice" })
```

## Debugging Scenarios

### Scenario 1: MCP Tool Returns Success but UI Shows Nothing

```markdown
## Debug Steps

1. **Verify API Response**
   - Check MCP tool response for IDs
   - Note: quizId, cmid values

2. **Check Direct URL**
   browser_navigate({ url: "https://moodle.dirk-schulenburg.net/mod/quiz/view.php?id={cmid}" })
   - If works: Quiz exists but not visible in course
   - If 404: Quiz creation failed silently

3. **Check Course Edit Mode**
   - Some items only visible in edit mode
   browser_click({ ref: "edit-mode-toggle" })
   browser_snapshot()

4. **Check User Permissions**
   - API user might see different than admin
   - Login as test user and verify
```

### Scenario 2: Visual Layout Bug

```markdown
## Debug Steps

1. **Take Full Page Screenshot**
   browser_take_screenshot({ fullPage: true, filename: "layout-bug.png" })

2. **Inspect Element**
   browser_snapshot({ ref_id: "problematic-element" })

3. **Check Responsive Behavior**
   browser_resize({ width: 768, height: 1024 })
   browser_take_screenshot({ filename: "tablet-view.png" })

4. **Check CSS Console Errors**
   browser_console_messages({ pattern: "CSS" })
```

### Scenario 3: Form Submission Failure

```markdown
## Debug Steps

1. **Fill Form Step by Step**
   browser_fill_form({
     fields: [
       { name: "Quiz Name", type: "textbox", ref: "input-name", value: "Test Quiz" },
       { name: "Time Limit", type: "textbox", ref: "input-time", value: "60" }
     ]
   })

2. **Monitor Network on Submit**
   browser_network_requests()  // Clear first

3. **Click Submit**
   browser_click({ ref: "submit-button" })
   browser_wait_for({ time: 3 })

4. **Check Network Response**
   browser_network_requests({ urlPattern: "quiz" })

5. **Check for Error Messages**
   browser_snapshot()
   browser_find({ query: "error" })
```

## Testing MCP Servers

### WordPress MCP Testing

```javascript
// Test wp_create_post via UI verification
// 1. Call MCP tool (via Claude)
// Result: { postId: 123, url: "https://..." }

// 2. Verify in browser
browser_navigate({ url: "https://www.dirk-schulenburg.net/wp-admin/post.php?post=123&action=edit" })
browser_snapshot()

// 3. Check frontend
browser_navigate({ url: "https://www.dirk-schulenburg.net/?p=123" })
browser_take_screenshot({ filename: "new-post-frontend.png" })
```

### Moodle MCP Testing

```javascript
// Test moodle_create_section via UI verification
// 1. Call MCP tool
// Result: { sectionId: 5 }

// 2. Navigate to course
browser_navigate({ url: "https://moodle.dirk-schulenburg.net/course/view.php?id=8" })

// 3. Verify section exists
browser_find({ query: "Section 5" })
browser_snapshot()

// 4. Check section content
browser_click({ ref: "section-5-toggle" })
browser_take_screenshot({ filename: "section-5-content.png" })
```

### n8n Workflow Testing

```javascript
// Test workflow execution via UI
// 1. Navigate to n8n
browser_navigate({ url: "https://n8n.dirk-schulenburg.net" })

// 2. Find workflow
browser_find({ query: "Email Router" })
browser_click({ ref: "workflow-email-router" })

// 3. Check execution history
browser_click({ ref: "executions-tab" })
browser_snapshot()

// 4. Check for errors
browser_find({ query: "error" })
browser_take_screenshot({ filename: "n8n-execution-log.png" })
```

## Error Documentation

### Screenshot Naming Convention

```
{date}_{tool}_{status}.png

Examples:
2026-01-19_moodle_create_quiz_success.png
2026-01-19_moodle_create_quiz_error_404.png
2026-01-19_wp_create_post_validation_error.png
```

### Bug Report Template

```markdown
## Bug Report

**Date:** 2026-01-19
**Tool:** moodle_create_quiz
**Severity:** High

### Steps to Reproduce
1. Call moodle_create_quiz with courseId=8, sectionNum=1, quizName="Test"
2. Tool returns success with quizId=15
3. Navigate to course view

### Expected Result
Quiz "Test" visible in section 1

### Actual Result
Quiz not visible. Direct URL returns 404.

### Evidence
- Screenshot: debug-session/moodle_create_quiz_error_404.png
- Console: No JS errors
- Network: POST to webservice returned 200 but response contains "exception"

### API Response
{
  "exception": "webservice_access_exception",
  "message": "Access denied"
}

### Root Cause
Missing capability: moodle/quiz:addinstance for webservice user
```

## Integration with Other Agents

### Handoff from Coding Agent

```markdown
## Agent-Handoff

**From:** Coding Agent
**To:** Debug Agent
**Context:** New tool implemented
**Artifacts:**
  - Tool: moodle_create_quiz
  - Expected: Quiz in course section
**Task:** Verify via UI
```

### Handoff to Documentation Agent

```markdown
## Agent-Handoff

**From:** Debug Agent
**To:** Documentation Agent
**Context:** Testing complete with screenshots
**Artifacts:**
  - Screenshots: debug-session/*.png
  - Test results: PASS/FAIL
**Task:** Document test results and usage examples
```

## Quick Reference

### Common Selectors for Target Sites

#### Moodle
```javascript
// Login
ref: "username-input", "password-input", "login-button"

// Course view
ref: "edit-mode-toggle", "section-{n}", "add-activity"

// Quiz
ref: "quiz-name-input", "quiz-submit", "quiz-question-{n}"
```

#### WordPress Admin
```javascript
// Login
ref: "user-login", "user-pass", "wp-submit"

// Post editor
ref: "post-title-input", "content-editor", "publish-button"

// Media library
ref: "upload-button", "media-library-grid"
```

#### n8n
```javascript
// Workflow list
ref: "workflow-{name}", "new-workflow-button"

// Execution
ref: "execute-workflow", "executions-tab", "execution-{id}"
```

### Debug Checklist

```markdown
- [ ] Browser console checked for errors
- [ ] Network requests inspected
- [ ] Element exists in DOM (snapshot)
- [ ] Element visible (screenshot)
- [ ] Form validation passed
- [ ] API response correct
- [ ] UI reflects API state
- [ ] Permissions verified
- [ ] Screenshots saved
- [ ] Bug report created (if issue found)
```

---

## Logging

Bei Ausführung dieses Skills wird automatisch geloggt:

| Feld | Wert |
|------|------|
| **Agent** | devops |
| **Action** | debug:test |
| **Context** | tool_under_test, target_url, screenshots_taken, issues_found |
| **Result** | success/failure |

**Beispiel-Log:**
```json
{
  "agent": "devops",
  "action": "debug:test",
  "context": "{\"tool_under_test\": \"moodle_create_quiz\", \"target_url\": \"moodle.dirk-schulenburg.net\", \"screenshots_taken\": 3, \"issues_found\": 1}",
  "result": "success"
}
```

---

*DevOps Sub-Agent - Debug Agent v1.0*
