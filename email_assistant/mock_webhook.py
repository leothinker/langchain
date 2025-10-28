import requests

WEBHOOK_URL = "http://127.0.0.1:2025/email"
payload = {
    "clientState": "demo-test-state-1234",
    "value": [
        {
            "subscriptionId": "11111111-2222-3333-4444-555555555555",
            "changeType": "created",
            "clientState": "demo-test-state-1234",
            "resource": "me/mailFolders('Inbox')/messages",
            "resourceData": {
                "@odata.type": "#Microsoft.Graph.Message",
                "id": "AQMkADAwATNiZmYAZC0yMGFlLWI0NmUtMDACLTAwCgBGAAADOY-Oe6UnlE6MvPUlyZP3DQcAXxFeN2tuRkSSrXtIp-nhywAAAgEMAAAAXxFeN2tuRkSSrXtIp-nhywAFyW3T4QAAAA==",
                "subject": "Demo message sent from script",
                "from": {
                    "emailAddress": {"address": "alice@example.com", "name": "Alice"}
                },
            },
        }
    ],
}
resp = requests.post(WEBHOOK_URL, json=payload)
print("HTTP status:", resp.status_code)
