# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess
import urllib.request
import zipfile
import tempfile

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def get_build_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist', 'CopyTextApp')

def download_file(url, dest_path):
    try:
        print(f"  Đang tải: {url}")
        urllib.request.urlretrieve(url, dest_path)
        print(f"  ✅ Đã tải xong: {os.path.basename(dest_path)}")
        return True
    except Exception as e:
        print(f"  ❌ Lỗi khi tải: {str(e)}")
        return False

def bundle_tesseract():
    print("\n[1/2] Đang bundle Tesseract OCR...")
    build_dir = get_build_dir()
    tesseract_dir = os.path.join(build_dir, 'tesseract')
    
    if os.path.exists(tesseract_dir):
        print("  ✅ Tesseract đã được bundle")
        return True
    
    # tesseract_url = "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.0.20221214/tesseract-ocr-w64-setup-5.3.0.20221214.exe"
    tesseract_url = "https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe"
    
    try:
        temp_dir = tempfile.mkdtemp()
        installer_path = os.path.join(temp_dir, 'tesseract_installer.exe')
        
        print("  📥 Đang tải Tesseract installer...")
        if not download_file(tesseract_url, installer_path):
            print("  ⚠️  Không thể tải Tesseract. App vẫn có thể chạy với EasyOCR.")
            return False
        
        print("  ⚠️  Tesseract installer đã được tải.")
        print("  💡 Người dùng sẽ cần cài Tesseract thủ công hoặc dùng EasyOCR.")
        print("  💡 File installer đã được copy vào package.")
        
        os.makedirs(tesseract_dir, exist_ok=True)
        shutil.copy2(installer_path, os.path.join(tesseract_dir, 'tesseract_installer.exe'))
        
        shutil.rmtree(temp_dir, ignore_errors=True)
        return True
    except Exception as e:
        print(f"  ⚠️  Lỗi khi bundle Tesseract: {str(e)}")
        print("  💡 App vẫn có thể chạy với EasyOCR.")
        return False

def bundle_easyocr_models():
    print("\n[2/2] Đang bundle EasyOCR models...")
    build_dir = get_build_dir()
    models_dir = os.path.join(build_dir, 'easyocr_models')
    
    if os.path.exists(models_dir):
        print("  ✅ EasyOCR models đã được bundle")
        return True
    
    user_models_dir = os.path.join(os.path.expanduser('~'), '.EasyOCR', 'model')
    if os.path.exists(user_models_dir):
        try:
            print("  Đang copy EasyOCR models từ user directory...")
            os.makedirs(models_dir, exist_ok=True)
            shutil.copytree(user_models_dir, os.path.join(models_dir, 'model'))
            print("  ✅ Đã copy EasyOCR models")
            return True
        except Exception as e:
            print(f"  ⚠️  Lỗi khi copy models: {str(e)}")
    
    print("  ⚠️  Không tìm thấy EasyOCR models.")
    print("  💡 Models sẽ được tải khi app chạy lần đầu.")
    return False

def main():
    print("="*60)
    print("BUNDLE DEPENDENCIES")
    print("="*60)
    print()
    
    build_dir = get_build_dir()
    if not os.path.exists(build_dir):
        print("❌ Thư mục build chưa tồn tại!")
        print("Vui lòng chạy build.bat trước.")
        return 1
    
    bundle_tesseract()
    bundle_easyocr_models()
    
    print()
    print("="*60)
    print("✅ Hoàn tất!")
    print("="*60)
    return 0

if __name__ == '__main__':
    sys.exit(main())

