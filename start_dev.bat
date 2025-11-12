@echo off
REM Script para Windows (CMD) que activa el venv y arranca el servidor en 8001
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
) else (
    echo No se detecto .venv\Scripts\activate.bat. Asegurate de crear el venv primero.
    exit /b 1
)
python manage.py runserver 8001
