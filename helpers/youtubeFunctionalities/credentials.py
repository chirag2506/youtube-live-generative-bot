from appUtils import log, writeJson, readJson, configuration, json
from google.oauth2.credentials import Credentials

def write(creds: Credentials):
    try:
        writeJson(configuration["GCP"]["OAuthToken"], json.loads(creds.to_json()))
    except Exception as e:
        log.error("Error in writing credentials: {}".format(e))

def read() -> Credentials:
    try:
        tokenJson = readJson(configuration["GCP"]["OAuthToken"])
        credentials = Credentials.from_authorized_user_info(tokenJson)
        return credentials
    except Exception as e:
        log.error("Error in reading credentials: {}".format(e))