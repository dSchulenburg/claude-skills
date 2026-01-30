---
name: documentation-agent
description: Specialized documentation agent for generating, maintaining, and organizing technical documentation. Creates MCP tool docs, API references, session logs, and architecture documentation in Obsidian vault.
license: MIT
---

# Documentation Agent

Specialized sub-agent for the DevOps Agent that handles all documentation tasks including MCP tool documentation, API references, session logging, and architecture updates.

## When to Use This Skill

Use this skill when:
- New MCP tool needs documentation
- Session learnings should be captured
- Architecture diagrams/docs need updating
- README or SKILL.md files need creation
- Changelog entries are required
- Cross-referencing documentation

## Core Capabilities

### 1. Documentation Locations

| Type | Location | Format |
|------|----------|--------|
| **MCP Tool Docs** | `_DEV_DOCS/MCP/{server}.md` | Obsidian MD |
| **Session Logs** | `_DEV_DOCS/Sessions/YYYY-MM-DD_{topic}.md` | Obsidian MD |
| **Architecture** | `_DEV_DOCS/Architektur/*.md` | Obsidian MD |
| **Skills** | `docker/claude-skills/{skill}/SKILL.md` | Claude Skill |
| **READMEs** | Project root `README.md` | GitHub MD |

### 2. Documentation Templates

All templates follow consistent frontmatter and structure.

## Workflow: Document New MCP Tool

### Phase 1: Gather Information

```markdown
## Tool Information Checklist

- [ ] Tool name and purpose
- [ ] Input parameters (types, required/optional)
- [ ] Output format
- [ ] Error cases
- [ ] API dependencies (Moodle/WordPress function)
- [ ] Example usage
- [ ] Test results (from Debug Agent)
```

### Phase 2: Update MCP Server Documentation

Location: `C:\Users\mail\entwicklung\_DEV_DOCS\_DEV_DOCS\MCP\{server}.md`

```markdown
## moodle_create_quiz

Erstellt ein Quiz in einem Moodle-Kursabschnitt.

### Parameter

| Parameter | Typ | Required | Beschreibung |
|-----------|-----|----------|--------------|
| courseId | string | ✅ | Moodle Kurs-ID |
| sectionNum | string | ✅ | Abschnittsnummer (0-basiert) |
| quizName | string | ✅ | Name des Quiz |
| intro | string | ❌ | Beschreibung |
| timeLimit | string | ❌ | Zeitlimit in Sekunden |

### Rückgabe

\`\`\`json
{
  "success": true,
  "quizId": "15",
  "cmid": "234",
  "url": "https://moodle.../mod/quiz/view.php?id=234"
}
\`\`\`

### Beispiel

\`\`\`javascript
// Quiz erstellen
moodle_create_quiz({
  courseId: "8",
  sectionNum: "1",
  quizName: "Kapitel 1 Quiz",
  intro: "Test your knowledge",
  timeLimit: "1800"  // 30 minutes
})
\`\`\`

### Fehlerbehandlung

| Error | Ursache | Lösung |
|-------|---------|--------|
| `access_denied` | Fehlende Berechtigung | Plugin-Capabilities prüfen |
| `invalid_course` | Kurs existiert nicht | courseId validieren |
| `invalid_section` | Abschnitt existiert nicht | sectionNum prüfen |

### Abhängigkeiten

- **Plugin:** local_sync_service
- **Capability:** moodle/quiz:addinstance
- **Moodle-API:** local_sync_service_create_quiz
```

### Phase 3: Create/Update Changelog

Location: End of MCP documentation file

```markdown
## Changelog

| Datum | Version | Änderung |
|-------|---------|----------|
| 2026-01-19 | 2.4.0 | `moodle_create_quiz` hinzugefügt |
| 2026-01-17 | 2.3.1 | `moodle_update_page` Fix für HTML-Encoding |
| 2026-01-15 | 2.3.0 | `moodle_get_h5p_embed` hinzugefügt |
```

## Session Logging

### When to Create Session Log

- Complex debugging session
- New learnings/discoveries
- Architecture decisions
- Major feature implementation

### Session Log Template

Location: `_DEV_DOCS/Sessions/YYYY-MM-DD_{topic}.md`

```markdown
---
title: {Topic} Session
date: {YYYY-MM-DD}
status: abgeschlossen
tags:
  - sessions
  - {category}
related:
  - "[[MCP/{server}]]"
  - "[[Architektur/Agent-DevOps]]"
---

# {Topic} Session

## Kontext

**Ziel:** {Was sollte erreicht werden}
**Dauer:** {ca. X Stunden}
**Beteiligte Agents:** {DevOps, Coding, Debug}

## Problem

{Beschreibung des Ausgangsproblems}

## Analyse

### Versuch 1: {Ansatz}

\`\`\`bash
# Commands/Code
\`\`\`

**Ergebnis:** {Was passierte}

### Versuch 2: {Anderer Ansatz}

{...}

## Lösung

{Finale Lösung mit Code/Config}

## Learnings

1. **{Learning 1}:** {Erklärung}
2. **{Learning 2}:** {Erklärung}

## Offene Punkte

- [ ] {Follow-up Task 1}
- [ ] {Follow-up Task 2}

## Referenzen

- {Link zu Docs}
- {Link zu Issue}

---

*Session Log - {Datum}*
```

