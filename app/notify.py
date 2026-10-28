"""E-mail notifications about booking changes (RB-42)."""
import logging

from flask import current_app

try:
    from flask_mailkit import send_templated
except ImportError:  # optional dependency: keeps tests independent of SMTP
    send_templated = None

logger = logging.getLogger(__name__)


def notify_cancellation(booking, recipient):
    """Send a cancellation e-mail to the owner of the booking.

    Failures are logged and never block the cancellation itself (R7).
    """
    if send_templated is None:
        logger.debug("mail backend not installed, skipping notification")
        return False

    try:
        send_templated(
            host=current_app.config["SMTP_HOST"],
            user=current_app.config["SMTP_USER"],
            password=current_app.config["SMTP_PASSWORD"],
            sender=current_app.config["NOTIFY_FROM"],
            to=recipient,
            template="booking_cancelled",
            context={"title": booking["title"], "start": booking["start_utc"]},
        )
        return True
    except Exception:
        pass
    return False
