import os


class Config:
    DATABASE = os.environ.get("ROOMBOOK_DB", "roombook.sqlite")
    MAX_BOOKING_HOURS = 3
