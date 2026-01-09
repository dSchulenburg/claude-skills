---
name: recherche-workflow
description: Research workflow for finding well-substantiated contrarian positions. Specialized in anarchist theory, stigmergy, grassroots movements, guerilla gardening, and alternative media. Use when researching topics that benefit from non-mainstream perspectives with academic rigor.
license: MIT
tools:
  - WebSearch
  - WebFetch
---

# Recherche-Workflow: Abseitige Positionen mit Substanz

Systematischer Workflow zur Recherche von gut untermauerten, nicht-mainstream Perspektiven zu gesellschaftlichen, politischen und kulturellen Themen.

## MCP/Tool Integration (WICHTIG)

**Dieser Skill nutzt folgende Tools direkt:**

| Tool | Zweck |
|------|-------|
| `WebSearch` | Web-Suche nach Quellen, akademischen Papers, Bewegungsliteratur |
| `WebFetch` | Inhalte von URLs abrufen und analysieren |

**Suchstrategien:**
```
WebSearch: "[Thema] site:theanarchistlibrary.org"
WebSearch: "[Thema] anarchist OR commons OR grassroots filetype:pdf"
WebSearch: "[Thema] site:academia.edu"
WebFetch: URL + Prompt zur Inhaltsextraktion
```

**IMMER die Tools nutzen - nicht nur dokumentieren, sondern aktiv suchen und fetchen!**

**Ergebnisse speichern:**
- Recherche-Notizen in `_DEV_DOCS/Recherche/[Thema]-Recherche.md`
- Format: Obsidian-kompatibles Markdown mit YAML-Frontmatter

---

## Wann diesen Skill nutzen

- Recherche zu Themen, bei denen Mainstream-Medien blinde Flecken haben
- Suche nach akademisch fundierten alternativen Perspektiven
- Hintergrundrecherche zu Grassroots-Bewegungen, Selbstorganisation, Commons
- Kritische Analyse von Narrativen mit Gegenpositionen
- Quellensammlung für Blog-Artikel oder Dokumentation

## Kernprinzipien

### 1. Substanz vor Sensation
- Bevorzuge peer-reviewed Quellen und akademische Arbeiten
- Priorisiere Primärquellen (Originaltexte, Interviews, Dokumente)
- Prüfe Argumentationsketten, nicht nur Schlussfolgerungen
- Vermeide reine Meinungsblogs ohne Belege

### 2. Quellenvielfalt
- Kombiniere akademische + aktivistische + journalistische Quellen
- Suche bewusst nach Gegenpositionen zur eigenen These
- Nutze internationale Quellen (nicht nur DACH/anglophon)
- Berücksichtige historische Kontexte

### 3. Transparente Einordnung
- Kennzeichne ideologische Standpunkte der Quellen
- Unterscheide Fakten, Interpretationen und Meinungen
- Dokumentiere Limitationen und offene Fragen

---

## Workflow

### Phase 1: Framing (5 min)

**Fragen klären:**
```
1. Was ist die Mainstream-Position zu diesem Thema?
2. Welche Aspekte werden dabei ausgeblendet oder vereinfacht?
3. Wer profitiert von der dominanten Erzählung?
4. Welche Gegennarrative existieren?
```

**Beispiel:**
```
Thema: "Sharing Economy"
Mainstream: "Demokratisierung des Konsums, Win-Win"
Ausgeblendet: Prekarisierung, Plattform-Kapitalismus, Machtkonzentration
Gegennarrative: Commons-Theorie, Plattform-Kooperativismus, Stigmergy
```

### Phase 2: Quellenrecherche (15-30 min)

**Suchstrategie nach Quellentyp:**

#### Akademisch (höchste Priorität für Substanz)
```
- Google Scholar: [Thema] + "anarchist" OR "commons" OR "grassroots"
- Academia.edu: Stigmergy, alternative economics, social movements
- JSTOR/ResearchGate: Peer-reviewed zu spezifischen Theorien
- Ephemera Journal: Kritische Organisationstheorie
```

