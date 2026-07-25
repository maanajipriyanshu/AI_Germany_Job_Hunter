from providers.groq_provider import GroqProvider


class ResumeOptimizer:
    provider = GroqProvider()

    @staticmethod
    def optimize(resume, job_description):
        prompt = f"""You are an ATS Resume Expert.

Resume:
{resume}

Job Description:
{job_description}

Return ONLY valid JSON.

{{
    "summary":"Improved professional summary",

    "experience":[
        "...",
        "...",
        "..."
    ],

    "skills":[
        "...",
        "...",
        "..."
    ],

    "keywords":[
        "...",
        "...",
        "..."
    ]
}}
"""

        return ResumeOptimizer.provider.analyze(prompt)