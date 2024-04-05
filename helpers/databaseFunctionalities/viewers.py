from appUtils import log, localizeTime, datetime
from helpers.databaseFunctionalities.database import viewerCollection
from helpers.databaseFunctionalities.schemas import Viewer
from googleapiclient.discovery import Resource
from helpers.youtubeFunctionalities.schemas import Message
from helpers.youtubeFunctionalities.users import getUserFromId
from typing import List
from bson.objectid import ObjectId

def addViewer(user: Viewer) -> str:
    try:
        viewer = viewerCollection.insert_one(
            {
                "Name": user.name, 
                "ChannelId": user.channelId,
                "Mod": user.mod,
                "Points": 1,
                "LastUpdated": user.lastUpdate
            }
        )
        return viewer.inserted_id
    except Exception as e:
        log.error("Error in inserting user to database: {}".format(e))
        return None

def updateViewerPoints(id: ObjectId, messageTime: datetime, score: int = 1) -> int:
    points = 0
    try:
        points = viewerCollection.find_one_and_update(
            {"_id": id},
            {
                '$inc': {'Points': score},
                '$set': {'LastUpdated': messageTime}
            }
        )["Points"]
    except Exception as e:
        log.error("Error in updating points: {}".format(e))
    return points

def getViewerId(channelId: str) -> str | None:
    viewerDataId = None
    try:
        user = viewerCollection.find_one({"ChannelId": channelId})
        if user is not None:
            viewerDataId = user["_id"]
        del user
    except Exception as e:
        log.error("Error in getting user ID: {}".format(e))
    return viewerDataId

def handlePointUpdate(client: Resource, message: Message, mods: List) -> Viewer:
    viewerDataId = getViewerId(message.userId)
    user = Viewer(
        name= "", channelId= message.userId, points=1,
        mod= True if message.userId in mods else False, lastUpdate= message.pubTime
    )
    if viewerDataId is None:
        user.name = getUserFromId(client, message.userId)
        viewerDataId = addViewer(user= user)
    else:
        viewer = viewerCollection.find_one({"_id": ObjectId(viewerDataId)})
        user.name = viewer["Name"]
        if localizeTime(viewer["LastUpdated"]) < message.pubTime:
            #update
            user.newMessage = True
            points = updateViewerPoints(id= ObjectId(viewerDataId), messageTime= message.pubTime, score= 1)
        else:
            points = None
        if points is not None and points != 0:
            user.points = points
        else:
            user.points = viewer["Points"]
            user.lastUpdate = localizeTime(viewer["LastUpdated"])
        del points
        del viewer
    return user

