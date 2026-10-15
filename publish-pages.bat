@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0publish-pages.ps1"
if errorlevel 1 (echo.&echo Publication failed. See the error above.)
pause
