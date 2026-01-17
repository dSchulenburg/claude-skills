# Skills für Claude.ai Upload vorbereiten
# Ausführen in PowerShell

$skillsPath = "C:\Users\mail\entwicklung\docker\claude-skills"
$outputPath = "C:\Users\mail\entwicklung\docker\claude-skills\claude-ai-skills-upload.zip"

# Fehlende Skills in Claude.ai
$skillsToUpload = @(
    "bswi-infobrief",
    "h5p-generator",
    "recherche-workflow",
    "moodle-course-workflow",
    "lernfeld-zu-moodle-kurs"
)

# Temporäres Verzeichnis erstellen
$tempDir = "$env:TEMP\claude-skills-upload"
if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force }
New-Item -ItemType Directory -Path $tempDir | Out-Null

# Skills kopieren
foreach ($skill in $skillsToUpload) {
    $source = Join-Path $skillsPath $skill
    $dest = Join-Path $tempDir $skill
    if (Test-Path $source) {
        Copy-Item -Path $source -Destination $dest -Recurse
        Write-Host "✓ $skill kopiert" -ForegroundColor Green
    } else {
        Write-Host "✗ $skill nicht gefunden" -ForegroundColor Red
    }
}

# ZIP erstellen
if (Test-Path $outputPath) { Remove-Item $outputPath -Force }
Compress-Archive -Path "$tempDir\*" -DestinationPath $outputPath -Force

# Aufräumen
Remove-Item $tempDir -Recurse -Force

Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host " ZIP erstellt: $outputPath" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Nächste Schritte:" -ForegroundColor Yellow
Write-Host "1. Öffne Claude.ai"
Write-Host "2. Gehe zu Project Settings → Project Knowledge"
Write-Host "3. Klicke 'Add Files'"
Write-Host "4. Wähle: $outputPath"
Write-Host ""
