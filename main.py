from datetime import datetime

from flask import Flask, redirect, render_template, request

from api import Api
from config import Config

app = Flask(__name__)
notifications = []
loginError = None

@app.route('/', methods=['GET', 'POST'])
def index():
    if (config.username is None) or (config.password is None) or (config.userId is None):
        return redirect('/user-data')

    if request.method == 'POST':
        executionDate = request.form['executionDate']
        courtId = request.form['courtId']
        fromDate = request.form['fromDate']
        toDate = request.form['toDate']

        api.schedule_add_activity(executionDate, config.username, config.password, config.userId, courtId, fromDate, toDate)
        notifications.append(f'Activity: <a href="https://app.courtculture.cc/radar(place:courts/{courtId})" target="_blank">Court {courtId}</a> from {fromDate} to {toDate}')
        return redirect("/")

    return render_template('index.html', notifications=notifications);

@app.route('/user-data', methods=["GET", "POST"])
def user_data():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        userId = None
        try:
            userId = str(api.get_user_id(username, password))
        except Exception:
            global loginError
            loginError = "Username or password incorrect"
            return redirect("/user-data")

        config.set_userId(userId)
        config.set_username(username)
        config.set_password(password)
        return redirect("/")

    return render_template('user-data.html', loginError=loginError, username=config.username); 
    

if __name__ == '__main__':
    global config
    config = Config()
    global api
    api = Api(config)

    app.run(debug=True)
