import requests

access_token = "eyJ0eXAiOiJKV1QiLCJub25jZSI6IkhHa2VaX1FlODJrWjNKczZ3SkJ2WlhSMUR6WXdlVTNoX1pUcm9sNWdJd1EiLCJhbGciOiJSUzI1NiIsIng1dCI6InlFVXdtWFdMMTA3Q2MtN1FaMldTYmVPYjNzUSIsImtpZCI6InlFVXdtWFdMMTA3Q2MtN1FaMldTYmVPYjNzUSJ9.eyJhdWQiOiJodHRwczovL2dyYXBoLm1pY3Jvc29mdC5jb20iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC82YmIyZjQyMy1kMzVjLTRiMGYtYjViZi0wNGI1OTQ3OTQwZjIvIiwiaWF0IjoxNzYxNjQyMTA4LCJuYmYiOjE3NjE2NDIxMDgsImV4cCI6MTc2MTY0NjI3MiwiYWNjdCI6MCwiYWNyIjoiMSIsImFjcnMiOlsicDEiXSwiYWlvIjoiQVpRQWEvOGFBQUFBYld3NXRoOHY3V0kyWnVCTXJabTQ4NG85TWVBNFR1aVB0NHNtanQzQzNpMThWWmd5WVJkTUhOQUE5T3g1Vkh6eHQ0a0FYWU1iVUJYWHZIVTd0amQ1cE5GQmV0aGVUZDJ5MTJWWFl6MGlqZlB0Mzd1VjFBTmNJS0lFb3Z3ZVhuaG4ydVFHeXFkT1JsYXlqSHE2cXYxMUZFWnNDd09BYmVUektjeEMzUUtiYmZld3NTZDkrSXBCR3hVVHU2c3k5YTR5IiwiYW1yIjpbInB3ZCIsIm1mYSJdLCJhcHBfZGlzcGxheW5hbWUiOiJlbWFpbF9hc3Npc3RhbnQiLCJhcHBpZCI6IjhhZmE0YWEwLWQ1ZmUtNGQ0My05Nzk2LTc1NmMxN2RmZWEyMSIsImFwcGlkYWNyIjoiMSIsImZhbWlseV9uYW1lIjoiTkVYWCIsImdpdmVuX25hbWUiOiJBZHZpc29yIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTE2LjQ5LjE0LjE2NiIsIm5hbWUiOiJBZHZpc29yIC0gTkVYWCIsIm9pZCI6IjBiNGI3MjUzLWFmNjYtNDk4Ny04Nzk4LTM1Mzg5ZWE3OGY1MSIsInBsYXRmIjoiMyIsInB1aWQiOiIxMDAzMjAwNTJGNzU2NUU4IiwicmgiOiIxLkFWWUFJX1N5YTF6VEQwdTF2d1MxbEhsQThnTUFBQUFBQUFBQXdBQUFBQUFBQUFBaUFXVldBQS4iLCJzY3AiOiJNYWlsLlJlYWQgTWFpbC5SZWFkQmFzaWMgTWFpbC5SZWFkV3JpdGUgTWFpbC5TZW5kIG9wZW5pZCBwcm9maWxlIFVzZXIuUmVhZCBVc2VyLlJlYWRCYXNpYy5BbGwgZW1haWwiLCJzaWQiOiIwMDliZDJiOS1hYjlhLTFkYjEtYWU0My0xZjUxOGZiOGVmZDkiLCJzaWduaW5fc3RhdGUiOlsia21zaSJdLCJzdWIiOiI1WXFOdUlVdDRvX2dXM01ua0pnbUNKT3lIbldaWHNJOWZOUUw3cDMtYlFVIiwidGVuYW50X3JlZ2lvbl9zY29wZSI6IkFTIiwidGlkIjoiNmJiMmY0MjMtZDM1Yy00YjBmLWI1YmYtMDRiNTk0Nzk0MGYyIiwidW5pcXVlX25hbWUiOiJhZHZpc29yQG5leHgtZ2xvYmFsLmNvbSIsInVwbiI6ImFkdmlzb3JAbmV4eC1nbG9iYWwuY29tIiwidXRpIjoiSFZfRXRHNF9lMG03MVo0dm91eGJBQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19hY2QiOjE3NjE1MTg1NzEsInhtc19hY3RfZmN0IjoiOSAzIiwieG1zX2Z0ZCI6IjJBTk1OT3N3MmZZZGZ2cEdxVjhnblNheTBUTEd3bGNtRzNBbDY0ZGN4WW9CYTI5eVpXRnpiM1YwYUMxa2MyMXoiLCJ4bXNfaWRyZWwiOiIyNiAxIiwieG1zX3N0Ijp7InN1YiI6IlB0UVFoMW1QWXZLbUxzUDlleFlGLXgxdHB0aUNYSGNaeWZfalFvdmdZc28ifSwieG1zX3N1Yl9mY3QiOiIyIDMiLCJ4bXNfdGNkdCI6MTY2MjcyNzI4MSwieG1zX3RudF9mY3QiOiIzIDEyIn0.msyN57AHRi0M8OSZBaye-jxdHaD5QJAVjXMUu00wZRN16PoUHaaUECktxJAGfsWtV3UfPlYvqh4ODx-YzU8s7trLpyCEhSDwEnP4PcKYHYzP4kYWPCw7FxIP9Ta9e1lMoZkgdQFU2LAOmlP7IjoHaNInFyvifFLC8h7ZZSpwf7Tn3bA467C2xC6v2Hi038jSYIjTh7TT08ywY5qhxIz1aQ5UY2I3jZWvg7VHukeaJUCxAr0FC2g29i-q_qDqgqgAQ87deKo7JaKybYpLaruap3ykv6SKYfuitoBNy8QLYQCZh3cgR54OFheTCDFsuRoICL2ktN73QByOPFN_Jmb4Gg"


# Step C: 读取邮件（假设你从 webhook 得到 message_id）
message_id = "AAMkAGVhMjY1Mjg3LTgwMTUtNDY3Ni04ODQyLTMxYjk4NDY3ZDZmZQBGAAAAAACET05KW8qMSYmz9r6LyeNABwB3kxzV2CgJRqsQB9xlacMhAAAAAAEMAAB3kxzV2CgJRqsQB9xlacMhAAAJaqCrAAA="
endpoint = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
headers = {"Authorization": "Bearer " + access_token}
resp = requests.get(endpoint, headers=headers)

if resp.status_code == 200:
    mail = resp.json()
    print("Subject:", mail.get("subject"))
    print("From:", mail.get("from"))
    print("Body preview:", mail.get("body"))
else:
    print("Failed to fetch message:", resp.status_code, resp.text)


# endpoint = "https://graph.microsoft.com/v1.0/me/sendMail"
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json",
# }
# body = {
#     "message": {
#         "subject": "Test email sent via Graph API",
#         "body": {"contentType": "Text", "content": "Hello — this is a test email."},
#         "toRecipients": [{"emailAddress": {"address": "scliu.leo@gmail.com"}}],
#     },
#     "saveToSentItems": True,
# }
# resp = requests.post(endpoint, headers=headers, json=body)
# print(resp.status_code, resp.text)
