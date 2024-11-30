import logging
import time

from config.settings import CHECK_INTERVAL
from src.chat_handler import ChatHandler
from src.job_analyzer import JobAnalyzer
from src.linkedin_client import LinkedInClient
from src.message_store import MessageStore
from src.notifier import Notifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    # Initialize components
    linkedin = LinkedInClient()
    chat_handler = ChatHandler()
    message_store = MessageStore()
    job_analyzer = JobAnalyzer(chat_handler)
    notifier = Notifier()

    # Login to LinkedIn
    if not linkedin.login():
        logger.error("Failed to login to LinkedIn")
        return

    logger.info("Started LinkedIn chat bot")

    while True:
        try:
            # Check for new messages
            # TODO: when we read a new message we should mark it as read
            new_messages = linkedin.get_messages()

            for message in new_messages:
                # Store message
                message_store.add_message(
                    message["conversation_id"], message["sender"], message["preview"]
                )

                # Get conversation history
                history = message_store.format_history(message["conversation_id"])

                # Generate response
                response = chat_handler.generate_response(
                    conversation_history=history,
                    message=message["preview"],
                    template_key="conversation_response",
                )

                # Analyze for job details
                analysis = job_analyzer.analyze_opportunity(history)
                if job_analyzer.should_notify(analysis):
                    notifier.notify_job_opportunity(analysis)

                if response:
                    # Send response
                    success = linkedin.send_message(
                        message["conversation_id"], response
                    )
                    if success:
                        # Store response
                        message_store.add_message(
                            message["conversation_id"], "JoãoGPT", response
                        )
                    else:
                        logger.error(f"Failed to send response to {message['sender']}")

            # Wait before next check
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()
