@echo off
title MediaMerge Django REST Backend
cd /d "%~dp0backend"
echo ========================================================
echo  Starting MediaMerge Django REST Backend (Port 8000)
echo ========================================================
call .\venv\Scripts\activate
python manage.py runserver 8000
pause
