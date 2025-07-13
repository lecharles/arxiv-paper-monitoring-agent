"""
Scheduler: schedule periodic execution of the agent pipeline.
"""

import time
import logging
import schedule

from main import run_pipeline

def run_scheduler(interval_hours: int, config: dict):
    """Schedule the agent pipeline to run every interval_hours."""
    def job():
        logging.info('Scheduled job: running pipeline')
        try:
            run_pipeline(config)
        except Exception as e:
            logging.error('Pipeline error: %s', e)

    schedule.every(interval_hours).hours.do(job)
    logging.info('Scheduler started: interval %d hours', interval_hours)
    while True:
        schedule.run_pending()
        time.sleep(60)