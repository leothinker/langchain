import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, Optional

from dotenv import load_dotenv
from langchain_core.tools import tool
from pydantic import BaseModel, Field

load_dotenv()
# Setup basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define paths for credentials and tokens
_ROOT = Path(__file__).parent.absolute()
_SECRETS_DIR = _ROOT / ".secrets"
TOKEN_PATH = _SECRETS_DIR / "o365_token.txt"

# We need to try importing the Gmail API libraries
# If they're not available, we'll use a mock implementation
try:
    from datetime import timedelta

    from O365 import Account, FileSystemTokenBackend

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Email content extraction function
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

    OFFICE365_API_AVAILABLE = True


except ImportError:
    # If Office365 API libraries aren't available, set flag to use mock implementation
    OFFICE365_API_AVAILABLE = False
    logger = logging.getLogger(__name__)


# Helper function that is used by the tool and can be imported elsewhere
def fetch_group_emails(
    email_address: str,
    minutes_since: int = 30,
    office365_token: Optional[str] = None,
    include_read: bool = False,
    skip_filters: bool = False,
) -> Iterator[Dict[str, Any]]:
    """
    Fetch recent emails from Gmail that involve the specified email address.

    This function retrieves emails where the specified address is either a sender
    or recipient, processes them, and returns them in a format suitable for the
    email assistant to process.

    Args:
        email_address: Email address to fetch messages for
        minutes_since: Only retrieve emails newer than this many minutes
        office365_token: Optional token for Gmail API authentication
        include_read: Whether to include already read emails (default: False)
        skip_filters: Skip thread and sender filtering (return all messages, default: False)

    Yields:
        Dict objects containing processed email information
    """
    use_mock = False

    # Check if we need to use mock implementation
    if not OFFICE365_API_AVAILABLE:
        logger.info("Office365 API not available, using mock implementation")
        use_mock = True

    # Check if required credential files exist
    if not use_mock and not office365_token:
        token_path = str(_SECRETS_DIR / "o365_token.txt")

        if not os.path.exists(token_path):
            logger.warning(
                "No Office365 API credentials found. Looking for o365_token.txt in .secrets directory"
            )
            logger.warning("Using mock implementation instead")
            use_mock = True

    # Return mock data if needed
    if use_mock:
        # For demo purposes, we return a mock email
        mock_email = {
            "from_email": "sender@example.com",
            "to_email": email_address,
            "subject": "Sample Email Subject",
            "page_content": "This is a sample email body for testing the email assistant.",
            "id": "mock-email-id-123",
            "thread_id": "mock-thread-id-123",
            "send_time": datetime.now().isoformat(),
        }

        yield mock_email
        return

    try:
        # Get Office365 API credentials from parameters, environment variables, or local files
        credentials = load_office365_credentials()

        token_backend = FileSystemTokenBackend(token_path=TOKEN_PATH)
        service = Account(credentials, token_backend=token_backend)

        # Calculate timestamp for filtering
        after = int((datetime.now() - timedelta(minutes=minutes_since)).timestamp())

        # Construct Office365 search query
        # This query searches for:
        # - Emails sent to or from the specified address
        # - Emails after the specified timestamp
        # - Including emails from all categories (inbox, updates, promotions, etc.)

        # Base query with time filter
        query = f"(to:{email_address} OR from:{email_address}) after:{after}"

        # Only include unread emails unless include_read is True
        if not include_read:
            query += " is:unread"
        else:
            logger.info("Including read emails in search")

        # Log the final query for debugging
        logger.info(f"Office365 search query: {query}")

        # Additional filter options (commented out by default)
        # If you want to include emails from specific categories, use:
        # query += " category:(primary OR updates OR promotions)"

        # Retrieve all matching messages (handling pagination)
        logger.info(
            f"Fetching emails for {email_address} from last {minutes_since} minutes"
        )

        mailbox = service.mailbox()
        max_results: int = 10
        query = mailbox.q().search(query)
        messages = mailbox.get_messages(limit=max_results)

        # Process each message
        count = 0
        for message in messages:
            try:
                # Get full message details
                thread_id = message.conversation_id

                # Get thread details to determine conversation context
                # Directly fetch the complete thread without any format restriction
                # This matches the exact approach in the test code that successfully gets all messages
                thread = mailbox.get_messages(
                    query=mailbox.q().equals("ConversationId", thread_id)
                )
                messages_in_thread = list(thread)
                logger.info(
                    f"Retrieved thread {thread_id} with {len(messages_in_thread)} messages"
                )

                # Sort messages by internalDate to ensure proper chronological ordering
                # This ensures we correctly identify the latest message
                if all(msg.modified for msg in messages_in_thread):
                    messages_in_thread.sort(key=lambda m: m.modified)
                    logger.info(
                        f"Sorted {len(messages_in_thread)} messages by internalDate"
                    )
                else:
                    # Fallback to ID-based sorting if internalDate is missing
                    messages_in_thread.sort(key=lambda m: m.object_id)
                    logger.info(
                        f"Sorted {len(messages_in_thread)} messages by ID (internalDate missing)"
                    )

                # Log details about the messages in the thread for debugging
                for idx, msg in enumerate(messages_in_thread):
                    subject = msg.subject
                    from_email = str(msg.sender)
                    date = msg.modified
                    logger.info(
                        f"  Message {idx + 1}/{len(messages_in_thread)}: ID={msg.object_id}, Date={date}, From={from_email}"
                    )

                # Log thread information for debugging
                logger.info(
                    f"Thread {thread_id} has {len(messages_in_thread)} messages"
                )

                # Analyze the last message in the thread to determine if we need to process it
                last_message = messages_in_thread[-1]
                last_from_email = str(last_message.sender)

                # If the last message was sent by the user, mark this as a user response
                # and don't process it further (assistant doesn't need to respond to user's own emails)
                if email_address == last_from_email.address:
                    yield {
                        "id": message.object_id,
                        "thread_id": message.conversation_id,
                        "user_respond": True,
                    }
                    continue

                # Check if this is a message we should process
                is_from_user = email_address == last_from_email.address
                is_latest_in_thread = message.object_id == last_message.object_id

                # Modified logic for skip_filters:
                # 1. When skip_filters is True, process all messages regardless of position in thread
                # 2. When skip_filters is False, only process if it's not from user AND is latest in thread
                should_process = skip_filters or (
                    not is_from_user and is_latest_in_thread
                )

                if not should_process:
                    if is_from_user:
                        logger.debug(
                            f"Skipping message {message.object_id}: sent by the user"
                        )
                    elif not is_latest_in_thread:
                        logger.debug(
                            f"Skipping message {message.object_id}: not the latest in thread"
                        )

                # Process the message if it passes our filters (or if filters are skipped)
                if should_process:
                    # Log detailed information about this message
                    logger.info(
                        f"Processing message {message.object_id} from thread {thread_id}"
                    )
                    logger.info(f"  Is latest in thread: {is_latest_in_thread}")
                    logger.info(f"  Skip filters enabled: {skip_filters}")

                    # If the user wants to process the latest message in the thread,
                    # use the last_message from the thread API call instead of the original message
                    # that matched the search query
                    if not skip_filters:
                        # Use original message if skip_filters is False
                        process_message = message
                    else:
                        # Use the latest message in the thread if skip_filters is True
                        process_message = last_message
                        logger.info(
                            f"Using latest message in thread: {process_message['id']}"
                        )

                    # Extract email metadata from headers
                    subject = process_message.subject
                    from_email = str(process_message.sender)
                    _to_email = str(message.to._recipients[0])
                    # for recipient in message.to._recipients:
                    #     _to_email.append(str(recipient))

                    # Extract and parse email timestamp
                    send_time = process_message.modified

                    # Extract email body content
                    body = clean_body(message.body)

                    # Yield the processed email data
                    yield {
                        "from_email": from_email,
                        "to_email": _to_email,
                        "subject": subject,
                        "page_content": body,
                        "id": process_message["id"],
                        "thread_id": process_message["threadId"],
                        "send_time": send_time,
                    }
                    count += 1

            except Exception as e:
                logger.warning(f"Failed to process message {message['id']}: {str(e)}")

        logger.info(
            f"Found {count} emails to process out of {len(messages)} total messages."
        )

    except Exception as e:
        logger.error(f"Error accessing Gmail API: {str(e)}")
        # Fall back to mock implementation
        mock_email = {
            "from_email": "sender@example.com",
            "to_email": email_address,
            "subject": "Sample Email Subject",
            "page_content": "This is a sample email body for testing the email assistant.",
            "id": "mock-email-id-123",
            "thread_id": "mock-thread-id-123",
            "send_time": datetime.now().isoformat(),
        }

        yield mock_email


