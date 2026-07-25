import streamlit as st


class CoverLetterGenerator:
    @staticmethod
    def show(job):
        cover_letter = job.get("cover_letter", "")
        if not cover_letter:
            st.info("No cover letter generated.")
            return

        st.divider()
        st.subheader("📄 Cover Letter")
        st.text_area(
            "Generated Cover Letter",
            cover_letter,
            height=300,
            key=f"cover_{job['company']}"
        )
        st.download_button(
            label="⬇ Download Cover Letter",
            data=cover_letter,
            file_name=f"{job['company']}_Cover_Letter.txt",
            mime="text/plain",
            key=f"download_{job['company']}"
        )