# -*- coding: utf-8 -*-
"""
CopyText App Installer
Tác giả: Bùi Quang Tiến THĐD
"""
import os
import sys
import shutil
import subprocess
import ctypes
import urllib.request
import tempfile
import time
import winreg

APP_NAME = "CopyText App"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Bùi Quang Tiến THĐD"
INSTALL_DIR = os.path.join(os.getenv('PROGRAMFILES', 'C:\\Program Files'), 'CopyTextApp') 
USER_INSTALL_DIR = os.path.join(os.getenv('LOCALAPPDATA', os.path.expanduser('~\\AppData\\Local')), 'CopyTextApp')

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if is_admin():
        return True
    else:
        print("⚠️  Cần quyền Administrator để cài đặt!")
        print("Đang yêu cầu quyền Admin...")
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{__file__}"', None, 1
            )
        except:
            print("❌ Không thể chạy với quyền Admin!")
            input("Nhấn Enter để thoát...")
        return False

def download_tesseract_installer():
    """Tải Tesseract installer về"""
    try:
        print("  📥 Đang tải Tesseract OCR installer...")
        print("  💡 Quá trình này có thể mất vài phút, vui lòng chờ...")
        
        # URL của Tesseract installer từ UB Mannheim (thử nhiều URL)
        urls = [
            # "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.4.0.20240605.exe",
            # "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe",
            # "https://github.com/UB-Mannheim/tesseract/releases/download/v5.4.0.20240605/tesseract-ocr-w64-setup-5.4.0.20240605.exe",
            # "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.1.20230401/tesseract-ocr-w64-setup-5.3.1.20230401.exe",
            "https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe",
        ]
        
        temp_dir = tempfile.gettempdir()
        installer_path = os.path.join(temp_dir, 'tesseract_installer.exe')
        
        # Xóa file cũ nếu có
        if os.path.exists(installer_path):
            try:
                os.remove(installer_path)
            except:
                pass
        
        # Tải file với progress
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, int(downloaded * 100 / total_size)) if total_size > 0 else 0
            if block_num % 10 == 0:  # Update mỗi 10 blocks
                print(f"  📥 Đã tải: {percent}%", end='\r')
        
        # Thử từng URL cho đến khi thành công
        for url in urls:
            try:
                print(f"  Đang thử URL: {url.split('/')[-1]}")
                urllib.request.urlretrieve(url, installer_path, show_progress)
                print(f"  ✅ Đã tải xong: {os.path.basename(installer_path)}")
                return installer_path
            except Exception as e:
                print(f"  ⚠️  URL này không khả dụng: {str(e)}")
                continue
        
        # Nếu tất cả URL đều thất bại
        print(f"  ❌ Không thể tải từ bất kỳ URL nào")
        return None
    except Exception as e:
        print(f"  ⚠️  Lỗi khi tải Tesseract installer: {str(e)}")
        return None

