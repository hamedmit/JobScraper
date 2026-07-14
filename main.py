import time

from src.logger import logger
from src.history import save_run
from src.notifications.telegram import TelegramNotification
from src.config.config import config
from src.scrapers.remotive import scrape
from src.ranker import rank_jobs
from src.exporter import export_csv

def main():

    # -----------------------------
    # Initialize run information
    # -----------------------------
    start_time = time.time()

    run_status = "SUCCESS"
    jobs_found = 0
    telegram_sent = False

    telegram = TelegramNotification()

    try:

        logger.info("=" * 60)
        logger.info("JobScraper started.")
        logger.info(f"Keywords    : {config.keywords}")
        logger.info(f"Locations   : {config.locations}")
        logger.info(f"Remote      : {config.remote}")
        logger.info(f"Sources     : {config.sources}")
        logger.info(f"Max Results : {config.max_results}")
        logger.info(f"Output      : {config.output}")
        # -----------------------------
        # Send startup notification
        # -----------------------------
        try:
            telegram.send("🚀 JobScraper started successfully.")
            telegram_sent = True
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")

        logger.info("Logger initialized successfully.")

        # =====================================================
        # Main application logic
        # =====================================================

        # TODO:
        # jobs_found = scraper.run()
        jobs = scrape()
        jobs_found = rank_jobs(jobs)
        try:
            export_csv(jobs_found)
            logger.info("CSV exported successfully.")
        except Exception as csv_error:
            logger.error(
                f"Failed to write in csv file: {csv_error}"
            )
        
        

        duplicates_removed = len(jobs) - len(jobs_found)

        logger.info(f"Duplicate Removed : {duplicates_removed}")
        logger.info("Top Jobs:")

        for job in jobs_found[:5]:

            logger.info(
                f"[{job['score']:3}] "
                f"{job['title']} | "
                f"{job['url']} | "
                f"{job['company']}"
            )

        jobs_count = len(jobs_found)

        logger.info(f"Unique Jobs : {jobs_count}")

        logger.info("JobScraper completed successfully.")

    except Exception as e:

        run_status = "FAILED"

        error_message = f"JobScraper failed.\n\nError:\n{e}"

        logger.exception(error_message)

        try:
            telegram.send(f"❌ {error_message}")
            telegram_sent = True
        except Exception as telegram_error:
            logger.error(
                f"Failed to send Telegram error message: {telegram_error}"
            )

    finally:

        run_duration = time.time() - start_time

        logger.info(f"Run Status : {run_status}")
        logger.info(f"Duration   : {run_duration:.2f} sec")
        logger.info("=" * 60)

        try:

            telegram.send(
                    f"""
                ✅ JobScraper Finished

                Jobs Found : {len(jobs_found)}

                Top Score  : {jobs_found[0]['score'] if jobs_found else 0}

                Duration   : {run_duration:.2f} sec

                Status     : {run_status}
                """
                    )

        except Exception as e:

            logger.error(e)
        try:
            save_run(
                status=run_status,
                duration=run_duration,
                telegram=telegram_sent,
                jobs=jobs_count,
                sources="Remotive"
            )

        except Exception as history_error:
            logger.error(
                f"Failed to save run history: {history_error}"
            )


if __name__ == "__main__":
    main()