from providers.groq_provider import GroqProvider


class Analyzer:

    @staticmethod
    def analyze(
        resume,
        job_description,
        recruiter_prompt
    ):

        prompt = f"""
{recruiter_prompt}

===========================
RESUME
===========================

{resume}

===========================
JOB DESCRIPTION
===========================

{job_description}
"""

        provider = GroqProvider()

        return provider.analyze(prompt)