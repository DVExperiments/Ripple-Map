@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
  py -3 preview.py
) else (
  where python >nul 2>nul
  if %ERRORLEVEL% EQU 0 (
    python preview.py
  ) else (
    echo Python was not found. Double-click index.html to open Ripple Map without Python.
    pause
  )
)
