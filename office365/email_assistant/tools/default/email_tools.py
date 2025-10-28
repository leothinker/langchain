from typing import Literal

from langchain_core.tools import tool
from pydantic import BaseModel


@tool
def write_email(to: str, subject: str, content: str) -> str:
    """Write and send an email."""
    # Placeholder response - in real app would send email
    return f"Email sent to {to} with subject '{subject}' and content: {content}"


@tool
class Done(BaseModel):
    """E-mail has been sent."""

    done: bool


@tool
class Question(BaseModel):
    """Question to ask user."""

    content: str
