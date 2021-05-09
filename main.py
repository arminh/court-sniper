from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from flask import Flask

import api
import config

app = Flask(__name__)

def scheduleAddActivity(username: str, password: str, userId: str, courtId: str, fromDate: str, toDate: str):
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    job = scheduler.add_job(api.getTokenAndCreateActivity, 'date', run_date=datetime.now(), args=[username, password, userId, courtId, fromDate, toDate])

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == '__main__':
    config.parseConfig()

    username = 'bla@blub.at'
    password = 'a12345'
    userId = "8186"
    courtId = "213"
    fromDate = "2021-05-10T16:00"
    toDate = "2021-05-10T18:00"

    scheduleAddActivity(username, password, userId, courtId, fromDate, toDate)
