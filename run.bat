cd /d %~dp0
set PYTHONPATH=%cd%
.\venv\Scripts\python.exe src\main.py
pause