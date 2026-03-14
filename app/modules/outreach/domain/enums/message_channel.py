from enum import Enum


class MessageChannel(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
