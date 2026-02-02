@echo off
chcp 65001 >nul
title Dong goi app de phan phoi
color 0A
echo.
echo ========================================
echo DONG GOI APP DE PHAN PHOI
echo Tac gia: Bui Quang Tien THDD
echo ========================================
echo.

set "APP_NAME=CopyTextApp"
set "APP_VERSION=1.0.0"
set "AUTHOR=BuiQuangTienTHDD"

echo [1/3] Dang tao phien ban PORTABLE (chi file exe)...
set "portable_zip=%APP_NAME%_v%APP_VERSION%_PORTABLE_%AUTHOR%.zip"
set "portable_path=dist\%portable_zip%"

if exist "%portable_path%" del /q "%portable_path%"

powershell -Command "Compress-Archive -Path 'dist\CopyTextApp.exe' -DestinationPath '%portable_path%' -Force"

if errorlevel 1 (
    echo ❌ Loi khi tao file ZIP portable!
) else (
    echo ✅ Da tao file ZIP portable: %portable_zip%
    for %%I in ("%portable_path%") do set "size_bytes=%%~zI"
    set /a size_mb=!size_bytes! / 1048576
    echo    Kich thuoc: !size_mb! MB
)

echo.
echo [2/3] Dang tao phien ban INSTALLER (voi Setup.exe)...
set "installer_zip=%APP_NAME%_v%APP_VERSION%_INSTALLER_%AUTHOR%.zip"
set "installer_path=dist\%installer_zip%"

if exist "%installer_path%" del /q "%installer_path%"

powershell -Command "Compress-Archive -Path 'dist\CopyTextApp\*' -DestinationPath '%installer_path%' -Force"

if errorlevel 1 (
    echo ❌ Loi khi tao file ZIP installer!
) else (
    echo ✅ Da tao file ZIP installer: %installer_zip%
    for %%I in ("%installer_path%") do set "size_bytes=%%~zI"
    set /a size_mb=!size_bytes! / 1048576
    echo    Kich thuoc: !size_mb! MB
)

echo.
echo [3/3] Thong tin phan phoi:
echo.
echo ========================================
echo ✅ HOAN TAT!
echo ========================================
echo.
echo PHIEN BAN PORTABLE (Chay truc tiep):
echo   File: %portable_zip%
echo   Vi tri: %portable_path%
echo   Cach dung: Giai nen va chay CopyTextApp.exe
echo   Uu diem: Khong can cai dat, chay ngay
echo.
echo PHIEN BAN INSTALLER (Cai dat nhu app thuong):
echo   File: %installer_zip%
echo   Vi tri: %installer_path%
echo   Cach dung: Giai nen va chay Setup.exe
echo   Uu diem: Tu dong cai dat, tao shortcut, giong Zalo/Unikey
echo.
echo ========================================
echo HUONG DAN PHAN PHOI:
echo ========================================
echo.
echo 1. PHIEN BAN PORTABLE:
echo    - Gui file: %portable_zip%
echo    - Nguoi dung giai nen va chay CopyTextApp.exe
echo    - Khong can cai dat, chay ngay
echo.
echo 2. PHIEN BAN INSTALLER (KHUYEN NGHI):
echo    - Gui file: %installer_zip%
echo    - Nguoi dung giai nen va chay Setup.exe
echo    - Tu dong cai dat, tao shortcut Desktop va Start Menu
echo    - Sau khi cai xong, tim app trong Start Menu hoac Desktop
echo.
echo Tac gia: Bui Quang Tien THDD
echo.
pause

