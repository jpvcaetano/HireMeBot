JOB_ANALYSIS_TEMPLATES = {
    "job_analysis": {
        "v1": {
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
}

# Track which version to use for each template
ACTIVE_VERSIONS = {
    "job_analysis": "v1"
} 