import os

from dotenv import load_dotenv

PATH_TO_PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PATH_TO_ENV = os.path.join(PATH_TO_PROJECT, '.env')

load_dotenv(PATH_TO_ENV)

DB_URL = os.getenv('DB_URL')

ADMIN_BOT_TOKEN = os.getenv('ADMIN_BOT_TOKEN')
CLIENT_BOT_TOKEN = os.getenv('CLIENT_BOT_TOKEN')
EMPLOYEE_BOT_TOKEN = os.getenv('EMPLOYEE_BOT_TOKEN')

DEFAULT_ADMIN_KEY_FOR_LOGIN = os.getenv('DEFAULT_ADMIN_KEY_FOR_LOGIN')
DEFAULT_EMPLOYEE_KEY_FOR_LOGIN = os.getenv('DEFAULT_EMPLOYEE_KEY_FOR_LOGIN')