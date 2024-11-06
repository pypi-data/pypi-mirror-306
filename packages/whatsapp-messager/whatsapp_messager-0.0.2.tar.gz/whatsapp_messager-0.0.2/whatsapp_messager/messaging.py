import requests
from typing import Dict, List, Any, Optional

# https://graph.facebook.com/v{self.version_number}/{self.phone_number_id}/messages


class WhatsAppSender:
    def __init__(
        self, access_token: str, phone_number_id: str, version_number: str = "v15.0"
    ):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.version_number = version_number
        self.base_url = f"https://graph.facebook.com/{self.version_number}/{self.phone_number_id}/messages"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def send_otp_message(self, recipient_phone_number: str, otp: str) -> Dict[str, Any]:
        """Send OTP message to recipient"""
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": str(recipient_phone_number),
            "type": "template",
            "template": {
                "name": "otp_template",
                "language": {"code": "en_US"},
                "components": [
                    {
                        "type": "body",
                        "parameters": [{"type": "text", "text": str(otp)}],
                    },
                    {
                        "type": "button",
                        "sub_type": "url",
                        "index": "0",
                        "parameters": [{"type": "text", "text": str(otp)}],
                    },
                ],
            },
        }

        response = requests.post(self.base_url, headers=self.headers, json=data)
        return self._process_response(response)

    def send_text_message(
        self, recipient_phone_number: str, message: str, country_code: str
    ) -> Optional[Dict]:
        """Send text message to recipient"""
        data = {
            "messaging_product": "whatsapp",
            "to": f"{country_code}{recipient_phone_number}",
            "type": "text",
            "text": {"body": message},
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, json=data)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending WhatsApp message: {e}")
            return None

    def _process_response(self, response: requests.Response) -> Dict[str, Any]:
        """Process WhatsApp API response"""
        status_code = response.status_code
        content = response.json()

        if status_code != 200:
            error_data = response.json().get("error")
            if error_data:
                details = error_data.get("error_data", {}).get(
                    "details", error_data["message"]
                )
                return {"success": False, "message": str(details)}

        if "contacts" in content:
            contacts = content["contacts"]
            if contacts:
                wa_id = contacts[0].get("wa_id")
                if wa_id:
                    phone_number = wa_id

        if "messages" in content:
            messages = content["messages"]
            if messages:
                message_status = messages[0].get("message_status")
                if message_status:
                    return {"success": True, "message": "Message sent successfully"}

        return {"success": False, "message": "Failed to send message"}
