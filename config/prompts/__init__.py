from .conversation_prompts import CONVERSATION_TEMPLATES
from .job_analysis_prompts import JOB_ANALYSIS_TEMPLATES
from .custom_criteria import JOB_CRITERIA

PROMPT_TEMPLATES = {
    **CONVERSATION_TEMPLATES,
    **JOB_ANALYSIS_TEMPLATES
} 