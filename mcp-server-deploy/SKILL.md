---
name: mcp-server-deploy
description: Deploy MCP servers from local development to production via Git and Docker. Handles code push, SSH deployment, container rebuild, and health verification.
license: MIT
---

# MCP Server Deployment Workflow

Complete workflow for deploying MCP servers from local development to the Hetzner production server via Git and Docker.

## When to Use This Skill

Use this skill when:
- Deploying new or updated MCP server code to production
- Setting up a new MCP server from scratch
- Rolling back to a previous version
- Checking deployment status and health

## Prerequisites

### Local Environment
- Git repository: `C:\Users\mail\entwicklung\docker\mcp-servers\{server-name}`
- SSH key: `C:\Users\mail\.ssh\hetzner_ssh_key`

### Server Environment
- **Host:** 95.217.163.192 (Hetzner)
- **User:** dirk
- **Path:** `/home/dirk/docker/mcp-servers/{server-name}`
- **Traefik:** Reverse proxy with auto-SSL

### MCP Servers

| Server | Local Port | Domain | Repo Path |
|--------|------------|--------|-----------|
| wp-mcp | 8000 | mcp-wp.dirk-schulenburg.net | mcp-servers/wp-mcp |
| moodle-mcp | 8001 | mcp-moodle.dirk-schulenburg.net | mcp-servers/moodle-mcp |
| imap-mcp | 8002 | mcp-imap.dirk-schulenburg.net | mcp-servers/imap-mcp |

## Quick Deploy

### One-Liner Deployment

```bash
# WordPress MCP
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 \
  'cd /home/dirk/docker/mcp-servers/wp-mcp && git pull && docker compose down && docker compose up -d --build'

# Moodle MCP
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 \
  'cd /home/dirk/docker/mcp-servers/moodle-mcp && git pull && docker compose down && docker compose up -d --build'

# IMAP MCP
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 \
  'cd /home/dirk/docker/mcp-servers/imap-mcp && git pull && docker compose down && docker compose up -d --build'
```

## Full Deployment Workflow

### Phase 1: Local Development

```bash
# 1. Navigate to project
cd C:\Users\mail\entwicklung\docker\mcp-servers\{server-name}

# 2. Make changes to code
# Edit src/server.mjs, etc.

# 3. Local testing
docker compose up --build

# 4. Test endpoint
curl http://localhost:8000/health
```

### Phase 2: Git Commit & Push

```bash
# 1. Stage changes
git add .

# 2. Commit with descriptive message
git commit -m "feat: add new tool moodle_create_quiz"

# 3. Push to remote
git push origin master
```

### Phase 3: Server Deployment

```bash
# 1. SSH to server
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192

# 2. Navigate to MCP server directory
cd /home/dirk/docker/mcp-servers/{server-name}

# 3. Pull latest code
git pull origin master

# 4. Rebuild and restart container
docker compose down
docker compose up -d --build
```

### Phase 4: Verification

```bash
# 1. Check container status
docker ps | grep mcp

# 2. Health check
curl https://mcp-{name}.dirk-schulenburg.net/health

# 3. View logs (if issues)
docker logs mcp-{name}-1 --tail 100

# 4. Test MCP call (from Claude)
# Use the MCP tool to verify functionality
```

## New MCP Server Setup

### Step 1: Create Local Structure

```
mcp-servers/{new-server}/
├── src/
│   ├── server.mjs
│   ├── config.mjs
│   └── tools/
├── Dockerfile
├── docker-compose.yml
├── package.json
└── .env
```

### Step 2: Docker Compose Template

```yaml
version: '3.8'
services:
  {server-name}:
    build: .
    container_name: {server-name}
    restart: unless-stopped
    env_file: .env
    networks:
      - proxy
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.{server-name}.rule=Host(`mcp-{short}.dirk-schulenburg.net`)"
      - "traefik.http.routers.{server-name}.entrypoints=websecure"
      - "traefik.http.routers.{server-name}.tls.certresolver=letsencrypt"
      - "traefik.http.services.{server-name}.loadbalancer.server.port=8000"

networks:
  proxy:
    external: true
```

