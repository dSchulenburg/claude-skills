---
name: moodle-section-analyzer
description: Analysiert Moodle-Kursabschnitte auf 4K-Defizite (Kreativität, Kritisches Denken, Kommunikation, Kollaboration), fehlende Interaktivität und Multimedia-Lücken. Gibt konkrete Optimierungsvorschläge mit H5P-Empfehlungen. Nutze wenn Lehrer einen Kurs modernisieren, mehr Engagement erreichen oder didaktisch aufwerten wollen.
---

# Moodle Section Analyzer

Analysiert Moodle-Abschnitte und identifiziert Optimierungspotenzial nach modernen didaktischen Prinzipien (4K, Gamification, Multimedia).

## Wann nutzen

- Bestehenden Moodle-Kurs modernisieren
- 4K-Defizite systematisch identifizieren
- Vor Einsatz des `moodle-section-optimizer` Skills
- Qualitätscheck für E-Learning-Inhalte

## Voraussetzungen

- **MCP Server**: moodle-mcp mit `moodle_get_course_contents`, `moodle_get_page`, `moodle_get_label`
- **Kurs-ID**: Muss bekannt sein

## Analyse-Framework

### 4K-Kompetenzmodell

| K | Beschreibung | Moodle-Indikatoren |
|---|--------------|-------------------|
| **Kreativität** | Eigene Lösungen entwickeln | Aufgaben, Wikis, H5P Drag&Drop |
| **Kritisches Denken** | Analysieren, Bewerten | Quizze, Selbsttests, Reflexionsaufgaben |
| **Kommunikation** | Ideen austauschen | Foren, Peer-Feedback, Präsentationen |
| **Kollaboration** | Zusammenarbeiten | Wikis, Gruppenforen, gemeinsame Dokumente |

### Engagement-Indikatoren

| Element | Typ | Engagement-Score |
|---------|-----|------------------|
| Label (nur Text) | Passiv | ⭐ |
| URL (externer Link) | Passiv | ⭐ |
| Page (Inhaltsseite) | Passiv | ⭐⭐ |
| Forum | Aktiv | ⭐⭐⭐ |
| Assignment | Aktiv | ⭐⭐⭐ |
| Quiz | Interaktiv | ⭐⭐⭐⭐ |
| H5P | Interaktiv | ⭐⭐⭐⭐⭐ |
| Wiki | Kollaborativ | ⭐⭐⭐⭐ |

### Multimedia-Check

| Element | Vorhanden? | Empfehlung |
|---------|------------|------------|
| Bilder | ❓ | Min. 1 pro Phase |
| Videos | ❓ | Für komplexe Konzepte |
| Infografiken | ❓ | Für Prozesse/Übersichten |
| Icons/Emojis | ❓ | Visuelle Orientierung |

## Workflow

### Schritt 1: Kursinhalt abrufen

```
moodle:moodle_get_course_contents
├── courseId: [KURS_ID]
└── Ausgabe: Alle Abschnitte mit Modulen
```

### Schritt 2: Abschnitt analysieren

Für jeden Abschnitt erfassen:

```yaml
abschnitt:
  id: [SECTION_ID]
  name: "[NAME]"
  module_count: [ANZAHL]
  
module_typen:
  labels: [N]
  pages: [N]
  urls: [N]
  forums: [N]
  assignments: [N]
  quizzes: [N]
  h5p: [N]
  wikis: [N]
  folders: [N]

4k_score:
  kreativität: [0-3]    # 0=fehlt, 1=schwach, 2=vorhanden, 3=stark
  kritisches_denken: [0-3]
  kommunikation: [0-3]
  kollaboration: [0-3]

engagement:
  passive_module: [N]   # Labels, URLs, Pages
  aktive_module: [N]    # Forums, Assignments
  interaktive_module: [N] # Quiz, H5P
  ratio: "[X]% passiv"

multimedia:
  bilder_in_labels: [true/false]
  videos: [true/false]
  externe_medien: [true/false]
```

### Schritt 3: Diagnose erstellen

```markdown
## Diagnose: [Abschnittsname]

### Stärken
- [Was bereits gut ist]

### 4K-Defizite
| K | Score | Problem | Empfehlung |
|---|-------|---------|------------|
| Kreativität | 1/3 | Keine kreativen Aufgaben | H5P Drag&Drop, offene Aufgaben |
| ... | ... | ... | ... |

### Engagement-Analyse
- Passiv/Aktiv-Ratio: [X]%/[Y]%
- Problem: [Beschreibung]
- Empfehlung: [Konkrete Maßnahme]

### Multimedia-Lücken
- [ ] Bilder fehlen
- [ ] Keine Videos
- [ ] Keine Infografiken

### Konkrete Optimierungsvorschläge

1. **[Vorschlag 1]**
   - Typ: [Label/H5P/Forum/...]
   - 4K-Bezug: [Welches K wird gestärkt]
   - Aufwand: ⭐/⭐⭐/⭐⭐⭐
   
2. **[Vorschlag 2]**
   ...
```

## Scoring-Regeln

### 4K-Score Berechnung

**Kreativität (0-3)**:
- 0: Nur passive Inhalte (Labels, URLs)
- 1: Assignments vorhanden, aber nur Textabgabe
- 2: Wikis oder offene Aufgaben
- 3: H5P kreativ (Drag&Drop, Branching), Projektaufgaben

