from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRATION_MINUTES = int(os.getenv("EXPIRATION_MINUTES", 60))
#SECRET_KEY = "your-default-secret-key"