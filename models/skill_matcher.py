import re

class SkillMatcher:
    SKILLS = [
        "python",
        "sql",
        "mysql",
        "postgresql",
        "power bi",
        "excel",
        "tableau",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "machine learning",
        "statistics",
        "etl",
        "data warehouse",
        "data visualization",
        "bigquery",
        "google cloud",
        "gcp",
        "azure",
        "aws",
        "spark",
        "hadoop",
        "git",
        "github",
        "streamlit",
        "docker",
        "linux"
    ]

    @staticmethod
    def extract_skills(text):

        text = text.lower()

        found = set()

        for skill in SkillMatcher.SKILLS:
            if re.search(r"\b" + re.escape(skill) + r"\b", text):
                found.add(skill)

        return found

    @staticmethod
    def match(resume, job):

        resume_skills = SkillMatcher.extract_skills(resume)
        job_skills = SkillMatcher.extract_skills(job)

        matched = resume_skills & job_skills
        missing = job_skills - resume_skills

        if len(job_skills) == 0:
            score = 0
        else:
            score = round(len(matched) / len(job_skills) * 100)

        return {
            "score": score,
            "matched": sorted(list(matched)),
            "missing": sorted(list(missing))
        }