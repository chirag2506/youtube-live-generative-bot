from dotenv import load_dotenv
load_dotenv()
from helpers.youtubeFunctionalities.client import getClient
from helpers.youtubeFunctionalities.stream import getStreamChatId
from helpers.youtubeFunctionalities.chat import getLiveChats, respondToChat
from helpers.youtubeFunctionalities.moderators import getModsList
from helpers.databaseFunctionalities.viewers import handlePointUpdate
from appUtils import log, configuration, readJson
import os, threading, time

streamId = os.environ.get("STREAM_ID", "")
nextPageToken = "" 

def handleChats(client, chatId):
    global nextPageToken
    if chatId != "":
        if os.path.isfile(configuration["Youtube"]["Mods"]):
            mods = readJson(configuration["Youtube"]["Mods"]).get("mods", [])
        else:
            mods = getModsList(client, chatId, nextPageToken)
        chats = getLiveChats(client, chatId, nextPageToken)
        for message in chats.messages:
            print("User: ", message.userId)
            print("Text: ", message.text)
            print("Time: ", message.pubTime)
            print("*"*100)
            if message.userId != os.environ["MANAGER_ACCOUNT_YOUTUBE_ID"]:
                user = handlePointUpdate(client, message, mods)
                if message.text.startswith("!") and user.newMessage == True:
                    respondToChat(client, message, user, chatId)
                del user
        print("*"*100)
        if chats.nextPage != "":
            nextPageToken = chats.nextPage
        del chats
        del mods
    else:
        log.info("Received empty chat ID")
    return

def executePeriodically(interval):
    youtube = getClient()
    chatId = getStreamChatId(youtube, streamId)
    log.info("Chat ID: {}".format(chatId))
    while True:
        handleChats(youtube, chatId)
        time.sleep(interval)

if __name__ == "__main__":
    interval = 5  # Time interval in seconds
    threading.Thread(target=executePeriodically, args=(interval, ), daemon=True).start()
    try:
        while True:
            time.sleep(1)  # Just to keep the main thread alive
    except KeyboardInterrupt:
        print("Exiting...")