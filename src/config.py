import os
from pathlib import Path

from dotenv import load_dotenv

PATH_TO_PROJECT = Path(__file__).parent.parent
PATH_TO_ENV = PATH_TO_PROJECT / '.env'

load_dotenv(PATH_TO_ENV)

DB_URL = os.getenv('DB_URL')

ADMIN_BOT_TOKEN = os.getenv('ADMIN_BOT_TOKEN')
CLIENT_BOT_TOKEN = os.getenv('CLIENT_BOT_TOKEN')
EMPLOYEE_BOT_TOKEN = os.getenv('EMPLOYEE_BOT_TOKEN')

DEFAULT_ADMIN_TOKEN_FOR_LOGIN = os.getenv('DEFAULT_ADMIN_TOKEN_FOR_LOGIN')
DEFAULT_EMPLOYEE_TOKEN_FOR_LOGIN = os.getenv('DEFAULT_EMPLOYEE_TOKEN_FOR_LOGIN')
