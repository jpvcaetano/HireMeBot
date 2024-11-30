from datetime import datetime
from typing import Any, Dict

from config.prompts import JOB_CRITERIA
from src.chat_handler import ChatHandler


class JobAnalyzer:
    def __init__(self, chat_handler: ChatHandler):
        self.chat_handler = chat_handler
        self.criteria = JOB_CRITERIA

    def analyze_opportunity(self, conversation_history: str) -> Dict[str, Any]:
        """Analyze a job opportunity against criteria"""
        analysis = self.chat_handler.generate_response(
            conversation_history=conversation_history,
            message=self.criteria,
            template_key="job_analysis",
        )

        return {
            "conversation_history": conversation_history,
            "analysis": analysis,
            "criteria_used": self.criteria,
            "analyzed_at": datetime.now().isoformat(),
        }

    def should_notify(self, analysis_result: Dict[str, Any]) -> bool:
        """Determine if an opportunity warrants notification"""
        # This could be enhanced with more sophisticated matching
        try:
            # Extract score from analysis text
            analysis_json = analysis_result["analysis"].to_json()
            if "Match Score" in analysis_text:
                score_line = [
                    line for line in analysis_text.split("\n") if "Match Score" in line
                ][0]
                score = int(score_line.split(":")[1].strip().split("/")[0])
                return score >= 70  # Notify for high-matching opportunities
            return False
        except Exception:
            return False
