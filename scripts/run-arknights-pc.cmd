@echo off
chcp 65001 >nul
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run-arknights-pc.ps1" %*
if errorlevel 1 (
  echo.
  echo Game build/start failed. Check Git, Python, Godot and terminal errors.
  pause
)
