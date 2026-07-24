from models.resume_reader import ResumeReader
from models.job_reader import JobReader
from models.analyzer import Analyzer
from utils.report_writer import ReportWriter

resume = ResumeReader.read_pdf("data/resume.pdf")

job = JobReader.read("data/job.txt")

with open("prompts/recruiter_prompt.txt", "r", encoding="utf-8") as f:
    recruiter_prompt = f.read()

result = Analyzer.analyze(
    resume,
    job,
    recruiter_prompt
)

ReportWriter.save_json(result)

print("Analysis completed successfully.")