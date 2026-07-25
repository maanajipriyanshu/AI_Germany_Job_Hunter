import pdfplumber


class ResumeReader:

    @staticmethod
    def read_pdf(pdf_file):

        text = ""

        with pdfplumber.open(pdf_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text