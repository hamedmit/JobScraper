from src.config.config import config


def calculate_score(job: dict) -> int:
    """
    Calculate a simple relevance score for a job.
    """

    score = 0

    text = (
        f"{job.get('title', '')} "
        f"{job.get('company', '')} "
        f"{job.get('location', '')} "
        f"{job.get('description', '')}"
    ).lower()

    # -------------------------
    # Positive keywords
    # -------------------------

    for keyword in config.keywords:

        if keyword.lower() in text:
            score += 20

    # -------------------------
    # Remote jobs
    # -------------------------

    if job.get("remote"):
        score += 10

    return min(score, 100)

def remove_duplicates(jobs: list) -> list:
    """
    Remove duplicate jobs based on URL.
    """

    unique_jobs = []
    seen_urls = set()

    for job in jobs:

        url = job.get("url", "").strip()

        if not url:
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)
        unique_jobs.append(job)

    return unique_jobs

def rank_jobs(jobs: list) -> list:
    jobs = remove_duplicates(jobs)
    for job in jobs:
        job["score"] = calculate_score(job)

    jobs.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return jobs