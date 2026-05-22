from enum import Enum

class UserRole(Enum):
    driver = "driver"
    admin = "admin"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]