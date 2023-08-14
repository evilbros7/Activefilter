from pyrogram import filters
from pyrogram.types import Message
import datetime
import asyncio
from database.users_chats_db import db
from bot import app  # Import the 'app' instance from bot.py

from info import ADMINS, LOG_CHANNEL

# Dictionary to store users' set log times
user_log_times = {}

# Command handler for setting log time
@app.on_message(filters.command("setlogtime") & filters.user(ADMINS))
async def set_log_time(_, message: Message):  # Change 'client' to '_' to ignore the unused parameter
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        command_parts = message.text.split()
        if len(command_parts) < 2:
            await message.reply("Usage: /setlogtime HH:MM")
            return

        time_parts = command_parts[1].split(":")
        if len(time_parts) != 2:
            await message.reply("Invalid time format. Please use HH:MM format.")
            return

        hours, minutes = map(int, time_parts)
        user_log_times[user_id] = (hours, minutes)
        await message.reply(f"Log time set to {hours:02d}:{minutes:02d}.")

    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# Function to send the log to the specified channel
async def send_log():
    while True:
        current_time = datetime.datetime.now()
        total_chat = await db.total_chat_count()
        total_users = await db.total_users_count()
        for user_id, log_time in user_log_times.items():
            if current_time.hour == log_time[0] and current_time.minute == log_time[1]:
                # Replace with your logic to fetch and format the log
                log_text = f"Log Send...\nDate/Time: {current_time}\nTotal Users: {total_users}\nTotal Chats: {total_chat}"
                await app.send_message(LOG_CHANNEL, log_text)  # Use 'app' instead of 'bot'

        await asyncio.sleep(60)  # Check every minute

# Start the log sending loop
@app.on_startup
async def start_log_sender(_):
    await asyncio.create_task(send_log())
    
