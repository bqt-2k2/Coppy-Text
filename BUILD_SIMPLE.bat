@echo off
chcp 65001 >nul
title Build CopyText App - One File
color 0A
echo.
echo ========================================
echo BUILD COPYTEXT APP - ONE FILE
echo Tac gia: Bui Quang Tien THDD
echo ========================================
echo.

echo [1/3] Dang build app thanh one-file executable...
pyinstaller --onefile --windowed --name=CopyTextApp --clean --noconfirm --hidden-import=pytesseract --hidden-import=PIL --hidden-import=numpy --hidden-import=pyperclip --hidden-import=easyocr main.py

if errorlevel 1 (
    echo.
    echo ❌ Loi khi build!
    pause
    exit /b 1
)

echo.
echo [2/3] Dang tao file ZIP de phan phoi...
set "APP_NAME=CopyTextApp"
set "APP_VERSION=1.0.0"
set "AUTHOR=BuiQuangTienTHDD"
set "zip_filename=%APP_NAME%_v%APP_VERSION%_ONE_FILE_%AUTHOR%.zip"
set "zip_path=dist\%zip_filename%"

if exist "%zip_path%" del /q "%zip_path%"

powershell -Command "Compress-Archive -Path 'dist\%APP_NAME%.exe' -DestinationPath '%zip_path%' -Force"

if errorlevel 1 (
    echo ❌ Loi khi tao file ZIP!
    pause
    exit /b 1
)

for %%I in ("%zip_path%") do set "size_bytes=%%~zI"
setlocal enabledelayedexpansion
set /a size_mb=!size_bytes! / 1048576

echo.
echo [3/3] Hoan tat!
echo.
echo ========================================
echo ✅ BUILD THANH CONG!
echo ========================================
echo.
echo File exe: dist\CopyTextApp.exe
echo File ZIP: %zip_path%
echo Kich thuoc: !size_mb! MB
echo.
echo ========================================
echo HUONG DAN PHAN PHOI:
echo ========================================
echo.
echo CACH 1: Gui file ZIP
echo   - File: %zip_filename%
echo   - Nguoi dung giai nen va chay CopyTextApp.exe
echo   - Khong can cai dat, chay ngay
echo.
echo CACH 2: Gui file exe truc tiep
echo   - File: dist\CopyTextApp.exe
echo   - Nguoi dung chay truc tiep
echo   - Khong can cai dat, chay ngay
echo.
echo ========================================
echo LUU Y:
echo ========================================
echo - One-file version: Khong can Setup.exe
echo - Nguoi dung chi can chay CopyTextApp.exe
echo - App se tu dong tim Tesseract hoac dung EasyOCR
echo - EasyOCR models se duoc tai tu dong lan dau chay
echo.
echo Tac gia: Bui Quang Tien THDD
echo.
pause

