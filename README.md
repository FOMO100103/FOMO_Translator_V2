# FOMO Translator V2

Ứng dụng dịch thuật Python gồm giao diện Desktop (PySide6) và Web (Streamlit), dùng chung lõi dịch, cấu hình và SQLite.

## Chức năng
- Anh ↔ Việt: tự nhận diện ngôn ngữ nguồn và dịch sang ngôn ngữ còn lại.
- Trung → Việt: chế độ riêng.
- Tự chia văn bản dài thành các đoạn và ghép kết quả.
- Sao chép bản dịch (Desktop; Web có thể chọn/copy nội dung).
- Lưu lịch sử vào SQLite.
- Chọn model bằng biến `OPENAI_MODEL` trong `.env`.

## Cài đặt Windows
1. Cài Python 3.11–3.13 64-bit để có độ tương thích dependency tốt hơn. Python 3.15.2 có thể chưa được mọi gói hỗ trợ đầy đủ; chưa xác nhận tương thích trên phiên bản đó.
2. Giải nén thư mục.
3. Chạy `install.bat`.
4. Mở `.env`, điền `OPENAI_API_KEY` của bạn.
5. Chạy `run_desktop.bat` hoặc `run_web.bat`.

## Đóng gói EXE
Chạy `build_exe.bat`. PyInstaller tạo thư mục `dist\FOMO_Translator_V2\`. Đây là bản onedir; giữ nguyên thư mục đi kèm. Sao chép `.env` vào cạnh file EXE, không nhúng API key vào bản build.

## Cấu hình
- `OPENAI_API_KEY`: API key từ OpenAI Platform.
- `OPENAI_MODEL`: model API muốn dùng, mặc định `gpt-4.1-mini`.
- `MAX_CHUNK_CHARS`: độ dài mục tiêu mỗi đoạn, mặc định 6000 ký tự.

## Bảo mật và chi phí
- Không chia sẻ file `.env`, không commit API key lên Git.
- API usage được tính phí riêng với gói ChatGPT.
- Lịch sử lưu cục bộ trong `fomo_history.db`.

## Cấu trúc
```text
FOMO_Translator_V2/
├── translator/       # lõi dịch, cấu hình, SQLite
├── desktop_app/      # giao diện PySide6
├── web_app/          # giao diện Streamlit
├── tests/            # kiểm thử cơ bản
├── .env.example
├── requirements.txt
└── *.bat             # cài đặt, chạy, build
```

## Chạy kiểm thử
```bat
.venv\Scripts\python.exe -m unittest discover -s tests -v
```
