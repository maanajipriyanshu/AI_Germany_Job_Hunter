import pdfplumber


class ResumeReader:
    @staticmethod
    def read_pdf(file_path: str) -> str:
        """
        Pulls the text out of a PDF resume, page by page.
        """
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text