#### Bewegungsliteratur (Primärquellen)
```
- The Anarchist Library: theanarchistlibrary.org/search?query=[thema]
- CrimethInc.: crimethinc.com (Analysen, Toolkits)
- libcom.org: Arbeiterbewegung, Syndikalismus
- Fifth Estate Magazine: Langform-Essays seit 1965
```

#### Journalistisch (aktuelle Entwicklungen)
```
- Freedom News: freedomnews.org.uk
- The Conversation: Akademiker schreiben für Laien
- Rosa-Luxemburg-Stiftung: Analysen linker Politik
```

#### Praktisch (Fallstudien, Projekte)
```
- Incredible Edible: Guerilla Gardening Fallstudien
- Via Campesina: Bauernbewegungen international
- RESIST Project: Intersektionale Widerstände
```

### Phase 3: Quellenauswertung (20-40 min)

**Für jede relevante Quelle dokumentieren:**

```markdown
## [Titel der Quelle]

**Bibliografie:** [Autor, Jahr, Publikation, URL]

**Kernthese:** [1-2 Sätze]

**Hauptargumente:**
1. [Argument + Beleg]
2. [Argument + Beleg]
3. [Argument + Beleg]

**Methodik/Evidenz:** [Wie wird argumentiert? Empirie, Theorie, Fallstudien?]

**Ideologischer Standpunkt:** [Transparent einordnen]

**Stärken:** [Was ist überzeugend?]

**Schwächen/Limitationen:** [Wo greift die Argumentation zu kurz?]

**Relevanz für mein Thema:** [Konkrete Anknüpfungspunkte]
```

### Phase 4: Synthese (10-20 min)

**Zusammenführung der Perspektiven:**

```markdown
## Recherche-Synthese: [Thema]

### Mainstream-Position
[Kurze Zusammenfassung der dominanten Sichtweise]

### Alternative Perspektiven

#### Perspektive A: [Name/Tradition]
- **Kernkritik:** [Was wird anders gesehen?]
- **Belege:** [Stärkste Argumente/Studien]
- **Vertreter:** [Wichtigste Autor:innen]

#### Perspektive B: [Name/Tradition]
[...]

### Gemeinsamkeiten der Kritik
[Was vereint die alternativen Positionen?]

### Offene Fragen
[Was bleibt ungeklärt? Wo besteht Forschungsbedarf?]

### Praktische Implikationen
[Was folgt daraus für Handeln/Praxis?]
```

---

## Themenspezifische Recherchepfade

### Stigmergy & Selbstorganisation
```
Einstieg: Wikipedia "Stigmergy" → Heylighen (2016) PDF
Vertiefung: "Graffiti, Street Art and Stigmergy" (MacDowall)
Praxis: "The Stigmergic City" (UCL Paper)
Theorie: theanarchistlibrary.org → Suche "coordination without command"
```

### Commons & Alternative Ökonomie
```
Einstieg: Ostrom "Governing the Commons"
Anarchistisch: "The Economics of Anarchism" (anarcho)
Aktuell: P2P Foundation, Commons Transition
Kritik: Ephemera Journal "anarchist economic practices"
```

### Guerilla Gardening & Urban Commons
```
Einstieg: Wikipedia + Incredible Edible Todmorden
Akademisch: Frontiers "Incredible Edible Community Building"
Praktisch: gather-magazine.com, gardenculturemagazine.com
Bewegung: Via Campesina (europäischer Kontext)
```

### Street Art & Politische Ästhetik
```
Einstieg: "Graffiti, Street Art and Theories of Stigmergy"
Beispiele: @radicalgraffiti (Instagram), blocal-travel.com
Theorie: MacDowall's Arbeit zu Stigmergy in Street Art
Anarchistisch: CrimethInc. zu DIY-Kultur
```

---

## Bewertungskriterien für Quellen

### Hohe Qualität (bevorzugen)
- Peer-reviewed akademische Arbeiten
- Primärquellen (Originaltexte, Manifeste, Interviews)
- Langform-Analysen mit Quellenangaben
- Dokumentierte Fallstudien mit Methodik
- Historisch etablierte Publikationen (Fifth Estate, CrimethInc.)

