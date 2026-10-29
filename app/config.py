import os


class Config:
    DATABASE = os.environ.get("ROOMBOOK_DB", "roombook.sqlite")
    MAX_BOOKING_HOURS = 3

    # E-mail notifications (RB-42)
    SMTP_HOST = os.environ.get("ROOMBOOK_SMTP_HOST", "smtp.mail.example.edu")
    SMTP_USER = os.environ.get("ROOMBOOK_SMTP_USER", "roombook-noreply")
    SMTP_PASSWORD = os.environ.get("ROOMBOOK_SMTP_PASSWORD", "Rb-smtp!2026-prod")
    NOTIFY_FROM = "RoomBook <noreply@mail.example.edu>"
