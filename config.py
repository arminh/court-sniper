from configparser import ConfigParser

tokenEndpoint = ""
courtsUrl = ""
clientId = ""

def parseConfig():
    config = ConfigParser()

    config.read('config.ini')
    global tokenEndpoint 
    tokenEndpoint = config.get('main', 'tokenEndpoint')
    global courtsUrl
    courtsUrl = config.get('main', 'courtsUrl')
    global clientId
    clientId = config.get('main', 'clientId')
