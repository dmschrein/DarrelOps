"""Scheduler"""
# darrelops/services/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from atexit import register as atexit_register

scheduler = BackgroundScheduler()

def start_scheduler():
    from .build_service import check_for_new_commits
    scheduler.add_job(
        func=check_for_new_commits,
        trigger=IntervalTrigger(seconds=60),
        id='check_for_new_commits',
        name='Check for new commits every 60 seconds',
        replace_existing=True
    )
    scheduler.start()
    atexit_register(lambda: scheduler.shutdown())