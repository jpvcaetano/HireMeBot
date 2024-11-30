import time
import logging
from config.settings import CHECK_INTERVAL
from src.linkedin_client import LinkedInClient
from src.chat_handler import ChatHandler
from src.job_analyzer import JobAnalyzer
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
            new_messages = linkedin.get_messages()
            
            for message in new_messages:
                # Store message
                message_store.add_message(
                    message['conversation_id'],
                    message['sender'],
                    message['preview']
                )
                
                # Get conversation history
                history = message_store.format_history(message['conversation_id'])
                
                # Generate response
                response = chat_handler.generate_response(
                    conversation_history=history,
                    context="Professional conversation with recruiter",
                    message=message['preview']
                )
                
                # Analyze for job details
                job_details = job_analyzer.extract_job_details(message['preview'])
                if job_details:
                    analysis = job_analyzer.analyze_opportunity(job_details)
                    if job_analyzer.should_notify(analysis):
                        notifier.notify_job_opportunity(analysis)
                
                # Send response
                if response:
                    success = linkedin.send_message(message['conversation_id'], response)
                    if not success:
                        logger.error(f"Failed to send response to {message['sender']}")
                
                # Notify user
                notifier.notify_new_message(message['sender'], message['preview'])
                
            # Wait before next check
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            logger.error(f"Error in main loop: {str(e)}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main() 