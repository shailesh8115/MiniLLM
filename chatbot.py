import ollama
from openai import OpenAI
from openai import OpenAI
from config import OPENAI_API_KEY

from config import (
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OLLAMA_MODEL,
)
from prompts import SYSTEM_PROMPT
class ChatBot:

    def __init__(self):

        self.provider = LLM_PROVIDER.lower()

        if self.provider == "openai":

            self.client = OpenAI(
                api_key=OPENAI_API_KEY
            )

    def chat(
        self,
        prompt,
        system_prompt=SYSTEM_PROMPT,
    ):

        if self.provider == "ollama":

            response = ollama.chat(

                model=OLLAMA_MODEL,

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
            )

            return response["message"]["content"]

        else:

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