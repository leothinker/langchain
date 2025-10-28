import datetime
import json
import os
from os import getenv

import msal
import requests
from dotenv import load_dotenv

load_dotenv()


CLIENT_ID = getenv("CLIENT_ID", "")
CLIENT_SECRET = getenv("CLIENT_SECRET", "")
TENANT_ID = getenv("TENANT_ID", "")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["https://graph.microsoft.com/.default"]


app = msal.ConfidentialClientApplication(
    client_id=CLIENT_ID,
    authority=AUTHORITY,
    client_credential=CLIENT_SECRET,
)


result = app.acquire_token_for_client(scopes=SCOPES)


if "error" in result:
    raise RuntimeError(f"获取 app token 失败: {result.get('error_description')}")
access_token = result["access_token"]
print("App access token:", access_token)


NGROK_URL = getenv("NGROK_DOMAIN")


subscription_url = "https://graph.microsoft.com/v1.0/subscriptions"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}


# TARGET_USER = "scliu.leo@outlook.com"
TARGET_USER = "advisor@nexx-global.com"
expire = "2025-10-25T11:00:00.0000000Z"

payload = {
    "changeType": "created",
    "notificationUrl": f"{NGROK_URL}/webhook",
    "resource": f"users/{TARGET_USER}/mailFolders('Inbox')/messages",
    "expirationDateTime": expire,
    "clientState": "9f294d2c-7396-4052-9f36-87f0548c08a4",
}
resp = requests.post(subscription_url, headers=headers, json=payload)
print(resp.status_code, resp.text)
