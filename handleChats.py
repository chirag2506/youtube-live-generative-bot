from helpers.youtubeFunctionalities.client import getClient
from helpers.youtubeFunctionalities.stream import getStreamChatId
from helpers.youtubeFunctionalities.chat import getLiveChats
from helpers.youtubeFunctionalities.moderators import getModsList
from appUtils import log, configuration, readJson
import os
from dotenv import load_dotenv
load_dotenv()

def handle():
    streamId = os.environ.get("STREAM_ID", "")
    nextPageToken = ""

    youtube = getClient()

    chatId = getStreamChatId(youtube, streamId)
    if chatId != "":
        log.info("Chat ID: {}".format(chatId))
        if os.path.isfile(configuration["Youtube"]["Mods"]):
            mods = readJson(configuration["Youtube"]["Mods"]).get("mods", [])
        else:
            mods = getModsList(youtube, chatId, nextPageToken)
        chats = getLiveChats(youtube, chatId)
        for message in chats.messages:
            print("User: ", message.userId)
            print("Text: ", message.text)
            print("*"*100)
            # if message.text.startswith("!"):

        nextPageToken = chats.nextPage
    else:
        log.info("Received empty chat ID")


if __name__ == "__main__":
    handle()