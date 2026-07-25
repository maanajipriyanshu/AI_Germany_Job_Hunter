class CoverLetterGenerator:

    @staticmethod
    def show(job):

        cover_letter = job.get("cover_letter", "")

        if cover_letter:

            import streamlit as st

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

        else:

            import streamlit as st

            st.info("No cover letter generated.")