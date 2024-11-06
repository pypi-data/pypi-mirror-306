from enum import Enum


class ExitStrategy(Enum):
    # System-wide
    OUT_OF_DOMAIN = "OUT_OF_DOMAIN"
    EMPTY = ""
    ON_ERROR = "ON_ERROR"

    # Module-specific
    ORDER = "ORDER"
    ACCOUNT = "ACCOUNT"
    PROMOTIONS = "PROMOTIONS"
    MACHINE = "MACHINE"
