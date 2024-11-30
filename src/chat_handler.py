import logging
import ssl

import certifi
from openai import OpenAI

from config.prompts import CONVERSATION_CRITERIA, JOB_CRITERIA, PROMPT_TEMPLATES
from config.prompts.conversation_prompts import ACTIVE_VERSIONS
from config.settings import OPENAI_API_KEY


class ChatHandler:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        # Disable SSL verification (not recommended for production)
        ssl_context = self.client._client._transport._pool._ssl_context
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

    def generate_response(
        self, conversation_history, message, template_key="initial_response"
    ):
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
                {
                    "role": "user",
                    "content": template["user"].format(
                        conversation_history=conversation_history,
                        message=message,
                        criteria=(
                            CONVERSATION_CRITERIA
                            if template_key == "conversation_response"
                            else (
                                JOB_CRITERIA if template_key == "job_analysis" else None
                            )
                        ),
                    ),
                },
            ]

            response = self.client.chat.completions.create(
                model="gpt-4o", messages=messages, temperature=0.7, max_tokens=500
            )

            return response.choices[0].message.content

        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            return None
