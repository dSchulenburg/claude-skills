---
name: docker-management
description: Manage Docker containers on the Hetzner server. Check status, view logs, restart services, and troubleshoot container issues via SSH.
license: MIT
agent: DevOps
---

# Docker Management

Complete workflow for managing Docker containers on the production Hetzner server.

## When to Use This Skill

Use this skill when:
- Checking container health and status
- Viewing and analyzing container logs
- Restarting or rebuilding containers
- Troubleshooting container issues
- Managing Docker resources (cleanup, volumes)

## Prerequisites

### SSH Access

```bash
# SSH Command
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192

# Or with alias (if configured)
ssh hetzner
```

### Server Details

| Property | Value |
|----------|-------|
| **Host** | 95.217.163.192 |
| **User** | dirk |
| **OS** | Ubuntu LTS 24 |
| **Docker** | Docker Compose v2 |

## Container Overview

### Running Services

| Container | Service | Port | Domain |
|-----------|---------|------|--------|
| traefik | Reverse Proxy | 80, 443 | - |
| n8n | Workflow Automation | 5678 | n8n.dirk-schulenburg.net |
| wordpress | Blog/CMS | - | www.dirk-schulenburg.net |
| moodle | LMS | - | moodle.dirk-schulenburg.net |
| moodle-db | MariaDB | 3306 | - |
| n8n-postgres | PostgreSQL | 5432 | - |
| wp-mcp | WordPress MCP | 8000 | mcp-wp.dirk-schulenburg.net |
| moodle-mcp | Moodle MCP | 8001 | mcp-moodle.dirk-schulenburg.net |
| imap-mcp | IMAP MCP | 8002 | mcp-imap.dirk-schulenburg.net |

### Directory Structure

```
/home/dirk/docker/
├── traefik/
│   ├── docker-compose.yml
│   └── traefik.yml
├── n8n/
│   └── docker-compose.yml
├── wordpress/
│   └── docker-compose.yml
├── moodle/
│   └── docker-compose.yml
└── mcp-servers/
    ├── wp-mcp/
    ├── moodle-mcp/
    └── imap-mcp/
```

## Quick Commands

### Check All Containers

```bash
# Via SSH
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'
```

### Check Specific Container

```bash
# Container status
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker ps -f name=n8n'

# Container logs (last 50 lines)
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker logs n8n --tail 50'

# Follow logs in real-time
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker logs n8n -f --tail 20'
```

### Health Checks

```bash
# Check all MCP servers
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 '
  echo "=== MCP Health Checks ==="
  curl -s https://mcp-wp.dirk-schulenburg.net/health && echo " - wp-mcp"
  curl -s https://mcp-moodle.dirk-schulenburg.net/health && echo " - moodle-mcp"
  curl -s https://mcp-imap.dirk-schulenburg.net/health && echo " - imap-mcp"
'
```

## Container Management

### Restart Container

```bash
# Restart single container
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker restart n8n'

# Restart via docker-compose
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker/n8n
  docker compose restart
'
```

### Stop and Start

```bash
# Stop
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker stop n8n'

# Start
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 'docker start n8n'
```

### Rebuild Container

```bash
# Rebuild with new code (MCP servers)
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker/mcp-servers/wp-mcp
  docker compose down
  docker compose up -d --build
'

# Rebuild without cache
ssh -i C:\Users\mail\.ssh\hetzner_ssh_key dirk@95.217.163.192 '
  cd /home/dirk/docker/mcp-servers/wp-mcp
  docker compose build --no-cache
  docker compose up -d
'
```

## Log Analysis

### View Logs

```bash
# Last 100 lines
docker logs {container} --tail 100

# Since timestamp
docker logs {container} --since 2026-01-16T10:00:00

# Last hour
docker logs {container} --since 1h

# Grep for errors
docker logs {container} 2>&1 | grep -i error
```

### Common Log Locations

| Service | Log Command |
|---------|-------------|
| Traefik | `docker logs traefik` |
| n8n | `docker logs n8n` |
| WordPress | `docker logs wordpress` |
| Moodle | `docker logs moodle` |
| MCP Servers | `docker logs mcp-{name}-1` |

### Log Patterns to Watch

```bash
# Error patterns
docker logs n8n 2>&1 | grep -E "(ERROR|FATAL|Exception)"

# Connection issues
docker logs traefik 2>&1 | grep -E "(502|503|504)"

# Authentication failures
docker logs mcp-wp-mcp-1 2>&1 | grep -i "auth"
```

## Troubleshooting

### Container Won't Start

