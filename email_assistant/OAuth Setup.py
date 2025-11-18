import os

from dotenv import load_dotenv
from O365 import Account

load_dotenv()

client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]
tenant_id = os.environ["AZURE_TENANT_ID"]
credentials = (client_id, client_secret)

# the default protocol will be Microsoft Graph
# the default authentication method will be "on behalf of a user"

account = Account(credentials, tenant_id=tenant_id)
if account.authenticate(
    scopes=["basic", "message_all"],
    redirect_uri="https://isadora-seriocomic-jacquelyn.ngrok-free.dev/email/oauth2/nativeclient",
):
    print("Authenticated!")

# 'basic' adds: 'https://graph.microsoft.com/User.Read'
# 'message_all' adds: 'https://graph.microsoft.com/Mail.ReadWrite' and 'https://graph.microsoft.com/Mail.Send'


# msg_id = "AAMkAGVhMjY1Mjg3LTgwMTUtNDY3Ni04ODQyLTMxYjk4NDY3ZDZmZQBGAAAAAACET05KW8qMSYmz9r6LyeNABwB3kxzV2CgJRqsQB9xlacMhAAAAAAEMAAB3kxzV2CgJRqsQB9xlacMhAAAJaqCrAAA="
# # user_id = "0b4b7253-af66-4987-8798-35389ea78f51"
# # mailbox = account.mailbox(resource=f"users/{user_id}")
# mailbox = account.mailbox()
# messages = [mailbox.get_message(object_id=msg_id)]

# if not messages:
#     print("No emails found matching the criteria")

# else:
#     print(f"Found {len(messages)} emails")
