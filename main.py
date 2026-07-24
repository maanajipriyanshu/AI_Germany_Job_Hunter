from models.resume_reader import ResumeReader
from models.job_loader import JobLoader
from models.analyzer import Analyzer
from utils.report_writer import ReportWriter
from utils.csv_writer import CSVWriter

# Read Resume
resume = ResumeReader.read_pdf("data/resume.pdf")

# Load all job descriptions
jobs = JobLoader.load_jobs("data/jobs")

print(f"Loaded {len(jobs)} jobs")

for job in jobs:
    print(job["name"])

# Read prompt
with open("prompts/recruiter_prompt.txt", "r", encoding="utf-8") as f:
    recruiter_prompt = f.read()

# Analyze all jobs
results = []

for job in jobs:

    print(f"\nAnalyzing {job['name']}...")

    result = Analyzer.analyze(
        resume,
        job["description"],
        recruiter_prompt
    )

    print(result)

    result["company"] = job["name"]

    results.append(result)

    # Save individual report
    ReportWriter.save_json(
        result,
        f"data/reports/{job['name']}.json"
    )

# Sort results
results.sort(
    key=lambda x: x["match_score"],
    reverse=True
)

# Save overall ranking
ReportWriter.save_json(
    results,
    "data/reports/job_ranking.json"
)

CSVWriter.save(
    results,
    "data/reports/job_ranking.csv"
)

# Print ranking
print("\n===== JOB RANKING =====\n")

for job in results:

    print(
        f"{job['company']:15}"
        f" Match: {job['match_score']}"
        f" ATS: {job['ats_score']}"
        f" Interview: {job['interview_probability']}"
    )