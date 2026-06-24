# 💧 Bot Telegram Nhắc Nhở Uống Nước

Bot Telegram giúp bạn duy trì thói quen uống nước đều đặn mỗi ngày, với tính năng nhắc nhở tự động, theo dõi tiến độ và thống kê.

## 📋 Yêu cầu

- **Python 3.9+** ([Tải tại đây](https://www.python.org/downloads/))
- **Tài khoản Telegram**

## 🚀 Hướng dẫn cài đặt

### Bước 1: Tạo Bot trên Telegram

1. Mở Telegram, tìm **[@BotFather](https://t.me/BotFather)**
2. Gửi lệnh `/newbot`
3. Đặt tên cho bot (VD: `Nhắc Uống Nước Bot`)
4. Đặt username cho bot (VD: `nhac_uong_nuoc_bot`)
5. BotFather sẽ gửi cho bạn một **Token** dạng: `1234567890:ABCdefGhIJKlmNOPQRSTuvwxyz`
6. Lưu token này lại!

### Bước 2: Cài đặt dependencies

```bash
cd "d:\bot tele"
py -m pip install -r requirements.txt
```

### Bước 3: Cấu hình Token

Tạo file `.env` trong thư mục project:

```bash
copy .env.example .env
```

Mở file `.env` và thay `your_bot_token_here` bằng token từ BotFather:

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGhIJKlmNOPQRSTuvwxyz
```

### Bước 4: Chạy Bot

```bash
py bot.py
```

Bot sẽ hiện thông báo: `✅ Bot đã sẵn sàng! Đang lắng nghe...`

## 📱 Cách sử dụng

Mở Telegram, tìm bot của bạn theo username đã đặt ở Bước 1, rồi gửi các lệnh:

| Lệnh | Chức năng |
|---|---|
| `/start` | Đăng ký và bật nhắc nhở |
| `/stop` | Tạm dừng nhắc nhở |
| `/drink` | Ghi nhận đã uống 1 ly (250ml) |
| `/status` | Xem tiến độ uống nước hôm nay |
| `/goal <số>` | Đặt mục tiêu (VD: `/goal 10`) |
| `/settings` | Xem cài đặt hiện tại |
| `/help` | Xem hướng dẫn |

## ⚙️ Cài đặt mặc định

| Cài đặt | Giá trị |
|---|---|
| Giờ bắt đầu nhắc | 7:00 |
| Giờ kết thúc nhắc | 22:00 |
| Khoảng cách nhắc | 60 phút |
| Mục tiêu | 8 ly (2000ml) |
| Mỗi ly | 250ml |

## 💡 Mẹo

- Mỗi lần nhận tin nhắn nhắc nhở, bấm nút **💧 Đã uống!** để ghi nhận nhanh
- Bot tự động reset bộ đếm vào **0:00 mỗi ngày**
- Dùng `/goal` để điều chỉnh mục tiêu phù hợp với bạn
- Bot sẽ tự khôi phục nhắc nhở khi khởi động lại

## 🗂️ Cấu trúc dự án

```
bot tele/
├── bot.py              # Entry point - Khởi chạy bot
├── config.py           # Cấu hình (token, thời gian, mục tiêu)
├── handlers.py         # Xử lý các lệnh và callback
├── scheduler.py        # Quản lý lịch nhắc nhở
├── storage.py          # Lưu trữ dữ liệu (JSON)
├── messages.py         # Các mẫu tin nhắn tiếng Việt
├── requirements.txt    # Dependencies
├── .env.example        # Mẫu file cấu hình
├── .env                # File cấu hình (tạo bởi bạn)
├── .gitignore          # Ignore files
└── README.md           # File này
```

## ☁️ Deploy lên Railway (chạy 24/7)

Nếu muốn bot chạy 24/7 mà không cần bật máy tính, bạn có thể deploy lên **Railway** (miễn phí $5/tháng — dư cho bot nhỏ).

### Bước 1: Đẩy code lên GitHub

1. Tạo repository mới trên [github.com](https://github.com/new) (đặt tên VD: `water-reminder-bot`)
2. Mở terminal tại thư mục project và chạy:

```bash
cd "d:\bot tele"
git init
git add .
git commit -m "Initial commit - Water Reminder Bot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/water-reminder-bot.git
git push -u origin main
```

### Bước 2: Tạo tài khoản Railway

1. Truy cập [railway.com](https://railway.com)
2. Đăng ký bằng tài khoản GitHub
3. Xác nhận email

### Bước 3: Tạo project trên Railway

1. Click **"New Project"**
2. Chọn **"Deploy from GitHub repo"**
3. Chọn repository `water-reminder-bot` vừa push
4. Railway sẽ tự detect Python project

### Bước 4: Cấu hình Token

1. Trong project trên Railway, vào tab **"Variables"**
2. Click **"New Variable"**
3. Thêm:
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: Token từ BotFather
4. Railway sẽ tự động redeploy

### Bước 5: Kiểm tra

1. Vào tab **"Deployments"** → kiểm tra trạng thái `SUCCESS`
2. Vào tab **"Logs"** → tìm dòng `✅ Bot đã sẵn sàng!`
3. Mở Telegram, gửi `/start` cho bot

> 💡 **Mẹo**: Mỗi khi push code mới lên GitHub, Railway sẽ tự động deploy lại!

---

## ❓ Xử lý lỗi

**Bot không chạy?**
- Kiểm tra đã tạo file `.env` với token đúng chưa
- Kiểm tra Python version: `py --version` (cần 3.9+)
- Kiểm tra đã cài dependencies: `py -m pip install -r requirements.txt`

**Bot chạy nhưng không nhận tin nhắn?**
- Đảm bảo bạn đã gửi `/start` cho bot trên Telegram
- Kiểm tra token có đúng không

**Bot không nhắc nhở?**
- Kiểm tra bot đang chạy (terminal phải mở)
- Kiểm tra đang trong khung giờ nhắc nhở (7:00-22:00)
- Gửi `/settings` để kiểm tra trạng thái

---

Made with ❤️ để giúp bạn khỏe mạnh hơn mỗi ngày! 💧
