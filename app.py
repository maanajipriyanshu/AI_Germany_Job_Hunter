import streamlit as st
from models.resume_reader import ResumeReader
from models.job_loader import JobLoader
from models.analyzer import Analyzer

st.set_page_config(
    page_title="AI Germany Job Hunter",
    page_icon="🇩🇪",
    layout="wide"
)

st.title("🇩🇪 AI Germany Job Hunter")
st.write("Analyze your resume against multiple job descriptions using AI.")

st.divider()

resume_file = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf"]
)

job_files = st.file_uploader(
    "📂 Upload Job Descriptions",
    type=["txt"],
    accept_multiple_files=True
)

st.divider()

if st.button("🚀 Analyze Jobs", use_container_width=True):

    if resume_file is None:
        st.error("Please upload your resume.")
        st.stop()

    if len(job_files) == 0:
        st.error("Please upload at least one job description.")
        st.stop()

    
    resume = ResumeReader.read_pdf(resume_file)

    jobs = JobLoader.load_jobs(job_files)

    with open(
        "prompts/recruiter_prompt.txt",
        "r",
        encoding="utf-8"
    ) as f:
        recruiter_prompt = f.read()

    results = []

    with st.spinner("Analyzing jobs..."):

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

    st.success("Analysis Complete!")


    st.subheader("🏆 Job Ranking")

    for job in results:

        st.write(
            f"**{job['company']}** "
            f"— Match: {job['match_score']}% | "
            f"ATS: {job['ats_score']}% | "
            f"Interview: {job['interview_probability']}%"
        )