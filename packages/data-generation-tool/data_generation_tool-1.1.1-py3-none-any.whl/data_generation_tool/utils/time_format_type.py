from enum import Enum


class TimeFormatType(Enum):
    HOUR_MIN_SEC_24 = "%H:%M:%S"
    HOUR_MIN_24 = "%H:%M"
    HOUR_24 = "%H"
    HOUR_MIN_SEC_12 = "%I:%M:%S %p"
    HOUR_MIN_12 = "%I:%M %p"
    HOUR_12 = "%I %p"
    MIN_SEC = "%M:%S"
    SEC_ONLY = "%S"
    HOUR_MIN_SEC_COMPACT = "%H%M%S"
    HOUR_MIN_COMPACT = "%H%M"
