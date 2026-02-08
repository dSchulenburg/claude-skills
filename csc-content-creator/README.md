# CSC Content Creator

Persönlicher Agenten-Service für die **Solidarische Hanfwirtschaft** (Cannabis Social Club).

## Übersicht

Der CSC Content Creator ist ein spezialisierter Skill, der professionelle, seriös-bildungsorientierte Inhalte für den Cannabis Social Club erstellt:

- **Blog-Artikel** für solidarische-hanfwirtschaft.de
- **Moodle-Schulungskurse** für Mitglieder
- **Recherche-Dokumentation** für interne Wissensbasis

## Architektur

```
┌─────────────────────────────────────────────┐
│          csc-content-creator                │
│                                             │
│  Phase 1: Recherche                         │
│  ├── WebSearch / WebFetch                   │
│  ├── CSC-Quellen (csc-quellen.md)           │
│  └── Synthese → Obsidian-Notiz              │
│                                             │
│  Phase 2: Content-Erstellung                │
│  ├── Blog-Artikel (WordPress-Gutenberg)     │
│  └── Moodle-Kurs (Sections + Aktivitäten)   │
│                                             │
│  Phase 3: Publishing                        │
│  ├── wp_create_post → CSC-WordPress         │
│  └── moodle_create_course → Moodle LMS      │
└─────────────────────────────────────────────┘
```

## Verwendung

```bash
# Skill aufrufen
/csc-content-creator

# Beispiel-Aufgaben
"Schreibe einen Blog-Artikel über die CanG-Änderungen 2026"
"Erstelle einen Moodle-Kurs 'Pflichtschulung für neue Mitglieder'"
"Recherchiere: Aktuelle Rechtsprechung zu Anbauvereinigungen"
```

## Tonalität

**STIL: Seriös, bildungsorientiert, faktenbasiert**

- ✅ Wissenschaftliche Quellen zitieren
- ✅ Rechtliche Aussagen mit § CanG belegen
- ✅ Medizinische Claims mit Studien belegen
- ✅ Prävention und Jugendschutz mitdenken
- ✅ Transparenz bei Limitationen
- ❌ Keine Verharmlosung oder Dramatisierung

## Infrastruktur

### WordPress-Anbindung (one.com)

Die CSC-Website **solidarische-hanfwirtschaft.de** wird bei **one.com** gehostet (externes Hosting). Der WP-MCP-Container auf dem Hetzner-Server verbindet sich über die WordPress REST API.

**Verbindungsweg:**
```
Claude Code → wp-csc-proxy → WP-MCP Container (Hetzner) → REST API → WordPress (one.com)
```

**Setup auf one.com:**

1. WordPress Admin → Benutzer → Anwendungskennwörter
2. Neues Application Password erstellen
3. Credentials in `mcp-servers/wp-mcp/.env.csc` eintragen:
   ```env
   WP_URL=https://solidarische-hanfwirtschaft.de
   WP_USER=<admin-username>
   WP_APP_PASSWORD=<application-password>
   ```

**Container starten:**
```bash
# Auf Hetzner-Server
docker compose -f docker-compose-wp-csc-mcp.yml up -d

# Logs prüfen
docker logs wp-csc-mcp -f
```

### Moodle-Anbindung

CSC-Kurse werden auf dem Hauptmoodle-Server erstellt. Der CSC-Context hat eigene API-Keys für Audit-Trail.

**Setup:**

1. Moodle-Kategorie "Cannabis Social Club" erstellen
2. CSC-API-Key in Moodle konfigurieren:
   ```bash
   # mcp-servers/moodle-mcp/.env
   MCP_API_KEYS=...,<csc-key>:csc
   ```

## MCP-Context: "csc"

Der Skill nutzt einen eigenen MCP-Context `csc` mit separaten API-Keys:

**Konfiguration:**
- `claude-proxies/.env` → CSC_WP_KEY, CSC_MOODLE_KEY
- `context-keys.mjs` → CSC-Context mit wp-csc + moodle
- `.mcp.json` → wordpress-csc Server-Eintrag

**Vorteile:**
- Separater Audit-Trail für CSC-Content
- Isolierte Berechtigungen
- Klare Trennung von Schul-/persönlichem Content

## Quellenverzeichnis

Alle Recherchen basieren auf kuratierten Quellen in `sources/csc-quellen.md`:

**Kategorien:**
- Rechtliches (CanG, BfArM, DHV)
- Medizin & Wissenschaft (PubMed, EMCDDA)
- Anbau & Agronomie (Fachliteratur)
- Prävention (BZgA, DHS)
- Vereinsrecht (CSC-Verbände)
- Internationaler Vergleich (Kanada, Malta, etc.)

## Kursvorlagen

Vordefinierte Moodle-Kursstrukturen in `templates/kurse.md`:

