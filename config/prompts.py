PROMPT_TEMPLATES = {
    "initial_response": {
        "system": """You are an AI assistant managing professional LinkedIn conversations. 
                    Your responses should be:
                    1. Professional and courteous
                    2. Focused on relevant job details
                    3. Concise but informative
                    4. Proactive in gathering important information""",
        "user": """Context: {context}
                Previous messages: {conversation_history}
                Recruiter's message: {message}
                
                Generate a professional response that:
                1. Maintains a friendly tone
                2. Asks relevant questions about the position
                3. Highlights relevant skills and experience
                4. Moves the conversation forward constructively"""
    },
    
    "job_analysis": {
        "system": """You are a job opportunity analyzer. Evaluate job details against 
                    specified criteria and provide structured analysis.""",
        "user": """Analyze this job opportunity against these criteria:
                {criteria}
                
                Job details:
                {job_details}
                
                Provide analysis in the following format:
                - Match Score (0-100)
                - Key Matches
                - Potential Concerns
                - Recommendation"""
    }
} 