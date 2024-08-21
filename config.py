import os


class Config(object):
    TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")

    APP_ID = int(os.environ.get("APP_ID", 29969440))

    API_HASH = os.environ.get("API_HASH", "d7d737e044f59b736691dd2c0fc7879e")
