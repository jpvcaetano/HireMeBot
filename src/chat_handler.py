from openai import OpenAI
from config.settings import OPENAI_API_KEY
from config.prompts import PROMPT_TEMPLATES, JOB_CRITERIA
from config.prompts.conversation_prompts import ACTIVE_VERSIONS
import logging

class ChatHandler:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
    def generate_response(self, conversation_history, message, template_key="initial_response"):
        """Generate a response using OpenAI's GPT model"""
        try:
            template_group = PROMPT_TEMPLATES.get(template_key)
            if not template_group:
                raise ValueError(f"Unknown template key: {template_key}")
            
            # Get active version for this template
            version = ACTIVE_VERSIONS.get(template_key, "v1")
            template = template_group.get(version)
            
            messages = [
                {"role": "system", "content": template["system"]},
                {"role": "user", "content": template["user"].format(
                    conversation_history=conversation_history,
                    message=message,
                    criteria=JOB_CRITERIA if template_key == "job_analysis" else None
                )}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            return None