def install_tesseract_silent(installer_path):
    """Cài đặt Tesseract một cách im lặng - thử nhiều cách"""
    print("  🔧 Đang cài đặt Tesseract OCR (silent mode)...")
    print("  💡 Quá trình này có thể mất vài phút, vui lòng chờ...")
    
    install_dir = r"C:\Program Files\Tesseract-OCR"
    
    # Thử nhiều cách cài đặt silent
    silent_params_list = [
        (['/S', f'/D={install_dir}'], "Standard silent"),
        (['/S', '/NCRC', f'/D={install_dir}'], "Silent + no CRC check"),
        (['/VERYSILENT', '/NORESTART', f'/DIR={install_dir}'], "Very silent (Inno Setup)"),
        (['/SILENT', '/NORESTART', f'/DIR={install_dir}'], "Silent (Inno Setup)"),
    ]
    
    for params, desc in silent_params_list:
        try:
            cmd = [installer_path] + params
            print(f"  Đang thử: {desc}...")
            result = subprocess.run(cmd, capture_output=True, timeout=600, text=True)
            
            # Đợi và kiểm tra nhiều lần
            for wait_time in [2, 5, 10, 15]:
                time.sleep(wait_time)
                tesseract_exe = os.path.join(install_dir, 'tesseract.exe')
                if os.path.exists(tesseract_exe):
                    print(f"  ✅ Đã cài đặt Tesseract thành công tại: {install_dir}")
                    return True
            
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  Cài đặt quá lâu với {desc}, thử cách khác...")
            # Kiểm tra xem có cài được không
            tesseract_exe = os.path.join(install_dir, 'tesseract.exe')
            if os.path.exists(tesseract_exe):
                print(f"  ✅ Tesseract đã được cài đặt tại: {tesseract_exe}")
                return True
            continue
        except Exception as e:
            print(f"  ⚠️  Lỗi với {desc}: {str(e)}")
            continue
    
    # Kiểm tra lại sau tất cả các lần thử
    print("  Đang kiểm tra lại...")
    time.sleep(5)
    tesseract_exe = os.path.join(install_dir, 'tesseract.exe')
    if os.path.exists(tesseract_exe):
        print(f"  ✅ Tesseract đã được cài đặt tại: {tesseract_exe}")
        return True
    
    print(f"  ❌ Không thể cài đặt Tesseract sau nhiều lần thử")
    return False

def add_to_system_path(path):
    """Thêm đường dẫn vào biến môi trường PATH của hệ thống"""
    try:
        # Mở registry key cho System Environment Variables
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
            0,
            winreg.KEY_READ | winreg.KEY_WRITE
        )
        
        try:
            # Đọc giá trị PATH hiện tại
            current_path, _ = winreg.QueryValueEx(key, 'Path')
            
            # Kiểm tra xem path đã tồn tại chưa
            paths = [p.strip() for p in current_path.split(';') if p.strip()]
            if path in paths:
                return True
            
            # Thêm path mới
            paths.append(path)
            new_path = ';'.join(paths)
            
            # Ghi lại vào registry
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            
            # Broadcast WM_SETTINGCHANGE để cập nhật môi trường
            try:
                import win32gui
                import win32con
                win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')
            except:
                pass
            
            return True
            
        finally:
            winreg.CloseKey(key)
            
    except (PermissionError, Exception):
        return add_to_user_path(path)

def add_to_user_path(path):
    """Thêm đường dẫn vào biến môi trường PATH của user"""
    try:
        # Mở registry key cho User Environment Variables
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r'Environment',
            0,
            winreg.KEY_READ | winreg.KEY_WRITE
        )
        
        try:
            # Đọc giá trị PATH hiện tại
            try:
                current_path, _ = winreg.QueryValueEx(key, 'Path')
            except FileNotFoundError:
                current_path = ''
            
            # Kiểm tra xem path đã tồn tại chưa
            paths = [p.strip() for p in current_path.split(';') if p.strip()]
            if path in paths:
                return True
            
            # Thêm path mới
            paths.append(path)
            new_path = ';'.join(paths)
            
            # Ghi lại vào registry
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            
            # Broadcast WM_SETTINGCHANGE để cập nhật môi trường
            try:
                import win32gui
                import win32con
                win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')
            except:
                pass
            
            return True
            
        finally:
            winreg.CloseKey(key)
            
    except Exception:
        return False

