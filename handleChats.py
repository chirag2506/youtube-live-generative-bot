from helpers.youtubeFunctionalities.client import getClient
from helpers.youtubeFunctionalities.stream import getStreamChatId
from helpers.youtubeFunctionalities.chat import getLiveChats
from helpers.youtubeFunctionalities.moderators import getModsList
from appUtils import log, configuration, readJson, respondToChat
import os, threading, time
from dotenv import load_dotenv
load_dotenv()

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
            print("Text: ", message.pubTime)
            print("*"*100)
            if message.text.startswith("!"):
                respondToChat(message)
        print("*"*100)
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