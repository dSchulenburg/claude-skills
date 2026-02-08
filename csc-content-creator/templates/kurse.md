# CSC-Kursvorlagen für Moodle

Vordefinierte Kursstrukturen für typische Cannabis Social Club Schulungen.

## Vorlage 1: Pflichtschulung Neue Mitglieder

**Dauer:** 90 Minuten
**Format:** Selbstlernkurs mit Abschlusstest
**Zertifikat:** Ja (nach bestandenem Test)

### Kursstruktur

#### Section 1: Willkommen & Vereinsrecht

**Lernziele:**
- Rechtsform und Struktur der Anbauvereinigung verstehen
- Rechte und Pflichten als Mitglied kennen
- Vereinssatzung und Organe benennen können

**Inhalte:**
- Label: Begrüßung mit CSC-Logo
- Page: "Unsere Satzung" (Auszüge mit Erklärungen)
- Page: "Organe: Vorstand, Mitgliederversammlung, Beirat"
- URL: Link zur vollständigen Satzung (Download)
- H5P: Quiz "Vereinsrecht" (5 Fragen)

**Beispiel-Label (HTML):**
```html
<div style="background: linear-gradient(135deg, #003366 0%, #00A3E0 100%);
            color: white; padding: 25px; border-radius: 8px;
            margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;">
  <h2 style="margin: 0 0 15px 0; color: white; font-size: 24px;">🌿 Willkommen bei der Solidarischen Hanfwirtschaft</h2>
  <p style="margin: 0; font-size: 16px; line-height: 1.6;">
    Diese Schulung ist Pflicht für alle neuen Mitglieder. Du lernst hier alles Wichtige über unseren Verein,
    deine Rechte und Pflichten, und den verantwortungsvollen Umgang mit Cannabis.
  </p>
  <p style="margin: 15px 0 0 0; font-size: 14px;">⏱️ Dauer: ca. 90 Minuten | 📝 Abschlusstest erforderlich</p>
</div>
```

#### Section 2: CanG-Grundlagen

**Lernziele:**
- Wichtigste Paragraphen des CanG kennen
- Eigenbedarf vs. Weitergabe unterscheiden
- Strafrechtliche Risiken verstehen

**Inhalte:**
- Label: "📖 Konsumcannabisgesetz (CanG) – Was du wissen musst"
- Page: "§ 3 CanG: Besitz und Eigenanbau"
- Page: "§ 11 CanG: Anbauvereinigungen"
- Page: "§ 34 CanG: Strafrechtliche Konsequenzen"
- URL: Link zum Gesetzestext (gesetze-im-internet.de)
- H5P: True/False Quiz "CanG-Mythen" (10 Aussagen)

**Beispiel-Page (Markdown → HTML):**
```markdown
# § 11 CanG: Anbauvereinigungen

## Was ist eine Anbauvereinigung?

Nach § 11 Absatz 1 CanG ist eine Anbauvereinigung ein **nicht-gewinnorientierter Verein**, der Cannabis ausschließlich für den Eigenbedarf seiner Mitglieder anbaut und weitergibt.

## Wichtige Regeln:

- ✅ **Maximal 500 Mitglieder** (§ 11 Abs. 2 CanG)
- ✅ **Nur Volljährige** (§ 12 Abs. 1 CanG)
- ✅ **Keine Werbung** (§ 16 CanG)
- ✅ **Meldepflicht an BfArM** (§ 13 CanG)
- ❌ **Keine Weitergabe an Dritte** (§ 34 CanG – strafbar!)

## Warum diese Regeln?

Das CanG soll den Schwarzmarkt eindämmen UND gleichzeitig Jugendschutz und Gesundheitsschutz gewährleisten. Anbauvereinigungen sind ein kontrollierter Rahmen.

---

**Quelle:** [Konsumcannabisgesetz (CanG)](https://www.gesetze-im-internet.de/cang/)
```

#### Section 3: Prävention & Verantwortung

**Lernziele:**
- Risiken und Nebenwirkungen von Cannabis benennen
- Safer-Use-Regeln anwenden
- Hilfsangebote kennen

