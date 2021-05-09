from datetime import datetime

import dateutil.parser
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, redirect, render_template, request

from api import Api
from config import Config

app = Flask(__name__)
notifications = []

def schedule_add_activity(executionDate: str, username: str, password: str, userId: str, courtId: str, fromDate: str, toDate: str):
    scheduler = BackgroundScheduler()
    scheduler.add_executor('processpool')

    date = dateutil.parser.isoparse(executionDate)
    job = scheduler.add_job(api.get_token_and_create_activity, 'date', run_date=date, args=[username, password, userId, courtId, fromDate, toDate])
    scheduler.start()
    notifications.append(f'Event: <a href="https://app.courtculture.cc/radar(place:courts/{courtId})" target="_blank">Court {courtId}</a> from {fromDate} to {toDate}')

    return redirect("/")

@app.route('/', methods=['GET', 'POST'])
def index():
        
    if config.username is None:
        return redirect('/user-data')

    if request.method == 'POST':
        schedule_add_activity(request.form['executionDate'], config.username, config.password, config.userId, request.form['courtId'], request.form['fromDate'], request.form['toDate'])
        return redirect("/")

    return render_template('index.html', notifications=notifications);

@app.route('/user-data', methods=["GET", "POST"])
def user_data(): 
    if request.method == "POST":
        if (config.username == None) or (config.password == None) or (config.userId == None):
            config.set_username(request.form["username"])
            config.set_password(request.form["password"])
            config.set_userId(request.form["userId"])
            return redirect("/")

    return render_template('user-data.html'); 
    

if __name__ == '__main__':
    global config
    config = Config()
    global api
    api = Api(config)

    username = 'bla@blub.at'
    password = 'a12345'
    userId = "8186"
    courtId = "213"
    fromDate = "2021-05-10T16:00"
    toDate = "2021-05-10T18:00"

    app.run(debug=True)
