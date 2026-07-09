from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
)

from prompts import SYSTEM_PROMPT


class ChatBot:

    def __init__(self):

        if not OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is missing.\n"
                "Add it to Streamlit Secrets or your .env file."
            )

        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def chat(
        self,
        prompt: str,
        system_prompt: str = SYSTEM_PROMPT,
    ) -> str:

        try:

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
                max_tokens=1024,
            )

            return response.choices[0].message.content

        except Exception as e:

            return f"❌ OpenAI Error:\n{str(e)}"


# Singleton
bot = ChatBot()