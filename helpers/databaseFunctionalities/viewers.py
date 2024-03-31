from appUtils import log
from helpers.databaseFunctionalities.database import viewerCollection
from helpers.databaseFunctionalities.schemas import Viewer
from bson.objectid import ObjectId
# viewers.insert_one({"Name": "rc", "Id": "2345432", "Mod": True, "Points": 1})

# viewers.find_one_and_update({"Name": "rc", "Points": 1}, {"$inc": {"Points": 1}})
print(viewerCollection.find_one({"Name": "rc"}).get("_id"))

def addViewer(user: Viewer):
    return

def updateViewerPoints(id: ObjectId, score: int = 1):
    return


