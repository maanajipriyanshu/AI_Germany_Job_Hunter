import os
import json

import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def get_api_key():
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return None


class GroqProvider:
    def __init__(self):
        api_key = get_api_key()
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Add it to a local .env file, "
                "or to your Streamlit Cloud app's Secrets."
            )
        self.client = Groq(api_key=api_key)

    def analyze(self, prompt):
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        response_text = response.choices[0].message.content
        response_text = response_text.replace("```json", "").replace("```", "").strip()

        return json.loads(response_text)