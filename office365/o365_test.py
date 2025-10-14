import os
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.tools.office365.utils import UTC_FORMAT
from O365 import Account, FileSystemTokenBackend
from O365.utils import QueryBuilder

load_dotenv()

# Setup paths
_ROOT = Path(__file__).parent.absolute() / "tools" / "office365"
_SECRETS_DIR = _ROOT / ".secrets"
TOKEN_PATH = _SECRETS_DIR / "o365_token.txt"


def to_upper_lower_case(value: str, upper: bool = True) -> str:
    """Convert string into upper or lower case"""

    value = re.sub(r"\w[\s\W]+\w", "", str(value))
    if not value:
        return value

    first_letter = str(value[0])
    if upper:
        first_letter = first_letter.upper()
    else:
        first_letter = first_letter.lower()

    return first_letter + re.sub(
        r"[\-_.\s]([a-z])", lambda matched: str(matched.group(1)).upper(), value[1:]
    )


def main():
    client_id = os.environ["CLIENT_ID"]
    client_secret = os.environ["CLIENT_SECRET"]
    credentials = (client_id, client_secret)

    # the default protocol will be Microsoft Graph
    # the default authentication method will be "on behalf of a user"

    token_backend = FileSystemTokenBackend(token_path=TOKEN_PATH)
    account = Account(credentials, token_backend=token_backend)
    # if account.authenticate(scopes=["basic", "message_all"]):
    #     print("Authenticated!")

    # 'basic' adds: 'https://graph.microsoft.com/User.Read'
    # 'message_all' adds: 'https://graph.microsoft.com/Mail.ReadWrite' and 'https://graph.microsoft.com/Mail.Send'

    mailbox = account.mailbox()
    builder = QueryBuilder(protocol=account.protocol)

    # query = builder.chain_or(
    #     builder.contains("subject", "george best"),
    #     builder.startswith("subject", "quotes"),
    # )

    # # 'created_date_time' will automatically be converted to the protocol casing.
    # # For example when using MS Graph this will become 'createdDateTime'.

    # query = query & builder.greater("created_date_time", datetime(2018, 3, 21))

    # print(query)

    # # contains(subject, 'george best') or startswith(subject, 'quotes') and createdDateTime gt '2018-03-21T00:00:00Z'
    # # note you can pass naive datetimes and those will be converted to you local timezone and then send to the api as UTC in iso8601 format

    # # To use Query objetcs just pass it to the query parameter:
    # filtered_messages = mailbox.get_messages(query=query)

    # # select only some properties for the retrieved messages:
    # query = builder.select("subject", "to_recipients", "created_date_time")

    # messages_with_selected_properties = mailbox.get_messages(query=query)

    # # searching is the easy part ;)
    # query = builder.search("george best is da boss")
    # messages = mailbox.get_messages(query=query)

    print(to_upper_lower_case("conversation_id"))

    query = builder.equals(
        "ConversationId",
        "AQQkADAwATNiZmYAZC0yMGFlLWI0NmUtMDACLTAwCgAQAAjdGbhrE0dHAJAqhXQbDVbT",
    )
    thread = mailbox.get_messages(limit=10, query=query)
    messages_in_thread = list(thread)
    print(len(messages_in_thread))
    # for message in mailbox.get_messages(limit=10, query=query):
    messages_in_thread.sort(key=lambda m: m.modified, reverse=True)
    print(messages_in_thread)
    for message in messages_in_thread:
        print(message)
        print(message.modified)


if __name__ == "__main__":
    main()
