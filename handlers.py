"""
Xử lý các lệnh và callback từ người dùng Telegram.
"""

import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import GLASS_ML
from messages import (
    WELCOME_MESSAGE,
    DRINK_RECORDED,
    HELP_MESSAGE,
    SETTINGS_MESSAGE,
    STATUS_MESSAGE,
    STOP_MESSAGE,
    ALREADY_STOPPED,
    ALREADY_STARTED,
    GOAL_SET,
    GOAL_INVALID,
    build_progress_bar,
    format_status_text,
    get_motivation_message,
    get_goal_reached_message,
)
from storage import get_user, create_user, add_drink, set_goal, set_active
from scheduler import setup_user_jobs, remove_user_jobs

logger = logging.getLogger(__name__)


def _drink_keyboard():
    """Inline keyboard sau khi ghi nhận uống nước."""
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("💧 Uống thêm ly nữa!", callback_data="drink"),
            InlineKeyboardButton("📊 Xem tiến độ", callback_data="status"),
        ]
    ])


# === Command Handlers ===

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /start — Đăng ký và bật nhắc nhở."""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Kiểm tra user đã tồn tại và đang active chưa
    existing = get_user(user_id)
    if existing and existing.get("is_active", False):
        await update.message.reply_text(ALREADY_STARTED, parse_mode="Markdown")
        return

    # Tạo hoặc cập nhật user
    user_data = create_user(user_id, chat_id)
    goal = user_data["goal"]
    interval = user_data["reminder_interval"]
    start = user_data["reminder_start"]
    end = user_data["reminder_end"]

    # Gửi tin nhắn chào mừng
    welcome = WELCOME_MESSAGE.format(
        interval=interval,
        start=start,
        end=end,
        goal=goal,
        goal_ml=goal * GLASS_ML,
    )
    await update.message.reply_text(
        welcome,
        parse_mode="Markdown",
        reply_markup=_drink_keyboard(),
    )

    # Thiết lập jobs nhắc nhở
    setup_user_jobs(context.application, user_id, chat_id, user_data)
    logger.info(f"User {user_id} đã bắt đầu nhắc nhở")


async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /stop — Tạm dừng nhắc nhở."""
    user_id = update.effective_user.id

    user = get_user(user_id)
    if not user or not user.get("is_active", False):
        await update.message.reply_text(ALREADY_STOPPED, parse_mode="Markdown")
        return

    # Tắt nhắc nhở
    set_active(user_id, False)
    remove_user_jobs(context.application, user_id)

    await update.message.reply_text(STOP_MESSAGE, parse_mode="Markdown")
    logger.info(f"User {user_id} đã dừng nhắc nhở")


async def drink_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /drink — Ghi nhận uống nước."""
    user_id = update.effective_user.id

    user = get_user(user_id)
    if not user:
        await update.message.reply_text(
            "❌ Bạn chưa đăng ký! Gửi /start để bắt đầu nhé~"
        )
        return

    # Ghi nhận
    updated_user = add_drink(user_id)
    current = updated_user["drinks_today"]
    goal = updated_user["goal"]
    percentage = min(int((current / goal) * 100), 100)
    progress_bar = build_progress_bar(current, goal)

    if current >= goal:
        motivation = get_goal_reached_message()
    else:
        motivation = get_motivation_message()

    message = DRINK_RECORDED.format(
        current=current,
        goal=goal,
        progress_bar=progress_bar,
        percentage=percentage,
        motivation=motivation,
    )

    await update.message.reply_text(
        message,
        parse_mode="Markdown",
        reply_markup=_drink_keyboard(),
    )
    logger.info(f"User {user_id} uống nước: {current}/{goal}")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /status — Xem tiến độ."""
    user_id = update.effective_user.id

    user = get_user(user_id)
    if not user:
        await update.message.reply_text(
            "❌ Bạn chưa đăng ký! Gửi /start để bắt đầu nhé~"
        )
        return

    current = user["drinks_today"]
    goal = user["goal"]
    percentage = min(int((current / goal) * 100), 100) if goal > 0 else 0
    progress_bar = build_progress_bar(current, goal)
    status_text = format_status_text(current, goal)

    message = STATUS_MESSAGE.format(
        goal=goal,
        goal_ml=goal * GLASS_ML,
        current=current,
        current_ml=current * GLASS_ML,
        percentage=percentage,
        progress_bar=progress_bar,
        status_text=status_text,
    )

    await update.message.reply_text(
        message,
        parse_mode="Markdown",
        reply_markup=_drink_keyboard(),
    )


