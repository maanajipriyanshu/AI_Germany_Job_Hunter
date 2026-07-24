import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

from models.resume_reader import ResumeReader

resume = ResumeReader.read_pdf("data/resume.pdf")

with open("data/job.txt", "r", encoding="utf-8") as f:
    job = f.read()

with open("prompts/recruiter_prompt.txt", "r", encoding="utf-8") as f:
    recruiter_prompt = f.read()

# stitch everything into one prompt
prompt = f"""
{recruiter_prompt}

==========================
RESUME
==========================

{resume}

==========================
JOB DESCRIPTION
==========================

{job}
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.3
)

try:
    response_text = response.choices[0].message.content.strip()

    # Remove Markdown if the AI wraps the JSON
    if response_text.startswith("```"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()

    result = json.loads(response_text)

    with open("data/output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    with open("data/output.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(result, indent=4))

    print(json.dumps(result, indent=4))
    print("\nAnalysis saved to data/output.json")

except json.JSONDecodeError:
    print("AI did not return valid JSON.")
    print(response.choices[0].message.content)

with open("data/output.txt", "w", encoding="utf-8") as f:
    f.write(json.dumps(result, indent=4))

print("\nAnalysis saved to data/output.txt")