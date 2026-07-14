import requests

from src.config.config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from src.notifications.base import Notification
from src.logger import logger


class TelegramNotification(Notification):

    def send(self, message: str):

        logger.info("[Telegram] Sending message...")

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }

        response = requests.post(url, data=payload)

        if response.status_code == 200:
            logger.info("[Telegram] Message sent successfully.")

        else:
            logger.error("[Telegram] Failed to send message.")
            logger.error(response.text)