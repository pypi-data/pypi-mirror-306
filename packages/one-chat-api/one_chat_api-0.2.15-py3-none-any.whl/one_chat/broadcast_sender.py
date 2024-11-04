# one_chat/broadcast_sender.py

import requests
import json


class BroadcastSender:
    def __init__(self, authorization_token):
        self.base_url = "https://chat-api.one.th/bc_msg/api/v1/broadcast_group"
        self.headers = {
            "Authorization": f"Bearer {authorization_token}",
            "Content-Type": "application/json",
        }

    def broadcast_message(self, bot_id, to, message):
        if len(to) > 100:
            return {"status": "fail", "message": "parameter to out of range."}

        payload = {"bot_id": bot_id, "to": to, "message": message}

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
