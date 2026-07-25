class JobLoader:

    @staticmethod
    def load_jobs(uploaded_files):

        jobs = []

        for file in uploaded_files:

            jobs.append({
                "name": file.name.replace(".txt", ""),
                "description": file.read().decode("utf-8")
            })

        return jobs