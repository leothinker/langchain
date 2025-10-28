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

account = Account(credentials, auth_flow_type="credentials", tenant_id=tenant_id)
if account.authenticate():
    print("Authenticated!")

# 'basic' adds: 'https://graph.microsoft.com/User.Read'
# 'message_all' adds: 'https://graph.microsoft.com/Mail.ReadWrite' and 'https://graph.microsoft.com/Mail.Send'
