"""
Bot Telegram Nhắc Nhở Uống Nước 💧
Entry point - Khởi chạy bot.
Hỗ trợ 2 mode:
  - Polling (local): py bot.py
  - Webhook (Render): tự detect qua RENDER_EXTERNAL_URL
"""

import logging
import sys

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
)

from config import BOT_TOKEN, WEBHOOK_MODE, RENDER_EXTERNAL_URL, PORT
from handlers import (
    start_command,
    stop_command,
    drink_command,
    status_command,
    goal_command,
    settings_command,
    help_command,
    button_callback,
)
from scheduler import restore_all_jobs

# === Cấu hình logging ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Giảm log spam từ httpx
logging.getLogger("httpx").setLevel(logging.WARNING)


def main():
    """Khởi chạy bot."""
    # Kiểm tra token
    if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
        logger.error(
            "❌ Chưa cấu hình TELEGRAM_BOT_TOKEN!\n"
            "   1. Tạo bot qua @BotFather trên Telegram\n"
            "   2. Copy token và tạo file .env:\n"
            "      TELEGRAM_BOT_TOKEN=your_token_here\n"
        )
        sys.exit(1)

    logger.info("🚀 Đang khởi động Bot Nhắc Uống Nước...")

    # Tạo application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # === Đăng ký command handlers ===
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("stop", stop_command))
    application.add_handler(CommandHandler("drink", drink_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("goal", goal_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("help", help_command))

    # === Đăng ký callback handler cho inline buttons ===
    application.add_handler(CallbackQueryHandler(button_callback))

    # === Khôi phục jobs cho các user đã đăng ký ===
    restore_all_jobs(application)

    # === Chạy bot ===
    if WEBHOOK_MODE:
        # --- Webhook mode (Render deployment) ---
        webhook_url = f"{RENDER_EXTERNAL_URL}/{BOT_TOKEN}"
        logger.info(f"✅ Bot chạy webhook mode tại port {PORT}")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,
            webhook_url=webhook_url,
            drop_pending_updates=True,
        )
    else:
        # --- Polling mode (local development) ---
        logger.info("✅ Bot đã sẵn sàng! Đang lắng nghe (polling mode)...")
        application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