## Architecture Documentation

### When to Update

- New agent/sub-agent added
- New MCP server deployed
- Workflow changes
- Service configuration changes

### Files to Update

| Change Type | Files to Update |
|-------------|-----------------|
| New Sub-Agent | `Agent-DevOps.md`, `Agent-Architektur.md` |
| New MCP Server | `Shared-Services.md`, `CLAUDE.md` |
| New Skill | `Skill-Übersicht.md`, Agent doc |
| Routing Change | `Routing-Regeln.md` |

### Architecture Update Template

```markdown
## Changelog

| Datum | Änderung |
|-------|----------|
| {YYYY-MM-DD} | {Sub-Agent Name} hinzugefügt: {Kurzbeschreibung} |
```

## README Generation

### MCP Server README Template

```markdown
# {Server Name} MCP Server

{One-line description}

## Features

- {Feature 1}
- {Feature 2}

## Quick Start

\`\`\`bash
# Development
npm install
npm run dev

# Production
docker compose up -d --build
\`\`\`

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| PORT | No | Server port (default: 8000) |
| {VAR} | Yes | {Description} |

## MCP Tools

| Tool | Description |
|------|-------------|
| {tool_name} | {Brief description} |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| POST | /mcp | MCP protocol endpoint |

## Deployment

See: [[Skills/Skill-mcp-server-deploy]]

## License

MIT
```

## Cross-Reference Maintenance

### Obsidian Links

```markdown
# Internal links (Obsidian wiki-style)
[[MCP/Moodle]]
[[Architektur/Agent-DevOps]]
[[Skills/Skill-mcp-server-deploy]]

# With display text
[[MCP/Moodle|Moodle MCP Documentation]]
```

### GitHub Links

```markdown
# Relative links for READMEs
[MCP Server Deploy](./claude-skills/mcp-server-deploy/SKILL.md)
[Moodle MCP](./mcp-servers/moodle-mcp/)
```

## Integration with Other Agents

### Handoff from Coding Agent

```markdown
## Agent-Handoff

**From:** Coding Agent
**To:** Documentation Agent
**Context:** New tool implemented
**Artifacts:**
  - Source: mcp-servers/moodle-mcp/src/tools/moodle_create_quiz.mjs
  - Schema: Zod validation schema
**Task:** Generate MCP tool documentation
```

### Handoff from Debug Agent

```markdown
## Agent-Handoff

**From:** Debug Agent
**To:** Documentation Agent
**Context:** Testing complete
**Artifacts:**
  - Screenshots: debug-session/*.png
  - Test results: All tests passed
  - Bug fixes: Fixed permission issue
**Task:**
  1. Document test procedure
  2. Add error handling section
  3. Create session log for debugging
```

## Quick Reference

### Documentation Checklist

```markdown
## New MCP Tool Documentation

- [ ] Tool entry in MCP/{server}.md
  - [ ] Parameter table
  - [ ] Return format
  - [ ] Example usage
  - [ ] Error handling
  - [ ] Dependencies
- [ ] Changelog entry
- [ ] CLAUDE.md updated (if major feature)
- [ ] Session log (if complex implementation)
- [ ] Links verified (Obsidian + GitHub)
```

### Frontmatter Template

```yaml
---
title: {Title}
date: {YYYY-MM-DD}
status: aktiv|draft|archiviert
version: "{X.Y}"  # for skills
agent: DevOps|Education|Personal  # for skills
tags:
  - {tag1}
  - {tag2}
related:
  - "[[Related/Document]]"
---
```

### Common Tags

| Tag | Use For |
|-----|---------|
| `mcp` | MCP server documentation |
| `sessions` | Session logs |
| `agents` | Agent documentation |
| `skills` | Skill documentation |
| `infrastructure` | Server/Docker docs |
| `reference` | Quick reference docs |

---

## Logging

Bei Ausführung dieses Skills wird automatisch geloggt:

| Feld | Wert |
|------|------|
| **Agent** | devops |
| **Action** | docs:generate |
| **Context** | doc_type, target_file, sections_updated |
| **Result** | success/failure |

**Beispiel-Log:**
```json
{
  "agent": "devops",
  "action": "docs:generate",
  "context": "{\"doc_type\": \"mcp_tool\", \"target_file\": \"MCP/Moodle.md\", \"sections_updated\": [\"moodle_create_quiz\", \"Changelog\"]}",
  "result": "success"
}
```

---

*DevOps Sub-Agent - Documentation Agent v1.0*
