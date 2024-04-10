import obsws_python as obs
import os
from appUtils import configuration

obsClient = obs.ReqClient(
    host= os.environ.get("OBS_HOST", "localhost"),
    port= configuration["OBS"]["Port"],
    password= os.environ.get("OBS_PASS", ""),
    timeout= configuration["OBS"]["Timeout"]
)