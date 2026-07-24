import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Create Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Read files
with open("data/resume.txt", "r", encoding="utf-8") as f:
    resume = f.read()

with open("data/job.txt", "r", encoding="utf-8") as f:
    job = f.read()

with open("prompts/recruiter_prompt.txt", "r", encoding="utf-8") as f:
    recruiter_prompt = f.read()

# Final prompt
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

# Ask AI
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

result = response.choices[0].message.content

print(result)

# Save output
with open("data/output.txt", "w", encoding="utf-8") as f:
    f.write(result)

print("\nAnalysis saved to data/output.txt")