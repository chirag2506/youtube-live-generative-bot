from helpers.youtubeFunctionalities.credentials import write as writeCred, read as readCred
from appUtils import log
import googleapiclient.discovery as discovery
from googleapiclient.discovery import Resource

API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def getClient() -> Resource:
    try:
        credentials = readCred()
        youtube = discovery.build(API_SERVICE_NAME, API_VERSION, credentials= credentials)
        writeCred(creds= credentials) # in case credentials were refreshed
        return youtube
    except Exception as e:
        log.error("Error in building client: {}".format(e))