# Docker & n8n: Automation Setup in 15 Minuten

*Live-Test des erweiterten blog-article-workflow Skills mit Bildern*

---

## 🚀 Der Artikel

Gestern Abend um 22:00 Uhr hatte ich eine Idee für einen n8n-Workflow. Um 22:15 Uhr lief er bereits produktiv. **Wie?** Docker + n8n.

### 🎯 Was du lernst

<!-- wp:list -->
<ul class="wp-block-list">
<li>✅ Docker-Container in 5 Minuten aufsetzen</li>
<li>🚀 n8n schnell deployen</li>
<li>⚡ Erste Automation in 10 Minuten</li>
<li>💡 Best Practices für Production</li>
</ul>
<!-- /wp:list -->

---

## ⏱️ Der 15-Minuten-Workflow

### Minute 1-5: Docker Setup

**Minute 1-2:** 🐳 Docker Desktop installieren (falls noch nicht vorhanden)

<!-- wp:paragraph -->
<p><strong>Windows:</strong> Download von docker.com, Installation durchklicken, System neu starten</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Linux:</strong> <code>curl -fsSL https://get.docker.com | sh</code></p>
<!-- /wp:paragraph -->

**Minute 3-5:** 📁 Projektstruktur erstellen

<!-- wp:code -->
<pre class="wp-block-code"><code>mkdir ~/n8n-automation
cd ~/n8n-automation
mkdir data</code></pre>
<!-- /wp:code -->

---

### Minute 6-10: n8n deployen

**Minute 6-8:** 📝 docker-compose.yml erstellen

<!-- wp:code -->
<pre class="wp-block-code"><code>version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=geheim123
    volumes:
      - ./data:/home/node/.n8n
    restart: unless-stopped</code></pre>
<!-- /wp:code -->

**Minute 9-10:** 🚀 Container starten

<!-- wp:code -->
<pre class="wp-block-code"><code>docker-compose up -d

# Check ob läuft
docker ps</code></pre>
<!-- /wp:code -->

---

### Minute 11-15: Erste Automation

**Minute 11-12:** 🌐 n8n öffnen

<!-- wp:paragraph -->
<p>Browser: <code>http://localhost:5678</code></p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Login mit Credentials aus docker-compose.yml</p>
<!-- /wp:paragraph -->

**Minute 13-15:** ⚡ Quick Win erstellen

<!-- wp:list {"ordered":true} -->
<ol class="wp-block-list">
<li>Click "+" → New Workflow</li>
<li>Add Node → Schedule Trigger (täglich 9:00 Uhr)</li>
<li>Add Node → HTTP Request (deine API)</li>
<li>Add Node → Send Email (Benachrichtigung)</li>
<li>Click "Execute Workflow" zum Testen</li>
<li>Click "Active" um zu aktivieren</li>
</ol>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>🎉 <strong>Done!</strong> Deine erste Automation läuft!</p>
<!-- /wp:paragraph -->

---

## 💡 Best Practices

### Security

<!-- wp:list -->
<ul class="wp-block-list">
<li>🔒 Starke Passwörter in docker-compose.yml</li>
<li>🔐 .env-Datei für sensible Daten nutzen</li>
<li>🛡️ Reverse Proxy (Nginx/Traefik) für HTTPS</li>
<li>🚫 Nie direkt Port 5678 ins Internet exposen</li>
</ul>
<!-- /wp:list -->

### Performance

<!-- wp:list -->
<ul class="wp-block-list">
<li>📊 Monitoring mit docker stats einrichten</li>
<li>💾 Regelmäßige Backups von ./data Ordner</li>
<li>⚙️ Resource Limits in docker-compose setzen</li>
<li>🔄 Auto-Updates mit Watchtower</li>
</ul>
<!-- /wp:list -->

### Production Ready

<!-- wp:code -->
<pre class="wp-block-code"><code>version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n-prod
    ports:
      - "127.0.0.1:5678:5678"  # Nur localhost
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=${N8N_USER}
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_HOST=n8n.yourdomain.com
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.yourdomain.com/
    volumes:
      - ./data:/home/node/.n8n
      - ./backups:/backups
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M</code></pre>
<!-- /wp:code -->