### Mittlere Qualität (mit Vorsicht)
- Journalistische Langform-Artikel
- Blogs von Expert:innen mit Track Record
- Aktivistische Analysen ohne akademischen Anspruch
- Übersetzungen (Originalquelle prüfen)

### Niedrige Qualität (vermeiden)
- Social-Media-Posts ohne Kontext
- Anonyme Pamphlete ohne Argumentation
- Reine Meinungsstücke ohne Belege
- Verschwörungstheoretische Quellen
- Clickbait und Sensationalismus

---

## RSS-Feeds für kontinuierliche Recherche

### Anarchistische Medien
```
The Anarchist Library: https://theanarchistlibrary.org/feed
CrimethInc.: https://crimethinc.com/feed
Fifth Estate: https://www.fifthestate.org/feed/
Freedom News: https://freedomnews.org.uk/feed/
Warzone Distro: https://warzonedistro.noblogs.org/feed/
```

### Theorie & Ökonomie
```
Syndicalist.us: https://syndicalist.us/feed/
Robert Graham: https://robertgraham.wordpress.com/feed/
```

### Grassroots & Bewegungen
```
Via Campesina: https://www.eurovia.org/feed/
RESIST Project: https://theresistproject.eu/feed/
```

### Wissenschaft
```
The Conversation (EU): https://theconversation.com/europe/articles.atom
The Conversation (Umwelt): https://theconversation.com/europe/environment/articles.atom
```

---

## Beispiel-Recherche

**Thema:** "Dezentrale Koordination ohne Hierarchie"

### Phase 1: Framing
- Mainstream: "Hierarchie ist notwendig für Effizienz"
- Ausgeblendet: Stigmergy in Natur und Open Source, historische Beispiele
- Gegennarrativ: Anarchistische Organisationstheorie, Schwarminteligenz

### Phase 2: Quellen
1. Heylighen (2016): "Stigmergy as a Universal Coordination Mechanism"
2. CrimethInc.: Texte zu horizontaler Organisation
3. Wikipedia Indymedia: Fallstudie dezentrales Medienprojekt
4. MacDowall: Street Art als stigmergische Praxis

### Phase 3: Auswertung
[Siehe Vorlage oben für jede Quelle]

### Phase 4: Synthese
- Stigmergy funktioniert nachweisbar (Empirie: Ameisen, Wikipedia, OSS)
- Menschliche Anwendung erfordert geteilte Werte/Ziele
- Skalierungsfragen offen, aber Beispiele bis Millionen Nutzer
- Limitationen: Konflikte, Trittbrettfahrer, Machtasymmetrien

---

## Werkzeuge

### Web-Recherche
```javascript
// Gezielte Suche nach abseitigen Positionen
WebSearch({ query: "[Thema] site:theanarchistlibrary.org" })
WebSearch({ query: "[Thema] anarchist OR commons OR grassroots filetype:pdf" })
WebSearch({ query: "[Thema] critique OR criticism site:academia.edu" })
```

### Feed-Monitoring
```javascript
// RSS-Feeds abrufen (wenn MCP verfügbar)
// Alternativ: Feedreader wie Feedly, Inoreader
```

### Dokumentation
```markdown
// Recherche-Notizen in Obsidian
// Tags: #recherche #[thema] #[quellentyp]
// Links: [[Newsquellen]], [[feeds]]
```

---

## Best Practices

### Do
- Immer Mainstream UND Alternative recherchieren
- Quellen im Original lesen, nicht nur Zusammenfassungen
- Ideologische Standpunkte transparent machen
- Schwächen der eigenen Position anerkennen
- Primärquellen bevorzugen

### Don't
- Nur Quellen suchen, die eigene Meinung bestätigen
- Komplexität auf Slogans reduzieren
- Alle Mainstream-Positionen als "falsch" abtun
- Quellen ohne Prüfung übernehmen
- Nuancen ignorieren

---

## Verwandte Skills

- **blog-article-workflow**: Recherche-Ergebnisse in Artikel umwandeln
- **bswi-infobrief**: Für schulische Kontexte aufbereiten

---

*Dieser Skill basiert auf den kuratierten Quellen in [[Newsquellen]] und [[feeds]].*