**Kritisches Denken (0-3)**:
- 0: Keine Selbsttests oder Reflexion
- 1: Foren für Diskussion
- 2: Quiz oder H5P-Selbsttest
- 3: Mehrstufige Analyse-Aufgaben, Peer-Review

**Kommunikation (0-3)**:
- 0: Keine Interaktion zwischen SuS
- 1: Ein allgemeines Forum
- 2: Aufgabenbezogene Foren
- 3: Peer-Feedback, Präsentationen, strukturierte Diskussionen

**Kollaboration (0-3)**:
- 0: Nur Einzelarbeit
- 1: Forum-Diskussionen
- 2: Wiki vorhanden
- 3: Explizite Gruppenaufgaben, gemeinsame Produkte

### Engagement-Score

```
Engagement-Score = (Aktiv×2 + Interaktiv×3) / (Passiv + Aktiv×2 + Interaktiv×3) × 100
```

- < 30%: 🔴 Kritisch (zu passiv)
- 30-50%: 🟡 Verbesserungswürdig
- 50-70%: 🟢 Gut
- > 70%: 🌟 Exzellent

## Beispiel-Analyse

### Input

```
Kurs-ID: 6
Abschnitt: 2 (Checkout-Prozess analysieren)
```

### Output

```markdown
## Diagnose: Abschnitt 2 - Den Checkout-Prozess analysieren

### Ist-Zustand
- 4 Module: 1 URL, 3 Foren
- Keine H5P, keine Quizze, keine Assignments
- Keine Bilder in Labels

### 4K-Score
| K | Score | Status |
|---|-------|--------|
| Kreativität | 0/3 | 🔴 Fehlt |
| Kritisches Denken | 1/3 | 🟡 Schwach |
| Kommunikation | 2/3 | 🟢 Vorhanden |
| Kollaboration | 1/3 | 🟡 Schwach |

### Engagement
- Passiv: 25% (1 URL)
- Aktiv: 75% (3 Foren)
- Interaktiv: 0%
- Score: 🟡 43% - Verbesserungswürdig

### Top-3 Optimierungen

1. **H5P Quiz "Checkout-Basics"**
   - 4K: Kritisches Denken ↑
   - Aufwand: ⭐⭐
   - Tool: h5p-generator

2. **Einführungs-Label mit Bild**
   - 4K: - (Orientierung)
   - Aufwand: ⭐
   - Tool: moodle_create_label

3. **H5P Drag&Drop "Checkout-Schritte"**
   - 4K: Kreativität ↑
   - Aufwand: ⭐⭐
   - Tool: h5p-generator
```

## Integration mit anderen Skills

| Skill | Zusammenspiel |
|-------|---------------|
| `moodle-section-optimizer` | Erhält Diagnose als Input |
| `h5p-generator` | Erstellt empfohlene H5P-Elemente |
| `lernfeld-zu-moodle-kurs` | Kann Analyzer für QA nutzen |

## Native Moodle H5P (empfohlen)

Seit dem `local_h5p_api` Plugin können H5P-Inhalte direkt in der Moodle Content Bank gespeichert werden. Dies hat Vorteile gegenüber WordPress-Embedding:

| Aspekt | WordPress H5P | Moodle H5P (nativ) |
|--------|---------------|-------------------|
| Backup | Nicht im Kurs-Export | ✅ Im Kurs-Backup |
| Embed | iframe zu WordPress | ✅ Moodle-native |
| Filter | Nein | ✅ `{h5p:id}` möglich |
| Abhängigkeit | WordPress muss laufen | ✅ Standalone |

**Empfohlener H5P-Workflow:**
1. H5P generieren mit `h5p-generator` Skill
2. Upload via `moodle_upload_h5p` (MCP Server v2.4.0+)
3. Embed via iframe oder Moodle-Filter `{h5p:contentid}`

**Embed-URL-Format:**
```
https://moodle.example.com/h5p/embed.php?url=https%3A%2F%2Fmoodle.example.com%2Fpluginfile.php%2F[contextid]%2Fcontentbank%2Fpublic%2F[contentid]%2F[filename]
```

## ⚠️ Kritische Warnung: Berechtigungen

Nach CLI-Befehlen im Moodle-Container können Berechtigungsprobleme auftreten:

**Symptom:** "Invalid permissions detected when trying to create a directory"

**Ursache:** CLI-Befehle als root erstellen Verzeichnisse mit `root:root` statt `daemon:daemon`

**Lösung:**
```bash
docker exec moodle chown -R daemon:daemon /bitnami/moodledata/
```

**Prävention:** CLI-Befehle als daemon ausführen:
```bash
docker exec -u daemon moodle php /bitnami/moodle/admin/cli/purge_caches.php
```

Siehe auch: [[Moodle-Learnings#KRITISCH moodledata Berechtigungsproblem]]

## Limitations

- Kann Inhaltsqualität nicht bewerten (nur Struktur)
- Matchplan-Abgleich erfordert manuellen Input
- H5P-Inhalte in Moodle nicht direkt analysierbar (nur Existenz prüfbar)

## Referenzen

- [[Moodle]] - MCP Server Dokumentation
- [[Moodle-Learnings]] - Troubleshooting & Best Practices
- [[local_h5p_api Plugin]] - H5P Upload/Embed API

---

*Skill Version: 1.1*
*Abhängigkeiten: moodle-mcp (v2.4.0+)*
*Letzte Aktualisierung: 2026-01-15*
