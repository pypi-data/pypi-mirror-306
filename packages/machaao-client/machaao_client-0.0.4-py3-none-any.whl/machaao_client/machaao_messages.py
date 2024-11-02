from pprint import pprint

from .machaao_elements import Image

from .machaao_templates import Templates


class MachaaoButtonMessage:
    def __init__(self, text: str, buttons=None, quick_replies=None, ads=None, msg_credit=None):
        self.text = text
        self.quick_replies = quick_replies
        self.ads = ads
        self.credits = msg_credit
        self.buttons = buttons
        self.text_msg_obj = self._create_button_attachment_message_object()

    def __str__(self):
        print("MachaaoButtonMessage object")
        pprint(self.text_msg_obj, indent=2)
        return ""

    @property
    def message(self):
        return self.text_msg_obj

    def _create_button_attachment_message_object(self):
        button_msg_template = Templates().buttonMessage
        button_msg_template["message"]["attachment"]["payload"]["text"] = self.text

        if self.credits:
            button_msg_template["credit"] = self.credits

        if self.buttons is not None:
            buttons = list()
            for b in self.buttons:
                buttons.append(b.button)

            button_msg_template["message"]["attachment"]["payload"]["buttons"] = buttons

        if self.quick_replies is not None:
            quick_replies = list()
            for qr in self.quick_replies:
                quick_replies.append(qr.quick_reply)

            button_msg_template["message"]["quick_replies"] = quick_replies

        return button_msg_template


class MachaaoTextMessage:
    def __init__(self, text: str, quick_replies=None, ads=None, msg_credit=None):
        self.text = text
        self.quick_replies = quick_replies
        self.ads = ads
        self.credits = msg_credit
        self.text_msg_obj = self._create_text_message_object()

    def __str__(self):
        print("MachaaoTextMessage object")
        pprint(self.text_msg_obj, indent=2)
        return ""

    @property
    def message(self):
        return self.text_msg_obj

    def _create_text_message_object(self):
        text_msg_template = Templates().textMessage
        text_msg_template["message"]["text"] = self.text

        if self.credits:
            text_msg_template["credit"] = self.credits

        if self.ads:
            text_msg_template["ad"] = True

        if self.quick_replies is not None:
            quick_replies = list()
            for qr in self.quick_replies:
                quick_replies.append(qr.quick_reply)

            text_msg_template["message"]["quick_replies"] = quick_replies

        return text_msg_template


class MachaaoImageMessage:

    def __init__(self, image_object: Image, quick_replies=None, ads=None, msg_credit=None):
        self.img_obj = image_object.image
        self.text = self.img_obj["title"]
        self.image_url = self.img_obj["image_url"]
        self.quick_replies = quick_replies
        self.ads = ads
        self.credits = msg_credit
        self.img_msg_obj = self._create_image_message_object()

    def __str__(self):
        print("MachaaoImageMessage object")
        pprint(self.img_msg_obj, indent=2)
        return ""

    @property
    def message(self):
        return self.img_msg_obj

    def _create_image_message_object(self):
        img_msg_template = Templates().imageMessage
        img_msg_template["message"]["text"] = self.text
        img_msg_template["message"]["attachment"]["payload"]["url"] = self.image_url

        if self.quick_replies is not None:
            quick_replies = list()
            for qr in self.quick_replies:
                quick_replies.append(qr.quick_reply)

            img_msg_template["message"]["quick_replies"] = quick_replies

        return img_msg_template
