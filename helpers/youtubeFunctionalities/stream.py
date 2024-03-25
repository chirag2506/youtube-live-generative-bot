from appUtils import log
from googleapiclient.discovery import Resource

def getStreamChatId(client: Resource, streamId: str, part: str = "liveStreamingDetails"):
    response = ""
    try:
        ytResponse = client.videos().list(
            part=part,
            id= streamId
        ).execute()
        items = ytResponse.get("items", [])
        if len(items) > 0:
            response = items[0].get("liveStreamingDetails", {}).get("activeLiveChatId", "")
    except Exception as e:
        log.error("Error in getting stream ID: {}".format(e))
    return response