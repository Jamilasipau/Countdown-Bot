import telebot
import datetime
import time
import pytz
import threading

# Replace with your Telegram bot token
BOT_TOKEN = "8107848491:AAFs-HAHYsCLlKGlWGMu-C7G1cCTkXrT3jo"
# Replace with your Telegram user ID
USER_ID = 6897739611

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

# Target date for the countdown
TARGET_DATE = datetime.date(2025, 8, 27)

# Indian Standard Time timezone
IST = pytz.timezone("Asia/Kolkata")

# Global flag to indicate bot status
bot_status = {"active": True}


def calculate_days_remaining():
    """Calculates the days remaining to the target date."""
    today = datetime.date.today()
    days_remaining = (TARGET_DATE - today).days
    return days_remaining


def wait_until_midnight():
    """Waits until 12 AM IST."""
    now = datetime.datetime.now(IST)
    next_midnight = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    wait_seconds = (next_midnight - now).total_seconds()
    time.sleep(wait_seconds)


def send_daily_message():
    """Sends the countdown message daily at 12 AM IST."""
    while True:
        try:
            # Wait until 12 AM IST
            wait_until_midnight()
            
            # Calculate remaining days
            days_remaining = calculate_days_remaining()
            
            # Compose message
            if days_remaining > 0:
                message = f"Countdown to 27 August 2025: {days_remaining} days remaining."
            elif days_remaining == 0:
                message = "Today is the day: 27 August 2025!"
            else:
                message = "The countdown has ended!"

            # Send the message
            bot.send_message(USER_ID, message)

        except Exception as e:
            # Log errors and notify the user
            error_message = f"An error occurred: {e}"
            bot.send_message(USER_ID, error_message)
            time.sleep(60)  # Retry after 60 seconds


@bot.message_handler(commands=["status"])
def handle_status(message):
    """Responds to /status command."""
    if message.chat.id == USER_ID:
        status_message = "Bot is active and running." if bot_status["active"] else "Bot is inactive."
        bot.send_message(USER_ID, status_message)


def run_bot():
    """Runs the bot in a separate thread."""
    bot.polling(non_stop=True)


if __name__ == "__main__":
    # Start the bot in a separate thread
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()

    # Start the daily message loop
    try:
        send_daily_message()
    except KeyboardInterrupt:
        bot_status["active"] = False
        print("Bot stopped.")
        