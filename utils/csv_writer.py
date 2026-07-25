import csv
import os


class CSVWriter:

    @staticmethod
    def save(results: list, path: str) -> None:
        """
        Save analysis results as a CSV file.

        Args:
            results: List of analysis result dictionaries.
            path: Output CSV file path.
        """

        directory = os.path.dirname(path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        try:

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
                        result.get("company", ""),
                        result.get("match_score", 0),
                        result.get("ats_score", 0),
                        result.get("interview_probability", 0),
                        ", ".join(result.get("missing_skills", []))
                    ])

        except Exception as e:
            raise RuntimeError(
                f"Failed to save CSV report to '{path}': {e}"
            ) from e