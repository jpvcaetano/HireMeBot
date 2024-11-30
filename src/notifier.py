import logging
from typing import Any, Dict

from notifypy import Notify


class Notifier:
    def __init__(self):
        self.notification = Notify()
        self.notification.application_name = "LinkedIn Bot"

    def notify_job_opportunity(self, analysis_result: Dict[str, Any]):
        """Notify about a matching job opportunity"""
        try:
            self.notification.title = "Matching Job Opportunity"
            self.notification.message = f"New job opportunity matches your criteria!\n{analysis_result['analysis'][:100]}..."
            self.notification.send()
        except Exception as e:
            logging.error(f"Failed to send notification: {str(e)}")
