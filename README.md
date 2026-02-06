# Build Instructions

## Building CopyTextApp.exe

```bash
pyinstaller --onefile --console --name=CopyTextApp --clean --noconfirm main.py
```

## Building Setup.exe

```bash
pyinstaller --onefile --console --name=Setup --clean --noconfirm installer.py
```

## Tesseract OCR Auto-Installation

The project includes automatic Tesseract installation:
- `CAI_TESSERACT_TU_DONG.bat` - Batch file to run automatic installation
- `tesseract_installer.py` - Python script that downloads, installs, and adds Tesseract to PATH
- `installer.py` - Main installer that includes Tesseract installation during app setup

Features:
- Automatically downloads Tesseract OCR installer
- Installs silently without user intervention
- Adds Tesseract to system PATH (with fallback to user PATH)
- Supports Windows 10 and later

### Requirements
- Python 3.x
- PyInstaller installed (`pip install pyinstaller`)
- Windows operating system (for Tesseract auto-install)

