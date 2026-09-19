@echo off
REM Projekt-Status: zeigt Git-Status + Unterschiede ComfyUI <-> Backup (nur Anzeige, aendert nichts)
setlocal
set REPO=%~dp0..
set PROJEKT=C:\Users\Olaf\Downloads\ComfyUI\ComfyUI_windows_portable_cuda130\ComfyUI\user\default\workflows\_PROJEKT-SplitSampler
set BACKUP=%REPO%\comfyui_projekt_backup
cd /d "%REPO%"
echo ===== GIT STATUS =====
git status --short --branch
echo.
echo ===== LETZTE COMMITS =====
git log --oneline -5
echo.
echo ===== UNTERSCHIEDE ComfyUI --^> Backup (Liste, ohne Kopieren) =====
if not exist "%BACKUP%" echo (noch kein Backup vorhanden)
robocopy "%PROJEKT%" "%BACKUP%" /MIR /L /NJH /NJS /NDL /NP /XD .git __pycache__ /XF *.log
echo.
echo Fertig. Zum Sichern: projekt_sichern_push.bat  Zum Holen: projekt_holen_pull.bat
pause