### Step 3: Dockerfile Template

```dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 8000

CMD ["node", "src/server.mjs"]
```

### Step 4: Initialize Git & Deploy

```bash
# Local
cd C:\Users\mail\entwicklung\docker\mcp-servers\{new-server}
git init
git add .
git commit -m "initial: {server-name} MCP server"
git remote add origin git@github.com:dSchulenburg/{repo-name}.git
git push -u origin master

# Server
ssh dirk@95.217.163.192
cd /home/dirk/docker/mcp-servers
git clone git@github.com:dSchulenburg/{repo-name}.git {new-server}
cd {new-server}
# Create .env with secrets
docker compose up -d --build
```

## Rollback Procedure

### Quick Rollback

```bash
# 1. SSH to server
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192

# 2. Navigate and rollback
cd /home/dirk/docker/mcp-servers/{server-name}
git log --oneline -5  # Find commit to rollback to
git checkout {commit-hash}

# 3. Rebuild
docker compose down && docker compose up -d --build
```

### Restore from Backup

```bash
# 1. Check backup
ls -la /mnt/backup/mcp-servers/

# 2. Restore if needed
cp -r /mnt/backup/mcp-servers/{server-name} /home/dirk/docker/mcp-servers/

# 3. Rebuild
cd /home/dirk/docker/mcp-servers/{server-name}
docker compose up -d --build
```

## Health Checks

### All MCP Servers

```bash
# Check all at once
curl -s https://mcp-wp.dirk-schulenburg.net/health && echo " - wp-mcp OK"
curl -s https://mcp-moodle.dirk-schulenburg.net/health && echo " - moodle-mcp OK"
curl -s https://mcp-imap.dirk-schulenburg.net/health && echo " - imap-mcp OK"
```

### Detailed Status

```bash
# Container status
docker ps --filter "name=mcp" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Resource usage
docker stats --no-stream --filter "name=mcp"
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs mcp-{name}-1 --tail 100

# Check compose file
docker compose config

# Rebuild without cache
docker compose build --no-cache
docker compose up -d
```

### Health Check Fails

```bash
# Test internal port
docker exec mcp-{name}-1 curl -s localhost:8000/health

# Check Traefik routing
docker logs traefik --tail 50 | grep mcp

# Verify DNS
nslookup mcp-{name}.dirk-schulenburg.net
```

### Git Conflicts

```bash
# Force pull (discard local changes on server)
git fetch origin
git reset --hard origin/master
docker compose down && docker compose up -d --build
```

## Environment Variables

### Required .env Variables

```env
# Common
PORT=8000
NODE_ENV=production
MCP_API_KEY=your-api-key

# wp-mcp specific
WP_URL=https://www.dirk-schulenburg.net
WP_USERNAME=username
WP_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx

# moodle-mcp specific
MOODLE_URL=https://moodle.dirk-schulenburg.net
MOODLE_TOKEN=your-token

# imap-mcp specific
IMAP_HOST=imap.example.com
IMAP_USER=user@example.com
IMAP_PASSWORD=password
```

## Commit Message Convention

```
feat: add new feature
fix: bug fix
docs: documentation only
refactor: code refactoring
test: adding tests
chore: maintenance
```

Examples:
- `feat: add moodle_create_quiz tool`
- `fix: handle empty response in wp_list_posts`
- `refactor: extract validation logic`

---

## Logging

Bei Ausführung dieses Skills wird automatisch geloggt:

| Feld | Wert |
|------|------|
| **Agent** | devops |
| **Action** | deploy:mcp_server |
| **Context** | server_name, version, health_status |
| **Result** | success/failure |

**Beispiel-Log:**
```json
{
  "agent": "devops",
  "action": "deploy:mcp_server",
  "context": "{\"server_name\": \"wp-mcp\", \"version\": \"1.2.0\", \"health_status\": \"OK\"}",
  "result": "success"
}
```

---

*DevOps Skill - MCP Server Deployment*
