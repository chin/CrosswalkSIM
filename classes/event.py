

from enum import Enum
try:
    import Queue as Q
except ImportError:
    import queue as Q

class event_list:
    def __init__(self):
        self.event_list = Q.PriorityQueue 

    def gets(self):
        self.event_list.get()

    def puts(self, x):
        self.event_list.put(self, x)

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
    def __init__(self, event_time, event_type, id):
        #event types are AUTO_ARRIVAL, PED_ARRIVAL, PED_AT_BUTTON, PED_IMPATIENT, GREEN_EXPIRES, YELLOW_EXPIRES, RED_EXPIRES, AUTO_EXIT, PED_EXIT
        self.time = event_time
        self.type = event_type
        self.id = id #the ID of the auto if AUTO_ARRIVAL/EXIT, or of ped if PED event

    #custom comparator to queue in priority q based on event time
    def __lt__(self, other):
        return self.time < other.time
    
    """
    def __cmp__(self, other):
        return self.cmp(self.time, other.time)
    
    def cmp(self, x, y):
        #http://portingguide.readthedocs.io/en/latest/comparisons.html
        
        #Replacement for built-in funciton cmp that was removed in Python 3
    
        #Compare the two objects x and y and return an integer according to
        #the outcome. The return value is negative if x < y, zero if x == y
        #and strictly positive if x > y.
    
        return (x > y) - (x < y)
    """
