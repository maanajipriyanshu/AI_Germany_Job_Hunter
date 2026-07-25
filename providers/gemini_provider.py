import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiProvider:

    def __init__(self):

        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def rewrite_cover_letter(
        self,
        cover_letter,
        style="German Corporate"
    ):

        prompt = f"""
You are a professional career coach.

Rewrite the following cover letter.

Requirements:

- Sound completely human.
- Remove AI clichés.
- Natural English.
- Confident but not exaggerated.
- Professional.
- Suitable for German recruiters.
- Keep all facts.
- Do not invent experience.
- Maximum 350 words.

Writing Style:
{style}

Cover Letter:

{cover_letter}
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text