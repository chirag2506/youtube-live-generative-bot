from appUtils import log
from googleapiclient.discovery import Resource
from helpers.youtubeFunctionalities.schemas import Message, Chat

def getLiveChats(client: Resource, liveChatId: str,  pageToken: str = "", part: str = "snippet") -> Chat:
    chat = Chat(messages= [], nextPage= "")
    try:
        ytResponse = client.liveChatMessages().list(
            part=part, liveChatId= liveChatId, pageToken= pageToken
        ).execute()
        items = ytResponse.get("items", [])
        for item in items:
            message = Message(
                id= item.get("id", ""),
                userId= item.get("snippet", {}).get("authorChannelId", ""),
                text= item.get("snippet", {}).get("displayMessage", ""),
                pubTime= item.get("snippet", {}).get("publishedAt", "")
            )
            chat.messages.append(message)
            del message
        chat.nextPage = ytResponse.get("nextPageToken", "")
        del items
        del ytResponse
    except Exception as e:
        log.error("Error in getting live chats: {}".format(e))
    return chat
    
def insertLiveChat(client: Resource, liveChatId: str, message: str, part: str = "snippet"):
    try:
        resource = {
            "snippet": {
                "liveChatId": liveChatId,
                "textMessageDetails": {
                "messageText": message
                },
                "type": "textMessageEvent"
            }
        }
        ytResponse = client.liveChatMessages().insert(part=part, body= resource).execute()
        # writeJson("./chats.json", ytResponse)
    except Exception as e:
        log.error("Error in sending message: {}".format(e))
        return