**Inhalte:**
- Label: "⚠️ Verantwortungsvoller Umgang – Deine Gesundheit zählt"
- Page: "Wirkungsweise von Cannabis (THC, CBD)"
- Page: "Risiken: Psychose, Abhängigkeit, Verkehrstauglichkeit"
- Page: "Safer Use: 10 Tipps für risikoarmen Konsum"
- URL: BZgA Cannabisprävention (cannabispraevention.de)
- URL: Sucht & Drogen Hotline (0800 313 0045)
- H5P: Fallbeispiele "Risikosituationen erkennen" (5 Szenarien)

**Beispiel-Safer-Use-Tipps (Moodle-Page):**
```html
<h2>10 Tipps für risikoarmen Konsum</h2>

<ol style="line-height: 1.8; font-size: 15px;">
  <li>🚫 <strong>Nicht vor dem 21. Lebensjahr</strong> – Gehirnentwicklung abwarten</li>
  <li>⏰ <strong>Konsumpausen einlegen</strong> – Toleranzentwicklung vermeiden</li>
  <li>🚗 <strong>Nie Auto fahren</strong> nach Konsum (§ 24a StVG – 0,0 Promille THC!)</li>
  <li>🤰 <strong>Nicht in Schwangerschaft/Stillzeit</strong></li>
  <li>🧠 <strong>Bei psychischen Erkrankungen</strong> Arzt konsultieren</li>
  <li>🌡️ <strong>Vaporisieren statt Rauchen</strong> – schont die Lunge</li>
  <li>📉 <strong>Niedrig dosieren</strong> – "Start low, go slow"</li>
  <li>🏡 <strong>Safe Environment</strong> – nur in vertrauter Umgebung</li>
  <li>🤝 <strong>Nicht alleine</strong> – vertraute Personen dabei haben</li>
  <li>📞 <strong>Hilfe holen</strong> bei Bad Trips (Sucht-Hotline: 0800 313 0045)</li>
</ol>

<div style="background: #FFF3CD; border-left: 4px solid #B5E505; padding: 15px; margin-top: 20px;">
  <p style="margin: 0;"><strong>💡 Merke:</strong> Safer Use bedeutet NICHT, dass Cannabis harmlos ist. Es gibt KEIN risikofreies Konsummuster!</p>
</div>

<p><small>Quellen: <a href="https://www.bzga.de/">BZgA</a>, <a href="https://www.dhs.de/">DHS</a>, <a href="https://nida.nih.gov/">NIDA</a></small></p>
```

#### Section 4: Hausordnung & Verhalten

**Lernziele:**
- Betriebsordnung des CSC kennen
- Verhalten bei Ausgabe und Events verstehen
- Datenschutz und Schweigepflicht respektieren

**Inhalte:**
- Label: "🏠 Unsere Hausordnung"
- Page: "Ausgabezeiten und Mengenbegrenzungen"
- Page: "Verhalten bei Events (keine Weitergabe!)"
- Page: "Datenschutz: Deine Daten sind sicher"
- H5P: Interactive Book "Hausordnung Rundgang" (mit Bildern)

#### Section 5: Abschlusstest

**Lernziele:**
- Alle Inhalte wiederholen und anwenden

**Inhalte:**
- Label: "📝 Abschlusstest – Zeige was du gelernt hast"
- H5P: Quiz (20 Fragen aus allen Sections)
  - Multiple Choice (10 Fragen)
  - True/False (10 Fragen)
  - Bestehensgrenze: 80% (16 von 20 richtig)
- Page: "Zertifikat erhalten" (nach bestandenem Test)

**Quiz-Beispielfragen:**
1. Wie viele Mitglieder darf eine Anbauvereinigung maximal haben? (500)
2. Ab welchem Alter ist die Mitgliedschaft erlaubt? (18)
3. Darf ich mein Cannabis an Freunde weitergeben? (NEIN – § 34 CanG!)
4. Welche THC-Grenze gilt im Straßenverkehr? (0,0 Promille)
5. Wo finde ich Hilfe bei Konsumproblemen? (Sucht-Hotline)

---

## Vorlage 2: Grundlagen des Indoor-Anbaus

**Dauer:** 3-4 Stunden
**Format:** Selbstlernkurs mit praktischen Aufgaben
**Zielgruppe:** Mitglieder mit Anbau-Interesse

