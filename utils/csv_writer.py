import csv
import os


class CSVWriter:

    @staticmethod
    def save(results, path):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Company",
                "Match Score",
                "ATS Score",
                "Interview Probability",
                "Missing Skills"
            ])

            for result in results:

                writer.writerow([
                    result["company"],
                    result["match_score"],
                    result["ats_score"],
                    result["interview_probability"],
                    ", ".join(result["missing_skills"])
                ])