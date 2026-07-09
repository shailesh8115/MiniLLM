import os
from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL
from prompts import SYSTEM_PROMPT


class ChatBot:

    def __init__(self):
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def chat(self, prompt, system_prompt=SYSTEM_PROMPT):

        full_prompt = f"""
{system_prompt}

{prompt}
"""

        response = self.client.models.generate_content(
            model=GEMINI_MODEL,
            contents=full_prompt,
        )

        return response.text


bot = ChatBot()