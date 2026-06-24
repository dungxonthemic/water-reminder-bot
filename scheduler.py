"""
Quản lý lịch nhắc nhở uống nước sử dụng JobQueue của python-telegram-bot.
"""

import logging
from datetime import time, datetime

import pytz
from telegram.ext import ContextTypes

from config import TIMEZONE, GLASS_ML
from messages import get_reminder_message, DAILY_RESET, build_progress_bar
from storage import get_user, get_all_active_users, reset_daily

logger = logging.getLogger(__name__)

# Timezone Việt Nam
TZ = pytz.timezone(TIMEZONE)


def _build_reminder_keyboard():
    """Tạo inline keyboard cho tin nhắn nhắc nhở."""
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup

    keyboard = [
        [
            InlineKeyboardButton("💧 Đã uống!", callback_data="drink"),
            InlineKeyboardButton("📊 Xem tiến độ", callback_data="status"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def send_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Gửi tin nhắn nhắc nhở uống nước cho một user."""
    job = context.job
    chat_id = job.chat_id
    user_id = job.data.get("user_id") if job.data else None

    if user_id is None:
        return

    # Kiểm tra user còn active không
    user = get_user(user_id)
    if not user or not user.get("is_active", False):
        # User đã tắt nhắc nhở, xóa job
        job.schedule_removal()
        return

    # Kiểm tra có trong khung giờ nhắc nhở không
    now = datetime.now(TZ)
    current_hour = now.hour
    start_hour = user.get("reminder_start", 7)
    end_hour = user.get("reminder_end", 22)

    if current_hour < start_hour or current_hour >= end_hour:
        return

    # Tạo tin nhắn nhắc nhở
    message = get_reminder_message()
    current = user.get("drinks_today", 0)
    goal = user.get("goal", 8)
    progress_bar = build_progress_bar(current, goal)

    message += f"\n\n📊 Hôm nay: **{current}/{goal} ly**\n{progress_bar}"

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            reply_markup=_build_reminder_keyboard(),
        )
        logger.info(f"Đã gửi nhắc nhở cho user {user_id}")
    except Exception as e:
        logger.error(f"Lỗi gửi nhắc nhở cho user {user_id}: {e}")


async def send_daily_reset(context: ContextTypes.DEFAULT_TYPE):
    """Reset bộ đếm và gửi tin nhắn chào buổi sáng."""
    job = context.job
    user_id = job.data.get("user_id") if job.data else None

    if user_id is None:
        return

    user = get_user(user_id)
    if not user or not user.get("is_active", False):
        return

    # Reset bộ đếm
    reset_daily(user_id)

    goal = user.get("goal", 8)
    message = DAILY_RESET.format(goal=goal, goal_ml=goal * GLASS_ML)

    try:
        await context.bot.send_message(
            chat_id=user.get("chat_id"),
            text=message,
            parse_mode="Markdown",
            reply_markup=_build_reminder_keyboard(),
        )
        logger.info(f"Đã reset hằng ngày cho user {user_id}")
    except Exception as e:
        logger.error(f"Lỗi gửi reset cho user {user_id}: {e}")


def setup_user_jobs(application, user_id: int, chat_id: int, user_data: dict):
    """Thiết lập các job nhắc nhở cho một user."""
    job_queue = application.job_queue

    # Xóa jobs cũ của user này (nếu có)
    remove_user_jobs(application, user_id)

    interval = user_data.get("reminder_interval", 60)

    # Job nhắc nhở theo interval
    job_queue.run_repeating(
        send_reminder,
        interval=interval * 60,  # Chuyển sang giây
        first=10,  # Bắt đầu sau 10 giây
        chat_id=chat_id,
        name=f"reminder_{user_id}",
        data={"user_id": user_id},
    )

    # Job reset hằng ngày lúc 0:00
    reset_time = time(hour=0, minute=0, second=0, tzinfo=TZ)
    job_queue.run_daily(
        send_daily_reset,
        time=reset_time,
        chat_id=chat_id,
        name=f"daily_reset_{user_id}",
        data={"user_id": user_id},
    )

    logger.info(
        f"Đã thiết lập jobs cho user {user_id}: "
        f"nhắc mỗi {interval} phút, reset lúc 00:00"
    )


def remove_user_jobs(application, user_id: int):
    """Xóa tất cả jobs của một user."""
    job_queue = application.job_queue
    job_names = [f"reminder_{user_id}", f"daily_reset_{user_id}"]

    for name in job_names:
        current_jobs = job_queue.get_jobs_by_name(name)
        for job in current_jobs:
            job.schedule_removal()

    logger.info(f"Đã xóa jobs cho user {user_id}")


def restore_all_jobs(application):
    """Khôi phục jobs cho tất cả user active khi bot khởi động lại."""
    active_users = get_all_active_users()

    for user in active_users:
        user_id = user["user_id"]
        chat_id = user["chat_id"]
        setup_user_jobs(application, user_id, chat_id, user)

    logger.info(f"Đã khôi phục jobs cho {len(active_users)} user(s)")
