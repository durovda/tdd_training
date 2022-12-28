from enum import Enum, auto


class CommandType (Enum):
    STOP = 1
    STATUS_UP = 2
    STATUS_DOWN = 3
    DISCHARGE = 4
    GET_STATUS = 5
    CALCULATE_STATISTICS = 6
    UNKNOWN = 7
