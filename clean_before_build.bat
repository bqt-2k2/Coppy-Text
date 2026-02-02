@echo off
chcp 65001 >nul
echo Dang don dep truoc khi build...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM CopyTextApp.exe /T >nul 2>&1
taskkill /F /IM Setup.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul
if exist "dist\CopyTextApp.exe" del /F /Q "dist\CopyTextApp.exe" >nul 2>&1
if exist "build" rmdir /s /q "build" >nul 2>&1
if exist "dist\CopyTextApp" rmdir /s /q "dist\CopyTextApp" >nul 2>&1
if exist "CopyTextApp.spec" del /F /Q "CopyTextApp.spec" >nul 2>&1
echo Da don dep xong!

