

from enum import Enum

class event_type(Enum):
    AUTO_ARRIVAL = 0
    PED_ARRIVAL = 1
    PED_AT_BUTTON = 2
    PED_IMPATIENT = 3
    GREEN_EXPIRES = 4
    YELLOW_EXPIRES = 5
    RED_EXPIRES = 6
    AUTO_EXIT = 7
    PED_EXIT = 8

class event:
    def __init__(self, arrival_time, event_type):
        #event types are AUTO_ARRIVAL, PED_ARRIVAL, PED_AT_BUTTON, PED_IMPATIENT, GREEN_EXPIRES, YELLOW_EXPIRES, RED_EXPIRES, AUTO_EXIT, PED_EXIT
        self.time = arrival_time
        self.type = event_type(event_type)

    