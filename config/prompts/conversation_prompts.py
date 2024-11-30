CONVERSATION_TEMPLATES = {
    "initial_response": {
        "v1": {
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
        "v2": {
            "system": """You are a professional networking assistant specialized in LinkedIn...""",
            "user": """Background: {context}..."""
        }
    },
    "follow_up": {
        "v1": {
            "system": """...""",
            "user": """..."""
        }
    }
}

# Track which version to use for each template
ACTIVE_VERSIONS = {
    "initial_response": "v1",
    "follow_up": "v1"
} 