def install_tesseract():
    print("\n[2/4] Đang kiểm tra Tesseract OCR...")
    
    tesseract_paths = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
        r'C:\Tesseract-OCR\tesseract.exe',
    ]
    
    username = os.getenv('USERNAME', '')
    if username:
        tesseract_paths.insert(1, rf'C:\Users\{username}\AppData\Local\Programs\Tesseract-OCR\tesseract.exe')
    
    for path in tesseract_paths:
        if os.path.exists(path):
            print(f"  ✅ Tesseract đã được cài đặt tại: {path}")
            # Thêm vào PATH nếu chưa có
            tesseract_dir = os.path.dirname(path)
            if add_to_system_path(tesseract_dir):
                print(f"  ✅ Đã thêm Tesseract vào PATH")
            return True
    
    print("  ⚠️  Tesseract chưa được cài đặt.")
    print("  📥 Đang tự động tải và cài đặt Tesseract OCR...")
    
    try:
        # Tải installer
        installer_path = download_tesseract_installer()
        if not installer_path:
            print("  ⚠️  Không thể tải Tesseract installer.")
            print("  💡 App vẫn có thể chạy với EasyOCR (đã được bundle)")
            return False
        
        # Cài đặt
        if install_tesseract_silent(installer_path):
            # Thêm vào PATH
            tesseract_dir = r"C:\Program Files\Tesseract-OCR"
            if add_to_system_path(tesseract_dir):
                print(f"  ✅ Đã thêm Tesseract vào PATH")
            # Xóa file installer tạm
            try:
                if os.path.exists(installer_path):
                    os.remove(installer_path)
            except:
                pass
            return True
        else:
            print("  ⚠️  Không thể cài đặt Tesseract tự động.")
            print("  💡 App vẫn có thể chạy với EasyOCR (đã được bundle)")
            # Xóa file installer tạm
            try:
                if os.path.exists(installer_path):
                    os.remove(installer_path)
            except:
                pass
            return False
    except Exception as e:
        print(f"  ⚠️  Lỗi khi cài đặt Tesseract: {str(e)}")
        print("  💡 App vẫn có thể chạy với EasyOCR (đã được bundle)")
        return False

def copy_easyocr_models(install_dir):
    print("\n[3/4] Đang copy EasyOCR models...")
    
    source_models = os.path.join(os.path.dirname(__file__), 'easyocr_models')
    if not os.path.exists(source_models):
        print("  ⚠️  Không tìm thấy EasyOCR models trong package.")
        return False
    
    dest_models = os.path.join(install_dir, 'easyocr_models')
    try:
        if os.path.exists(dest_models):
            shutil.rmtree(dest_models)
        shutil.copytree(source_models, dest_models)
        print(f"  ✅ Đã copy EasyOCR models")
        return True
    except Exception as e:
        print(f"  ⚠️  Lỗi khi copy models: {str(e)}")
        return False

def create_shortcuts(exe_path):
    print("\n[4/4] Đang tạo shortcuts...")
    
    shortcuts_created = 0
    
    try:
        # Tạo shortcut trên Desktop
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        if os.path.exists(desktop):
            desktop_shortcut = os.path.join(desktop, f'{APP_NAME}.lnk')
            vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{desktop_shortcut}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{exe_path}"
oLink.WorkingDirectory = "{os.path.dirname(exe_path)}"
oLink.Description = "{APP_NAME} - Trích xuất text từ hình ảnh"
oLink.Save
'''
            vbs_file = os.path.join(os.path.dirname(exe_path), 'create_desktop_shortcut.vbs')
            with open(vbs_file, 'w', encoding='utf-8') as f:
                f.write(vbs_script)
            
            subprocess.run(['cscript', '//nologo', vbs_file], capture_output=True)
            if os.path.exists(vbs_file):
                os.remove(vbs_file)
            
            if os.path.exists(desktop_shortcut):
                print(f"  ✅ Đã tạo shortcut trên Desktop")
                shortcuts_created += 1
    except Exception as e:
        print(f"  ⚠️  Lỗi khi tạo shortcut Desktop: {str(e)}")
    
    try:
        # Tạo shortcut trong Start Menu
        start_menu = os.path.join(os.getenv('APPDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs')
        if not os.path.exists(start_menu):
            start_menu = os.path.join(os.getenv('PROGRAMDATA', ''), 'Microsoft', 'Windows', 'Start Menu', 'Programs')
        
        if os.path.exists(start_menu):
            start_menu_shortcut = os.path.join(start_menu, f'{APP_NAME}.lnk')
            vbs_script = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{start_menu_shortcut}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{exe_path}"
oLink.WorkingDirectory = "{os.path.dirname(exe_path)}"
oLink.Description = "{APP_NAME} - Trích xuất text từ hình ảnh"
oLink.Save
'''
            vbs_file = os.path.join(os.path.dirname(exe_path), 'create_startmenu_shortcut.vbs')
            with open(vbs_file, 'w', encoding='utf-8') as f:
                f.write(vbs_script)
            
            subprocess.run(['cscript', '//nologo', vbs_file], capture_output=True)
            if os.path.exists(vbs_file):
                os.remove(vbs_file)
            
            if os.path.exists(start_menu_shortcut):
                print(f"  ✅ Đã tạo shortcut trong Start Menu")
                shortcuts_created += 1
    except Exception as e:
        print(f"  ⚠️  Lỗi khi tạo shortcut Start Menu: {str(e)}")
    
    return shortcuts_created > 0

