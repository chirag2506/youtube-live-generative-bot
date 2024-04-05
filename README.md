# Youtube Live Generative Bot

- Get chat messages: https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list
    - livechatid
    - next page token
    - part: snippet

- Get channel details: https://developers.google.com/youtube/v3/docs/channels/list
    - id
    - part: snippet

- Get live chat ID: https://developers.google.com/youtube/v3/live/docs/liveBroadcasts/list
    - id
    - part: snippet

- Get live active chat ID: https://developers.google.com/youtube/v3/docs/videos/list
    - id
    - part: liveStreamingDetails
    - gives back `20 char + liveChatID`
    - "liveChatId": "KicKGFVDLVpPZmZpVWtiMGhvTWE1dVZraEpEQRILYXhDTEpvZ1RGenm"
    - "activeLiveChatId": "Cg0KC2F4Q0xKb2dURnpzKicKGFVDLVpPZmZpVWtiMGhvTWE1dVZraEpEQRILYXhDTEpvZ1RGenm"

- Insert chat message: https://developers.google.com/youtube/v3/live/docs/liveChatMessages/insert
    - {
        "snippet": {
            "liveChatId": "",
            "textMessageDetails": {
            "messageText": ""
            },
            "type": "textMessageEvent"
        }
      }
    - part: snippet


Note that all of the methods for the YouTube Live Streaming API require OAuth 2.0 authorization.

min python: 3.11 for datetime.isoformat