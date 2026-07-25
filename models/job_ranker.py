from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class JobRanker:
    @staticmethod
    def rank(resume, jobs):
        documents = [resume]
        for job in jobs:
            documents.append(job["description"])

        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform(documents)
        resume_vector = vectors[0]
        job_vectors = vectors[1:]

        scores = cosine_similarity(resume_vector, job_vectors)[0]

        ranked_jobs = []
        for score, job in zip(scores, jobs):
            ranked_jobs.append({
                "name": job["name"],
                "description": job["description"],
                "score": score
            })

        ranked_jobs.sort(key=lambda x: x["score"], reverse=True)
        return ranked_jobs