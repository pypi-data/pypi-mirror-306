class Templates:
    def __init__(self):
        pass

    @property
    def textMessage(self):
        template = {
            "users": [],
            "identifier": "BROADCAST_FB_QUICK_REPLIES",
            "notificationType": "REGULAR",
            "message": {},
            "credit": 0,
            "ad": False
        }

        return template

    @property
    def buttonMessage(self):
        template = {
            "users": [],
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": "",
                        "buttons": [{
                        }]
                    }
                }
            },
            "credit": 0,
            "ad": False
        }

        return template

    @property
    def imageMessage(self):
        template = {
            "users": [],
            "identifier": "BROADCAST_FB_TEMPLATE_GENERIC",
            "notificationType": "REGULAR",
            "source": "firebase",
            "message": {
                "text": "",
                "attachment": {
                    "type": "image",
                    "payload": {
                        "url": ""
                    }
                },
            }
        }

        return template
