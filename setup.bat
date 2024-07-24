@echo off
setlocal

:: setup venv
if not exist "venv" (
    echo Setting up virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

:: install dependencies
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found.
)

echo Setup completed.
pause
endlocal
