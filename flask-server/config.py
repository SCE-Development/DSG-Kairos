import base64
import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    APIKEY = (base64.b64encode(str.encode(os.environ["INSIGHTLY_APIKEY"]))).decode()
    HOST = os.environ.get("RDS_HOST_NAME"),
    USER = os.environ.get("RDS_USER"),
    PASSWORD = os.environ.get("RDS_PASSWORD"),
    DATABASE = os.environ.get("DATABASE"),
    USE_SCHEDULER = True,
    DEBUG = False