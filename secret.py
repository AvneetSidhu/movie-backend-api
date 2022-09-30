from dotenv import load_dotenv
import os 

load_dotenv()

ENV = os.getenv("MYENV")

API_KEY = os.getenv('MOVIEAPIKEY')
BASE_URL = os.getenv('BASEURL')

ADMIN_USER = os.getenv('ADMINUSER')
ADMIN_PASS = os.getenv('ADMINPASS')
