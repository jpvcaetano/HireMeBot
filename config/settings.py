import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LinkedIn credentials
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Application settings
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))  # Default 5 minutes
MAX_RETRIES = 3
SELENIUM_TIMEOUT = 10

# LinkedIn URLs
LINKEDIN_BASE_URL = "https://www.linkedin.com"
LINKEDIN_LOGIN_URL = f"{LINKEDIN_BASE_URL}/login"
LINKEDIN_MESSAGING_URL = f"{LINKEDIN_BASE_URL}/messaging"
