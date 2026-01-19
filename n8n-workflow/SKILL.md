---
name: n8n-workflow
description: Create, debug, and manage n8n workflows. Use for building automations, analyzing workflow executions, fixing errors, and optimizing performance.
license: MIT
agent: DevOps
---

# n8n Workflow Management

Complete workflow for creating, debugging, and managing n8n automations.

## When to Use This Skill

Use this skill when:
- Creating new n8n workflows
- Debugging failed workflow executions
- Analyzing workflow performance
- Migrating or copying workflows
- Building integrations between services

## Prerequisites

### MCP Tools Available

The n8n MCP server provides these tools:

| Tool | Description |
|------|-------------|
| `n8n_list_workflows` | List all workflows with status |
| `n8n_get_workflow` | Get workflow details by ID |
| `n8n_get_workflow_structure` | Get nodes and connections only |
| `n8n_create_workflow` | Create new workflow |
| `n8n_update_full_workflow` | Full workflow update |
| `n8n_update_partial_workflow` | Incremental updates (add/remove nodes) |
| `n8n_delete_workflow` | Delete workflow |
| `n8n_list_executions` | List execution history |
| `n8n_get_execution` | Get execution details |
| `n8n_validate_workflow` | Validate workflow structure |
| `n8n_autofix_workflow` | Auto-fix common issues |
| `n8n_trigger_webhook_workflow` | Trigger webhook workflow |

### Access

- **URL:** https://n8n.dirk-schulenburg.net
- **API:** Via n8n MCP Gateway

## Quick Start

### List All Workflows

```javascript
n8n_list_workflows({
  limit: 100,
  active: true  // Optional: filter by active status
})
```

### Get Workflow Details

```javascript
// Full workflow with parameters
n8n_get_workflow({ id: "123" })

// Structure only (nodes + connections)
n8n_get_workflow_structure({ id: "123" })

// Minimal info
n8n_get_workflow_minimal({ id: "123" })
```

### Check Executions

```javascript
// Recent executions for a workflow
n8n_list_executions({
  workflowId: "123",
  limit: 10
})

// Get execution details
n8n_get_execution({
  id: "456",
  mode: "summary"  // preview, summary, filtered, full
})
```

## Creating Workflows

### Basic Workflow Structure

```javascript
n8n_create_workflow({
  name: "My Automation",
  nodes: [
    {
      id: "trigger-1",
      name: "Webhook Trigger",
      type: "n8n-nodes-base.webhook",
      typeVersion: 1,
      position: [250, 300],
      parameters: {
        path: "my-webhook",
        httpMethod: "POST"
      }
    },
    {
      id: "http-1",
      name: "HTTP Request",
      type: "n8n-nodes-base.httpRequest",
      typeVersion: 4,
      position: [450, 300],
      parameters: {
        url: "https://api.example.com/data",
        method: "GET"
      }
    }
  ],
  connections: {
    "trigger-1": {
      main: [[{ node: "http-1", type: "main", index: 0 }]]
    }
  }
})
```

### Common Node Types

| Node Type | Use Case |
|-----------|----------|
| `n8n-nodes-base.webhook` | HTTP trigger |
| `n8n-nodes-base.scheduleTrigger` | Cron/interval trigger |
| `n8n-nodes-base.httpRequest` | API calls |
| `n8n-nodes-base.set` | Set/transform data |
| `n8n-nodes-base.if` | Conditional logic |
| `n8n-nodes-base.switch` | Multiple conditions |
| `n8n-nodes-base.code` | Custom JavaScript |
| `n8n-nodes-base.emailSend` | Send emails |
| `n8n-nodes-base.slack` | Slack integration |

### Workflow Patterns

#### Pattern 1: Webhook → Process → Respond

```javascript
{
  nodes: [
    { type: "webhook", id: "1", position: [250, 300] },
    { type: "set", id: "2", position: [450, 300] },
    { type: "respondToWebhook", id: "3", position: [650, 300] }
  ],
  connections: {
    "1": { main: [[{ node: "2" }]] },
    "2": { main: [[{ node: "3" }]] }
  }
}
```

#### Pattern 2: Schedule → Fetch → Notify

```javascript
{
  nodes: [
    { type: "scheduleTrigger", id: "1", position: [250, 300] },
    { type: "httpRequest", id: "2", position: [450, 300] },
    { type: "if", id: "3", position: [650, 300] },
    { type: "slack", id: "4", position: [850, 200] },
    { type: "noOp", id: "5", position: [850, 400] }
  ],
  connections: {
    "1": { main: [[{ node: "2" }]] },
    "2": { main: [[{ node: "3" }]] },
    "3": { main: [[{ node: "4" }], [{ node: "5" }]] }
  }
}
```

## Debugging Workflows

### Step 1: Check Execution History

```javascript
// List recent executions
n8n_list_executions({
  workflowId: "123",
  status: "error",
  limit: 5
})
```

### Step 2: Analyze Failed Execution

```javascript
// Get execution with full data
n8n_get_execution({
  id: "456",
  mode: "full",
  includeInputData: true
})
```

### Step 3: Identify Error

Look for:
- **Node that failed:** Check `error` field
- **Input data:** What data reached the failing node
- **Error message:** API errors, validation errors, etc.

### Step 4: Fix and Test

