@echo off
title MediaMerge Platform Launcher
echo ========================================================
echo  Launching MediaMerge Full-Stack Platform (P11)
echo  Backend:  http://127.0.0.1:8000
echo  Frontend: http://127.0.0.1:3000
echo ========================================================
start "MediaMerge Backend" cmd /k "cd /d %~dp0backend && .\venv\Scripts\activate && python manage.py runserver 8000"
timeout /t 3 /nobreak >nul
start "MediaMerge Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 2 /nobreak >nul
start http://localhost:3000
echo MediaMerge platform started successfully!
pause
