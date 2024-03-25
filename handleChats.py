from helpers.youtubeFunctionalities.client import getClient
from helpers.youtubeFunctionalities.stream import getStreamChatId
from appUtils import log
import os
from dotenv import load_dotenv
load_dotenv()

streamId = os.environ.get("STREAM_ID", "")
nextPageToken = ""

youtube = getClient()

chatId = getStreamChatId(youtube, streamId)
if chatId != "":
    print(chatId)
else:
    log.info("Received empty chat ID")
