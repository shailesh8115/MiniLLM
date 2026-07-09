from openai import OpenAI

from config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
)

from prompts import SYSTEM_PROMPT


class ChatBot:

    def __init__(self):

        if LLM_PROVIDER.lower() != "openai":
            raise ValueError(
                "Only OpenAI is supported for Streamlit Cloud."
            )

        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is missing. Add it to Streamlit Secrets."
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def chat(
        self,
        prompt,
        system_prompt=SYSTEM_PROMPT,
    ):

        response = self.client.chat.completions.create(

            model=OPENAI_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=0.2,
        )

        return response.choices[0].message.content


bot = ChatBot()