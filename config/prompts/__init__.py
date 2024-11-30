from .conversation_prompts import CONVERSATION_TEMPLATES
from .custom_criteria import JOB_CRITERIA
from .job_analysis_prompts import JOB_ANALYSIS_TEMPLATES
from .required_job_details import CONVERSATION_CRITERIA

PROMPT_TEMPLATES = {**CONVERSATION_TEMPLATES, **JOB_ANALYSIS_TEMPLATES}
