from telegram import Bot
from telegram.error import TelegramError
from logging import Logger

import os
from dotenv import load_dotenv
import asyncio

def init_telegram_bot() -> tuple[Bot, str]:
    load_dotenv()
    api_key = os.getenv("TELEGRAM_API_KEY")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    bot = Bot(api_key)
    
    return bot, chat_id

async def send_top_global_workflow_output_alert(bot: Bot, chat_id: str, message: str, logger: Logger):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info("Message sent")
    except TelegramError as e:
        logger.error(f"error: {e}")
        
async def send_telegram_message(bot: Bot, chat_id: str, message: str, logger: Logger):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        logger.info("Message sent")
    except TelegramError as e:
        logger.error(f"error: {e}")

async def send_daily_follower_report(bot: Bot, chat_id: str, report_path: str, logger: Logger):
    try:
        with open(report_path, "rb") as file:
            await bot.send_document(chat_id=chat_id, 
                                    document=file,
                                    read_timeout=60,
                                    write_timeout=60)
        logger.info("report sent")
    except TelegramError as e:
        logger.error(f"error: {e}")