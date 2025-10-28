from os import getenv

from dotenv import load_dotenv
from msal import ConfidentialClientApplication

load_dotenv()

AZURE_APP_ID = getenv("AZURE_CLIENT_ID", "")
AZURE_APP_TENANT = getenv("AZURE_TENANT_ID", "")
AZURE_APP_SECRET = getenv("AZURE_CLIENT_SECRET", "")
REDIRECT_URI = getenv("REDIRECT_URI", "")

# scopes = ["https://graph.microsoft.com/.default"]
scopes = ["Mail.Read", "Mail.ReadBasic"]


def _getToken():
    """
    Acquires an access token for authentication using the `ConfidentialClientApplication` class from the `msal` library.

    Returns:
    - str: The access token obtained for authentication with the Microsoft Graph API.
    """
    instance = ConfidentialClientApplication(
        client_id=AZURE_APP_ID,
        client_credential=AZURE_APP_SECRET,
        authority=f"https://login.microsoftonline.com/{AZURE_APP_TENANT}/",
    )

    token = instance.get_authorization_request_url(
        scopes=scopes,
        redirect_uri=REDIRECT_URI,
    )
    access_token = token

    if access_token:
        return access_token
    else:
        print("Failed to get the token")


if __name__ == "__main__":
    print(_getToken())
