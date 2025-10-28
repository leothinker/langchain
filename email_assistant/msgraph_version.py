import asyncio
from os import getenv

from azure.identity import DeviceCodeCredential
from dotenv import load_dotenv
from msgraph import GraphServiceClient
from msgraph.generated.models.subscription import Subscription
from msgraph.graph_service_client import GraphServiceClient

load_dotenv()
scopes = ["User.Read"]

# Multi-tenant apps can use "common",
# single-tenant apps must use the tenant ID from the Azure portal
tenant_id = getenv("AZURE_TENANT_ID", "")

# Values from app registration
client_id = getenv("AZURE_CLIENT_ID", "")

# azure.identity
credential = DeviceCodeCredential(tenant_id=tenant_id, client_id=client_id)

graph_client = GraphServiceClient(credential, scopes)


async def main():
    request_body = Subscription(
        change_type="created,updated",
        notification_url="https://isadora-seriocomic-jacquelyn.ngrok-free.dev/webhook",
        lifecycle_notification_url="https://isadora-seriocomic-jacquelyn.ngrok-free.dev/lifecycle",
        resource="/me/mailfolders('inbox')/messages",
        expiration_date_time="2025-10-30T11:00:00.0000000Z",
        client_state="9f294d2c-7396-4052-9f36-87f0548c08a4",
    )

    result = await graph_client.subscriptions.post(request_body)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
