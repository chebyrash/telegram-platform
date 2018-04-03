import json
import logging

from .base_bot import BaseBot


class TelegramClient(BaseBot):
    def __init__(self, config: dict = None):
        super().__init__(self.process_message)
        with open("config.json", "r") as file: #With 'r' it's READEBLY | yay ^.^
            self._config = config if config is not None else json.loads(file.read())["telegram_client"]
            file.close() #A K A yebanstvo

    @staticmethod
    def _log(message: str):
        logging.info("[TELEGRAM CLIENT] %s" % message)

    def run(self):
        super().run()
        """После этой строки запуск всяких серверов или клиентов"""

    async def process_message(self, message: dict):
        pass
        """Здесь обработка сообщений от центрального сервера"""
