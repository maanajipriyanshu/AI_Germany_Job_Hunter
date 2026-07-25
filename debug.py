from services.analysis_service import AnalysisService
import traceback

try:

    results = AnalysisService.run(
        resume_path="temp/resume.pdf",      # Change if needed
        jobs_folder="temp/jobs"
    )

    print("\n========== RESULTS ==========\n")

    for job in results:
        print(f"Company: {job['company']}")
        print(f"Match: {job['match_score']}")
        print(f"ATS: {job['ats_score']}")
        print(f"Interview: {job['interview_probability']}")
        print("-" * 50)

except Exception:
    print("\n========== FULL TRACEBACK ==========\n")
    traceback.print_exc()