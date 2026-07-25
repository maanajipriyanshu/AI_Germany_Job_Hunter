from models.resume_reader import ResumeReader
from models.job_loader import JobLoader
from models.analyzer import Analyzer
from utils.report_writer import ReportWriter


resume = ResumeReader.read_pdf("data/resume.pdf")

jobs = JobLoader.load_jobs("data/jobs")

with open(
    "prompts/recruiter_prompt.txt",
    "r",
    encoding="utf-8"
) as f:

    recruiter_prompt = f.read()


results = []

for job in jobs:

    result = Analyzer.analyze(

        resume,

        job["description"],

        recruiter_prompt
    )

    result["company"] = job["name"]

    results.append(result)


results.sort(

    key=lambda x: x["match_score"],

    reverse=True
)


ReportWriter.save_json(results)


print("\n========== JOB RANKING ==========\n")

for job in results:

    print(
        f"{job['company']:15}"
        f" Match: {job['match_score']}"
        f" | ATS: {job['ats_score']}"
        f" | Interview: {job['interview_probability']}"
    )