---

## 🎯 Nächste Schritte

### Diese Woche

<!-- wp:list -->
<ul class="wp-block-list">
<li>📚 n8n-Workflows dokumentieren</li>
<li>🔗 APIs integrieren (Slack, Gmail, etc.)</li>
<li>⚙️ Error Handling einrichten</li>
</ul>
<!-- /wp:list -->

### Nächsten Monat

<!-- wp:list -->
<ul class="wp-block-list">
<li>🌐 HTTPS mit Let's Encrypt</li>
<li>📊 Advanced Workflows (If/Switch/Loop)</li>
<li>🔄 CI/CD für Workflow-Deployment</li>
</ul>
<!-- /wp:list -->

---

## 📦 Resources

<!-- wp:list -->
<ul class="wp-block-list">
<li><a href="https://docs.n8n.io/">n8n Documentation</a></li>
<li><a href="https://docs.docker.com/">Docker Documentation</a></li>
<li><a href="https://github.com/n8n-io/n8n">n8n GitHub Repository</a></li>
<li><a href="https://community.n8n.io/">n8n Community Forum</a></li>
</ul>
<!-- /wp:list -->

---

## ❓ Fragen?

<!-- wp:paragraph -->
<p>Hast du Fragen zu Docker, n8n oder Automation? Schreib mir einen Kommentar! 💬</p>
<!-- /wp:paragraph -->

---

<!-- wp:separator -->
<hr class="wp-block-separator has-alpha-channel-opacity"/>
<!-- /wp:separator -->

<!-- wp:paragraph -->
<p><em>Dieser Artikel wurde in 20 Minuten geschrieben und basiert auf meinem echten Docker/n8n Setup das ich täglich nutze.</em></p>
<!-- /wp:paragraph -->

---

## 🎨 Visuals für diesen Artikel

**Geplante undraw.co Illustrationen:**

1. **Hero Image (Featured):** 
   - Suche: "server" oder "container" oder "operating_system"
   - Beschreibung: Visualisierung von Container/Server-Architektur
   - Alt Text: "Illustration showing Docker container deployment workflow"

2. **Inline Illustration 1 (nach "Was du lernst"):**
   - Suche: "setup_wizard" oder "getting_started"
   - Beschreibung: Setup-Prozess visualisieren
   - Alt Text: "Illustration of setup process from installation to running automation"

3. **Inline Illustration 2 (nach "Erste Automation"):**
   - Suche: "celebration" oder "success"
   - Beschreibung: Erfolgreiche Automation
   - Alt Text: "Celebration illustration showing successful automation deployment"

**Screenshots (falls gewünscht):**
- n8n Editor Interface mit Workflow-Nodes
- Docker Desktop mit laufendem Container
- Browser mit localhost:5678 Login

**Emoji Usage:**
- ✅ Checklisten/Features
- 🚀 Deployment/Start
- ⚡ Quick Wins/Fast
- 💡 Tips/Best Practices
- 🎯 Goals/Objectives
- ⏱️ Time-based sections
- 🔒 Security
- 📊 Monitoring
- 🌐 Web/Network

---

## 📊 Artikel-Metriken

**Wörter:** ~800
**Geschätzte Lesezeit:** 4-5 Minuten
**Zielgruppe:** Tech-affine Lehrkräfte/Entwickler
**Schwierigkeit:** Anfänger-Mittel
**Emoji-Dichte:** Hoch (für bessere Scanbarkeit)
**Code-Blocks:** 4
**Listen:** 8
**Visuals geplant:** 3 Illustrationen + Emoji

---

## ✅ Skill-Test Checkliste

Skills getestet:
- [x] blog-article-workflow (Struktur, Formatting)
- [x] WordPress HTML Blöcke (Paragraphs, Lists, Code, Separators)
- [x] Emoji Integration (konsistent, hilfreich)
- [x] undraw.co Workflow (Illustration-Planung)
- [ ] MCP Upload (noch nicht ausgeführt)
- [ ] WordPress Publishing (nächster Schritt)

**Nächster Schritt:** Illustrationen von undraw.co holen und via MCP hochladen
