import csv
from pathlib import Path
from datetime import datetime

REPORT_DIR = Path("output/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "run_history.csv"


def save_run(status: str,
             duration: float,
             telegram: bool,
             jobs: int,
             sources: str):

    file_exists = REPORT_FILE.exists() and REPORT_FILE.stat().st_size > 0

    with open(REPORT_FILE,
              mode="a",
              newline="",
              encoding="utf-8") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Time",
                "Status",
                "Duration(sec)",
                "Jobs",
                "Telegram",
                "sources"
            ])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            status,
            round(duration, 2),
            jobs,
            "Yes" if telegram else "No",
            sources
        ])