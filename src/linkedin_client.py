import logging
import re
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
        # options.add_argument("--headless")  # Run in headless mode
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

            # Uncheck the "Keep me logged in" checkbox
            try:
                keep_logged_in_checkbox = self.driver.find_element(
                    By.ID, "rememberMeOptIn-checkbox"
                )
                if keep_logged_in_checkbox.is_selected():
                    # Use JavaScript to uncheck the box
                    self.driver.execute_script(
                        "arguments[0].click();", keep_logged_in_checkbox
                    )
            except Exception as e:
                logging.warning(f"Could not uncheck 'Remember me' box: {str(e)}")

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

                # Handle the first message differently to avoid marking it as read
                flag = False
                if ii == 0:
                    try:

                        message_blocks = self.wait.until(
                            EC.presence_of_all_elements_located(
                                (By.CSS_SELECTOR, "li.msg-s-message-list__event")
                            )
                        )
                        # Scroll to the last message so it fully loads
                        self.scroll_to_element(message_blocks[-1])
                        # Search for the last message name
                        pattern = r"\n([A-Za-zÀ-ÿ\s]+)\s\d{2}:\d{2}\n"
                        last_message_name = re.search(pattern, message_blocks[-1].text)

                        # If the sender name matches your name, skip it
                        if "João Caetano" in last_message_name.group(1):
                            continue
                        else:
                            flag = True
                    except Exception as e:
                        logging.warning(
                            f"Could not determine first message sender: {str(e)}"
                        )

                if "unread" in thread.get_attribute("class") or flag:
                    # Find the clickable element that contains the conversation link
                    link_element = thread.find_element(
                        By.CSS_SELECTOR, "div.msg-conversation-listitem__link"
                    )

                    # Get the current URL before clicking
                    link_element.click()
                    conversation_id = self.driver.current_url.split(
                        "/messaging/thread/"
                    )[1].strip("/")

                    sender = thread.find_element(
                        By.CSS_SELECTOR, ".msg-conversation-card__participant-names"
                    ).text
                    preview = thread.find_element(
                        By.CSS_SELECTOR, ".msg-conversation-card__message-snippet"
                    ).text

                    unread_messages.append(
                        {
                            "conversation_id": conversation_id,
                            "sender": sender,
                            "preview": preview,
                        }
                    )

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

    def scroll_to_element(self, element):
        """Scrolls to element first, then to the top of the page"""
        # First scroll to element to ensure it's loaded
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'auto', block: 'start'});", element
        )
        time.sleep(1)  # Brief pause to ensure element is loaded