def main():
    print("="*60)
    print(f"  {APP_NAME} v{APP_VERSION}")
    print(f"  Tác giả: {APP_AUTHOR}")
    print("="*60)
    print()
    
    if not is_admin():
        print("⚠️  Cần quyền Administrator để cài đặt!")
        print("Đang yêu cầu quyền Admin...")
        run_as_admin()
        return
    
    print("Đang cài đặt app...")
    print()
    
    exe_source = 'CopyTextApp.exe'
    if not os.path.exists(exe_source):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        exe_source = os.path.join(script_dir, 'CopyTextApp.exe')
        if not os.path.exists(exe_source):
            print("❌ Không tìm thấy file CopyTextApp.exe!")
            print("Vui lòng chạy installer từ thư mục chứa file .exe")
            input("\nNhấn Enter để thoát...")
            return
    
    install_dir = INSTALL_DIR
    try:
        os.makedirs(install_dir, exist_ok=True)
    except PermissionError:
        install_dir = USER_INSTALL_DIR
        os.makedirs(install_dir, exist_ok=True)
        print(f"⚠️  Không thể cài vào Program Files. Cài vào: {install_dir}")
    
    print(f"[1/4] Đang copy files vào: {install_dir}")
    
    try:
        # Đóng app nếu đang chạy
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'CopyTextApp.exe', '/T'], 
                         capture_output=True, timeout=5)
            import time
            time.sleep(1)
        except:
            pass
        
        exe_path = os.path.join(install_dir, 'CopyTextApp.exe')
        
        # Xóa file cũ nếu tồn tại
        if os.path.exists(exe_path):
            try:
                os.remove(exe_path)
            except:
                # Nếu không xóa được, đổi tên
                try:
                    os.rename(exe_path, exe_path + '.old')
                except:
                    pass
        
        shutil.copy2(exe_source, exe_path)
        print(f"  ✅ Đã copy CopyTextApp.exe")
        
        files_to_copy = [
            'HUONG_DAN_CAI_DAT_CHO_NGUOI_KHAC.md',
            'LICENSE.txt'
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                try:
                    shutil.copy2(file, os.path.join(install_dir, file))
                    print(f"  ✅ Đã copy {file}")
                except:
                    pass
        
        copy_easyocr_models(install_dir)
        
    except Exception as e:
        print(f"❌ Lỗi khi copy files: {str(e)}")
        print(f"💡 Thử đóng app CopyTextApp nếu đang chạy, sau đó chạy lại Setup.exe")
        input("\nNhấn Enter để thoát...")
        return
    
    install_tesseract()
    create_shortcuts(exe_path)
    
    print()
    print("="*60)
    print("✅ CÀI ĐẶT HOÀN TẤT!")
    print("="*60)
    print()
    print(f"App đã được cài đặt tại: {install_dir}")
    print("Bạn có thể tìm app trên Desktop hoặc chạy từ:")
    print(f"  {exe_path}")
    print()
    print("🚀 Bạn có muốn chạy app ngay bây giờ không? (Y/N): ", end='')
    
    try:
        choice = input().strip().upper()
        if choice == 'Y':
            subprocess.Popen([exe_path])
    except:
        pass
    
    input("\nNhấn Enter để thoát...")

if __name__ == '__main__':
    main()