```bash
# 1. Check logs
docker logs {container} --tail 100

# 2. Check compose config
cd /home/dirk/docker/{service}
docker compose config

# 3. Check ports
netstat -tlnp | grep {port}

# 4. Check disk space
df -h

# 5. Check memory
free -h
```

### Container Keeps Restarting

```bash
# Check restart policy
docker inspect {container} | grep -A 5 RestartPolicy

# Check exit code
docker inspect {container} | grep -A 3 State

# View recent events
docker events --since 1h --filter container={container}
```

### Network Issues

```bash
# List networks
docker network ls

# Inspect network
docker network inspect proxy

# Check container network
docker inspect {container} | grep -A 20 Networks

# Test internal connectivity
docker exec {container} ping {other-container}
```

### Port Conflicts

```bash
# Check what's using a port
netstat -tlnp | grep {port}
lsof -i :{port}

# Check container port mapping
docker port {container}
```

## Resource Management

### Check Resource Usage

```bash
# Live stats
docker stats

# One-time snapshot
docker stats --no-stream

# Specific containers
docker stats n8n wordpress moodle
```

### Cleanup Commands

```bash
# Remove stopped containers
docker container prune -f

# Remove unused images
docker image prune -f

# Remove unused volumes (CAREFUL!)
docker volume prune -f

# Full cleanup (unused containers, networks, images)
docker system prune -f

# Nuclear option (removes everything unused including volumes)
docker system prune -a --volumes -f
```

### Check Disk Usage

```bash
# Docker disk usage
docker system df

# Detailed breakdown
docker system df -v
```

## Backup & Restore

### Database Backup

```bash
# PostgreSQL (n8n)
docker exec n8n-postgres pg_dump -U n8n n8n > backup_n8n_$(date +%Y%m%d).sql

# MariaDB (Moodle)
docker exec moodle-db mysqldump -u root -p$MYSQL_ROOT_PASSWORD moodle > backup_moodle_$(date +%Y%m%d).sql
```

### Volume Backup

```bash
# List volumes
docker volume ls

# Backup volume to tar
docker run --rm -v {volume_name}:/data -v $(pwd):/backup alpine tar cvf /backup/{volume_name}.tar /data
```

### Restore Database

```bash
# PostgreSQL
cat backup_n8n.sql | docker exec -i n8n-postgres psql -U n8n n8n

# MariaDB
cat backup_moodle.sql | docker exec -i moodle-db mysql -u root -p$MYSQL_ROOT_PASSWORD moodle
```

## Service-Specific Commands

### Traefik

```bash
# Check routing
docker logs traefik | grep -E "Adding route|Router"

# Debug mode (add to traefik.yml)
# log:
#   level: DEBUG

# View current routes
curl -s http://localhost:8080/api/http/routers | jq
```

### n8n

```bash
# Access CLI
docker exec -it n8n n8n

# Export workflows
docker exec n8n n8n export:workflow --all --output=/data/workflows.json

# Import workflow
docker exec n8n n8n import:workflow --input=/data/workflow.json
```

### Databases

```bash
# PostgreSQL shell
docker exec -it n8n-postgres psql -U n8n n8n

# MariaDB shell
docker exec -it moodle-db mysql -u root -p
```

## Monitoring

### Simple Health Script

```bash
#!/bin/bash
# Save as /home/dirk/check_health.sh

echo "=== Container Status ==="
docker ps --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "=== Resource Usage ==="
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"

echo ""
echo "=== Disk Usage ==="
df -h /

echo ""
echo "=== Health Checks ==="
curl -sf https://n8n.dirk-schulenburg.net/healthz > /dev/null && echo "n8n: OK" || echo "n8n: FAIL"
curl -sf https://moodle.dirk-schulenburg.net > /dev/null && echo "moodle: OK" || echo "moodle: FAIL"
curl -sf https://www.dirk-schulenburg.net > /dev/null && echo "wordpress: OK" || echo "wordpress: FAIL"
```

### Alerting (via n8n)

Create n8n workflow:
1. Schedule trigger (every 5 min)
2. HTTP Request to health endpoints
3. IF node to check status
4. Email/Slack notification on failure

## Quick Reference

### One-Liners

```bash
# All container status
ssh hetzner 'docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"'

# Restart all MCP servers
ssh hetzner 'for d in wp-mcp moodle-mcp imap-mcp; do cd /home/dirk/docker/mcp-servers/$d && docker compose restart; done'

# View all logs with errors
ssh hetzner 'docker ps -q | xargs -I {} docker logs {} 2>&1 | grep -i error | tail -20'

# Disk cleanup
ssh hetzner 'docker system prune -f && docker image prune -f'
```

---

*DevOps Skill - Docker Management*
