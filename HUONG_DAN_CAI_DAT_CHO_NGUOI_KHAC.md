# CopyText App - Hướng dẫn cài đặt

**Tác giả:** Bùi Quang Tiến THĐD  
**Phiên bản:** 1.0.0

---

## 📥 Cài đặt

### Cách 1: Dùng Installer (KHUYẾN NGHỊ)

1. Giải nén file ZIP
2. Chạy file **`Setup.exe`** (có thể cần quyền Administrator)
3. Installer sẽ tự động:
   - Cài app vào Program Files
   - Cài Tesseract OCR (nếu chưa có)
   - Copy EasyOCR models
   - Tạo shortcut trên Desktop và Start Menu
4. Sau khi cài xong, bạn có thể:
   - Tìm app trong Start Menu
   - Hoặc click vào shortcut trên Desktop
   - App sẽ hiện icon nổi ở góc màn hình

### Cách 2: Chạy trực tiếp (Portable)

1. Giải nén file ZIP
2. Double-click vào `CopyTextApp.exe`
3. App sẽ chạy ngay (không cần cài đặt)

---

## 🚀 Sử dụng

1. **Chạy app** → Icon nổi (📷) xuất hiện ở góc phải màn hình
2. **Click trái vào icon** → Màn hình tối đi, sẵn sàng chọn vùng
3. **Kéo chuột** để chọn vùng có text
4. **Thả chuột** → App tự động xử lý OCR
5. **Dán text** bằng Ctrl+V như bình thường

### Các thao tác với icon:
- **Click trái**: Chụp màn hình
- **Click phải**: Mở menu (Thoát, Chụp màn hình)
- **Double-click**: Thoát app
- **Kéo**: Di chuyển icon

---

## ⚙️ Tính năng

- ✅ Hỗ trợ tiếng Việt và tiếng Anh (mặc định tiếng Việt)
- ✅ Tự động cải thiện chất lượng ảnh
- ✅ Text được nối liên tục, không xuống dòng
- ✅ Kéo thả icon đến vị trí bất kỳ
- ✅ Đóng app dễ dàng (click phải hoặc double-click)

---

## 🔧 Troubleshooting

### Lỗi "Tesseract not found"
→ App đã có sẵn EasyOCR. Nếu vẫn lỗi, thử chạy `CAI_TESSERACT_TU_DONG.bat` để cài Tesseract hệ thống

### OCR không chính xác
→ Đảm bảo vùng chọn có text rõ ràng, không mờ
→ Thử với vùng chọn lớn hơn

### App không chạy
→ Đảm bảo đã cài đặt đầy đủ bằng Setup.exe
→ Thử chạy với quyền Administrator

---

## 📝 Ghi chú

- App đã được bundle đầy đủ EasyOCR models
- Không cần cài Python hay dependencies khác
- Sau khi cài đặt, app sẽ tự động chạy khi khởi động Windows (nếu muốn)

---

**Tác giả:** Bùi Quang Tiến THĐD