### Kursstruktur

#### Section 1: Biologie der Cannabis-Pflanze

**Inhalte:**
- Page: "Cannabis sativa, indica, ruderalis"
- Page: "Wachstumsphasen: Keimung, Wachstum, Blüte, Ernte"
- Page: "THC, CBD, Terpene – Cannabinoide verstehen"
- H5P: Image Hotspots "Anatomie der Pflanze"

#### Section 2: Substrate & Bewässerung

**Inhalte:**
- Page: "Erdsubstrate vs. Hydroponic"
- Page: "pH-Wert und EC-Wert messen"
- Page: "Bewässerungssysteme (Hand, Tropf, DWC)"
- H5P: Drag & Drop "Substrat-Komponenten"

#### Section 3: Licht & Belüftung

**Inhalte:**
- Page: "LED vs. NDL – Lichttechnologien"
- Page: "Lichtzyklen: 18/6 (Wachstum), 12/12 (Blüte)"
- Page: "Abluft, Zuluft, Umwälzung – Klimakontrolle"
- H5P: Quiz "Lichtberechnung"

#### Section 4: Nährstoffe & Düngung

**Inhalte:**
- Page: "NPK – Stickstoff, Phosphor, Kalium"
- Page: "Wachstumsdünger vs. Blütedünger"
- Page: "Mangelerscheinungen erkennen und beheben"
- H5P: Image Sequencing "Düngezyklus"

#### Section 5: Ernte & Trocknung

**Inhalte:**
- Page: "Erntezeitpunkt bestimmen (Trichome prüfen)"
- Page: "Trocknung: Temperatur, Luftfeuchte, Dauer"
- Page: "Fermentation (Curing) für besseres Aroma"
- H5P: Timeline "Vom Schnitt zum Genuss"

#### Section 6: Praxis-Aufgabe & Zertifikat

**Inhalte:**
- Assignment: "Dein erster Grow-Plan" (Upload PDF/Dokument)
- Page: "Zertifikat herunterladen"

---

## Vorlage 3: Compliance & Dokumentation

**Dauer:** 60 Minuten
**Format:** Pflichtschulung für Vorstand/Beauftragte
**Zertifikat:** Ja

### Kursstruktur

#### Section 1: Meldepflichten an BfArM

**Inhalte:**
- Page: "§ 13 CanG: Anzeigepflicht"
- Page: "Formular ausfüllen (Schritt-für-Schritt)"
- Page: "Änderungsmeldungen (Vorstandswechsel, Standort)"
- URL: BfArM-Formular Download

#### Section 2: Buchführung & Rückverfolgbarkeit

**Inhalte:**
- Page: "Bestandsbuch führen (gesetzliche Anforderung)"
- Page: "Ausgabe-Dokumentation"
- Page: "Aufbewahrungspflichten (10 Jahre)"
- H5P: Interactive Book "Muster-Bestandsbuch"

#### Section 3: Kontrollen durch Behörden

**Inhalte:**
- Page: "Wer kontrolliert? (BfArM, Ordnungsamt, Polizei)"
- Page: "Vorbereitung auf Kontrollen (Checkliste)"
- Page: "Rechte und Pflichten bei Kontrollen"

#### Section 4: Datenschutz & Mitgliederverwaltung

**Inhalte:**
- Page: "DSGVO-Anforderungen für CSCs"
- Page: "Mitgliederdaten sicher speichern"
- Page: "Auskunftsrechte und Löschpflichten"
- H5P: Quiz "Datenschutz-Szenarien"

---

## Vorlage 4: Prävention & Harm Reduction

**Dauer:** 2 Stunden
**Format:** Pflichtschulung (jährliche Auffrischung)
**Zielgruppe:** Alle Mitglieder

### Kursstruktur

#### Section 1: Wirkung & Pharmakologie

**Inhalte:**
- Page: "THC-Wirkung im Gehirn (Endocannabinoid-System)"
- Page: "Akute Effekte: Entspannung, Wahrnehmung, Appetit"
- Page: "Wirkungsdauer: Inhalation vs. Oral"
- H5P: Video mit Quiz "Wie Cannabis wirkt" (z.B. BZgA-Video)

