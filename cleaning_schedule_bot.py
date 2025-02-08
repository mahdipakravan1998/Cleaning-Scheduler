import nest_asyncio
nest_asyncio.apply()  # Allow nested event loops

import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Enable logging (useful for debugging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Cleaning Schedule Code ---

participants = ["Hassan", "Kasra", "Mahdi", "Salar"]
no_cleaning_days = ["Thursday"]
start_cleaning_count = 0  # Reset cleaning count to 0 after the first cycle

def generate_cleaning_schedule():
    cleaning_count = {participant: start_cleaning_count for participant in participants}
    schedule = []
    days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    def get_next_cleaner(day, day_index, week_number):
        nonlocal cleaning_count
        # Exclude Hassan on Sunday of Week 1
        if week_number % 2 == 1 and day_index == 0:
            available_cleaners = [p for p in participants if p != "Hassan" and day not in no_cleaning_days]
        else:
            available_cleaners = [p for p in participants if day not in no_cleaning_days]
        next_cleaner = min(available_cleaners, key=lambda p: cleaning_count[p])
        cleaning_count[next_cleaner] += 1
        return next_cleaner

    current_day_index = 0
    total_days = 33  # Run the schedule for 33 days for equal distribution
    week_number = 1

    for _ in range(total_days):
        day_of_week = days_of_week[current_day_index % len(days_of_week)]
        if current_day_index % 7 == 0 and current_day_index != 0:
            week_number += 1
        if day_of_week not in no_cleaning_days:
            cleaner = get_next_cleaner(day_of_week, current_day_index % 7, week_number)
        else:
            cleaner = "No Cleaning"
        schedule.append((day_of_week, cleaner, dict(cleaning_count)))
        current_day_index += 1

    return schedule

# --- Bot Command Handlers (Async) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    await update.message.reply_text(
        "Hello! I am your Cleaning Scheduler bot. Type /schedule to see the cleaning schedule."
    )

async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate and send the cleaning schedule."""
    cleaning_schedule = generate_cleaning_schedule()
    schedule_message = "Cleaning Schedule:\n\n"
    for day, cleaner, count in cleaning_schedule:
        schedule_message += f"{day:<12} {cleaner:<10}\n"
        schedule_message += f"Cleaning Count: {count}\n\n"
    await update.message.reply_text(schedule_message)

# --- Main Function to Run the Bot ---

async def main():
    # Replace with your actual bot token
    TOKEN = "7681758129:AAGC6-MrQz2mRth4KkE5yEgUGOhLjmabYSo"
    application = ApplicationBuilder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("schedule", schedule_command))

    # Run the bot until you press Ctrl+C
    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())