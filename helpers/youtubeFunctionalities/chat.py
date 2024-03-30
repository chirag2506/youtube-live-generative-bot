from appUtils import log, configuration
from googleapiclient.discovery import Resource
from helpers.youtubeFunctionalities.schemas import Message, Chat
from helpers.youtubeFunctionalities.users import getUserFromId
from helpers.llmFunctionalities.llm import respondToFaq
from typing import List
from copy import deepcopy

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
        resource = deepcopy(configuration["Youtube"]["Payload"]["SendMessage"])
        resource["snippet"]["liveChatId"] = liveChatId
        resource["snippet"]["textMessageDetails"]["messageText"] = message
        client.liveChatMessages().insert(part=part, body= resource).execute()
        del resource
    except Exception as e:
        log.error("Error in sending message: {}".format(e))
    return 

def respondToChat(client: Resource, message: Message, chatId: str, mods: List):
    query = message.text.split(" ")
    command = query[0][1:]
    if(command.lower() == "ask"):
        query.pop(0)
        question = (" ").join(query)
        response = respondToFaq(question)
        print(response)
    elif(command.lower() == "game"):
        response = "I am currently playing {}".format(configuration["Youtube"]["CurrentGame"])
        # configuration["Youtube"]["CurrentGame"] = "NEW GAME"
    elif(command.lower() == "points"):
        response = "Sorry people! I am developing the loyalty system right now. It will take some time."
    else:
        response = "Invalid command. Valid commands: !ask <query>, !game, !points"
    del query
    del command
    insertLiveChat(client, chatId, response)
    del response
    return
