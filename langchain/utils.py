"""
    UTILITY FILE
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union, List
from random import randint

from jose import jwt
from sendgrid.helpers.mail import SendGridException
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.exception.base_exceptions import email_not_sent
from app import schemas
from app.core.configuration import settings


async def simple_send(
    email: schemas.EmailSchema,
    html_content: str,
    subject: str,
) -> Optional[str]:
    """
    Send Email
    """
    message = Mail(
        from_email=f"Fastapi Boilerplate <{settings.FROM_EMAIL}>",
        to_emails=email.dict().get("email"),
        subject=subject,
    )
    message.add_content(html_content, mime_type="text/html")
    try:
        send_grid = SendGridAPIClient(settings.SENDGRID_API_KEY)
        send_grid.send(message)
    except SendGridException as e:
        raise email_not_sent
