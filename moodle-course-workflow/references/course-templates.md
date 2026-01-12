# Course Templates

Example course structures for common educational scenarios.

## Template 1: Short Workshop (4 Modules)

```yaml
course:
  fullname: "Workshop: Introduction to Topic"
  shortname: "WORKSHOP-TOPIC"
  format: topics
  numsections: 4

sections:
  - num: 1
    name: "Welcome & Overview"
    content:
      - type: label
        text: "Welcome to this workshop..."
      - type: url
        name: "Pre-Workshop Survey"
        url: "https://forms.example.com/pre"

  - num: 2
    name: "Core Concepts"
    content:
      - type: page
        name: "Interactive Lesson"
        h5p_id: 12  # Course Presentation
      - type: url
        name: "Further Reading"
        url: "https://example.com/article"

  - num: 3
    name: "Hands-On Practice"
    content:
      - type: page
        name: "Practice Exercise"
        h5p_id: 13  # Drag & Drop
      - type: label
        text: "Submit your work in the forum below"

  - num: 4
    name: "Wrap-Up & Next Steps"
    content:
      - type: page
        name: "Knowledge Check"
        h5p_id: 14  # Quiz
      - type: url
        name: "Post-Workshop Survey"
        url: "https://forms.example.com/post"
```

## Template 2: Full Course (12 Modules)

```yaml
course:
  fullname: "Comprehensive Course: Subject Area"
  shortname: "COURSE-SUBJECT"
  format: topics
  numsections: 12

sections:
  - num: 0
    name: "Course Information"
    content:
      - type: label
        text: "<h3>Welcome to the Course</h3><p>Course overview and objectives...</p>"
      - type: page
        name: "Syllabus"
        content: "Full course syllabus..."
      - type: url
        name: "Course Forum"
        url: "/mod/forum/view.php?id=XXX"

  - num: 1
    name: "Module 1: Foundations"
    content:
      - type: label
        text: "Learning objectives for Module 1..."
      - type: page
        name: "Introduction"
        h5p_id: 101  # Interactive Video
      - type: page
        name: "Self-Check Quiz"
        h5p_id: 102  # Quiz
      - type: url
        name: "Supplementary Material"
        url: "https://example.com/mod1"

  # Modules 2-11 follow same pattern...

  - num: 12
    name: "Module 12: Capstone Project"
    content:
      - type: label
        text: "Final project instructions..."
      - type: page
        name: "Project Guidelines"
        content: "Detailed guidelines for the capstone..."
      - type: url
        name: "Submit Your Project"
        url: "/mod/assign/view.php?id=XXX"
```

## Template 3: Cannabis Cultivation Course (Grower-Kurs)

Based on the EduGrow project specification:

