import os
import sys

def preload_easyocr_models():
    try:
        import easyocr
        print("Đang tải EasyOCR models...")
        print("Lần đầu sẽ tải khoảng 100MB, vui lòng chờ...")
        
        reader = easyocr.Reader(['vi', 'en'], gpu=False, verbose=True)
        
        print("\n✅ Đã tải xong EasyOCR models!")
        print("Models đã được lưu vào cache và sẽ không cần tải lại.")
        return True
    except ImportError:
        print("EasyOCR chưa được cài đặt. Bỏ qua preload.")
        return False
    except Exception as e:
        print(f"❌ Lỗi khi tải models: {str(e)}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("PRELOAD EASYOCR MODELS")
    print("=" * 60)
    print()
    
    success = preload_easyocr_models()
    
    if success:
        print("\n✅ Hoàn tất! Models đã sẵn sàng.")
    else:
        print("\n⚠️  Không thể preload models.")
    
    input("\nNhấn Enter để thoát...")

