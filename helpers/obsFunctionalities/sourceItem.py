from time import sleep
from appUtils import log, os
from helpers.obsFunctionalities.obs import obsClient

BASE_PATH = os.environ["REDEEM_FILES_LOCATION"]

def redeemMeme(memeName: str, user: str):
    try:
        obsClient.set_input_settings(
            "redeemAudio", 
            {"local_file":  "{}/{}.mp3".format(BASE_PATH, memeName)},
            True
        )
        obsClient.set_input_settings(
            "redeemText",
            {"text": user},
            True
        )
        obsClient.set_input_settings(
            "redeemMeme",
            {"file": "{}/{}.png".format(BASE_PATH, memeName)},
            True
        )
        obsClient.trigger_media_input_action("redeemAudio", "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART")
        sleep(0.5)
        while True:
            # print(obsClient.get_media_input_status("redeemMeme").media_state)
            if obsClient.get_media_input_status("redeemAudio").media_state == "OBS_MEDIA_STATE_ENDED":
                obsClient.set_input_settings(
                    "redeemAudio",
                    {"local_file": ""},
                    True
                )
                obsClient.set_input_settings(
                    "redeemText",
                    {"text": ""},
                    True
                )
                obsClient.set_input_settings(
                    "redeemMeme",
                    {"file": ""},
                    True
                )
                log.info("Completed Meme {} by {}".format(memeName, user))
                break
    except Exception as e:
        log.error("Error in redeeming meme: {}".format(e))
    return

