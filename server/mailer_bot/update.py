from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from mailer_bot import jobs

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(jobs.sendAlerts, 'interval', minutes=1)
    scheduler.start()