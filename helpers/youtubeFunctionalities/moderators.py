from appUtils import log, writeJson, configuration
from googleapiclient.discovery import Resource

def getModsList(client: Resource, liveChatId: str,  pageToken: str = "", part: str = "snippet", maxResults: int = 50):
    mods = []
    try:
        ytResponse = client.liveChatModerators().list(
            part=part, liveChatId= liveChatId, pageToken= pageToken, maxResults= maxResults
        ).execute() # quota heavy operation
        items = ytResponse.get("items", [])
        for item in items:
            user = item.get("snippet", {}).get("moderatorDetails", {}).get("channelId", None)
            if user is not None:
                mods.append(user)
            del user
        del items
        writeJson(configuration["Youtube"]["Mods"], {"mods": mods})
    except Exception as e:
        log.error("Error in getting moderators: {}".format(e))
    return mods