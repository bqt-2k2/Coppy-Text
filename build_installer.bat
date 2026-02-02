@echo off
chcp 65001 >nul
echo ========================================
echo Building CopyText App with Installer...
echo Tac gia: Bui Quang Tien THDD
echo ========================================
echo.

echo [0/6] Cleaning old build files...
call clean_before_build.bat
echo.

echo [1/6] Installing dependencies...
pip install pyinstaller --quiet
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo Loi khi cai dat dependencies!
    pause
    exit /b 1
)
echo Da cai dat dependencies

echo.
echo [2/6] Preloading EasyOCR models (if available)...
python preload_models.py 2>nul
echo Da preload models (neu co)

echo.
echo [3/6] Building main executable...
pyinstaller --onefile --windowed --name=CopyTextApp --clean --noconfirm --hidden-import=pytesseract --hidden-import=PIL --hidden-import=numpy --hidden-import=pyperclip --hidden-import=easyocr main.py

if errorlevel 1 (
    echo Loi khi build!
    pause
    exit /b 1
)

echo.
echo [4/6] Creating installation package...
if not exist "dist\CopyTextApp" mkdir "dist\CopyTextApp"
copy "dist\CopyTextApp.exe" "dist\CopyTextApp\" >nul 2>&1
copy "HUONG_DAN_CAI_DAT_CHO_NGUOI_KHAC.md" "dist\CopyTextApp\" >nul 2>&1
copy "LICENSE.txt" "dist\CopyTextApp\" >nul 2>&1
rem Removed: CAI_TESSERACT_TU_DONG.bat - installer.py handles Tesseract automatically

echo.
echo [5/6] Bundling dependencies (Tesseract + EasyOCR models)...
python bundle_dependencies.py
if errorlevel 1 (
    echo ⚠️  Khong the bundle dependencies. App van co the chay nhung can cai them.
)

echo.
echo [6/6] Building installer...
cd dist\CopyTextApp
copy "..\..\installer.py" "installer.py" >nul 2>&1
pyinstaller --onefile --console --name=Setup --clean --noconfirm installer.py
if errorlevel 1 (
    echo ⚠️  Khong the build installer. Nguoi dung co the chay installer.py truc tiep.
) else (
    move "dist\Setup.exe" "Setup.exe" >nul 2>&1
    rmdir /s /q "build" "dist" >nul 2>&1
    del "installer.py" >nul 2>&1
    del "Setup.spec" >nul 2>&1
    echo ✅ Da tao Setup.exe
)
cd ..\..

echo.
echo ========================================
echo Build complete!
echo ========================================
echo.
echo File .exe: dist\CopyTextApp\CopyTextApp.exe
echo Installer: dist\CopyTextApp\Setup.exe
echo Package: dist\CopyTextApp\
echo.
echo Huong dan phan phoi:
echo 1. Gui toan bo thu muc dist\CopyTextApp\ cho nguoi dung
echo 2. Nguoi dung chay Setup.exe de cai dat
echo 3. Sau khi cai xong, app se tu dong chay
echo.
echo Tac gia: Bui Quang Tien THDD
echo.
pause
