from dotenv import load_dotenv
import os
from pathlib import Path
import yaml

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


CONFIG_FILE = Path("src/config/config.yaml")


class Config:

    def __init__(self):

        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            self.data = yaml.safe_load(file)

    @property
    def keywords(self):
        return self.data.get("keywords", [])

    @property
    def locations(self):
        return self.data.get("locations", [])

    @property
    def remote(self):
        return self.data.get("remote", False)

    @property
    def sources(self):
        return self.data.get("sources", [])

    @property
    def max_results(self):
        return self.data.get("max_results", 100)

    @property
    def output(self):
        return self.data.get("output", "google_sheets")


config = Config()