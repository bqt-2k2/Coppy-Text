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
        
        # Setup SSL context để tải file
        import ssl
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Tải file với SSL context
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
        urllib.request.install_opener(opener)
        
        # Tải file với progress
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, int(downloaded * 100 / total_size)) if total_size > 0 else 0
            if block_num % 10 == 0:  # Update mỗi 10 blocks
                print(f"  📥 Đang tải: {percent}%", end='\r')
        
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

def add_tesseract_to_path(install_dir):
    """Thêm Tesseract vào System PATH"""
    try:
        print("  🔧 Đang thêm Tesseract vào PATH...")
        
        # Kiểm tra xem đã có trong PATH chưa
        current_path = os.environ.get('PATH', '')
        if install_dir in current_path:
            print("  ✅ Tesseract đã có trong PATH")
            return True
        
        # Thêm vào User PATH (không cần admin)
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment', 0, winreg.KEY_ALL_ACCESS)
        try:
            user_path, _ = winreg.QueryValueEx(key, 'Path')
        except WindowsError:
            user_path = ''
        
        if install_dir not in user_path:
            new_path = user_path + ';' + install_dir if user_path else install_dir
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            print(f"  ✅ Đã thêm Tesseract vào PATH: {install_dir}")
            
            # Broadcast WM_SETTINGCHANGE để cập nhật PATH
            import ctypes
            HWND_BROADCAST = 0xFFFF
            WM_SETTINGCHANGE = 0x1A
            SMTO_ABORTIFHUNG = 0x0002
            result = ctypes.c_long()
            ctypes.windll.user32.SendMessageTimeoutW(
                HWND_BROADCAST, WM_SETTINGCHANGE, 0, 'Environment',
                SMTO_ABORTIFHUNG, 5000, ctypes.byref(result)
            )
        
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"  ⚠️  Lỗi khi thêm vào PATH: {str(e)}")
        print(f"  💡 Bạn có thể thêm thủ công: {install_dir}")
        return False

def download_language_data(install_dir):
    """Tải file ngôn ngữ tiếng Việt cho Tesseract"""
    try:
        tessdata_dir = os.path.join(install_dir, 'tessdata')
        vie_file = os.path.join(tessdata_dir, 'vie.traineddata')
        
        # Kiểm tra đã có chưa
        if os.path.exists(vie_file):
            print("  ✅ Language data tiếng Việt đã có")
            return True
        
        print("  📥 Đang tải language data tiếng Việt...")
        
        # URL của file ngôn ngữ tiếng Việt
        # url = "https://github.com/tesseract-ocr/tessdata/raw/main/vie.traineddata"
        url = "https://github.com/tesseract-ocr/tessdata_best/raw/main/vie.traineddata"
        
        # Tạo thư mục tessdata nếu chưa có
        os.makedirs(tessdata_dir, exist_ok=True)
        
        # Tải file với SSL context (bỏ qua verify certificate nếu cần)
        import ssl
        
        # Tạo SSL context không verify certificate
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Tải file với progress
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, int(downloaded * 100 / total_size)) if total_size > 0 else 0
            if block_num % 5 == 0:  # Update mỗi 5 blocks
                print(f"  📥 Đang tải: {percent}%", end='\r')
        
        # Tải file với SSL context
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ssl_context))
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, vie_file, show_progress)
        print()
        
        if os.path.exists(vie_file):
            file_size = os.path.getsize(vie_file)
            if file_size > 0:
                print(f"  ✅ Đã tải language data tiếng Việt ({file_size // 1024} KB)")
                return True
            else:
                print("  ⚠️  File tải về bị lỗi (0 KB)")
                os.remove(vie_file)
                return False
        else:
            print("  ⚠️  Không thể tải language data")
            return False
    except Exception as e:
        print(f"  ⚠️  Lỗi khi tải language data: {str(e)}")
        print("  💡 App vẫn có thể chạy với EasyOCR (đã được bundle)")
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
            # Thêm vào PATH và tải language data
            tesseract_dir = os.path.dirname(path)
            add_tesseract_to_path(tesseract_dir)
            download_language_data(tesseract_dir)
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
            # Xóa file installer tạm
            try:
                if os.path.exists(installer_path):
                    os.remove(installer_path)
            except:
                pass
            
            # Thêm vào PATH và tải language data
            install_dir = r"C:\Program Files\Tesseract-OCR"
            add_tesseract_to_path(install_dir)
            download_language_data(install_dir)
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
