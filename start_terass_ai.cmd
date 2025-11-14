@echo off
REM Windows launcher for TERASS業動サポートAI desktop app.
REM This batch file calls the accompanying PowerShell script with the
REM appropriate execution policy to set up the environment and start
REM the application. Double-click this file to run the app.

setlocal

REM Determine the absolute path to the scripts directory
set SCRIPT_DIR=%~dp0scripts

REM Use PowerShell with -NoProfile to avoid loading the user's profile
powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%\start_desktop.ps1"

endlocal
