
from pymongo.mongo_client import MongoClient
from appUtils import log
import os

connectionString = "mongodb+srv://{}:{}@youtube-live-manager.2gady4u.mongodb.net/?retryWrites=true&w=majority&appName=youtube-live-manager".format(
    os.environ["MONGO_DB_USER"], os.environ["MONGO_DB_PASS"]
)

# Create a new client and connect to the server
client = MongoClient(connectionString)
db = client[os.environ["MONGO_DB_NAME"]]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)