from appUtils import log
from googleapiclient.discovery import Resource

def getUserFromId(client: Resource, channelId: str, part: str = "snippet"):
    userName = ""
    try:
        ytResponse = client.channels().list(
            part=part, id= channelId
        ).execute()
        items = ytResponse.get("items", [])
        if len(items) > 0:
            userName= items[0].get("snippet", {}).get("title", "")
        del items
        del ytResponse
    except Exception as e:
        log.error("Error in getting user from channel ID: {}".format(e))
    return userName
