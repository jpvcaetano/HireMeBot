import logging
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import (
    LINKEDIN_EMAIL,
    LINKEDIN_LOGIN_URL,
    LINKEDIN_MESSAGING_URL,
    LINKEDIN_PASSWORD,
    SELENIUM_TIMEOUT,
)
from src.message_store import MessageStore


class LinkedInClient:
    def __init__(self):
        self.driver = None
        self.wait = None
        self._setup_driver()

    def _setup_driver(self):
        """Initialize Chrome driver with appropriate options"""
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

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
                By.CSS_SELECTOR, "button[type='submit']"
            )
            login_button.click()

            # Wait for login to complete
            self.wait.until(EC.url_contains("feed"))
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
            for ii, thread in enumerate(message_threads):
                thread_class = thread.get_attribute("class")

                #TODO: this is a hack to avoid making the first message read since self.driver.get(LINKEDIN_MESSAGING_URL) opens it and makes it read. 
                # We should make this more robust and clean in the future
                if ii == 0:
                    # Get the last message sender
                    last_message_sender = thread.find_element(
                        By.CSS_SELECTOR, ".msg-conversation-card__message-snippet-sender"
                    ).text.strip(" •")  # Remove the bullet point that LinkedIn adds
   
                    # If the last message is from myself, we skip it
                    if last_message_sender == "Jo\u00e3o Caetano":
                        continue
                    else:
                        thread_class = "unread"

                if "unread" in thread_class:
                    # Find the clickable element that contains the conversation link
                    link_element = thread.find_element(
                        By.CSS_SELECTOR, "div.msg-conversation-listitem__link"
                    )
                    
                    # Get the current URL before clicking
                    link_element.click()
                    conversation_id = self.driver.current_url.split('/messaging/thread/')[1].strip('/')
                    
                    # Go back to the messages list
                    self.driver.back()
                    
                    sender = thread.find_element(
                        By.CSS_SELECTOR, ".msg-conversation-card__participant-names"
                    ).text
                    preview = thread.find_element(
                        By.CSS_SELECTOR, ".msg-conversation-card__message-snippet"
                    ).text

                    unread_messages.append({
                        "conversation_id": conversation_id,
                        "sender": sender,
                        "preview": preview,
                    })

            return unread_messages

        except Exception as e:
            logging.error(f"Error fetching messages: {str(e)}")
            return []

    def send_message(self, conversation_id: str, message: str) -> bool:
        """Send a message in a specific conversation"""
        try:
            # Navigate to the specific conversation
            conversation_url = f"{LINKEDIN_MESSAGING_URL}/thread/{conversation_id}/"
            self.driver.get(conversation_url)

            # Wait for and find the message input field
            message_input = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[role='textbox'][contenteditable='true']")
                )
            )

            # Clear any existing text and send our message
            message_input.clear()
            message_input.send_keys(message)

            # Find and click the send button
            send_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            send_button.click()

            # Add a small delay to allow the message to be sent
            time.sleep(2)

            return True

        except Exception as e:
            logging.error(f"Failed to send message: {str(e)}")
            return False
