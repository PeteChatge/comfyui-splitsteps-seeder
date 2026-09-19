@echo off
REM Holen: pull von GitHub, kopiert Backup zurueck nach ComfyUI
setlocal
set REPO=%~dp0..
set PROJEKT=C:\Users\Olaf\Downloads\ComfyUI\ComfyUI_windows_portable_cuda130\ComfyUI\user\default\workflows\_PROJEKT-SplitSampler
set BACKUP=%REPO%\comfyui_projekt_backup
cd /d "%REPO%"
echo ===== PULL von GitHub =====
git pull --ff-only
if errorlevel 1 echo FEHLER beim Pull - ggf. erst projekt_sichern_push.bat laufen lassen. & pause & exit /b 1
if not exist "%BACKUP%" echo FEHLER: kein Backup im Repo. & pause & exit /b 1
if not exist "%PROJEKT%" mkdir "%PROJEKT%"
echo ===== KOPIERE Backup --^> ComfyUI =====
robocopy "%BACKUP%" "%PROJEKT%" /MIR /XD .git __pycache__ /XF *.log /NJH /NJS
if errorlevel 8 echo FEHLER beim Kopieren & pause & exit /b 1
echo.
echo Fertig. ComfyUI ggf. neu laden (Workflows-Liste aktualisieren).
pause
