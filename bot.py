import random
import asyncio
import os
from telegram.ext import ApplicationBuilder, ContextTypes
from telegram.request import HTTPXRequest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# ================= CONFIG =================
TOKEN = "8588524506:AAF44_0hhiKTf0zwSwfJdD2wWLzKvRwrQAc"
CHANNEL_ID = -1003727406190

GRID_SIZE = 5
BOMBS = 3
SAFE_PICKS = 5

SEND_EVERY = 120
SCAN_DURATION = 60
PROGRESS_STEPS = 10
# =========================================

def generate_signal():
    total_tiles = GRID_SIZE * GRID_SIZE
    safe_positions = random.sample(range(total_tiles), SAFE_PICKS)

    accuracy = random.randint(90, 100)
    filled_blocks = accuracy // 10
    accuracy_bar = "█" * filled_blocks + "░" * (10 - filled_blocks)

    grid = ["⭐" if i in safe_positions else "⬛" for i in range(total_tiles)]

    grid_text = ""
    for row in range(0, total_tiles, GRID_SIZE):
        row_tiles = " ".join(grid[row:row + GRID_SIZE])
        grid_text += f"┃  {row_tiles}  ┃\n"

    text = (
        "💣 1WIN • MINES SIGNAL 💣\n\n"
        "┏━━━━━━━━━━━━━━┓\n"
        f"┃ 💣 Bombs        : {BOMBS:<2}        ┃\n"
        f"┃ ⭐ Safe Moves: {SAFE_PICKS:<2}       ┃\n"
        f"┃ 🎯 Accuracy    :{accuracy}%    ┃\n"
        f"┃ 📊 Confidence: {accuracy_bar}┃\n"
        "┗━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "🔮 PREDICTED\n"
        "┏━━━━━━━━━━━━┓\n"
        f"{grid_text}"
        "┗━━━━━━━━━━━━┛\n\n"
        "🎁 PROMO CODE: SUCC1WIN\n"
        "⚠️ Only for 1WIN users"
    )

    buttons = [
        [InlineKeyboardButton("🚀 Play Now", url="https://1win.com/casino/play/v_spribe:miniroulette")],
        [InlineKeyboardButton("🎁 REGISTER", url="https://1win.com")]
    ]
    return text, InlineKeyboardMarkup(buttons)

async def send_signal_job(context: ContextTypes.DEFAULT_TYPE):
    message = await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="👀 Scanning mines signal...\n🧠 Looking for high accuracy signal\n\n📊 Signal loading...\n░░░░░░░░░░"
    )

    sleep_per_step = SCAN_DURATION / PROGRESS_STEPS

    for step in range(1, PROGRESS_STEPS + 1):
        await asyncio.sleep(sleep_per_step)
        bar = "█" * step + "░" * (PROGRESS_STEPS - step)

        try:
            await context.bot.edit_message_text(
                chat_id=CHANNEL_ID,
                message_id=message.message_id,
                text=f"👀 Scanning mines signal...\n🧠 Looking for high accuracy signal\n\n📊 Progress:\n{bar}"
            )
        except Exception:
            pass

    try:
        await context.bot.delete_message(chat_id=CHANNEL_ID, message_id=message.message_id)
    except Exception:
        pass

    text, markup = generate_signal()
    await context.bot.send_message(chat_id=CHANNEL_ID, text=text, reply_markup=markup)

def main():
    print("🤖 Starting Channel signal bot...")
    request = HTTPXRequest(connect_timeout=30, read_timeout=30)

    app = (ApplicationBuilder().token(TOKEN).request(request).build())
    app.job_queue.run_repeating(send_signal_job, interval=SEND_EVERY, first=5)

    print("🤖 Channel signal bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()