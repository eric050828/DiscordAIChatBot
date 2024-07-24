@echo off
setlocal

:: check if Git is installed
echo Checking for Git...
where git >nul 2>&1
if ERRORLEVEL 1 (
    echo Git is not installed.
    echo Please install Git from https://git-scm.com/download/win
    pause
    exit /b 1
)

:: go to project directory
cd /d %~dp0

if not exist ".git" (
    echo initialize git
    git init
    git branch -M main
)

:: remote
echo Checking remote repository configuration...
git remote -v
if ERRORLEVEL 1 (
    echo No remote repository configured.
    echo remote repository configuring...
    git remote add origin https://github.com/eric050828/DiscordAIChatBot.git
)

:: fetch lecal repo status
echo Fetching the current status of the local repository...
git fetch

:: check update
echo Checking for updates...
for /f "tokens=*" %%i in ('git rev-parse HEAD') do set LOCAL_COMMIT=%%i
for /f "tokens=*" %%i in ('git rev-parse @{u}') do set REMOTE_COMMIT=%%i

:: pull new change
if "%LOCAL_COMMIT%" == "%REMOTE_COMMIT%" (
    echo Already up to date.
) else (
    echo New updates found. Pulling latest changes...
    git pull https://github.com/eric050828/DiscordAIChatBot.git main
    if ERRORLEVEL 1 (
        echo Failed to pull the latest changes.
        pause
        exit /b 1
    )
    echo Updates applied successfully.
)

pause
endlocal