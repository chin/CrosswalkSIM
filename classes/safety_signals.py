from classes import event as e
from classes import ped as p
from enum import Enum
from classes import input as i

#instead of storing walk light and traffic signal value
#track the states of that state diagram
#bottom is minGreenLight reqGreenLight, minGreenLightTime
#right is reqGreenLightWITHBUTTON, yellowOnExpire
#middle is "buttonReady" triggerImmediatelyOnButtonPress, yellowOnPress

#The pointer to the global event_list
#will be passed in to this variable
#from SIM when it initializes
#event_list = None
#ped_list = None

#need to be able to use these
t = None
event_list = None
ped_list = None

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q

class crosswalksignal(Enum):
    RED_WALK = 0
    YELLOW_NO_WALK = 1 
    GREEN_MANDATORY_PERIOD = 2
    GREEN_GO_YELLOW_ON_TIMER = 3
    GREEN_GO_YELLOW_ON_PRESS = 4

class safety_signals:
     #might not be used
    def __init__(self):
        self.signal = crosswalksignal.GREEN_GO_YELLOW_ON_PRESS
        self.red_timer = 0
        self.m = 0
        self.waiting_peds =  Q.PriorityQueue()

    def __str__(self):
        return "Signal: enum %s" %(self.signal)

    def change_signal(self, signal):
        self.signal = signal
       
    #definitions for functions changing the safety signals
    def button_press(self, request_pushed):
        if self.signal is crosswalksignal.GREEN_GO_YELLOW_ON_PRESS:
            if request_pushed:
                self.yellow_begins()
        elif self.signal is crosswalksignal.GREEN_MANDATORY_PERIOD:
            if request_pushed:
                self.signal = crosswalksignal.GREEN_GO_YELLOW_ON_TIMER
        elif self.signal is crosswalksignal.GREEN_GO_YELLOW_ON_TIMER:
            pass
        
        elif self.signal is crosswalksignal.YELLOW_NO_WALK:
            pass

        elif self.signal is crosswalksignal.RED_WALK:
            pass
        #return self

    def ped_at_button( self, peds ):
        ped_list.remove(peds)
        if self.signal is crosswalksignal.RED_WALK:
            if peds.can_cross( self.red_timer - t ) and self.m <= 20:
                event_list.put( e.event(t + peds.exit_time(), e.event_type.PED_EXIT, peds.id, peds ) )
                self.m += 1
            else:
                self.waiting_peds.put(peds)  
        else:
            wrp = self.walk_request_pushed( self.waiting_peds.qsize() ) #signal in no_walk state
            self.button_press(wrp)
            event_list.put( e.event( t + 60, e.event_type.PED_IMPATIENT, peds.id ) )
            self.waiting_peds.put(peds)  
                    
    def ped_impatient(self):
        wrp = self.walk_request_pushed( self.waiting_peds.qsize()  )
        self.button_press(wrp)
        #return self

    def yellow_begins(self):
        self.signal = crosswalksignal.YELLOW_NO_WALK
        event_list.put( e.event( t + 8, e.event_type.YELLOW_EXPIRES, self.waiting_peds.qsize() ) )#yellow timer = 8s
        #return self

    def yellow_expires(self):
        self.red_begins()
        #return self

    def red_expires(self):
        self.green_begins()
        #return self

    def red_begins(self):
        #get rid of all the patient events in the event list
        i = 0
        while i in range(event_list.qsize()):
            ev = event_list.get(i)
            i += 1
            if ev.type is e.event_type.PED_IMPATIENT:
                pass
            else:
                event_list.put(ev)
        self.red_timer = t + 18
        print("t is", t, "red timer is ", self.red_timer, "queue is ", self.waiting_peds.qsize())
        self.signal = crosswalksignal.RED_WALK
        event_list.put( e.event( t + 18, e.event_type.RED_EXPIRES, self.waiting_peds.qsize()  ) )#red timer = 18s: pedestians can walk
        self.m = 1
        while self.waiting_peds.qsize() > 0 and self.m <= 20:
            peds = self.waiting_peds.get()
            event_list.put( e.event(t + peds.exit_time(), e.event_type.PED_EXIT, peds.id, peds ) )
            self.m += 1

    def green_begins(self):
        self.signal = crosswalksignal.GREEN_MANDATORY_PERIOD
        event_list.put( e.event( t + 35, e.event_type.GREEN_EXPIRES, self.waiting_peds.qsize()  ) )#green timer = 35s
        for i in range(self.waiting_peds.qsize()):
            wrp = self.walk_request_pushed( 0 )
            self.button_press(wrp)
        event_list.put( e.event( t + 60, e.event_type.PED_IMPATIENT, "multiple peds" ) ) 

    def green_expires(self):
        if self.signal is crosswalksignal.GREEN_MANDATORY_PERIOD:
            self.signal = crosswalksignal.GREEN_GO_YELLOW_ON_PRESS
        elif self.signal is crosswalksignal.GREEN_GO_YELLOW_ON_TIMER:
            self.yellow_begins()
        #return self

    def walk_request_pushed(self, n):
        u = i.input.getNext_ButtonTracefile_UniformRand(i) #def from SIM file
        num = n
        prob = button_prob(num)
        if u < prob:
            return True
        else:
            return False

    def get_ped(self, ped):
        return ( p.ped.button/ped.velocity)
    
def button_prob( n):
    if n is 0:
        return (15/16)
    else:
        return 1/(n+1)