#### Section 2: Risiken & Nebenwirkungen

**Inhalte:**
- Page: "Kurzzeitrisiken: Angst, Paranoia, Kreislauf"
- Page: "Langzeitrisiken: Abhängigkeit, Psychose, Lungenschäden"
- Page: "Besondere Risikogruppen (Jugendliche, Schwangere, psychisch Kranke)"
- H5P: Branching Scenario "Risiko-Entscheidungen"

#### Section 3: Konsummuster & Safer Use

**Inhalte:**
- Page: "Risikoarmer Konsum (10 Tipps)"
- Page: "Mischkonsum vermeiden (Alkohol, Medikamente)"
- Page: "Toleranzentwicklung und Pausen"
- H5P: Flashcards "Safer Use Regeln"

#### Section 4: Hilfsangebote & Kontakte

**Inhalte:**
- Page: "Wann hole ich Hilfe? (Warnsignale)"
- Page: "Suchtberatungsstellen in deiner Nähe"
- Page: "Telefonhotlines (kostenlos & anonym)"
- URL: BZgA Cannabisprävention
- URL: Sucht & Drogen Hotline
- H5P: Quiz "Hilfe finden"

---

## Styling-Guidelines für Labels

### Standard-Begrüßungslabel

```html
<div style="background: linear-gradient(135deg, #003366 0%, #00A3E0 100%);
            color: white; padding: 25px; border-radius: 8px;
            margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;">
  <h2 style="margin: 0 0 15px 0; color: white; font-size: 24px;">🌿 [Kurstitel]</h2>
  <p style="margin: 0; font-size: 16px; line-height: 1.6;">[Kurzbeschreibung]</p>
  <p style="margin: 15px 0 0 0; font-size: 14px;">⏱️ Dauer: [Zeit] | 📝 [Abschluss-Info]</p>
</div>
```

### Lernziel-Label

```html
<div style="background: #F5F5F5; border-left: 4px solid #00A3E0;
            padding: 20px; margin: 20px 0; border-radius: 4px;">
  <h3 style="margin: 0 0 10px 0; color: #003366;">📚 Lernziele</h3>
  <ul style="margin: 0; padding-left: 20px; line-height: 1.8;">
    <li>Lernziel 1</li>
    <li>Lernziel 2</li>
    <li>Lernziel 3</li>
  </ul>
</div>
```

### Warn-Label (z.B. Prävention)

```html
<div style="background: #FFF3CD; border-left: 4px solid #B5E505;
            padding: 20px; margin: 20px 0; border-radius: 4px;">
  <h3 style="margin: 0 0 10px 0; color: #856404;">⚠️ Wichtiger Hinweis</h3>
  <p style="margin: 0; color: #856404;">[Warntext]</p>
</div>
```

### Tipp-Label

```html
<div style="background: #E7F3FF; border-left: 4px solid #00A3E0;
            padding: 15px; margin: 20px 0; border-radius: 4px;">
  <p style="margin: 0;"><strong>💡 Tipp:</strong> [Tipp-Text]</p>
</div>
```

### Quellen-Label (Section-Ende)

```html
<div style="background: #FAFAFA; border-top: 2px solid #DDD;
            padding: 15px; margin: 30px 0 0 0; font-size: 13px;">
  <p style="margin: 0 0 10px 0;"><strong>📖 Quellen & weiterführende Links:</strong></p>
  <ul style="margin: 0; padding-left: 20px;">
    <li><a href="URL">Quelle 1</a></li>
    <li><a href="URL">Quelle 2</a></li>
  </ul>
</div>
```

---

## H5P-Content-Typen (empfohlen)

| Content Type | Use Case | Beispiel |
|--------------|----------|----------|
| **Multiple Choice** | Wissensüberprüfung | "Welche Aussage zu § 11 CanG ist korrekt?" |
| **True/False** | Mythen entlarven | "Cannabis macht immer abhängig – Wahr oder Falsch?" |
| **Drag & Drop** | Zuordnungsaufgaben | "Ordne Nährstoffe den Mangelsymptomen zu" |
| **Interactive Video** | Video mit Quizfragen | BZgA-Präventionsvideo mit Checkpoints |
| **Flashcards** | Wiederholung | "Safer Use Regeln" |
| **Branching Scenario** | Fallbeispiele | "Was tust du in dieser Risikosituation?" |
| **Image Hotspots** | Anatomie | "Teile der Cannabis-Pflanze benennen" |
| **Timeline** | Prozesse | "Vom Samen zur Ernte" |

