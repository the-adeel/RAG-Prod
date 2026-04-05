import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your .env file.")

TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": [
                "aerich.models","doc",
            ],
            "default_connection": "default",
        },
    },
}