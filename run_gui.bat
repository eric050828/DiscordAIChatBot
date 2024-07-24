@REM @echo off
@REM set BATCHPATH=%~dp0
@REM %BATCHPATH%venv\Scripts\pythonw.exe  %BATCHPATH%src\gui.py
@REM exit
@echo off
set PYTHONPATH=%cd%
.\venv\Scripts\python.exe .\src\gui.py
exit