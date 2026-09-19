@echo off
REM Sichern: kopiert _PROJEKT-SplitSampler aus ComfyUI ins Repo-Backup, commit + push nach GitHub
setlocal
set REPO=%~dp0..
set PROJEKT=C:\Users\Olaf\Downloads\ComfyUI\ComfyUI_windows_portable_cuda130\ComfyUI\user\default\workflows\_PROJEKT-SplitSampler
set BACKUP=%REPO%\comfyui_projekt_backup
if not exist "%PROJEKT%" echo FEHLER: Projekt-Ordner nicht gefunden: %PROJEKT% & pause & exit /b 1
if not exist "%BACKUP%" mkdir "%BACKUP%"
echo ===== KOPIERE ComfyUI --^> Backup =====
robocopy "%PROJEKT%" "%BACKUP%" /MIR /XD .git __pycache__ /XF *.log /NJH /NJS
if errorlevel 8 echo FEHLER beim Kopieren & pause & exit /b 1
cd /d "%REPO%"
git add -A
git diff --cached --quiet
if errorlevel 1 goto COMMIT
echo Nichts zu sichern - alles schon auf GitHub.
pause
exit /b 0
:COMMIT
for /f "tokens=*" %%d in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm"') do set STEMP=%%d
git commit -m "Projekt-Backup %STEMP%"
git push
if errorlevel 1 echo FEHLER beim Push - ggf. erst projekt_holen_pull.bat laufen lassen. & pause & exit /b 1
echo.
echo Gesichert und gepusht.
pause
