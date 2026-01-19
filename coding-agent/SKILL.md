---
name: coding-agent
description: Specialized coding agent with Context7 integration for documentation-aware code generation. Creates, refactors, and extends MCP servers and Node.js/Python projects with up-to-date library documentation.
license: MIT
agent: DevOps
version: "1.0"
---

# Coding Agent

Specialized sub-agent for the DevOps Agent that handles code creation, refactoring, and extension with intelligent documentation lookup via Context7.

## When to Use This Skill

Use this skill when:
- Creating new MCP server tools or endpoints
- Implementing new features in existing projects
- Refactoring code with modern best practices
- Integrating new libraries (npm/pip packages)
- Writing code that needs up-to-date API documentation

## Core Capabilities

### 1. Context7 Documentation Lookup

Before writing code that uses external libraries, ALWAYS look up current documentation:

```
# Step 1: Resolve library ID
Use: resolve-library-id with libraryName

# Step 2: Fetch documentation
Use: get-library-docs with context7CompatibleLibraryID and topic
```

### Common Libraries for MCP Development

| Library | Context7 ID | Common Topics |
|---------|-------------|---------------|
| Express | `/expressjs/express` | routing, middleware, error handling |
| Node.js | `/nodejs/node` | fs, http, streams |
| Zod | `/colinhacks/zod` | schemas, validation |
| MCP SDK | `/anthropics/mcp-typescript` | tools, resources, prompts |
| Playwright | `/microsoft/playwright` | selectors, actions, assertions |
| IMAP | `/mscdex/node-imap` | connection, fetch, search |

## Workflow: New MCP Tool

### Phase 1: Requirements Analysis

```markdown
## Tool Specification

**Name:** moodle_create_quiz
**Purpose:** Create a quiz in a Moodle course section
**Parameters:**
  - courseId (required): Moodle course ID
  - sectionNum (required): Section number
  - quizName (required): Name of the quiz
  - intro (optional): Quiz description
  - timeLimit (optional): Time limit in seconds

**Returns:** Quiz ID and URL

**Moodle API:** mod_quiz_add_instance (requires local_sync_service plugin)
```

### Phase 2: Documentation Lookup

```javascript
// 1. Check MCP SDK patterns
get-library-docs("/anthropics/mcp-typescript", topic="tools")

// 2. Check validation library
get-library-docs("/colinhacks/zod", topic="object schemas")

// 3. Check HTTP client if needed
get-library-docs("/axios/axios", topic="post requests")
```

### Phase 3: Implementation

```javascript
// src/tools/moodle_create_quiz.mjs
import { z } from 'zod';

// Schema with Zod (validated patterns from Context7)
const CreateQuizSchema = z.object({
  courseId: z.string().min(1),
  sectionNum: z.string().min(1),
  quizName: z.string().min(1),
  intro: z.string().optional(),
  timeLimit: z.string().optional(),
});

export async function moodle_create_quiz(params, config) {
  const validated = CreateQuizSchema.parse(params);

  const response = await fetch(`${config.MOODLE_URL}/webservice/rest/server.php`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      wstoken: config.MOODLE_TOKEN,
      wsfunction: 'local_sync_service_create_quiz',
      moodlewsrestformat: 'json',
      courseid: validated.courseId,
      sectionnum: validated.sectionNum,
      name: validated.quizName,
      intro: validated.intro || '',
      timelimit: validated.timeLimit || '0',
    }),
  });

  const data = await response.json();

  if (data.exception) {
    throw new Error(`Moodle API Error: ${data.message}`);
  }

  return {
    success: true,
    quizId: data.quizid,
    url: `${config.MOODLE_URL}/mod/quiz/view.php?id=${data.cmid}`,
  };
}
```

### Phase 4: Tool Registration

