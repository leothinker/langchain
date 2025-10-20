import datetime
import json
import os
from os import getenv

import msal
import requests
from dotenv import load_dotenv

load_dotenv()

# Azure应用注册信息
CLIENT_ID = getenv("CLIENT_ID", "")
CLIENT_SECRET = getenv("CLIENT_SECRET", "")
TENANT_ID = getenv("TENANT_ID", "")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["User.Read", "Mail.Read", "Notifications.ReadWrite.CreatedByApp"]


app = msal.PublicClientApplication(client_id=CLIENT_ID, authority=AUTHORITY)


# 发起设备码流程
flow = app.initiate_device_flow(scopes=SCOPES)
if "user_code" not in flow:
    raise RuntimeError(f"Device flow 启动失败: {flow}")
print("\n=== 请在浏览器打开下面的链接并输入验证码 ===")
print(flow["message"])  # 直接复制到浏览器
print("=== 等待授权完成后脚本会继续 ===\n")
result = app.acquire_token_by_device_flow(flow)  # 轮询等待用户完成

# token_response = app.acquire_token_interactive(scopes=SCOPES)
# access_token = token_response.get("access_token")


if "error" in result:
    print("❌ 授权失败")
    print("Error:", result.get("error"))
    print("Desc :", result.get("error_description"))
else:
    access_token = result["access_token"]
    refresh_token = result.get("refresh_token")  # 只要用户同意 offline_access，就会返回
    print("\n✅ Access token 已获取")
    print("access_token (前30字符):", access_token)
    if refresh_token:
        print("✅ 同时拿到了 refresh_token（可用于后续刷新）")
    print(f"有效期约 {result.get('expires_in') // 60} 分钟")


NGROK_URL = getenv("NGROK_DOMAIN")

NOTIFICATION_URL = f"{NGROK_URL}/webhook"  # 你的Webhook URL
resource = "/me/mailFolders('Inbox')/messages"

expire = "2025-10-17T11:00:00.0000000Z"


# # 2. 创建订阅
subscription_url = "https://graph.microsoft.com/v1.0/subscriptions"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}
subscription_body = {
    "changeType": "created",  # 监听创建事件
    "notificationUrl": NOTIFICATION_URL,
    "resource": resource,  # 资源：收件箱中的邮件
    "expirationDateTime": "2025-10-17T11:00:00.0000000Z",  # 订阅过期时间，最长不超过3天
    "clientState": "9f294d2c-7396-4052-9f36-87f0548c08a4",  # 用于验证通知的合法性:cite[4]
}

response = requests.post(subscription_url, headers=headers, json=subscription_body)

print("Status:", response.status_code)
print("Response:", response.text)
print("Json:", response.json())
