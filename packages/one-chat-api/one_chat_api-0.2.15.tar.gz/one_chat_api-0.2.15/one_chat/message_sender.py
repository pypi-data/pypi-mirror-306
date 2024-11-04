# one_chat/message_sender.py

import requests
import json
import re


class MessageSender:
    def __init__(self, authorization_token):
        self.base_url = "https://chat-api.one.th/message/api/v1/push_message"
        self.headers = {
            "Authorization": f"Bearer {authorization_token}",
            "Content-Type": "application/json",
        }

    def send_message(self, to, bot_id, message, custom_notification=None):
        payload = {"to": to, "bot_id": bot_id, "type": "text", "message": message}
        if custom_notification:
            payload["custom_notification"] = custom_notification

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)

            if response.status_code == 200:
                return json.dumps(response.json(), indent=4)
            else:
                return self._handle_error(response)
        except requests.exceptions.RequestException as e:
            return {"status": "fail", "message": f"Request failed: {str(e)}"}

    def send_file(self, to, bot_id, file_path, custom_notification=None):
        data = {
            "to": to,
            "bot_id": bot_id,
            "type": "file",
        }

        if custom_notification:
            data["custom_notification"] = custom_notification

        headers = {k: v for k, v in self.headers.items() if k.lower() != "content-type"}

        with open(file_path, "rb") as file:
            files = {
                "file": (file_path, file),
            }

            try:
                response = requests.post(
                    self.base_url, headers=headers, data=data, files=files
                )

                if response.status_code == 200:
                    return json.dumps(response.json(), indent=4)
                else:
                    print(f"Response Status: {response.status_code}")
                    print(f"Response Content: {response.content}")
                    return self._handle_error(response)
            except requests.exceptions.RequestException as e:
                return {"status": "fail", "message": f"Request failed: {str(e)}"}

    def send_webview(self, to, bot_id, url, custom_notification=None):
        if not re.match(r"^(http|https)://", url):
            return {
                "status": "fail",
                "message": "Please specify a protocol (http or https) in the URL.",
            }

        payload = {
            "to": to,
            "bot_id": bot_id,
            "type": "web",
            "url": url,
        }

        if custom_notification:
            payload["custom_notification"] = custom_notification

        try:
            response = requests.post(self.base_url, headers=self.headers, json=payload)

            if response.status_code == 200:
                return json.dumps(response.json(), indent=4)
            else:
                return self._handle_error(response)
        except requests.exceptions.RequestException as e:
            return {"status": "fail", "message": f"Request failed: {str(e)}"}

    def _handle_error(self, response):
        try:
            error_response = response.json()
            return {
                "status": error_response.get("status", "fail"),
                "message": error_response.get("message", "Unknown error occurred."),
            }
        except json.JSONDecodeError:
            return {"status": "fail", "message": "Invalid response from the server."}
