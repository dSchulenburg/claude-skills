@echo off
REM ========================================
REM Claude Skills Installation Script
REM ========================================
REM
REM Dieses Script kopiert deine Custom Skills
REM in das Claude Desktop Skills-Verzeichnis
REM
REM Autor: Dirk
REM Datum: 03.01.2026
REM ========================================

echo.
echo ========================================
echo  Claude Skills Installation
echo ========================================
echo.

REM Definiere Pfade
set "SOURCE_DIR=C:\Users\mail\OneDrive\Dokumente\EigeneProjekte\dev\claude-skills"
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

REM Kopiere Skills
echo [1/2] Kopiere blog-article-workflow...
if exist "%SOURCE_DIR%\blog-article-workflow" (
    xcopy /E /I /Y "%SOURCE_DIR%\blog-article-workflow" "%TARGET_DIR%\blog-article-workflow" >nul
    echo       DONE: blog-article-workflow kopiert
) else (
    echo       WARNUNG: blog-article-workflow nicht gefunden!
)

echo.
echo [2/2] Kopiere h5p-wordpress-workflow...
if exist "%SOURCE_DIR%\h5p-wordpress-workflow" (
    xcopy /E /I /Y "%SOURCE_DIR%\h5p-wordpress-workflow" "%TARGET_DIR%\h5p-wordpress-workflow" >nul
    echo       DONE: h5p-wordpress-workflow kopiert
) else (
    echo       WARNUNG: h5p-wordpress-workflow nicht gefunden!
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
echo 3. Teste mit diesem Prompt:
echo    "Erstelle einen Blog-Artikel ueber Git Workflows"
echo.
echo Claude sollte jetzt automatisch den
echo blog-article-workflow Skill nutzen!
echo.
echo ========================================
echo.
echo Skills installiert in:
echo %TARGET_DIR%
echo.
echo Druecke eine Taste zum Beenden...
pause >nul
