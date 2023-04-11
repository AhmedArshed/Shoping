import os
from dotenv import load_dotenv


load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")

DB_URL = os.getenv("DB_URL")
DB_NAME = os.getenv("DB_NAME")