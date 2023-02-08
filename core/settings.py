from os import environ as env
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DB_HOST = env.get('DB_HOST')
    DB_PORT = env.get('DB_PORT')
    DB_USER = env.get('DB_USER')
    DB_PASS = env.get('DB_PASS')
    DB_NAME = env.get('DB_NAME')


settings = Settings()