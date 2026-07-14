import csv
from pathlib import Path

OUTPUT_DIR = Path("output/reports")
OUTPUT_DIR.mkdir(exist_ok=True)

CSV_FILE = OUTPUT_DIR / "jobs.csv"


def export_csv(jobs: list):
    file_exists = CSV_FILE.exists() and CSV_FILE.stat().st_size > 0
    with open(
        CSV_FILE,
        mode="a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Score",
            "Title",
            "Company",
            "Location",
            "Remote",
            "Date",
            "Source",
            "URL"
        ])

        for job in jobs:

            writer.writerow([

                job.get("score", 0),

                job.get("title", ""),

                job.get("company", ""),

                job.get("location", ""),

                job.get("remote", ""),

                job.get("date", ""),

                job.get("source", ""),

                job.get("url", "")
            ])