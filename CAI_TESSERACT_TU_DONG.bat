@echo off
chcp 65001 >nul
title Tu dong cai dat Tesseract OCR
color 0B

net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Da co quyen Administrator
    goto :run
) else (
    echo [WARNING] Chua co quyen Administrator!
    echo.
    echo Script can quyen Administrator de cai dat.
    echo Dang mo lai voi quyen Administrator...
    echo.
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run
echo.
echo ============================================================
echo    TU DONG CAI DAT TESSERACT OCR
echo ============================================================
echo.
echo Script nay se:
echo - Tu dong tai Tesseract OCR
echo - Tu dong cai dat vao: C:\Program Files\Tesseract-OCR
echo - Khong can can thiep cua nguoi dung
echo.
echo Luu y: Can ket noi internet
echo.
pause
echo.

python tesseract_installer.py

echo.
echo ============================================================
pause

