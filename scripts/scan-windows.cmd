@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0.."
set "GAME_DIR=%~1"
if "%GAME_DIR%"=="" (
  echo 请拖拽本地游戏文件夹到本脚本上，或输入目录路径。
  set /p GAME_DIR=文件夹路径：
)
if not exist "%GAME_DIR%\" (
  echo 路径不存在：%GAME_DIR%
  pause
  exit /b 1
)
where py >nul 2>nul
if %ERRORLEVEL%==0 (
  set "PY=py -3"
) else (
  set "PY=python"
)
if not exist "reports" mkdir "reports"
set "PYTHONPATH=%CD%\src"
%PY% -m erlab scan "%GAME_DIR%" --out "reports\latest-scan.json"
if errorlevel 1 (
  echo 扫描失败，请确认已经安装 Python 3.10 或以上版本。
  pause
  exit /b 1
)
echo 扫描成功：reports\latest-scan.json
pause
