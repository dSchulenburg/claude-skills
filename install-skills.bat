@echo off
REM ========================================
REM Claude Skills Installation Script
REM ========================================
REM
REM Kopiert alle Skills aus dem Docker-Repo
REM in das Claude Desktop Skills-Verzeichnis
REM
REM Autor: Dirk
REM Aktualisiert: 19.01.2026
REM ========================================

echo.
echo ========================================
echo  Claude Skills Installation
echo ========================================
echo.

REM Definiere Pfade
set "SOURCE_DIR=C:\Users\mail\entwicklung\docker\claude-skills"
set "TARGET_DIR=%APPDATA%\Claude\skills"

echo Source: %SOURCE_DIR%
echo Target: %TARGET_DIR%
echo.

REM Erstelle Target-Verzeichnis falls nicht vorhanden
if not exist "%TARGET_DIR%" (
    echo [INFO] Erstelle Skills-Verzeichnis: %TARGET_DIR%
    mkdir "%TARGET_DIR%"
    echo.
)

REM Liste aller Skills (nur Ordner mit SKILL.md)
echo Kopiere Skills...
echo.

REM DevOps Agent Skills
echo [DevOps Agent]
for %%S in (coding-agent debug-agent documentation-agent docker-management mcp-server-deploy n8n-workflow) do (
    if exist "%SOURCE_DIR%\%%S\SKILL.md" (
        xcopy /E /I /Y "%SOURCE_DIR%\%%S" "%TARGET_DIR%\%%S" >nul 2>&1
        echo   [OK] %%S
    ) else (
        echo   [--] %%S (keine SKILL.md)
    )
)
echo.

REM Education Agent Skills
echo [Education Agent]
for %%S in (bswi-infobrief h5p-designer h5p-generator h5p-wordpress-workflow lernfeld-zu-moodle-kurs moodle-course-workflow moodle-section-analyzer moodle-section-optimizer) do (
    if exist "%SOURCE_DIR%\%%S\SKILL.md" (
        xcopy /E /I /Y "%SOURCE_DIR%\%%S" "%TARGET_DIR%\%%S" >nul 2>&1
        echo   [OK] %%S
    ) else (
        echo   [--] %%S (keine SKILL.md)
    )
)
echo.

REM Personal Agent Skills
echo [Personal Agent]
for %%S in (blog-article-workflow recherche-workflow) do (
    if exist "%SOURCE_DIR%\%%S\SKILL.md" (
        xcopy /E /I /Y "%SOURCE_DIR%\%%S" "%TARGET_DIR%\%%S" >nul 2>&1
        echo   [OK] %%S
    ) else (
        echo   [--] %%S (keine SKILL.md)
    )
)
echo.

echo ========================================
echo  Installation abgeschlossen!
echo ========================================
echo.
echo Naechste Schritte:
echo.
echo 1. Claude Desktop KOMPLETT schliessen
echo    (auch im System Tray beenden!)
echo.
echo 2. Claude Desktop neu starten
echo.
echo Skills installiert in:
echo %TARGET_DIR%
echo.
echo ========================================
echo.
echo Druecke eine Taste zum Beenden...
pause >nul
