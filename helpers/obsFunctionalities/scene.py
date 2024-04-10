from appUtils import log, configuration
from helpers.obsFunctionalities.obs import obsClient

def getActiveScreen():
    scene = ""
    try:
        scene = obsClient.get_current_program_scene().current_program_scene_name
    except Exception as e:
        log.error("Error in getting active OBS screen: {}".format(e))
    return scene
    