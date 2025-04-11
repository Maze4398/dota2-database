import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Configuration
    OPENDOTA_API_URL = "https://api.opendota.com/api"
    RATE_LIMIT = 60  # requests per minute
    REQUESTS_PER_DAY = 2000
    
    # Data storage
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
    RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
    PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
    
    @staticmethod
    def ensure_dirs_exist():
        os.makedirs(Config.RAW_DATA_DIR, exist_ok=True)
        os.makedirs(Config.PROCESSED_DATA_DIR, exist_ok=True)