---

## Deployment-Checkliste

Vor Kursveröffentlichung prüfen:

- [ ] Alle Lernziele klar definiert?
- [ ] Sections logisch strukturiert?
- [ ] Labels mit CSS-Styling (BS:WI Farben)?
- [ ] Quellen in jeder Section angegeben?
- [ ] H5P-Quizze funktionieren?
- [ ] Abschlusstest vorhanden (bei Pflichtkursen)?
- [ ] Barrierefreiheit (Alt-Texte, Kontrast)?
- [ ] Links aktuell & erreichbar?
- [ ] Zertifikat konfiguriert?
- [ ] Teilnehmer korrekt eingeschrieben?

---

## Beispiel-Code: Kurs erstellen (Moodle MCP)

```javascript
// 1. Kurs anlegen
const course = await moodle_create_course({
  fullname: "CSC Pflichtschulung für neue Mitglieder",
  shortname: "CSC-PFLICHT-2026",
  categoryid: 2, // CSC-Kategorie
  summary: "Einführung in Vereinsrecht, CanG, Prävention und Hausordnung. Pflichtschulung für alle neuen Mitglieder der Solidarischen Hanfwirtschaft.",
  format: "topics" // oder "weeks"
});

// 2. Section 1 erstellen
const section1 = await moodle_create_section({
  courseid: course.id,
  name: "1. Willkommen & Vereinsrecht",
  summary: "Lerne unseren Verein, die Satzung und deine Rechte als Mitglied kennen."
});

// 3. Begrüßungslabel erstellen
await moodle_create_label({
  courseid: course.id,
  section: 1,
  name: "Willkommen",
  intro: `<div style="background: linear-gradient(135deg, #003366 0%, #00A3E0 100%);
                      color: white; padding: 25px; border-radius: 8px;
                      margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                      text-align: center;">
            <h2 style="margin: 0 0 15px 0; color: white; font-size: 24px;">🌿 Willkommen bei der Solidarischen Hanfwirtschaft</h2>
            <p style="margin: 0; font-size: 16px; line-height: 1.6;">
              Diese Schulung ist Pflicht für alle neuen Mitglieder. Du lernst hier alles Wichtige über unseren Verein,
              deine Rechte und Pflichten, und den verantwortungsvollen Umgang mit Cannabis.
            </p>
            <p style="margin: 15px 0 0 0; font-size: 14px;">⏱️ Dauer: ca. 90 Minuten | 📝 Abschlusstest erforderlich</p>
          </div>`
});

// 4. Page "Unsere Satzung" erstellen
await moodle_create_page({
  courseid: course.id,
  section: 1,
  name: "Unsere Satzung",
  content: `<h2>Satzung der Solidarischen Hanfwirtschaft e.V.</h2>
            <p>Unsere Anbauvereinigung ist ein eingetragener, gemeinnütziger Verein nach § 11 CanG...</p>
            <!-- Weitere Inhalte -->`
});

// 5. H5P-Quiz hochladen und Aktivität erstellen
const h5pFile = await moodle_upload_h5p({
  filepath: "C:/path/to/vereinsrecht-quiz.h5p"
});

await moodle_create_h5p_activity({
  courseid: course.id,
  section: 1,
  name: "Quiz: Vereinsrecht",
  h5pfileid: h5pFile.itemid
});

console.log(`✅ Kurs erstellt: https://moodle.dirk-schulenburg.net/course/view.php?id=${course.id}`);
```

---

## Updates & Ergänzungen

**Letzte Aktualisierung:** 2026-02-08

**Neue Vorlagen hinzufügen:**
- Kursstruktur dokumentieren
- Lernziele definieren
- Beispiel-Code bereitstellen

**Vorlagen anpassen:**
- Bei Gesetzesänderungen (CanG-Updates)
- Bei neuen wissenschaftlichen Erkenntnissen
- Nach Feedback von Teilnehmern
