import json
from base64 import b64decode
from datetime import datetime

import jwt
import requests
from requests.structures import CaseInsensitiveDict

c = 'UTF-8'


class MachaaoSession:
    def __init__(self, request, environ="dev", server_session_create_time=None):
        self.base_url = self.get_base_url(environ)
        self.API_ENDPOINT = self.base_url + "/v1/messages/send"
        self.user_id, self.api_token = self._extract_sender_and_token(request)
        self.user_message, self.user, self.os, self.client, self.sdk, self.attachments, self.timezone = self._extract_message(request)
        print(f"New message received: {self.user_message}")
        self.metadata = self._extract_metadata(request)
        self.headers = self.generate_header()
        self.server_session_create_time = server_session_create_time

    @staticmethod
    def get_base_url(env):
        url_dict = {
            "dev": "https://ganglia-dev.machaao.com",
            "prod": "https://ganglia.machaao.com",
        }
        return url_dict.get(env)

    @staticmethod
    def _extract_sender_and_token(req):
        user_id = req.headers["machaao-user-id"]
        api_token = req.headers.get("bot-token")
        print(f"User ID: {user_id}")
        return user_id, api_token

    def _extract_message(self, req):
        decoded_jwt = None
        body = req.json
        if body and body["raw"]:
            decoded_jwt = jwt.decode(body["raw"], self.api_token, algorithms='HS512', options={'verify_iat': False})
        text = decoded_jwt.get("sub")
        if isinstance(text, str):
            text = json.loads(decoded_jwt["sub"])

        message = text["messaging"][0]["message_data"]["text"]
        timezone = text["messaging"][0]["user"]["timezone"]

        attachments = dict()
        if text["messaging"][0]["message_data"].get("attachment") is not None:
            for attachment in text["messaging"][0]["message_data"]["attachment"]:
                if attachment["type"] == "image/png":
                    attachments["image"] = attachment["url"]

        _user = text["messaging"][0]["user"]
        _client = text["messaging"][0]["client"]

        try:
            _os = text["messaging"][0]["type"]
        except Exception as e:
            _os = "android"

        _sdk = text["messaging"][0]["version"]
        if _sdk:
            _sdk = _sdk.replace('v', '')

        return message, _user, _os, _client, _sdk, attachments, timezone

    def _extract_metadata(self, req):
        decoded_jwt = None
        body = req.json
        if body and body["raw"]:
            decoded_jwt = jwt.decode(body["raw"], self.api_token, algorithms='HS512', options={'verify_iat': False})
        sub = decoded_jwt.get("sub")
        if sub:
            messaging = sub.get("messaging")
        else:
            messaging = None

        if messaging and len(messaging):
            data = messaging[0]
            return data

    def check_balance(self, DEFAULT_HTTP_TIMEOUT=10):
        balance = 0

        e = 'L3YxL2NvaW5zL2JhbGFuY2UvY2hlY2s='
        check = b64decode(e).decode(c)

        url = f"{self.base_url}{check}"

        headers = CaseInsensitiveDict()
        headers["api_token"] = self.api_token
        headers["Content-Type"] = "application/json"

        data = {
            "userId": self.user_id,
            "coins": 1
        }

        resp = requests.post(url, data=json.dumps(data), headers=headers, timeout=DEFAULT_HTTP_TIMEOUT)

        if resp.status_code == 200:
            out = resp.json()
            if out and out["balance"]:
                balance = out["balance"]

        print(f"balance: {balance}, user_id: {self.user_id}")

        return balance

    @staticmethod
    def parse(data):
        msg_type = data.get('type')
        created_at = data.get('_created_at')
        if msg_type == "outgoing":
            # parse the outer and the inner message payload
            msg_data = json.loads(data['message'])
            msg_data_2 = json.loads(msg_data['message']['data']['message'])

            if msg_data_2 and msg_data_2.get('text', ''):
                text_data = msg_data_2['text']
            elif msg_data_2 and msg_data_2.get('attachment', None) and msg_data_2['attachment'].get('payload', '') and \
                    msg_data_2['attachment']['payload'].get('text', ''):
                text_data = msg_data_2['attachment']['payload']['text']
            else:
                text_data = ""
        else:
            msg_data = json.loads(data['incoming'])
            if msg_data['message_data']['text']:
                text_data = msg_data['message_data']['text']
            else:
                text_data = ""

        if created_at:
            date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
            created_at = datetime.strptime(created_at, date_format)

        return msg_type, created_at, str.strip(text_data)

    def get_recent_texts(self, limit: int, current_session=False, process_for_ai=False):
        e = "L3YxL2NvbnZlcnNhdGlvbnMvaGlzdG9yeS8="
        check = b64decode(e).decode(c)

        url = f"{self.base_url}{check}{self.user_id}/{limit}"
        limit += 1
        headers = CaseInsensitiveDict()
        headers["api_token"] = self.api_token
        headers["Content-Type"] = "application/json"

        resp = requests.get(url, headers=headers, timeout=10)

        if resp.status_code == 200:
            messages = resp.json()[:-1]
            if current_session:
                filtered_messages = list()
                for message in messages:
                    create_time_stamp = message.get("_created_at")
                    create_time = datetime.strptime(create_time_stamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                    if create_time > self.server_session_create_time:
                        filtered_messages.append(message)

                while len(filtered_messages) > 0 and (filtered_messages[0].get("type") == "outgoing"):
                    _ = filtered_messages.pop(0)

                messages = filtered_messages

            if process_for_ai:
                last_qualified_convo_time = self.get_user_tag("last_qualified_convo_time")
                qualified = True
                processed_messages = list()
                for text in messages[::-1]:
                    msg_type, created_at, text_data = self.parse(text)

                    try:
                        if last_qualified_convo_time is not None:
                            q_last_reset_convo_time = datetime.fromtimestamp(last_qualified_convo_time)
                            qualified = created_at >= q_last_reset_convo_time
                    except Exception as err:
                        print(f"error in processing qualified convo history check for {self.user_id} - {err}")

                    other_qualification_criteria = text_data and "ooops," not in text_data.lower() and "aditemidentifier" not in text_data.lower() and "balance" not in text_data.lower() and "error" not in text_data.lower() and "multi language" not in text_data.lower() and "~" not in text_data.lower()
                    if qualified and other_qualification_criteria:
                        if msg_type is not None:
                            outgoing = ("ai", text_data)
                            processed_messages.append(outgoing)
                        else:
                            incoming = ("user", text_data)
                            processed_messages.append(incoming)
                messages = processed_messages
            return messages

    def add_tag_to_user(self, tag, value, status=1):
        """ This function is used to add tag to userId."""

        e = "L3YxL3VzZXJzL3RhZy8="
        check = b64decode(e).decode(c)

        url = f"{self.base_url}{check}{self.user_id}"

        headers = {
            "api_token": self.api_token,
            "Content-Type": "application/json",
        }

        if value is not None:
            values = [value]
        else:
            values = []

        payload = {
            "tag": tag,
            "source": 'firebase',
            "status": status,
            "values": values,
        }

        print(f"sending tag: {payload} to server: {url}...")
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            print("Successfully added tag")
        else:
            print(f"Error in adding tag. Error code: {response.status_code}")

    def _fetch_tags_for_user(self):
        e = "L3YxL3VzZXJzL3RhZ3Mv"
        check = b64decode(e).decode(c)

        _cache_ts_param = str(datetime.now().timestamp())
        url = f"{self.base_url}{check}{self.user_id}?v={_cache_ts_param}"

        headers = {
            "api_token": self.api_token,
            "Content-Type": "application/json",
        }

        response = requests.request("GET", url, headers=headers, timeout=10)
        if response and response.status_code == 200:
            tags = dict()
            for tag in response.json():
                if tag.get('name') is not None:
                    val = tag.get('values')
                    # print(val)
                    if isinstance(val, list) and len(val) > 0:
                        tags[tag.get('name')] = val[0]
                    else:
                        tags[tag.get('name')] = None
            return tags
        else:
            print("Could not connect to Machaao Tags API")
            return []

    def get_user_tag(self, tag_name: str, default=None):
        ret = None
        user_tags = self._fetch_tags_for_user()
        if user_tags:
            ret = user_tags.get(tag_name)

        if ret is not None:
            return ret
        return default

    def get_bot_details(self, tag_name: str, no_cache=True):
        e = "L3YxL2JvdHMvY29uZmln"
        check = b64decode(e).decode(c)

        _cache_ts_param = str(datetime.now().timestamp())

        url = f"{self.base_url}/v1/bots/config"

        if no_cache:
            url = f"{self.base_url}/v1/bots/config?v={_cache_ts_param}"

        headers = {
            "api_token": self.api_token,
            "Content-Type": "application/json",
        }

        response = requests.request("GET", url, headers=headers)

        if response and response.status_code == 200:
            data = response.json()
            return data.get(tag_name)
        else:
            return None

    def generate_header(self):
        headers = {
            "api_token": self.api_token,
            "Content-Type": "application/json"
        }
        return headers

    def send_message(self, payload):
        message = payload.message
        message["users"] = [self.user_id]
        resp = requests.post(url=self.API_ENDPOINT, data=json.dumps(message), headers=self.headers)
        return str(resp.status_code)
