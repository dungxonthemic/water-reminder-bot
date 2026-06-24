"""
Các mẫu tin nhắn tiếng Việt cho bot nhắc nhở uống nước.
"""

import random

# === Tin nhắn nhắc nhở uống nước (ngẫu nhiên) ===
REMINDER_MESSAGES = [
    "💧 Đã đến giờ uống nước rồi nè! Cơ thể bạn đang cần nước đấy~",
    "🥤 Uống một ly nước đi bạn ơi! Giữ sức khỏe là quan trọng nhất!",
    "💦 Nhắc nhẹ: Uống nước thôi! Nước giúp da đẹp và tinh thần sảng khoái~",
    "🌊 Đừng quên uống nước nhé! Mỗi ngụm nước đều quý giá!",
    "💧 Hey! Ly nước của bạn đâu rồi? Uống ngay đi nào!",
    "🍶 Nghỉ tay một chút, uống ngụm nước rồi làm tiếp nhé!",
    "💦 Bạn đã uống nước chưa? Cơ thể cần 2 lít nước mỗi ngày đó!",
    "🫗 Uống nước = Yêu bản thân! Đừng quên nhé! 💪",
    "💧 Thời gian uống nước đây~ Hãy giữ thói quen tốt bạn nhé!",
    "🥛 Một ly nước cho sức khỏe! Bạn đang làm rất tốt rồi!",
    "💧 Ping! Đây là lời nhắc uống nước từ bot yêu thương của bạn~ 🤖❤️",
    "🌿 Cơ thể bạn đang khát nước đấy! Uống một ly ngay thôi!",
]

# === Tin nhắn chào mừng ===
WELCOME_MESSAGE = """
🌟 **Chào mừng bạn đến với Bot Nhắc Uống Nước!** 💧

Mình sẽ giúp bạn duy trì thói quen uống nước đều đặn mỗi ngày.

📋 **Cách sử dụng:**
• /drink hoặc bấm nút 💧 — Ghi nhận uống nước
• /status — Xem tiến độ hôm nay
• /goal `<số>` — Đặt mục tiêu số ly
• /settings — Xem cài đặt hiện tại
• /stop — Tạm dừng nhắc nhở
• /start — Bật lại nhắc nhở
• /help — Xem hướng dẫn

⏰ **Nhắc nhở đã được bật!**
Mình sẽ nhắc bạn mỗi {interval} phút từ {start}:00 đến {end}:00.

🎯 Mục tiêu hôm nay: **{goal} ly nước** ({goal_ml}ml)

Chúc bạn một ngày tràn đầy năng lượng! 💪
"""

# === Tin nhắn ghi nhận uống nước ===
DRINK_RECORDED = """
✅ **Tuyệt vời!** Đã ghi nhận 1 ly nước (250ml)! 💧

📊 Tiến độ hôm nay: **{current}/{goal} ly**
{progress_bar}
{percentage}% hoàn thành

{motivation}
"""

# === Tin nhắn khi đạt mục tiêu ===
GOAL_REACHED_MESSAGES = [
    "🎉🎊 **CHÚC MỪNG!** Bạn đã uống đủ nước hôm nay! Quá xuất sắc! 🏆",
    "🥳🌟 **TUYỆT VỜI!** Mục tiêu hoàn thành! Bạn thật giỏi! 💪✨",
    "🏆🎯 **HOÀN HẢO!** Đủ nước rồi! Cơ thể bạn đang cảm ơn bạn đấy! 💕",
    "🌈⭐ **AMAZING!** Bạn đã chinh phục mục tiêu uống nước hôm nay! 🚀",
]

# === Tin nhắn động viên (chưa đạt mục tiêu) ===
MOTIVATION_MESSAGES = [
    "Cố lên! Bạn sắp đạt mục tiêu rồi! 💪",
    "Mỗi ly nước đều quan trọng! Tiếp tục nhé! 🌟",
    "Bạn đang làm rất tốt! Giữ vững nhé! ⭐",
    "Nước = Sức khỏe = Hạnh phúc! 🌈",
    "Thật tuyệt khi bạn nhớ uống nước! 👏",
    "Keep going! Bạn là ngôi sao! ⭐",
]

# === Tin nhắn trạng thái ===
STATUS_MESSAGE = """
📊 **Tiến Độ Uống Nước Hôm Nay**

🎯 Mục tiêu: **{goal} ly** ({goal_ml}ml)
💧 Đã uống: **{current} ly** ({current_ml}ml)
📈 Tiến độ: {percentage}%

{progress_bar}

{status_text}
"""

