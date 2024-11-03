class Image:
    def __init__(self, image_url, title, subtitle=None):
        self.image_url = image_url
        self.title = title
        self.subtitle = subtitle
        self.image_obj = self._create_image_object()

    def _create_image_object(self):
        img_dict = {
            "title": self.title,
            "image_url": self.image_url
        }

        if self.subtitle is not None:
            img_dict["subtitle"] = self.subtitle

        return img_dict

    @property
    def image(self):
        return self.image_obj


class Button:
    def __init__(self, title, btn_type, payload=None):
        self.title = title
        self.btn_type = btn_type
        self.payload = payload
        self.btn_obj = self._create_button_object()

    def _create_button_object(self):
        btn_dict = {
            "title": self.title,
            "type": self.btn_type,
        }

        if self.payload is not None:
            btn_dict["payload"] = self.payload

        return btn_dict

    @property
    def button(self):
        return self.btn_obj


class QuickReply:
    def __init__(self, content_type, title, payload):
        self.title = title
        self.content_type = content_type
        self.payload = payload
        self.qr_obj = self._create_quick_reply_object()

    def _create_quick_reply_object(self):
        qr_dict = {
            "content_type": self.content_type,
            "title": self.title,
            "payload": self.payload
        }

        return qr_dict

    @property
    def quick_reply(self):
        return self.qr_obj
