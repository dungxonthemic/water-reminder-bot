"""
Bot Telegram Nhắc Nhở Uống Nước 💧
Entry point - Khởi chạy bot.
Hỗ trợ 2 mode:
  - Polling (local): py bot.py
  - Webhook (Render): tự detect qua RENDER_EXTERNAL_URL
"""

import logging
import sys
import asyncio
import json

import tornado.web
from telegram import BotCommand, Update
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


async def post_init(application):
    """Thiết lập các lệnh (Commands Menu) cho bot."""
    commands = [
        BotCommand("start", "Bắt đầu nhắc nhở uống nước 💧"),
        BotCommand("drink", "Ghi nhận lượng nước đã uống 🥤"),
        BotCommand("status", "Xem thống kê nước uống hôm nay 📊"),
        BotCommand("goal", "Thay đổi mục tiêu lượng nước 🎯"),
        BotCommand("settings", "Thay đổi cấu hình nhắc nhở ⚙️"),
        BotCommand("help", "Xem hướng dẫn chi tiết ℹ️"),
        BotCommand("stop", "Tạm dừng nhắc nhở uống nước 🛑"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("✅ Đã thiết lập Menu Lệnh tự động.")


class MainHandler(tornado.web.RequestHandler):
    """Handler cho trang chủ (root path) để trả về 200 OK cho keep-alive."""
    def get(self):
        self.set_status(200)
        self.write("OK")


class TelegramWebhookHandler(tornado.web.RequestHandler):
    """Handler nhận webhook updates từ Telegram."""
    async def post(self):
        try:
            # Lấy dữ liệu update từ Telegram
            data = json.loads(self.request.body)
            # Chuyển đổi thành đối tượng Update và đẩy vào hàng đợi của bot
            ptb_app = self.settings["ptb_app"]
            update = Update.de_json(data, ptb_app.bot)
            await ptb_app.update_queue.put(update)
            self.set_status(200)
            self.write("OK")
        except Exception as e:
            logger.error(f"Lỗi khi xử lý webhook: {e}")
            self.set_status(500)
            self.write("Internal Server Error")


async def run_webhook_mode(application):
    """Chạy bot ở chế độ Webhook với custom Tornado server để hỗ trợ GET /."""
    # Khởi tạo application (sẽ chạy post_init để cài menu tự động)
    await application.initialize()
    await application.start()

    # Thiết lập webhook URL với Telegram
    webhook_url = f"{RENDER_EXTERNAL_URL}/{BOT_TOKEN}"
    await application.bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True,
    )
    logger.info(f"🚀 Đã đăng ký webhook thành công với Telegram: {webhook_url}")

    # Tạo ứng dụng Tornado hỗ trợ cả GET / (cho cron-job) và POST /token (cho Telegram)
    tornado_app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/" + BOT_TOKEN, TelegramWebhookHandler),
    ], ptb_app=application)

    tornado_app.listen(PORT, address="0.0.0.0")
    logger.info(f"✅ Web server đang lắng nghe tại port {PORT}")

    try:
        # Vòng lặp vô hạn giữ server hoạt động
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Đang dừng bot...")
    finally:
        # Giải phóng tài nguyên khi dừng
        await application.stop()
        await application.shutdown()
        logger.info("👋 Bot đã dừng hoàn toàn.")


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

    # Tạo application với post_init để cài đặt menu lệnh
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

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
        # --- Webhook mode (Render deployment với custom Tornado) ---
        asyncio.run(run_webhook_mode(application))
    else:
        # --- Polling mode (local development) ---
        logger.info("✅ Bot đã sẵn sàng! Đang lắng nghe (polling mode)...")
        application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