async def goal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /goal <số> — Đặt mục tiêu."""
    user_id = update.effective_user.id

    user = get_user(user_id)
    if not user:
        await update.message.reply_text(
            "❌ Bạn chưa đăng ký! Gửi /start để bắt đầu nhé~"
        )
        return

    # Lấy số từ args
    if not context.args or len(context.args) < 1:
        await update.message.reply_text(GOAL_INVALID, parse_mode="Markdown")
        return

    try:
        new_goal = int(context.args[0])
        if new_goal < 1 or new_goal > 50:
            await update.message.reply_text(
                "❌ Mục tiêu phải từ 1 đến 50 ly nhé!", parse_mode="Markdown"
            )
            return
    except ValueError:
        await update.message.reply_text(GOAL_INVALID, parse_mode="Markdown")
        return

    set_goal(user_id, new_goal)
    message = GOAL_SET.format(goal=new_goal, goal_ml=new_goal * GLASS_ML)
    await update.message.reply_text(message, parse_mode="Markdown")
    logger.info(f"User {user_id} đặt mục tiêu: {new_goal} ly")


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /settings — Xem cài đặt."""
    user_id = update.effective_user.id

    user = get_user(user_id)
    if not user:
        await update.message.reply_text(
            "❌ Bạn chưa đăng ký! Gửi /start để bắt đầu nhé~"
        )
        return

    status = "🟢 Đang bật" if user.get("is_active", False) else "🔴 Đã tắt"

    message = SETTINGS_MESSAGE.format(
        start=user.get("reminder_start", 7),
        end=user.get("reminder_end", 22),
        interval=user.get("reminder_interval", 60),
        goal=user.get("goal", 8),
        goal_ml=user.get("goal", 8) * GLASS_ML,
        status=status,
    )

    await update.message.reply_text(message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /help — Hướng dẫn."""
    await update.message.reply_text(HELP_MESSAGE, parse_mode="Markdown")


# === Callback Query Handler ===

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý khi user bấm inline button."""
    query = update.callback_query
    await query.answer()  # Acknowledge callback

    user_id = query.from_user.id
    action = query.data

    if action == "drink":
        # Ghi nhận uống nước
        user = get_user(user_id)
        if not user:
            await query.edit_message_text(
                "❌ Bạn chưa đăng ký! Gửi /start để bắt đầu nhé~"
            )
            return

        updated_user = add_drink(user_id)
        current = updated_user["drinks_today"]
        goal = updated_user["goal"]
        percentage = min(int((current / goal) * 100), 100)
        progress_bar = build_progress_bar(current, goal)

        if current >= goal:
            motivation = get_goal_reached_message()
        else:
            motivation = get_motivation_message()

        message = DRINK_RECORDED.format(
            current=current,
            goal=goal,
            progress_bar=progress_bar,
            percentage=percentage,
            motivation=motivation,
        )

        await query.edit_message_text(
            message,
            parse_mode="Markdown",
            reply_markup=_drink_keyboard(),
        )
        logger.info(f"User {user_id} uống nước (button): {current}/{goal}")

    elif action == "status":
        # Xem tiến độ
        user = get_user(user_id)
        if not user:
            await query.edit_message_text(
                "❌ Bạn chưa đăng ký! Gửi /start để bắt đầu nhé~"
            )
            return

        current = user["drinks_today"]
        goal = user["goal"]
        percentage = min(int((current / goal) * 100), 100) if goal > 0 else 0
        progress_bar = build_progress_bar(current, goal)
        status_text = format_status_text(current, goal)

        message = STATUS_MESSAGE.format(
            goal=goal,
            goal_ml=goal * GLASS_ML,
            current=current,
            current_ml=current * GLASS_ML,
            percentage=percentage,
            progress_bar=progress_bar,
            status_text=status_text,
        )

        await query.edit_message_text(
            message,
            parse_mode="Markdown",
            reply_markup=_drink_keyboard(),
        )
