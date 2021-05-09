from datetime import datetime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler

tokenEndpoint = "https://auth.courtculture.cc/auth/realms/courtculture/protocol/openid-connect/token";
courtsUrl = "https://app.courtculture.cc/api/courts"
clientId = "cc-app-client"


def getToken(username, password):
    params = {
        "grant_type": 'password',
        "client_id": clientId,
        "username": username,
        "password": password
    }

    response = requests.post(url = tokenEndpoint, data = params)
    data = response.json()
    accessToken = data.get("access_token")
    return accessToken + "___" + accessToken + "___" + accessToken;


def getTokenAndCreateActivity(username, password, userId, courtId, fromDate, toDate):
    token = getToken(username, password)
    createActivity(token, userId, courtId, fromDate, toDate)


def createActivity(token, userId, courtId, fromDate, toDate):
    headers = { "Cookie": "q_session=" + token }
    url = f'{courtsUrl}/{courtId}/activities'

    payload = {
        "begin": fromDate,
        "end": toDate,
        "id": userId,
        "identity": {"id": userId, "anonymous": "false"},
        "courtId": courtId,
        "description": "I'm on the court.",
        "gadgetAvailable": "true",
        "anonymous": "false",
        "requiredParticipants": "0"
    }

    response = requests.post(url=url, json=payload, headers=headers)
    data = response.json()
    print(data)

if __name__ == '__main__':

    username = 'bla@blub.at'
    password = 'a12345'
    userId = "8186"
    courtId = "213"
    fromDate = "2021-05-06T16:00"
    toDate = "2021-05-06T18:00"

    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    job = scheduler.add_job(getTokenAndCreateActivity, 'date', run_date=datetime(2021, 5, 5, 23, 27), args=[username, password, userId, courtId, fromDate, toDate])

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
