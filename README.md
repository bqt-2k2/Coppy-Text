# Build Instructions

## Building CopyTextApp.exe

```bash
pyinstaller --onefile --console --name=CopyTextApp --clean --noconfirm main.py
```

## Building Setup.exe

```bash
pyinstaller --onefile --console --name=Setup --clean --noconfirm installer.py
```

### Requirements
- Python 3.x
- PyInstaller installed (`pip install pyinstaller`)

