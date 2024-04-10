from appUtils import log, configuration, localizeTime
from googleapiclient.discovery import Resource
from helpers.youtubeFunctionalities.schemas import Message, Chat
from helpers.databaseFunctionalities.schemas import Viewer
from helpers.databaseFunctionalities.viewers import handleRedeemPoints
from helpers.llmFunctionalities.llm import respondToFaq
from helpers.obsFunctionalities.scene import getActiveScreen
from helpers.obsFunctionalities.sourceItem import redeemMeme
from datetime import datetime
import pytz
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
            messageTime = item.get("snippet", {}).get("publishedAt", "")
            messageTime = datetime.fromisoformat(messageTime) if messageTime != "" else datetime.now(pytz.utc)
            message = Message(
                id= item.get("id", ""),
                userId= item.get("snippet", {}).get("authorChannelId", ""),
                text= item.get("snippet", {}).get("displayMessage", ""),
                pubTime= localizeTime(messageTime)
            )
            chat.messages.append(message)
            del messageTime
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

def respondToChat(client: Resource, message: Message, user: Viewer, chatId: str):
    query = message.text.split(" ")
    command = query[0][1:]
    response = ""
    if(command.lower() == "ask"):
        query.pop(0)
        question = (" ").join(query)
        response = respondToFaq(question)
    elif(command.lower() == "game"):
        response = "Percy is currently playing {}".format(configuration["Youtube"]["CurrentGame"])
        # configuration["Youtube"]["CurrentGame"] = "NEW GAME"
    elif(command.lower() == "quests"):
        response = "You have completed {} quests. Keep chatting to increase the number of quest points (qp) and !redeem to to redeem the quests for a reward.".format(user.points)
    elif(command.lower() == "redeem"):
        if getActiveScreen() in configuration["OBS"]["RedeemScreens"]:
            query.pop(0)
            quest = (" ").join(query)
            if quest == "":
                response = "Redeem what? You need to specify what want to redeem the quests for. You can !ask me valid redeem choices"
            else:
                if quest == "aughh":
                    if user.points < 10:
                        response = "Insufficient quest points. Minimum for this: {}. You have completed {} quests.".format(10, user.points)
                    else:
                        redeemMeme("aughh", user.name)
                        points = handleRedeemPoints(user.channelId, 10, message.pubTime)
                        response = "Redeemed '{}'. Points left: {}".format("aughh", points)
                elif quest == "clap":
                    if user.points < 5:
                        response = "Insufficient quest points. Minimum for this: {}. You have completed {} quests.".format(5, user.points)
                    else:
                        redeemMeme("clap", user.name)
                        points = handleRedeemPoints(user.channelId, 5, message.pubTime)
                        response = "Redeemed '{}'. Points left: {}".format("clap", points)
                elif quest == "no":
                    if user.points < 5:
                        response = "Insufficient quest points. Minimum for this: {}. You have completed {} quests.".format(5, user.points)
                    else:
                        redeemMeme("no", user.name)
                        points = handleRedeemPoints(user.channelId, 5, message.pubTime)
                        response = "Redeemed '{}'. Points left: {}".format("no", points)
                elif quest == "rats":
                    if user.points < 25:
                        response = "Insufficient quest points. Minimum for this: {}. You have completed {} quests.".format(25, user.points)
                    else:
                        redeemMeme("rats", user.name)
                        points = handleRedeemPoints(user.channelId, 25, message.pubTime)
                        response = "Redeemed '{}'. Points left: {}".format("rats", points)
                else:
                    response = "Invalid redeem choice. You can !ask me valid redeem choices"
        else:
            response = "Let Percy switch to game screen first, then you can start redeeming quests for rewards."
    elif(command.lower() == "help"):
        response = "!ask <query> to ask a question, !game to get current game name, !quests to get your current loyalty points, !redeem <item> to redeem quests (for more info, use !ask)"
    else:
        response = "I'm sorry but this is an invalid command. type !help to get list of commands."
    del query
    del command
    response = "@{} {}".format(user.name, response)
    log.info("Bot Response: {}".format(response))
    insertLiveChat(client, chatId, response)
    del response
    return
