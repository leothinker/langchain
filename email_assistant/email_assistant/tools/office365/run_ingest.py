import asyncio
import hashlib
import logging
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.tools.office365.utils import UTC_FORMAT
from langgraph_sdk import get_client
from O365 import Account, FileSystemTokenBackend, Message

logger = logging.getLogger(__name__)
load_dotenv()

# Setup paths
_ROOT = Path(__file__).parent.absolute()
_SECRETS_DIR = _ROOT / ".secrets"
TOKEN_PATH = _SECRETS_DIR / "o365_token.txt"


def load_office365_credentials():
    """Authenticate using the Microsoft Graph API"""
    if "CLIENT_ID" in os.environ and "CLIENT_SECRET" in os.environ:
        client_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]
        credentials = (client_id, client_secret)
        return credentials
    else:
        logger.error(
            "Error: The CLIENT_ID and CLIENT_SECRET environmental variables have not "
            "been set. Visit the following link on how to acquire these authorization "
            "tokens: https://learn.microsoft.com/en-us/graph/auth/"
        )
        return None


def clean_body(body: str) -> str:
    """Clean body of a message or event."""
    try:
        from bs4 import BeautifulSoup

        try:
            # Remove HTML
            soup = BeautifulSoup(str(body), "html.parser")
            body = soup.get_text()

            # Remove return characters
            body = "".join(body.splitlines())

            # Remove extra spaces
            body = " ".join(body.split())

            return str(body)
        except Exception:
            return str(body)
    except ImportError:
        return str(body)


def extract_email_data(message: Message):
    """Extract key information from a Office365 message."""
    email_data = {}
    email_data["from_email"] = str(message.sender)

    email_data["page_content"] = clean_body(message.body)

    email_data["subject"] = message.subject

    email_data["send_time"] = message.modified.strftime(UTC_FORMAT)

    email_data["to_email"] = str(message.to._recipients[0])
    # for recipient in message.to._recipients:
    #     email_data["to_email"].append(str(recipient))

    email_data["id"] = message.object_id
    email_data["thread_id"] = message.conversation_id

    return email_data


async def ingest_email_to_langgraph(
    email_data, graph_name, url="http://127.0.0.1:2024"
):
    """Ingest an email to LangGraph."""
    # Connect to LangGraph server
    client = get_client(url=url)

    # Create a consistent UUID for the thread
    raw_thread_id = email_data["thread_id"]
    thread_id = str(
        uuid.UUID(hex=hashlib.md5(raw_thread_id.encode("UTF-8")).hexdigest())
    )
    print(f"Office365 thread ID: {raw_thread_id} → LangGraph thread ID: {thread_id}")

    thread_exists = False
    try:
        # Try to get existing thread info
        thread_info = await client.threads.get(thread_id)
        thread_exists = True
        print(f"Found existing thread: {thread_id}")
    except Exception as e:
        # If thread doesn't exist, create it
        print(f"Creating new thread: {thread_id}")
        thread_info = await client.threads.create(thread_id=thread_id)

    # If thread exists, clean up previous runs
    if thread_exists:
        try:
            # List all runs for this thread
            runs = await client.runs.list(thread_id)

            # Delete all previous runs to avoid state accumulation
            for run_info in runs:
                run_id = run_info.id
                print(f"Deleting previous run {run_id} from thread {thread_id}")
                try:
                    await client.runs.delete(thread_id, run_id)
                except Exception as e:
                    print(f"Failed to delete run {run_id}: {str(e)}")
        except Exception as e:
            print(f"Error listing/deleting runs: {str(e)}")

    # Update thread metadata with current email ID
    await client.threads.update(thread_id, metadata={"email_id": email_data["id"]})

    # Create a fresh run for this email
    print(f"Creating run for thread {thread_id} with graph {graph_name}")

    run = await client.runs.create(
        thread_id,
        graph_name,
        input={
            "messages": [
                (
                    "user",
                    f"Help me to respond to this email: {email_data['page_content']}",
                )
            ],
            # "email_input": {
            #     "from": email_data["from_email"],
            #     "to": email_data["to_email"],
            #     "subject": email_data["subject"],
            #     "body": email_data["page_content"],
            #     "id": email_data["id"],
            # },
        },
        # multitask_strategy="rollback",
    )

    print(f"Run created successfully with thread ID: {thread_id}")

    return thread_id, run


async def fetch_and_process_emails():
    """Fetch emails from Office365 and process them through LangGraph."""
    # Load Office365 credentials
    credentials = load_office365_credentials()
    if not credentials:
        print("Failed to load Office365 credentials")
        return 1
    token_backend = FileSystemTokenBackend(token_path=TOKEN_PATH)

    # Build Office365 service
    service = Account(credentials, token_backend=token_backend)

    # Process emails
    processed_count = 0

    try:
        # Get messages from the specified email address
        email_address = "scliu.leo@outlook.com"
        mailbox = service.mailbox()
        max_results: int = 10

        # Construct Gmail search query
        query = f"to:{email_address} OR from:{email_address}"

        print(f"Office365 search query: {query}")

        # Execute the search
        query = mailbox.q().search(query)
        messages = list(mailbox.get_messages(limit=max_results))

        if not messages:
            print("No emails found matching the criteria")
            return 0

        print(f"Found {len(messages)} emails")

        # Process each email

        for i, message in enumerate(messages):
            # Extract email data
            email_data = extract_email_data(message)

            print(f"\nProcessing email {i + 1}/{len(messages)}:")
            print(f"From: {email_data['from_email']}")
            print(f"Subject: {email_data['subject']}")
            print(f"Content: {email_data['page_content']}")
            print(f"ID: {email_data['id']}")

            # Ingest to LangGraph
            # thread_id, run = await ingest_email_to_langgraph(
            #     email_data, "email_assistant"
            # )

            processed_count += 1
            return 0

        print(f"\nProcessed {processed_count} emails successfully")
        return 0

    except Exception as e:
        print(f"Error processing emails: {str(e)}")
        return 1


if __name__ == "__main__":
    # Get command line arguments
    # args = parse_args()

    # Run the script
    exit(asyncio.run(fetch_and_process_emails()))
