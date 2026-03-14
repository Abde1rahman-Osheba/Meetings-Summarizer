from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEACTIVATED = "deactivated"