# === Tin nhắn cài đặt ===
SETTINGS_MESSAGE = """
⚙️ **Cài Đặt Hiện Tại**

⏰ Giờ bắt đầu nhắc: **{start}:00**
⏰ Giờ kết thúc nhắc: **{end}:00**
🔁 Khoảng cách nhắc: **{interval} phút**
🎯 Mục tiêu: **{goal} ly/ngày** ({goal_ml}ml)
📍 Trạng thái: **{status}**

💡 Dùng /goal `<số>` để thay đổi mục tiêu.
"""

# === Tin nhắn help ===
HELP_MESSAGE = """
📖 **Hướng Dẫn Sử Dụng Bot Uống Nước** 💧

📋 **Các lệnh:**
• /start — Bật nhắc nhở uống nước
• /stop — Tạm dừng nhắc nhở
• /drink — Ghi nhận đã uống 1 ly (250ml)
• /status — Xem tiến độ hôm nay
• /goal `<số>` — Đặt mục tiêu (VD: /goal 10)
• /settings — Xem cài đặt hiện tại
• /help — Xem hướng dẫn này

💡 **Mẹo:**
• Mỗi lần nhận tin nhắn nhắc nhở, bấm nút 💧 để ghi nhận nhanh
• Bot sẽ tự động reset bộ đếm vào 0:00 mỗi ngày
• Uống nước đều đặn giúp tăng cường sức khỏe và sự tập trung!

🤖 Bot được tạo với ❤️ để giúp bạn khỏe mạnh hơn mỗi ngày!
"""

# === Tin nhắn dừng ===
STOP_MESSAGE = """
⏸️ **Đã tạm dừng nhắc nhở!**

Bạn sẽ không nhận được tin nhắn nhắc uống nước nữa.
Gửi /start bất cứ lúc nào để bật lại nhé! 💧
"""

# === Tin nhắn khi đã dừng rồi mà bấm stop ===
ALREADY_STOPPED = "⏸️ Nhắc nhở đã tắt rồi bạn ơi! Gửi /start để bật lại nhé~"

# === Tin nhắn khi đã bật rồi mà bấm start ===
ALREADY_STARTED = "✅ Nhắc nhở đang bật rồi bạn ơi! Mình đang theo dõi cho bạn~"

# === Tin nhắn đặt mục tiêu ===
GOAL_SET = "🎯 Đã đặt mục tiêu mới: **{goal} ly/ngày** ({goal_ml}ml)! Cố gắng nhé! 💪"
GOAL_INVALID = "❌ Vui lòng nhập số hợp lệ! VD: /goal 8"

# === Tin nhắn reset hằng ngày ===
DAILY_RESET = """
🌅 **Chào buổi sáng!** Một ngày mới bắt đầu rồi!

🎯 Mục tiêu hôm nay: **{goal} ly nước** ({goal_ml}ml)
💧 Bộ đếm đã được reset về 0.

Hãy bắt đầu ngày mới với một ly nước nhé! 💪
"""


def get_reminder_message() -> str:
    """Lấy một tin nhắn nhắc nhở ngẫu nhiên."""
    return random.choice(REMINDER_MESSAGES)


def get_goal_reached_message() -> str:
    """Lấy một tin nhắn chúc mừng ngẫu nhiên."""
    return random.choice(GOAL_REACHED_MESSAGES)


def get_motivation_message() -> str:
    """Lấy một tin nhắn động viên ngẫu nhiên."""
    return random.choice(MOTIVATION_MESSAGES)


def build_progress_bar(current: int, goal: int, length: int = 10) -> str:
    """Tạo thanh progress bar bằng emoji."""
    if goal <= 0:
        return "⬜" * length

    filled = min(int((current / goal) * length), length)
    empty = length - filled
    return "🟩" * filled + "⬜" * empty


def format_status_text(current: int, goal: int) -> str:
    """Tạo text trạng thái dựa trên tiến độ."""
    if current >= goal:
        return get_goal_reached_message()
    elif current >= goal * 0.75:
        return "🔥 Sắp đạt mục tiêu rồi! Chỉ còn {} ly nữa thôi!".format(goal - current)
    elif current >= goal * 0.5:
        return "👍 Đã qua nửa chặng đường! Tiếp tục phát huy nhé!"
    elif current > 0:
        return "💧 Mới bắt đầu thôi, cố gắng uống thêm nhé!"
    else:
        return "😅 Bạn chưa uống ly nào hôm nay! Bắt đầu ngay thôi!"
