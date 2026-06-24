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

## ☁️ Deploy lên Render (chạy 24/7 — MIỄN PHÍ)

Deploy bot lên **Render** để chạy 24/7 mà không cần bật máy tính. **Hoàn toàn miễn phí, không cần thẻ tín dụng.**

### Bước 1: Đẩy code lên GitHub

*(Bỏ qua nếu đã push code rồi)*

```bash
cd "d:\bot tele"
git add .
git commit -m "Add Render deployment"
git push origin main
```

### Bước 2: Tạo tài khoản Render

1. Truy cập [render.com](https://render.com)
2. Đăng ký bằng tài khoản **GitHub**

### Bước 3: Tạo Web Service

1. Vào Dashboard → click **"New +"** → chọn **"Web Service"**
2. Chọn **"Build and deploy from a Git repository"** → Next
3. Kết nối repo **`water-reminder-bot`** từ GitHub
4. Điền thông tin:
   - **Name**: `water-reminder-bot`
   - **Region**: Singapore (gần Việt Nam nhất)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot.py`
5. Chọn plan **"Free"**
6. Click **"Create Web Service"**

### Bước 4: Cấu hình Token

1. Trong service vừa tạo, vào tab **"Environment"**
2. Click **"Add Environment Variable"**
3. Thêm:
   - **Key**: `TELEGRAM_BOT_TOKEN`
   - **Value**: Token từ BotFather
4. Click **"Save Changes"** → Render sẽ tự deploy lại

### Bước 5: Giữ bot luôn hoạt động (Keep-Alive)

Render free tier sẽ tắt bot sau 15 phút không có hoạt động. Để giữ bot luôn chạy:

1. Truy cập [cron-job.org](https://cron-job.org) → đăng ký tài khoản miễn phí
2. Click **"Create Cronjob"**
3. Điền:
   - **Title**: `Keep bot alive`
   - **URL**: `https://water-reminder-bot.onrender.com` (thay bằng URL Render của bạn)
   - **Schedule**: Every **14 minutes**
4. Save → Bot sẽ luôn được đánh thức và chạy 24/7!

### Bước 6: Kiểm tra

1. Vào tab **"Logs"** trên Render → tìm dòng `✅ Bot chạy webhook mode`
2. Mở Telegram, gửi `/start` cho bot

> 💡 **Mẹo**: Mỗi khi push code mới lên GitHub, Render sẽ tự động deploy lại!

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
