@echo off
chcp 65001 >nul
cd /d "%~dp0.."
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0run-offline.ps1" %*
if errorlevel 1 (
  echo Startup failed. Install Git, Python 3 and compatible Godot.
  pause
)
