# -*- coding: utf-8 -*-
"""
Tesseract OCR Auto Installer
Tự động tải, cài đặt và thêm Tesseract vào PATH
Tác giả: Bùi Quang Tiến THĐD
"""
import os
import sys
import subprocess
import urllib.request
import tempfile
import time
import winreg
import ctypes

TESSERACT_INSTALL_DIR = r"C:\Program Files\Tesseract-OCR"
TESSERACT_EXE = os.path.join(TESSERACT_INSTALL_DIR, 'tesseract.exe')

def is_admin():
    """Kiểm tra quyền Administrator"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def print_header():
    """In header của script"""
    print("\n" + "="*60)
    print("  TỰ ĐỘNG CÀI ĐẶT TESSERACT OCR")
    print("  Tác giả: Bùi Quang Tiến THĐD")
    print("="*60 + "\n")

def check_tesseract_installed():
    """Kiểm tra xem Tesseract đã được cài đặt chưa"""
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
            print(f"✅ Tesseract đã được cài đặt tại: {path}")
            return path
    
    return None

def download_tesseract_installer():
    """Tải Tesseract installer về"""
    try:
        print("📥 Đang tải Tesseract OCR installer...")
        print("💡 Quá trình này có thể mất vài phút, vui lòng chờ...\n")
        
        # URL của Tesseract installer
        urls = [
            "https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe",
            "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.4.0.20240605.exe",
        ]
        
        temp_dir = tempfile.gettempdir()
        installer_path = os.path.join(temp_dir, 'tesseract_installer.exe')
        
        # Xóa file cũ nếu có
        if os.path.exists(installer_path):
            try:
                os.remove(installer_path)
            except (OSError, PermissionError):
                pass
        
        # Tải file với progress
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            percent = min(100, int(downloaded * 100 / total_size)) if total_size > 0 else 0
            if block_num % 20 == 0:  # Update mỗi 20 blocks
                print(f"  📥 Đã tải: {percent}%", end='\r')
        
        # Thử từng URL cho đến khi thành công
        for url in urls:
            try:
                print(f"  Đang thử tải từ: {url.split('/')[-1]}")
                urllib.request.urlretrieve(url, installer_path, show_progress)
                print(f"\n  ✅ Đã tải xong: {os.path.basename(installer_path)}\n")
                return installer_path
            except Exception as e:
                print(f"  ⚠️  URL này không khả dụng: {str(e)}")
                continue
        
        # Nếu tất cả URL đều thất bại
        print(f"  ❌ Không thể tải từ bất kỳ URL nào")
        return None
    except Exception as e:
        print(f"⚠️  Lỗi khi tải Tesseract installer: {str(e)}")
        return None

def install_tesseract_silent(installer_path):
    """Cài đặt Tesseract một cách im lặng"""
    print("🔧 Đang cài đặt Tesseract OCR...")
    print("💡 Quá trình này có thể mất vài phút, vui lòng chờ...\n")
    
    # Thử nhiều cách cài đặt silent
    silent_params_list = [
        (['/S', f'/D={TESSERACT_INSTALL_DIR}'], "Standard silent"),
        (['/S', '/NCRC', f'/D={TESSERACT_INSTALL_DIR}'], "Silent + no CRC check"),
        (['/VERYSILENT', '/NORESTART', f'/DIR={TESSERACT_INSTALL_DIR}'], "Very silent (Inno Setup)"),
    ]
    
    for params, desc in silent_params_list:
        try:
            cmd = [installer_path] + params
            print(f"  Đang thử: {desc}...")
            result = subprocess.run(cmd, capture_output=True, timeout=300, text=True)
            
            # Đợi và kiểm tra nhiều lần
            for wait_time in [3, 5, 10]:
                time.sleep(wait_time)
                if os.path.exists(TESSERACT_EXE):
                    print(f"  ✅ Đã cài đặt Tesseract thành công tại: {TESSERACT_INSTALL_DIR}\n")
                    return True
            
        except subprocess.TimeoutExpired:
            print(f"  ⚠️  Cài đặt quá lâu với {desc}, thử cách khác...")
            # Kiểm tra xem có cài được không
            if os.path.exists(TESSERACT_EXE):
                print(f"  ✅ Tesseract đã được cài đặt tại: {TESSERACT_EXE}\n")
                return True
            continue
        except Exception as e:
            print(f"  ⚠️  Lỗi với {desc}: {str(e)}")
            continue
    
    # Kiểm tra lại sau tất cả các lần thử
    print("  Đang kiểm tra lại...")
    time.sleep(5)
    if os.path.exists(TESSERACT_EXE):
        print(f"  ✅ Tesseract đã được cài đặt tại: {TESSERACT_EXE}\n")
        return True
    
    print(f"  ❌ Không thể cài đặt Tesseract sau nhiều lần thử\n")
    return False

def add_to_system_path(path):
    """Thêm đường dẫn vào biến môi trường PATH của hệ thống"""
    try:
        print(f"🔧 Đang thêm Tesseract vào PATH hệ thống...")
        
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
                print(f"  ✅ PATH đã chứa: {path}\n")
                return True
            
            # Thêm path mới
            paths.append(path)
            new_path = ';'.join(paths)
            
            # Ghi lại vào registry
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            print(f"  ✅ Đã thêm vào PATH: {path}\n")
            
            # Broadcast WM_SETTINGCHANGE để cập nhật môi trường
            try:
                import win32gui
                import win32con
                win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')
            except ImportError:
                # win32gui không có sẵn, PATH sẽ có hiệu lực sau khi khởi động lại
                pass
            except Exception:
                # Không thể broadcast, PATH sẽ có hiệu lực sau khi khởi động lại
                pass
            
            return True
            
        finally:
            winreg.CloseKey(key)
            
    except PermissionError:
        print("  ⚠️  Không có quyền ghi vào System PATH")
        print("  💡 Đang thử thêm vào User PATH...\n")
        return add_to_user_path(path)
    except Exception as e:
        print(f"  ⚠️  Lỗi khi thêm vào System PATH: {str(e)}")
        print("  💡 Đang thử thêm vào User PATH...\n")
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
                print(f"  ✅ User PATH đã chứa: {path}\n")
                return True
            
            # Thêm path mới
            paths.append(path)
            new_path = ';'.join(paths)
            
            # Ghi lại vào registry
            winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, new_path)
            print(f"  ✅ Đã thêm vào User PATH: {path}\n")
            
            # Broadcast WM_SETTINGCHANGE để cập nhật môi trường
            try:
                import win32gui
                import win32con
                win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SETTINGCHANGE, 0, 'Environment')
            except ImportError:
                # win32gui không có sẵn, PATH sẽ có hiệu lực sau khi khởi động lại
                pass
            except Exception:
                # Không thể broadcast, PATH sẽ có hiệu lực sau khi khởi động lại
                pass
            
            return True
            
        finally:
            winreg.CloseKey(key)
            
    except Exception as e:
        print(f"  ❌ Lỗi khi thêm vào User PATH: {str(e)}\n")
        return False

def verify_installation():
    """Xác minh cài đặt thành công"""
    print("🔍 Đang xác minh cài đặt...")
    
    # Kiểm tra file tesseract.exe
    if not os.path.exists(TESSERACT_EXE):
        print(f"  ❌ Không tìm thấy {TESSERACT_EXE}\n")
        return False
    
    # Kiểm tra chạy được không
    try:
        result = subprocess.run(
            [TESSERACT_EXE, '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0] if result.stdout else 'Unknown version'
            print(f"  ✅ Tesseract hoạt động tốt: {version_line}\n")
            return True
        else:
            print(f"  ⚠️  Tesseract không chạy được\n")
            return False
    except Exception as e:
        print(f"  ⚠️  Lỗi khi kiểm tra Tesseract: {str(e)}\n")
        return False

def main():
    """Hàm chính"""
    print_header()
    
    # Kiểm tra quyền admin
    if not is_admin():
        print("⚠️  Cảnh báo: Script đang chạy không có quyền Administrator")
        print("💡 Một số chức năng có thể không hoạt động (như thêm vào System PATH)\n")
    
    # Kiểm tra Tesseract đã cài chưa
    existing_path = check_tesseract_installed()
    if existing_path:
        print("✅ Tesseract đã sẵn sàng sử dụng!\n")
        
        # Kiểm tra và thêm vào PATH nếu chưa có
        tesseract_dir = os.path.dirname(existing_path)
        if add_to_system_path(tesseract_dir):
            print("✅ Đã cập nhật PATH thành công!\n")
        
        print("="*60)
        print("Lưu ý: Bạn có thể cần khởi động lại Command Prompt")
        print("       hoặc ứng dụng để PATH có hiệu lực")
        print("="*60 + "\n")
        return
    
    print("⚠️  Tesseract chưa được cài đặt")
    print("📥 Bắt đầu quá trình cài đặt tự động...\n")
    
    # Tải installer
    installer_path = download_tesseract_installer()
    if not installer_path:
        print("❌ Không thể tải Tesseract installer")
        print("💡 Vui lòng tải thủ công từ: https://github.com/tesseract-ocr/tesseract/releases\n")
        input("Nhấn Enter để thoát...")
        sys.exit(1)
    
    # Cài đặt
    if not install_tesseract_silent(installer_path):
        print("❌ Không thể cài đặt Tesseract tự động")
        print("💡 Vui lòng cài đặt thủ công bằng cách chạy:")
        print(f"   {installer_path}\n")
        input("Nhấn Enter để thoát...")
        sys.exit(1)
    
    # Xóa file installer tạm
    try:
        if os.path.exists(installer_path):
            os.remove(installer_path)
    except (OSError, PermissionError):
        pass
    
    # Thêm vào PATH
    if add_to_system_path(TESSERACT_INSTALL_DIR):
        print("✅ Đã thêm Tesseract vào PATH!\n")
    else:
        print("⚠️  Không thể thêm vào PATH tự động")
        print(f"💡 Vui lòng thêm thủ công: {TESSERACT_INSTALL_DIR}\n")
    
    # Xác minh cài đặt
    if verify_installation():
        print("="*60)
        print("✅ CÀI ĐẶT HOÀN TẤT!")
        print("="*60 + "\n")
        print("Tesseract OCR đã được cài đặt và cấu hình thành công!")
        print(f"Đường dẫn: {TESSERACT_INSTALL_DIR}")
        print("\nLưu ý: Bạn có thể cần khởi động lại Command Prompt")
        print("       hoặc ứng dụng để PATH có hiệu lực\n")
    else:
        print("⚠️  Cài đặt hoàn tất nhưng có thể có lỗi")
        print("💡 Vui lòng kiểm tra lại cài đặt\n")
    
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Đã hủy bởi người dùng\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Lỗi không mong muốn: {str(e)}\n")
        import traceback
        traceback.print_exc()
        input("\nNhấn Enter để thoát...")
        sys.exit(1)
    
    input("Nhấn Enter để thoát...")
