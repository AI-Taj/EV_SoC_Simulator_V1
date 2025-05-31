@echo off
echo Adding all changes and committing...
cd /d "C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1"
git add .
set /p MESSAGE="Enter commit message: "
git commit -m "%MESSAGE%"
git push origin main
pause
