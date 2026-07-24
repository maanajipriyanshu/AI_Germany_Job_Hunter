import json
import os


class ReportWriter:

    @staticmethod
    def save_json(result, path):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)