1. **Pflichtschulung Neue Mitglieder** (90 min)
2. **Grundlagen des Indoor-Anbaus** (3-4h)
3. **Compliance & Dokumentation** (60 min)
4. **Prävention & Harm Reduction** (2h)

## Content-Templates

| Template | Format | Beispiel |
|----------|--------|----------|
| Rechtsinformation | Blog | "CanG 2024: Was dein CSC wissen muss" |
| Anbauguide | Kurs | "Grundlagen des Indoor-Anbaus" |
| Prävention | Kurs | "Verantwortungsvoller Umgang" |
| Vereinsnews | Blog | "Monatsbericht: Anbaufortschritt" |
| FAQ | Blog/Page | "Häufige Fragen zum CSC-Beitritt" |
| Compliance | Kurs | "Dokumentationspflichten nach CanG" |

## Deployment

### Phase C: WordPress einrichten (manuell auf one.com)

**TODO (nach Server-Deployment):**

1. ✅ Application Password erstellen
2. ⏳ Theme installieren/anpassen
3. ⏳ Grundseiten erstellen:
   - Startseite
   - Über uns
   - Blog
   - Mitglied werden
   - Kontakt
4. ⏳ Kategorien anlegen:
   - Cannabis-Wissen
   - Vereinsnews
   - Recht & Compliance
   - Anbau & Praxis
   - Prävention
5. ⏳ Menüstruktur aufbauen

### Testing

**Skill-Test:**
```bash
/csc-content-creator
> "Recherchiere: CanG 2024 Änderungen"
```

**Erwartetes Verhalten:**
1. WebSearch nach "CanG Änderungen 2024"
2. WebFetch von Gesetzestexten (BfArM, gesetze-im-internet.de)
3. WebFetch von DHV-Kommentaren
4. Synthese in `_DEV_DOCS/CSC/CanG-2024-Recherche.md`
5. Quellenangaben mit ⭐⭐⭐⭐⭐-Bewertung

**Blog-Output-Test:**
```bash
/csc-content-creator
> "Schreibe einen Artikel: CanG § 11 erklärt"
```

**Erwartetes Ergebnis:**
- WordPress-Gutenberg HTML
- Mindestens 3 Quellen
- § CanG-Referenzen
- Seriöser Ton
- Featured Image (undraw.co)

**Moodle-Kurs-Test:**
```bash
/csc-content-creator
> "Erstelle Kurs: CSC Pflichtschulung"
```

**Erwartetes Ergebnis:**
- Moodle-Kurs mit 5 Sections
- Labels mit BS:WI CSS-Styling
- H5P-Quizze
- Abschlusstest
- Zertifikat

## Verzeichnisstruktur

```
claude-skills/csc-content-creator/
├── SKILL.md                      # Haupt-Skill-Definition
├── README.md                     # Diese Datei
├── sources/
│   └── csc-quellen.md           # Kuratiertes Quellenverzeichnis
└── templates/
    └── kurse.md                 # Moodle-Kursvorlagen

claude-proxies/
├── wp-csc-proxy.mjs             # WordPress CSC Proxy
├── context-keys.mjs             # CSC-Context-Konfiguration
└── .env                         # CSC_WP_KEY, CSC_MOODLE_KEY

mcp-servers/wp-mcp/
└── .env.csc                     # WordPress one.com Credentials

_DEV_DOCS/CSC/
└── *.md                         # Recherche-Notizen
```

## Roadmap

### ✅ Phase A: Skill & Content
- [x] SKILL.md erstellt
- [x] Quellenverzeichnis (csc-quellen.md)
- [x] Kursvorlagen (kurse.md)

### ✅ Phase B: MCP-Infrastruktur
- [x] CSC-Context in context-keys.mjs
- [x] wp-csc-proxy.mjs erstellt
- [x] .mcp.json erweitert
- [x] docker-compose-wp-csc-mcp.yml
- [x] .env.csc Template
- [x] API-Keys generiert

### ⏳ Phase C: WordPress Setup (manuell)
- [ ] Application Password erstellen
- [ ] Theme installieren
- [ ] Grundseiten erstellen
- [ ] Container deployen

### ⏳ Phase D: Testing & Refinement
- [ ] Skill-Test durchführen
- [ ] Ersten Blog-Artikel generieren
- [ ] Ersten Moodle-Kurs erstellen
- [ ] Feedback-Loop etablieren

## Support

**Dokumentation:**
- [CSC-Quellenverzeichnis](sources/csc-quellen.md)
- [Moodle-Kursvorlagen](templates/kurse.md)
- [CLAUDE.md](../../CLAUDE.md)

**Verwandte Skills:**
- `blog-article-workflow` – Blog-Artikel-Erstellung
- `moodle-course-workflow` – Moodle-Kurse
- `recherche-workflow` – Recherche-Methodik
- `h5p-generator` – H5P-Content erstellen

**Fragen/Probleme:**
- Recherche-Archiv: `_DEV_DOCS/CSC/`
- Session-Logs: `~/.claude/projects/.../`
