import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqProvider:

    def __init__(self):
        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

    def analyze(self, prompt):

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        response_text = response.choices[0].message.content.strip()

        if response_text.startswith("```"):
            response_text = (
                response_text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        return json.loads(response_text)