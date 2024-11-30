import logging
from typing import Any, Dict

from notifypy import Notify


class Notifier:
    def __init__(self):
        self.notification = Notify()
        self.notification.application_name = "LinkedIn Bot"

    def notify_new_message(self, sender: str, preview: str):
        """Notify about a new LinkedIn message"""
        try:
            self.notification.title = f"New LinkedIn Message from {sender}"
            self.notification.message = (
                preview[:100] + "..." if len(preview) > 100 else preview
            )
            self.notification.send()
        except Exception as e:
            logging.error(f"Failed to send notification: {str(e)}")

    def notify_job_opportunity(self, analysis_result: Dict[str, Any]):
        """Notify about a matching job opportunity"""
        try:
            self.notification.title = "Matching Job Opportunity"
            self.notification.message = f"New job opportunity matches your criteria!\n{analysis_result['analysis'][:100]}..."
            self.notification.send()
        except Exception as e:
            logging.error(f"Failed to send notification: {str(e)}")
