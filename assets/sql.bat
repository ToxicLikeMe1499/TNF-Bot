@echo off

REM Check if the script is running with administrative privileges
NET SESSION >nul 2>&1
if %errorLevel% == 0 (
    echo Administrative privileges detected. Proceeding with the script.
) else (
    PowerShell -Command "Start-Process '%0' -Verb RunAs"
    exit /b
)

net start MySQL80
