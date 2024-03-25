from appUtils import log

def getLiveChats(client, liveChatId: str,  pageToken: str = "", part: str = "snippet"):
    # client.liveBroadcasts().list(part=part, ).execute()
    return