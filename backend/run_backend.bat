@echo off
cd /d "c:\Users\kusum\OneDrive\Desktop\resume-analyser\backend"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