```javascript
// Update specific node
n8n_update_partial_workflow({
  id: "123",
  operations: [
    {
      type: "updateNode",
      nodeId: "http-1",
      parameters: {
        url: "https://correct-url.com/api"
      }
    }
  ]
})
```

### Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `ECONNREFUSED` | API unreachable | Check URL, network |
| `401 Unauthorized` | Bad credentials | Update API key |
| `undefined` in expression | Missing data | Add null check |
| `Workflow could not be activated` | Missing credentials | Configure credentials |

## Updating Workflows

### Partial Update (Recommended)

```javascript
// Add a node
n8n_update_partial_workflow({
  id: "123",
  operations: [
    {
      type: "addNode",
      node: {
        id: "new-node",
        name: "New Step",
        type: "n8n-nodes-base.set",
        typeVersion: 3,
        position: [600, 300],
        parameters: {}
      }
    },
    {
      type: "addConnection",
      sourceNodeId: "existing-node",
      targetNodeId: "new-node"
    }
  ]
})
```

### Full Update

```javascript
n8n_update_full_workflow({
  id: "123",
  name: "Updated Name",
  nodes: [...],  // Complete node array
  connections: {...}  // Complete connections
})
```

## Validation & Auto-Fix

### Validate Workflow

```javascript
n8n_validate_workflow({
  id: "123",
  options: {
    validateNodes: true,
    validateConnections: true,
    validateExpressions: true,
    profile: "runtime"  // minimal, runtime, ai-friendly, strict
  }
})
```

### Auto-Fix Issues

```javascript
// Preview fixes
n8n_autofix_workflow({
  id: "123",
  applyFixes: false  // Preview only
})

// Apply fixes
n8n_autofix_workflow({
  id: "123",
  applyFixes: true,
  confidenceThreshold: "high"
})
```

## Workflow Templates

### Template: Daily Report

```javascript
n8n_create_workflow({
  name: "Daily Report",
  nodes: [
    {
      id: "schedule",
      name: "Daily 8am",
      type: "n8n-nodes-base.scheduleTrigger",
      typeVersion: 1,
      position: [250, 300],
      parameters: {
        rule: {
          interval: [{ field: "cronExpression", expression: "0 8 * * *" }]
        }
      }
    },
    {
      id: "fetch",
      name: "Fetch Data",
      type: "n8n-nodes-base.httpRequest",
      typeVersion: 4,
      position: [450, 300],
      parameters: {
        url: "={{ $env.API_URL }}/report",
        method: "GET"
      }
    },
    {
      id: "email",
      name: "Send Report",
      type: "n8n-nodes-base.emailSend",
      typeVersion: 2,
      position: [650, 300],
      parameters: {
        fromEmail: "noreply@example.com",
        toEmail: "team@example.com",
        subject: "Daily Report - {{ $now.format('yyyy-MM-dd') }}",
        text: "={{ $json.reportContent }}"
      }
    }
  ],
  connections: {
    "schedule": { main: [[{ node: "fetch", type: "main", index: 0 }]] },
    "fetch": { main: [[{ node: "email", type: "main", index: 0 }]] }
  }
})
```

### Template: Webhook API Proxy

```javascript
n8n_create_workflow({
  name: "API Proxy",
  nodes: [
    {
      id: "webhook",
      name: "Incoming Request",
      type: "n8n-nodes-base.webhook",
      typeVersion: 1,
      position: [250, 300],
      parameters: {
        path: "proxy",
        httpMethod: "POST",
        responseMode: "responseNode"
      }
    },
    {
      id: "transform",
      name: "Transform",
      type: "n8n-nodes-base.set",
      typeVersion: 3,
      position: [450, 300],
      parameters: {
        mode: "manual",
        duplicateItem: false,
        assignments: {
          assignments: [
            { name: "processed", value: "={{ $json.data }}", type: "string" }
          ]
        }
      }
    },
    {
      id: "respond",
      name: "Respond",
      type: "n8n-nodes-base.respondToWebhook",
      typeVersion: 1,
      position: [650, 300],
      parameters: {
        respondWith: "json",
        responseBody: "={{ $json }}"
      }
    }
  ],
  connections: {
    "webhook": { main: [[{ node: "transform", type: "main", index: 0 }]] },
    "transform": { main: [[{ node: "respond", type: "main", index: 0 }]] }
  }
})
```

## Best Practices

### Naming Conventions
- Workflows: `[Category] Description` (e.g., `[Email] Daily Newsletter`)
- Nodes: Descriptive action (e.g., `Fetch User Data`, `Send Slack Alert`)

### Error Handling
- Use `continueOnFail` for non-critical nodes
- Add error workflows for critical processes
- Log errors to external service

### Performance
- Limit data early with filters
- Use pagination for large datasets
- Batch operations when possible

### Security
- Use credentials instead of hardcoded secrets
- Validate webhook input
- Limit webhook exposure (authentication)

## Troubleshooting

### Workflow Won't Activate

```javascript
// Check for issues
n8n_validate_workflow({ id: "123" })

// Common causes:
// - Missing credentials
// - Invalid expressions
// - Disconnected nodes
```

### Execution Timeout

```javascript
// Check execution time
n8n_get_execution({ id: "456", mode: "preview" })

// Solutions:
// - Split into smaller workflows
// - Add pagination
// - Use async patterns
```

### Memory Issues

- Reduce data size with Set node
- Use pagination
- Process in batches

---

*DevOps Skill - n8n Workflow Management*
