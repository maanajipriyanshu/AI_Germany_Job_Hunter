import streamlit as st
import pandas as pd

from models.resume_reader import ResumeReader
from models.job_loader import JobLoader
from models.analyzer import Analyzer
from models.skill_matcher import SkillMatcher
from features.cover_letter_generator import CoverLetterGenerator


st.set_page_config(
    page_title="AI Germany Job Hunter",
    page_icon="🇩🇪",
    layout="wide"
)

DEFAULT_STATE = {
    "resume": None,
    "jobs": [],
    "results": [],
    "recruiter_prompt": "",
    "analysis_complete": False
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

st.title("🇩🇪 AI Germany Job Hunter")
st.write("Analyze your resume against multiple German job descriptions using AI.")
st.divider()

resume_file = st.file_uploader("📄 Upload Resume", type=["pdf"])
job_files = st.file_uploader("📂 Upload Job Descriptions", type=["txt"], accept_multiple_files=True)

st.divider()

if st.button("🚀 Analyze Jobs", width="stretch"):
    if resume_file is None:
        st.error("Please upload your resume.")
        st.stop()

    if not job_files:
        st.error("Please upload at least one job description.")
        st.stop()

    with st.spinner("Reading resume..."):
        resume = ResumeReader.read_pdf(resume_file)

    with st.spinner("Loading jobs..."):
        jobs = JobLoader.load_jobs(job_files)

    with open("prompts/recruiter_prompt.txt", "r", encoding="utf-8") as f:
        recruiter_prompt = f.read()

    with st.spinner("Matching skills..."):
        for job in jobs:
            skill_result = SkillMatcher.match(resume, job["description"])
            job["skill_score"] = skill_result["score"]
            job["matched"] = skill_result["matched"]
            job["missing"] = skill_result["missing"]

    jobs.sort(key=lambda x: x["skill_score"], reverse=True)

    st.session_state.resume = resume
    st.session_state.jobs = jobs
    st.session_state.results = []
    st.session_state.recruiter_prompt = recruiter_prompt
    st.session_state.analysis_complete = True

if st.session_state.analysis_complete:
    resume = st.session_state.resume
    jobs = st.session_state.jobs
    recruiter_prompt = st.session_state.recruiter_prompt

    st.subheader("📊 Local Skill Matching")

    table = pd.DataFrame([
        {
            "Company": job["name"],
            "Skill Match": f"{job['skill_score']}%",
            "Matched": ", ".join(job["matched"]),
            "Missing": ", ".join(job["missing"])
        }
        for job in jobs
    ])

    st.dataframe(table, width="stretch")
    st.divider()

    st.subheader("✅ Select Jobs for AI Analysis")

    company_names = [job["name"] for job in jobs]
    default_selection = [job["name"] for job in jobs if job["skill_score"] >= 50]

    selected_company_names = st.multiselect(
        "Choose jobs for AI analysis",
        options=company_names,
        default=default_selection,
        key="selected_jobs"
    )

    selected_jobs = [job for job in jobs if job["name"] in selected_company_names]

    if st.button("🤖 Analyze Selected Jobs"):
        if not selected_jobs:
            st.warning("Please select at least one job.")
            st.stop()

        results = []

        with st.spinner("Analyzing selected jobs..."):
            progress = st.progress(0)
            total = len(selected_jobs)

            for index, job in enumerate(selected_jobs):
                result = Analyzer.analyze(
                    resume,
                    job["description"],
                    recruiter_prompt
                )

                # Check if analysis failed
                if result is None:
                    st.error(f"AI analysis failed for {job['name']}")
                    continue

                if isinstance(result, dict) and result.get("success") is False:
                    st.error(f"{job['name']}: {result['error']}")
                    continue
                result["company"] = job["name"]
                result["description"] = job["description"]
                result["skill_score"] = job["skill_score"]
                result["matched"] = job["matched"]
                result["missing"] = job["missing"]

                results.append(result)
                progress.progress((index + 1) / total)

        results.sort(key=lambda x: x["match_score"], reverse=True)
        st.session_state.results = results

    if st.session_state.results:
        st.success("Analysis Complete!")
        st.subheader("🏆 AI Analysis")

        results = st.session_state.results

        for job in results:
            with st.expander(
                f"{job['company']} | Skill {job['skill_score']}% | AI {job['match_score']}%",
                expanded=False
            ):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("AI Match", f"{job['match_score']}%")

                with col2:
                    st.metric("ATS Score", f"{job['ats_score']}%")

                with col3:
                    st.metric("Interview Probability", f"{job['interview_probability']}%")

                st.success("Matched Skills")
                st.write(", ".join(job["matched"]) if job["matched"] else "None")

                st.warning("Missing Skills")
                st.write(", ".join(job["missing"]) if job["missing"] else "None")

                st.subheader("💪 Strengths")
                for item in job["strengths"]:
                    st.write(f"✅ {item}")

                st.subheader("📈 Resume Improvements")
                for item in job["resume_improvements"]:
                    st.write(f"• {item}")

                st.subheader("📚 Learning Plan")
                for item in job["learning_plan"]:
                    st.write(f"• {item}")

                st.subheader("💡 ATS Tips")
                for item in job["ats_tips"]:
                    st.write(f"• {item}")

                CoverLetterGenerator.show(job)