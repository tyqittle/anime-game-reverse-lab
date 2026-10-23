@echo off
chcp 65001 >nul
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-arknights-solo.ps1" %*
if errorlevel 1 (
  echo.
  echo Start failed. Check Node.js 22+, Git, and the pinned upstream source.
  pause
)
