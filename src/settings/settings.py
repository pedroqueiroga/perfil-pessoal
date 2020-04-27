import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv('PORT', '5000'))
DEBUG = bool(os.getenv('DEBUG', 'False'))
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')
API_KEY = os.getenv('MAILGUN_API_KEY')
MY_EMAIL = os.getenv('MY_EMAIL')
