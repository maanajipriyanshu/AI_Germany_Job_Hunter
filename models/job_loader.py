import os


class JobLoader:

    @staticmethod
    def load_jobs(folder):

        jobs = []

        for file in os.listdir(folder):

            if file.endswith(".txt"):

                path = os.path.join(folder, file)

                with open(path, "r", encoding="utf-8") as f:

                    jobs.append({
                        "name": file.replace(".txt", ""),
                        "description": f.read()
                    })

        return jobs