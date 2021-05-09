import requests


class Api:
    tokenEndpoint = None
    courtsUrl = None
    clientId= None
    sessionUrl=None

    def __init__(self, config):
        self.tokenEndpoint = config.tokenEndpoint
        self.courtsUrl = config.courtsUrl
        self.clientId = config.clientId
        self.sessionUrl = config.sessionUrl

    def get_token(self, username, password):
        params = {
            "grant_type": 'password',
            "client_id": self.clientId,
            "username": username,
            "password": password
        }

        response = requests.post(url = self.tokenEndpoint, data = params)
        data = response.json()
        accessToken: str = data.get("access_token")

        return accessToken + "___" + accessToken + "___" + accessToken;

    def get_user_id(self, username, password): 
        token = self.get_token(username, password)
        headers = { "Cookie": "q_session=" + token }
        response = requests.get(url=self.sessionUrl, headers=headers)

        if response.status_code == 200:
            data = response.json();
            return data.get("identityId")

        raise Exception("Username or password incorrect")


    def get_token_and_create_activity(self, username, password, userId, courtId, fromDate, toDate):
        token = self.get_token(username, password)
        self.create_activity(token, userId, courtId, fromDate, toDate)


    def create_activity(self, token, userId, courtId, fromDate, toDate):
        headers = { "Cookie": "q_session=" + token }
        url = f'{self.courtsUrl}/{courtId}/activities'

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
        fromDate = "2021-05-10T16:00"
        toDate = "2021-05-10T18:00"

        parseConfig()
        scheduler = BlockingScheduler()
        scheduler.add_executor('processpool')
        job = scheduler.add_job(get_token_and_create_activity, 'date', run_date=datetime.now(), args=[username, password, userId, courtId, fromDate, toDate])

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
