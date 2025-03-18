import requests
import os
from base64 import b64encode


def get_mtn_access_token():
    url = "https://sandbox.momodeveloper.mtn.com/collection/token/"
    consumer_key = os.getenv("MTN_USSD_CONSUMER_KEY")
    consumer_secret = os.getenv("MTN_USSD_CONSUMER_SECRET")

    auth_header = b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Ocp-Apim-Subscription-Key": "YOUR_SUBSCRIPTION_KEY"  # Replace with your subscription key
    }

    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    return None
