from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.settings import (
    LINKEDIN_EMAIL, 
    LINKEDIN_PASSWORD,
    LINKEDIN_LOGIN_URL,
    LINKEDIN_MESSAGING_URL,
    SELENIUM_TIMEOUT
)
import logging

class LinkedInClient:
    def __init__(self):
        self.driver = None
        self.wait = None
        self._setup_driver()
        
    def _setup_driver(self):
        """Initialize Chrome driver with appropriate options"""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, SELENIUM_TIMEOUT)
        
    def login(self):
        """Perform LinkedIn login"""
        try:
            self.driver.get(LINKEDIN_LOGIN_URL)
            
            # Find and fill email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_input.send_keys(LINKEDIN_EMAIL)
            
            # Find and fill password
            password_input = self.driver.find_element(By.ID, "password")
            password_input.send_keys(LINKEDIN_PASSWORD)
            
            # Click login button
            login_button = self.driver.find_element(
                By.CSS_SELECTOR, 
                "button[type='submit']"
            )
            login_button.click()
            
            # Wait for login to complete
            self.wait.until(
                EC.url_contains("feed")
            )
            return True
            
        except TimeoutException as e:
            logging.error(f"Login failed: {str(e)}")
            return False
            
    def get_messages(self):
        """Fetch unread messages from LinkedIn"""
        try:
            self.driver.get(LINKEDIN_MESSAGING_URL)
            
            # Wait for messages to load
            message_threads = self.wait.until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "div.msg-conversation-card")
                )
            )
            
            unread_messages = []
            for thread in message_threads:
                if "unread" in thread.get_attribute("class"):
                    conversation_id = thread.get_attribute("data-conversation-id")
                    sender = thread.find_element(
                        By.CSS_SELECTOR, 
                        ".msg-conversation-card__participant-names"
                    ).text
                    preview = thread.find_element(
                        By.CSS_SELECTOR, 
                        ".msg-conversation-card__message-snippet"
                    ).text
                    
                    unread_messages.append({
                        'conversation_id': conversation_id,
                        'sender': sender,
                        'preview': preview
                    })
                    
            return unread_messages
            
        except Exception as e:
            logging.error(f"Error fetching messages: {str(e)}")
            return [] 