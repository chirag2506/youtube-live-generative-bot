from logger import putlog
from datetime import datetime
import json
import os
import pytz

log = putlog(__file__)

def readFile(filename):
    content = ""

    try:
        with open(filename, 'r') as fileContent:
            content = fileContent.read()
    except Exception as Err:
        log.error("{}".format(Err))

    return content

def readJson(filename):
    content = {}

    try:
        content = json.loads(readFile(filename))
    except Exception as Err:
        log.error("{}".format(Err),exc_info=True)

    return content

def writeFile(filename, content):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    status = "success"
    try:
        with open(filename, 'w') as fileSource:
            fileSource.write(content)
    except Exception as Err:
        log.error("{}".format(Err))
        status = "failed"

    return status

def writeJson(filename, content):
    status = "Success"

    try:
        contentDump = json.dumps(content, indent=4, sort_keys=True)
        writeFile(filename, contentDump)
    except Exception as Err:
        log.error("{}".format(Err))
        status = "Failed"

    return status

configFile = "config/app.setting.json"
configuration = readJson(configFile)

def localizeTime(time: datetime) -> datetime:
    try:
        timeZone = pytz.timezone(configuration["App"]["TimeZone"])
        if time.tzinfo is None:
            time = pytz.utc.localize(time)
        newTime = time.astimezone(timeZone).replace(microsecond=0)
        return newTime
    except Exception as e:
        log.info("Error in localizing time: {}".format(e))