class FetchEmailsInput(BaseModel):
    """
    Input schema for the fetch_emails_tool.
    """

    email_address: str = Field(description="Email address to fetch emails for")
    minutes_since: int = Field(
        default=30, description="Only retrieve emails newer than this many minutes"
    )


@tool(args_schema=FetchEmailsInput)
def fetch_emails_tool(email_address: str, minutes_since: int = 30) -> str:
    """
    Fetches recent emails from Gmail for the specified email address.

    Args:
        email_address: Email address to fetch messages for
        minutes_since: Only retrieve emails newer than this many minutes (default: 30)

    Returns:
        String summary of fetched emails
    """
    emails = list(fetch_group_emails(email_address, minutes_since))

    if not emails:
        return "No new emails found."

    result = f"Found {len(emails)} new emails:\n\n"

    for i, email in enumerate(emails, 1):
        if email.get("user_respond", False):
            result += f"{i}. You already responded to this email (Thread ID: {email['thread_id']})\n\n"
            continue

        result += f"{i}. From: {email['from_email']}\n"
        result += f"   To: {email['to_email']}\n"
        result += f"   Subject: {email['subject']}\n"
        result += f"   Time: {email['send_time']}\n"
        result += f"   ID: {email['id']}\n"
        result += f"   Thread ID: {email['thread_id']}\n"
        result += f"   Content: {email['page_content'][:200]}...\n\n"

    return result


if __name__ == "__main__":
    fetch_emails_tool("scliu.leo@outlook.com")
