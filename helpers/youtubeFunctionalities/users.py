from appUtils import log
from googleapiclient.discovery import Resource

def getUserFromId(client: Resource, channelId: str, part: str = "snippet"):
    try:
        True
    except Exception as e:
        log.error("Error in getting user from channel ID: {}".format(e))
