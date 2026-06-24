"""
Cấu hình cho bot Telegram nhắc nhở uống nước.
Load từ file .env hoặc sử dụng giá trị mặc định.
"""

import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# === Telegram Bot Token ===
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# === Cài đặt nhắc nhở mặc định ===
DEFAULT_REMINDER_START_HOUR = 7      # Bắt đầu nhắc từ 7:00
DEFAULT_REMINDER_END_HOUR = 22       # Kết thúc nhắc lúc 22:00
DEFAULT_REMINDER_INTERVAL = 60       # Nhắc mỗi 60 phút
DEFAULT_GOAL = 8                     # Mục tiêu 8 ly nước / ngày
GLASS_ML = 250                       # Mỗi ly = 250ml

# === Timezone ===
TIMEZONE = "Asia/Ho_Chi_Minh"

# === Lưu trữ dữ liệu ===
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "users.json")
