import time
import requests

from src.logger import logger
from urllib.parse import quote_plus
from src.config.config import config

USER_AGENT = {
    "User-Agent": "Mozilla/5.0"
}


def build_urls():

    urls = []

    for keyword in config.keywords:

        query = quote_plus(keyword)

        urls.append(
            f"https://remotive.com/api/remote-jobs?search={query}&limit={config.max_results}"
        )

    return urls


def scrape():

    logger.info("Searching Remotive...")

    jobs = []
    urls = build_urls()
    for url in urls:

        try:
            logger.info(f"Links: : {url}")
            response = requests.get(
                url,
                headers=USER_AGENT,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            for job in data.get("jobs", []):

                jobs.append(
                    {
                        "title": job.get("title", ""),
                        "company": job.get("company_name", ""),
                        "location": "Remote",
                        "remote": True,
                        "url": job.get("url", ""),
                        "date": (job.get("publication_date") or "")[:10],
                        "source": "Remotive",
                    }
                )

        except Exception as e:

            logger.error(f"Remotive Error: {e}")

        time.sleep(1)

    logger.info(f"Remotive -> {len(jobs)} jobs found.")

    return jobs