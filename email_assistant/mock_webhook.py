import requests

WEBHOOK_URL = "http://127.0.0.1:2025/email/notificationClient"
payload = {
    "value": [
        {
            "subscriptionId": "6e06fbdd-c26c-408a-bd8c-751b9ea7bda1",
            "subscriptionExpirationDateTime": "2025-10-30T11:00:00+00:00",
            "changeType": "created",
            "resource": "Users/0b4b7253-af66-4987-8798-35389ea78f51/Messages/AAMkAGVhMjY1Mjg3LTgwMTUtNDY3Ni04ODQyLTMxYjk4NDY3ZDZmZQBGAAAAAACET05KW8qMSYmz9r6LyeNABwB3kxzV2CgJRqsQB9xlacMhAAAAAAEMAAB3kxzV2CgJRqsQB9xlacMhAAAJaqC5AAA=",
            "resourceData": {
                "@odata.type": "#Microsoft.Graph.Message",
                "@odata.id": "Users/0b4b7253-af66-4987-8798-35389ea78f51/Messages/AAMkAGVhMjY1Mjg3LTgwMTUtNDY3Ni04ODQyLTMxYjk4NDY3ZDZmZQBGAAAAAACET05KW8qMSYmz9r6LyeNABwB3kxzV2CgJRqsQB9xlacMhAAAAAAEMAAB3kxzV2CgJRqsQB9xlacMhAAAJaqC5AAA=",
                "@odata.etag": 'W/"CQAAABYAAAB3kxzV2CgJRqsQB9xlacMhAAAJawE8"',
                "id": "AAMkAGVhMjY1Mjg3LTgwMTUtNDY3Ni04ODQyLTMxYjk4NDY3ZDZmZQBGAAAAAACET05KW8qMSYmz9r6LyeNABwB3kxzV2CgJRqsQB9xlacMhAAAAAAEMAAB3kxzV2CgJRqsQB9xlacMhAAAJaqC5AAA=",
            },
            "clientState": "9f294d2c-7396-4052-9f36-87f0548c08a4",
            "tenantId": "6bb2f423-d35c-4b0f-b5bf-04b5947940f2",
        }
    ]
}
resp = requests.post(WEBHOOK_URL, json=payload)
print("HTTP status:", resp.status_code)
