"""
Quản lý lưu trữ dữ liệu người dùng bằng JSON file.
"""

import json
import os
from datetime import date
from typing import Optional

from config import (
    DATA_DIR,
    DATA_FILE,
    DEFAULT_GOAL,
    DEFAULT_REMINDER_END_HOUR,
    DEFAULT_REMINDER_INTERVAL,
    DEFAULT_REMINDER_START_HOUR,
    GLASS_ML,
)


def _ensure_data_dir():
    """Tạo thư mục data nếu chưa có."""
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_data() -> dict:
    """Đọc dữ liệu từ file JSON."""
    _ensure_data_dir()
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_data(data: dict):
    """Ghi dữ liệu vào file JSON."""
    _ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user(user_id: int) -> Optional[dict]:
    """Lấy thông tin user. Trả về None nếu chưa đăng ký."""
    data = _load_data()
    user_key = str(user_id)
    if user_key not in data:
        return None

    user = data[user_key]

    # Auto-reset nếu qua ngày mới
    today = date.today().isoformat()
    if user.get("last_reset") != today:
        user["drinks_today"] = 0
        user["last_reset"] = today
        data[user_key] = user
        _save_data(data)

    return user


def create_user(user_id: int, chat_id: int) -> dict:
    """Tạo user mới hoặc cập nhật user hiện tại."""
    data = _load_data()
    user_key = str(user_id)
    today = date.today().isoformat()

    if user_key in data:
        # User đã tồn tại, chỉ bật lại
        data[user_key]["is_active"] = True
        data[user_key]["chat_id"] = chat_id
    else:
        # Tạo mới
        data[user_key] = {
            "chat_id": chat_id,
            "goal": DEFAULT_GOAL,
            "drinks_today": 0,
            "last_reset": today,
            "reminder_start": DEFAULT_REMINDER_START_HOUR,
            "reminder_end": DEFAULT_REMINDER_END_HOUR,
            "reminder_interval": DEFAULT_REMINDER_INTERVAL,
            "is_active": True,
        }

    _save_data(data)
    return data[user_key]


def add_drink(user_id: int) -> Optional[dict]:
    """Ghi nhận 1 ly nước. Trả về thông tin user đã cập nhật."""
    data = _load_data()
    user_key = str(user_id)

    if user_key not in data:
        return None

    # Auto-reset nếu qua ngày mới
    today = date.today().isoformat()
    if data[user_key].get("last_reset") != today:
        data[user_key]["drinks_today"] = 0
        data[user_key]["last_reset"] = today

    data[user_key]["drinks_today"] += 1
    _save_data(data)
    return data[user_key]


def set_goal(user_id: int, goal: int) -> Optional[dict]:
    """Đặt mục tiêu mới. Trả về thông tin user đã cập nhật."""
    data = _load_data()
    user_key = str(user_id)

    if user_key not in data:
        return None

    data[user_key]["goal"] = goal
    _save_data(data)
    return data[user_key]


def set_active(user_id: int, active: bool) -> Optional[dict]:
    """Bật/tắt nhắc nhở cho user."""
    data = _load_data()
    user_key = str(user_id)

    if user_key not in data:
        return None

    data[user_key]["is_active"] = active
    _save_data(data)
    return data[user_key]


def get_all_active_users() -> list[dict]:
    """Lấy danh sách tất cả user đang bật nhắc nhở."""
    data = _load_data()
    active_users = []
    today = date.today().isoformat()

    for user_id, user in data.items():
        if user.get("is_active", False):
            # Auto-reset nếu qua ngày mới
            if user.get("last_reset") != today:
                user["drinks_today"] = 0
                user["last_reset"] = today

            user["user_id"] = int(user_id)
            active_users.append(user)

    # Lưu lại nếu có thay đổi
    _save_data(data)
    return active_users


def reset_daily(user_id: int) -> Optional[dict]:
    """Reset bộ đếm uống nước cho user."""
    data = _load_data()
    user_key = str(user_id)

    if user_key not in data:
        return None

    data[user_key]["drinks_today"] = 0
    data[user_key]["last_reset"] = date.today().isoformat()
    _save_data(data)
    return data[user_key]