```yaml
course:
  fullname: "Professional Cannabis Cultivation (CEA)"
  shortname: "CSC-GROWER-101"
  categoryid: 2  # CSC Courses
  format: topics
  numsections: 12
  summary: |
    CEA-basierter, rechtssicherer Cannabis-Anbau.
    Für Mitglieder lizenzierter Cannabis Social Clubs.

sections:
  - num: 1
    name: "Modul 1: Recht & Compliance"
    summary: "Cannabisgesetz, Pflichten, Haftung"
    content:
      - type: label
        text: |
          <h4>Lernziele</h4>
          <ul>
            <li>CanG verstehen</li>
            <li>Rollen im Verein kennen</li>
            <li>Dokumentationspflichten beherrschen</li>
          </ul>
      - type: page
        name: "Pflicht-Quiz: Rechtliche Grundlagen"
        h5p_id: 201  # Required quiz
        note: "Zugangsvoraussetzung für weitere Module"
      - type: url
        name: "SOP: Compliance & Dokumentation"
        url: "/mod/resource/view.php?id=XXX"

  - num: 2
    name: "Modul 2: Botanik & Entwicklung"
    summary: "Genotyp, Phänotyp, Wachstumsphasen"
    content:
      - type: page
        name: "Entwicklungsphasen erkennen"
        h5p_id: 202  # Interactive image hotspots
      - type: label
        text: "<h4>Glossar: CEA-Begriffe</h4>..."
      - type: url
        name: "Arbeitsblatt: Stressursachen"
        url: "/mod/resource/view.php?id=XXX"

  - num: 3
    name: "Modul 3: Lichttechnik"
    summary: "PPFD, DLI, Spektren"
    content:
      - type: page
        name: "Interaktiver DLI-Rechner"
        h5p_id: 203  # Calculator or fill-in-blanks
      - type: url
        name: "SOP: Lichtsetup & Messung"
        url: "/mod/resource/view.php?id=XXX"
      - type: url
        name: "PAR-Messprotokoll (Download)"
        url: "/mod/resource/view.php?id=XXX"

  - num: 4
    name: "Modul 4: Klima & VPD"
    summary: "Temperatur, Luftfeuchte, Luftbewegung"
    content:
      - type: page
        name: "Interaktives VPD-Diagramm"
        h5p_id: 204  # Interactive chart
      - type: url
        name: "SOP: Klimakontrolle"
        url: "/mod/resource/view.php?id=XXX"

  - num: 5
    name: "Modul 5: Substrate & Bewässerung"
    content:
      - type: page
        name: "Substrat-Vergleich"
        h5p_id: 205  # Comparison/sorting
      - type: url
        name: "Diagnose-Checkliste"
        url: "/mod/resource/view.php?id=XXX"

  - num: 6
    name: "Modul 6: Nährstoffe"
    content:
      - type: page
        name: "Mangelsymptome erkennen"
        h5p_id: 206  # Image hotspots
      - type: page
        name: "Diagnose-Quiz"
        h5p_id: 207  # Quiz

  - num: 7
    name: "Modul 7: IPM & Pflanzenschutz (Pflichtmodul)"
    content:
      - type: label
        text: "<strong>Pflichtmodul</strong> - Abschluss erforderlich"
      - type: page
        name: "IPM-Grundlagen"
        h5p_id: 208
      - type: page
        name: "Pflichtprüfung IPM"
        h5p_id: 209  # Required quiz
      - type: url
        name: "SOP: Schädlingsmanagement"
        url: "/mod/resource/view.php?id=XXX"

  - num: 8
    name: "Modul 8: Training & Wuchslenkung"
    content:
      - type: page
        name: "LST vs HST Vergleich"
        h5p_id: 210  # Interactive comparison

  - num: 9
    name: "Modul 9: Ernte & Nachbearbeitung"
    content:
      - type: page
        name: "Trichom-Bestimmung"
        h5p_id: 211  # Image identification
      - type: url
        name: "Ernte-Checkliste"
        url: "/mod/resource/view.php?id=XXX"

  - num: 10
    name: "Modul 10: Qualität & Analytik"
    content:
      - type: page
        name: "COA lesen"
        h5p_id: 212  # Document analysis

  - num: 11
    name: "Modul 11: Nachhaltigkeit"
    content:
      - type: label
        text: "Wahlmodul zu Energieeffizienz..."

  - num: 12
    name: "Modul 12: SOPs & Abschluss"
    content:
      - type: label
        text: "<h4>Abschlussarbeit</h4><p>Erstelle deine eigene Grow-SOP</p>"
      - type: url
        name: "SOP-Vorlage"
        url: "/mod/resource/view.php?id=XXX"
      - type: url
        name: "Peer-Review Forum"
        url: "/mod/forum/view.php?id=XXX"
```

## Template Usage

To deploy a template:

1. **Parse the YAML** structure
2. **Create course** with basic settings
3. **Loop through sections** and create each
4. **Add content** based on type:
   - `label` → `moodle_create_label`
   - `page` → `moodle_create_page` (with H5P embed if h5p_id present)
   - `url` → `moodle_create_url`

## H5P Content Mapping

| Module | H5P Type | Content |
|--------|----------|---------|
| Compliance Quiz | QuestionSet | Legal knowledge test |
| Development Stages | ImageHotspots | Plant growth phases |
| DLI Calculator | Arithmetic | Light calculations |
| VPD Diagram | InteractiveVideo | Climate explanation |
| Symptom Recognition | FindTheHotspot | Deficiency diagnosis |
| IPM Test | QuestionSet | Pest management |

---

*Templates should be adapted to specific course requirements and available H5P content.*
