# Matchplan-Struktur

Dokumentation der Matchplan-Struktur für die automatische Analyse.

## Typische Matchplan-Struktur

### Spalten (3-spaltig)

| Spalte | Inhalt | Extrahieren für |
|--------|--------|-----------------|
| **Lehrhandeln** | Folienreferenz, Impuls, Zeitangabe | Aktivitätstyp, Reihenfolge |
| **Schülerhandeln** | Arbeitsauftrag, Sozialform, Dauer | Aufgabenstellung, Gruppenform |
| **Begründung** | Lernziel, didaktische Intention | Abschnittsbeschreibung |

### Beispiel-Zeile

```
| Folie 3: "Kauf, du Arsch"    | Formulierung in eigenen   | Bedeutsamkeit des         |
| Ziel: Über die Irritation    | Worten. 15 min            | Lerngegenstands verankern |
| Einstieg ins Thema schaffen  |                           |                           |
```

## Erkennungsmuster

### Folien-Referenzen

```regex
Folie[n]?\s*(\d+)(?:\s*[-–und]\s*(\d+))?
```

Beispiele:
- "Folie 3" → Einzelfolie
- "Folien 1 und 2" → Foliengruppe
- "Folie 6, 7, 8" → Mehrere Folien

### Zeitangaben

```regex
(\d+)\s*(min|Min|Minuten|h|Std)
```

Beispiele:
- "15 min" → 15 Minuten
- "Ca. 60 Minuten" → 60 Minuten
- "ca. 45 min" → 45 Minuten

### Sozialformen

| Keyword | Sozialform | Moodle-Aktivität |
|---------|------------|------------------|
| "Einzelarbeit" | EA | Aufgabe |
| "zu zweit" | PA | Forum/Wiki |
| "Gruppenarbeit" | GA | Forum/Wiki |
| "Plenum" | PL | Label/Page |
| "LSG" (Lehrer-Schüler-Gespräch) | UG | - |

### Handlungsverben → Aktivitätstyp

| Verb | Aktivität | Moodle |
|------|-----------|--------|
| "diskutieren" | Diskussion | Forum |
| "recherchieren" | Recherche | URL + Forum |
| "präsentieren" | Präsentation | Forum/Aufgabe |
| "bearbeiten" | Aufgabe | Aufgabe |
| "visualisieren" | Erstellen | Aufgabe |
| "lesen", "gucken" | Rezeption | URL/Page |
| "beantworten" | Fragen | Forum |

## Folien-Cluster zu Abschnitten

### Strategie

```
Folien mit gleichem Thema → 1 Moodle-Abschnitt
Themen-Wechsel erkennbar an:
  - Neue Überschrift in Matchplan
  - "Neues Thema", "Nächster Schritt"
  - Deutlich andere Lernziele
```

### Beispiel LS01

```
Cluster 1: Folien 1-8 → "Checkout-Prozess analysieren"
  - F1-2: Orientierung
  - F3: Einstieg
  - F4-5: Begriffsklärung
  - F6-8: Abbruchgründe

Cluster 2: Folien 9-11 → "Beispielunternehmen"
  - F9: Fond-of Imagefilm
  - F10: Webshop erkunden
  - F11: Checkout-Prozess

Cluster 3: Folien 12-14 → "Prozessmodellierung"
  - F12: Deep Dive EPK
  - F13: EPK anwenden
  - F14: Offene Fragen
```

## Matchplan → Moodle Mapping

### Aktivitäts-Zuordnung

```yaml
matchplan_zeile:
  lehrhandeln: "Folie 6-8: Abbruchgründe"
  schuelerhandeln: "Einzelarbeit Ca. 60 Minuten"
  begruendung: "Kundensicht fokussieren"

moodle_aktivitaet:
  type: forum  # oder assign
  name: "Forum zur Aufgabe X: Abbruchgründe analysieren"
  beschreibung: "Analysieren Sie mögliche Abbruchgründe aus Kundensicht..."
```

### Entscheidungsbaum

```
Schülerhandeln enthält...
├── "diskutieren", "Forum", "austauschen"
│   └── → Forum
├── "bearbeiten AB", "Arbeitsblatt"
│   └── → Aufgabe (assign)
├── "recherchieren", "erkunden"
│   └── → URL + Forum
├── "präsentieren"
│   └── → Forum oder Aufgabe
├── "gemeinsam", "kollaborativ"
│   └── → Wiki
└── "lesen", "gucken", "aufnehmen"
    └── → URL oder Page (kein eigenes Modul)
```

## Automatisierungs-Ansatz

### Phase 1: Matchplan parsen

```python
def parse_matchplan(docx_path):
    doc = Document(docx_path)
    rows = []
    
    for table in doc.tables:
        for row in table.rows[1:]:  # Skip header
            cells = [cell.text for cell in row.cells]
            if len(cells) >= 3:
                rows.append({
                    'lehrhandeln': cells[0],
                    'schuelerhandeln': cells[1],
                    'begruendung': cells[2]
                })
    
    return rows
```

### Phase 2: Folien-Cluster bilden

```python
def cluster_folien(rows):
    clusters = []
    current_cluster = []
    
    for row in rows:
        folien = extract_folien(row['lehrhandeln'])
        
        if is_new_topic(row):
            if current_cluster:
                clusters.append(current_cluster)
            current_cluster = [row]
        else:
            current_cluster.append(row)
    
    return clusters
```

### Phase 3: Moodle-Struktur generieren

```python
def generate_moodle_structure(clusters):
    sections = []
    
    for i, cluster in enumerate(clusters):
        section = {
            'position': i + 2,  # 0 und 1 sind reserviert
            'name': extract_section_name(cluster),
            'modules': []
        }
        
        for row in cluster:
            module = map_to_moodle_activity(row)
            if module:
                section['modules'].append(module)
        
        sections.append(section)
    
    return sections
```

## Limitationen

### Was nicht automatisch erkannt wird:
- LOOP-URLs (müssen manuell zugeordnet werden)
- Aufgaben-Nummerierung (Kontext-abhängig)
- Welche Folien für SuS vs. LuL sind
- Versteckte Abschnitte

### Manuelle Nacharbeit nötig:
- Foren erstellen (API-Limitation)
- Assignments erstellen (API-Limitation)
- Dateien hochladen
- LOOP-Links zuordnen

---

*Dokumentation für automatische Matchplan-Analyse*
