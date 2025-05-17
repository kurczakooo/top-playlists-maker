from telegram import Bot
from telegram.error import TelegramError

import os
from dotenv import load_dotenv
import asyncio

load_dotenv()
api_key = os.getenv("TELEGRAM_API_KEY")
chat_id = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(api_key)

async def send_top_global_workflow_output_alert(bot: Bot, chat_id: str, message: str):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        print("Message sent")
    except TelegramError as e:
        print(f"error: {e}")
        

async def send_daily_follower_report(bot: Bot, chat_id: str, report_path: str):
    try:
        with open(report_path, "rb") as file:
            await bot.send_document(chat_id=chat_id, 
                                    document=file,
                                    read_timeout=60,
                                    write_timeout=60)
        print("report sent")
    except TelegramError as e:
        print(f"error: {e}")