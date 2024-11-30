from datetime import datetime
from typing import Dict, Any
from config.prompts import JOB_CRITERIA
from src.chat_handler import ChatHandler

class JobAnalyzer:
    def __init__(self, chat_handler: ChatHandler):
        self.chat_handler = chat_handler
        self.criteria = JOB_CRITERIA
        
    def extract_job_details(self, message: str) -> Dict[str, Any]:
        """Extract structured job details from a message"""
        # This could be enhanced with more sophisticated parsing
        return {
            "raw_description": message,
            "extracted_at": datetime.now().isoformat()
        }
        
    def analyze_opportunity(self, job_details: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a job opportunity against criteria"""
        analysis = self.chat_handler.generate_response(
            conversation_history="",
            # TODO: Add criteria to the prompt
            message=str(job_details),
            template_key="job_analysis"
        )
        
        return {
            "job_details": job_details,
            "analysis": analysis,
            "criteria_used": self.criteria,
            "analyzed_at": datetime.now().isoformat()
        }
        
    def should_notify(self, analysis_result: Dict[str, Any]) -> bool:
        """Determine if an opportunity warrants notification"""
        # This could be enhanced with more sophisticated matching
        try:
            # Extract score from analysis text
            analysis_text = analysis_result["analysis"]
            if "Match Score" in analysis_text:
                score_line = [line for line in analysis_text.split('\n') 
                            if "Match Score" in line][0]
                score = int(score_line.split(':')[1].strip().split('/')[0])
                return score >= 70  # Notify for high-matching opportunities
            return False
        except Exception:
            return False 