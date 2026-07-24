import json


class ReportWriter:

    @staticmethod
    def save_json(result, path="data/output.json"):

        with open(path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)