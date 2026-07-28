@echo off
setlocal enabledelayedexpansion

set ENV_NAME=ai-agent
set MODEL=qwen2.5-coder:32b
set OLLAMA_URL=http://localhost:11434

echo ==================================
echo Starting AI coding environment
echo ==================================

REM ----------------------------------
REM Check project path
REM ----------------------------------

if "%~1"=="" (
    set PROJECT_PATH=%CD%
) else (
    set PROJECT_PATH=%~1
)

if not exist "%PROJECT_PATH%" (
    echo ERROR: Project path does not exist:
    echo %PROJECT_PATH%
    pause
    exit /b 1
)

echo Project:
echo %PROJECT_PATH%

REM ----------------------------------
REM Check Conda
REM ----------------------------------

echo.
echo Checking Conda...

where conda >nul 2>&1

if errorlevel 1 (
    echo ERROR: Conda not found.
    pause
    exit /b 1
)

REM ----------------------------------
REM Create Conda environment if missing
REM ----------------------------------

echo Checking environment...

conda env list | findstr "%ENV_NAME%" >nul

if errorlevel 1 (
    echo Environment missing.
    echo Creating %ENV_NAME%...

    conda env create -f "%~dp0..\environment.yml"

    if errorlevel 1 (
        echo Failed creating Conda environment.
        pause
        exit /b 1
    )
)

echo Activating environment...

call conda activate %ENV_NAME%

if errorlevel 1 (
    echo Failed activating environment.
    pause
    exit /b 1
)

REM ----------------------------------
REM Check Ollama
REM ----------------------------------

echo.
echo Checking Ollama...

where ollama >nul 2>&1

if errorlevel 1 (
    echo ERROR: Ollama not installed.
    pause
    exit /b 1
)

REM Check whether Ollama server responds

powershell -Command "try { Invoke-WebRequest -Uri %OLLAMA_URL% -UseBasicParsing -TimeoutSec 2 | Out-Null; exit 0 } catch { exit 1 }"

if errorlevel 1 (
    echo Starting Ollama...
    start "" ollama serve
    timeout /t 5 >nul
) else (
    echo Ollama already running.
)

REM ----------------------------------
REM Check model
REM ----------------------------------

echo.
echo Checking model:

ollama list | findstr "%MODEL%" >nul

if errorlevel 1 (
    echo Model missing:
    echo %MODEL%

    echo Pulling model...
    ollama pull %MODEL%

    if errorlevel 1 (
        echo Failed pulling model.
        pause
        exit /b 1
    )
)

REM ----------------------------------
REM Start Aider
REM ----------------------------------

echo.
echo Starting Aider...

cd /d "%PROJECT_PATH%"

set OLLAMA_API_BASE=%OLLAMA_URL%

aider ^
 --config "%~dp0..\config\aider.conf.yml" ^
 --read "%~dp0..\prompts\coding-agent.md"

pause