```javascript
// In server.mjs - register the tool
server.tool(
  'moodle_create_quiz',
  'Create a quiz in a Moodle course section',
  {
    courseId: { type: 'string', description: 'Moodle course ID' },
    sectionNum: { type: 'string', description: 'Section number (0-based)' },
    quizName: { type: 'string', description: 'Name of the quiz' },
    intro: { type: 'string', description: 'Quiz description (optional)' },
    timeLimit: { type: 'string', description: 'Time limit in seconds (optional)' },
  },
  async (params) => {
    return await moodle_create_quiz(params, config);
  }
);
```

## Code Quality Standards

### 1. Error Handling

```javascript
// Always wrap external calls
try {
  const result = await externalApi.call(params);
  return { success: true, data: result };
} catch (error) {
  console.error(`[${toolName}] Error:`, error.message);
  return {
    success: false,
    error: error.message,
    code: error.code || 'UNKNOWN_ERROR'
  };
}
```

### 2. Input Validation

```javascript
// Use Zod for all inputs
const schema = z.object({
  required: z.string().min(1),
  optional: z.string().optional().default('default'),
  numeric: z.coerce.number().positive(),
});
```

### 3. Logging

```javascript
// Structured logging
console.log(`[${new Date().toISOString()}] [${toolName}] ${message}`);
```

### 4. TypeScript-like JSDoc

```javascript
/**
 * Creates a quiz in Moodle
 * @param {Object} params - Tool parameters
 * @param {string} params.courseId - Course ID
 * @param {string} params.quizName - Quiz name
 * @param {Object} config - Server configuration
 * @returns {Promise<{success: boolean, quizId?: string, error?: string}>}
 */
```

## Refactoring Patterns

### Extract Common Logic

```javascript
// Before: Duplicated API calls
// After: Shared utility
// utils/moodle-api.mjs
export async function callMoodleApi(wsfunction, params, config) {
  const response = await fetch(`${config.MOODLE_URL}/webservice/rest/server.php`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      wstoken: config.MOODLE_TOKEN,
      wsfunction,
      moodlewsrestformat: 'json',
      ...params,
    }),
  });

  const data = await response.json();
  if (data.exception) throw new Error(data.message);
  return data;
}
```

### Modernize Async Patterns

```javascript
// Before: Callbacks
// After: async/await with Promise.all for parallel operations
const [courses, users] = await Promise.all([
  fetchCourses(),
  fetchUsers(),
]);
```

## Integration with DevOps Agent

### Handoff to Debug Agent

```markdown
## Agent-Handoff

**From:** Coding Agent
**To:** Debug Agent
**Context:** New tool implemented, needs browser testing
**Artifacts:**
  - Tool: moodle_create_quiz
  - Test URL: https://moodle.dirk-schulenburg.net
**Task:** Verify quiz creation via UI
```

### Handoff to Documentation Agent

```markdown
## Agent-Handoff

**From:** Coding Agent
**To:** Documentation Agent
**Context:** New tool ready for documentation
**Artifacts:**
  - Tool: moodle_create_quiz
  - Source: mcp-servers/moodle-mcp/src/tools/moodle_create_quiz.mjs
**Task:** Generate MCP tool documentation
```

## Quick Reference

### Context7 Lookup Template

```
1. resolve-library-id: "{library-name}"
2. get-library-docs: ID from step 1, topic: "{specific-topic}"
3. Apply patterns to implementation
```

### File Structure for New Tool

```
mcp-servers/{server}/
├── src/
│   ├── server.mjs          # Add tool registration
│   ├── tools/
│   │   └── {tool_name}.mjs # Tool implementation
│   └── utils/
│       └── {api}.mjs       # Shared utilities
└── tests/
    └── {tool_name}.test.mjs # Unit tests
```

### Commit Message

```
feat({server}): add {tool_name} tool

- Implements {brief description}
- Uses {library} for {purpose}
- Closes #{issue} (if applicable)
```

---

*DevOps Sub-Agent - Coding Agent v1.0*
