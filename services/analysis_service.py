import os

from models.resume_reader import ResumeReader
from models.job_loader import JobLoader
from models.analyzer import Analyzer
from utils.report_writer import ReportWriter
from utils.csv_writer import CSVWriter


class AnalysisService:
    @staticmethod
    def run(resume_path: str, jobs_folder: str, prompt_path: str = "prompts/recruiter_prompt.txt") -> list:
        """Analyze a resume against all uploaded job descriptions.

        Args:
            resume_path: Path to resume PDF.
            jobs_folder: Folder containing job description text files.
            prompt_path: Recruiter prompt file.

        Returns:
            List of analysis results sorted by match score.
        """
        if not os.path.exists(resume_path):
            raise FileNotFoundError(f"Resume not found: {resume_path}")
        if not os.path.exists(jobs_folder):
            raise FileNotFoundError(f"Jobs folder not found: {jobs_folder}")
        if not os.path.exists(prompt_path):
            raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

        resume = ResumeReader.read_pdf(resume_path)
        if not resume.strip():
            raise ValueError("Resume contains no readable text.")

        jobs = JobLoader.load_jobs(jobs_folder)
        if not jobs:
            raise ValueError("No job descriptions were found.")

        with open(prompt_path, "r", encoding="utf-8") as f:
            recruiter_prompt = f.read().strip()

        os.makedirs("data/reports", exist_ok=True)

        results = []
        for index, job in enumerate(jobs, start=1):
            print(f"[{index}/{len(jobs)}] Analyzing {job['name']}...")

            result = Analyzer.analyze(
                resume=resume,
                job=job["description"],
                recruiter_prompt=recruiter_prompt
            )
            result["company"] = job["name"]
            results.append(result)

            ReportWriter.save_json(result, f"data/reports/{job['name']}.json")

        results.sort(key=lambda x: x.get("match_score", 0), reverse=True)

        ReportWriter.save_json(results, "data/reports/job_ranking.json")
        CSVWriter.save(results, "data/reports/job_ranking.csv")

        return results