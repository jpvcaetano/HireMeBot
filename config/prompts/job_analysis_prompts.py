JOB_ANALYSIS_TEMPLATES = {
    "job_analysis": {
        "v1": {
            "system": """You are a job opportunity analyzer. Evaluate job details present in LinkedIn conversations between recruiter and candidate against criteria and provide structured analysis.""",
            "user": """Analyze this job opportunity against these criteria:
                    {criteria}
                    
                    Job details:
                    {job_details}
                    
                    Provide analysis in the following format:
                    - Match Score (0-100)
                    - Key Matches
                    - Potential Concerns
                    - Recommendation
                    Start by analyzing the conversation history and create a summary of the job details.
                    Conversation history:
                    {conversation_history}
                    
                    Now analyze the job details against the criteria and provide a matching score between 0 and 100.
                    Criteria:
                    {criteria}

                    Provide your analysis as a JSON object with the following fields:
                    - match_score (0-100)
                    - summary of the job details
                    """,
        }
    }
}

# Track which version to use for each template
ACTIVE_VERSIONS = {"job_analysis": "v1"}
