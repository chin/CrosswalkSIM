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
pedNum = None
t = None
event_list = None
ped_list = None
waiting_peds = None

class crosswalksignal(Enum):
    RED_WALK = 0
    YELLOW_NO_WALK = 1 
    GREEN_MANDATORY_PERIOD = 2
    GREEN_GO_YELLOW_ON_TIMER = 3
    GREEN_GO_YELLOW_ON_PRESS = 4

class safety_signals:
     #might not be used
    def __init__(self):
        self.safety_signals.safetySignal = crosswalksignal.GREEN_GO_YELLOW_ON_PRESS
        self.red_timer = 0

    def __str__(self):
        return "Signal: enum %s" %(self.safety_signals.safetySignal)

    def change_signal(self, signal):
        self.safety_signals.safetySignal = signal
       
    #definitions for functions changing the safety signals
    def button_press(self, request_pushed):
        if self.safety_signals.safetySignal is crosswalksignal.GREEN_GO_YELLOW_ON_PRESS:
            if request_pushed:
                self.safety_signals.yellow_begins(self)
            
        elif self.safety_signals.safetySignal is crosswalksignal.GREEN_GO_YELLOW_ON_TIMER:
            self.safety_signals.yellow_begins(self)
        
        elif self.safety_signals.safetySignal is crosswalksignal.YELLOW_NO_WALK:
            pass

        elif self.safety_signals.safetySignal is crosswalksignal.RED_WALK:
            pass
        #return self

    def ped_at_button( self ):
        for peds in ped_list:
            if peds.ped_at_button( t ):
                waiting_peds.put(peds)
                ped_list.remove(peds)
                #remove from orriginal list?
        wrp = self.safety_signals.walk_request_pushed( self, waiting_peds.qsize() ) #signal in no_walk state
        self.safety_signals.button_press(self, wrp)
        if self.safety_signals.safetySignal != crosswalksignal.YELLOW_NO_WALK:
            event_list.put( e.event( t + 60, e.event_type.PED_IMPATIENT, peds.id ) )
        if self.safety_signals.safetySignal != crosswalksignal.RED_WALK:
            peds = waiting_peds.get(-1)
            if peds.can_cross( self.safety_signals.red_timer - t ):
                event_list.put( e.event(t + peds.exit_time(), e.event_type.PED_EXIT, peds.id ) )
            else:
                waiting_peds.put(peds)

    
                    
    def ped_impatient(self):
        wrp = self.safety_signals.walk_request_pushed( self, waiting_peds.qsize()  )
        self.safety_signals.button_press(self, wrp)
        #return self

    def yellow_begins(self):
        self.safety_signals.safetySignal = crosswalksignal.YELLOW_NO_WALK
        event_list.put( e.event( t + 8, e.event_type.YELLOW_EXPIRES, waiting_peds.qsize() ) )#yellow timer = 8s
        #return self

    def yellow_expires(self):
        self.safety_signals.red_begins(self)
        #return self

    def red_expires(self):
        self.safety_signals.green_begins(self)
        #return self

    def red_begins(self):
        self.safety_signals.red_timer = t + 18
        print("t is", t, "red timer is ", self.safety_signals.red_timer)
        self.safety_signals.safetySignal = crosswalksignal.RED_WALK
        event_list.put( e.event( t + 18, e.event_type.RED_EXPIRES, waiting_peds.qsize()  ) )#red timer = 18s: pedestians can walk
        m = 1
        while waiting_peds.qsize() >0 and m <= 20:
            peds = waiting_peds.get()
            event_list.put( e.event(t + peds.exit_time(), e.event_type.PED_EXIT, peds.id ) )
            m += 1

    def green_begins(self):
        self.safety_signals.safetySignal = crosswalksignal.GREEN_MANDATORY_PERIOD
        event_list.put( e.event( t + 35, e.event_type.GREEN_EXPIRES, waiting_peds.qsize()  ) )#green timer = 35s
        #return self

    def green_expires(self):
        if self.safety_signals.safetySignal is crosswalksignal.GREEN_MANDATORY_PERIOD:
            self.safety_signals.safetySignal = crosswalksignal.GREEN_GO_YELLOW_ON_PRESS
        elif self.safety_signals.safetySignal is crosswalksignal.GREEN_GO_YELLOW_ON_TIMER:
            pass
        #return self

    def walk_request_pushed(self, n):
        u = i.input.getNext_ButtonTracefile_UniformRand(i) #def from SIM file
        num = n
        prob = button_prob(self, num)
        if u < prob:
            return True
        else:
            return False

    def get_ped(self, ped):
        return ( p.ped.button/ped.velocity)
    
def button_prob( self, n):
    if n is 0:
        return (15/16)
    else:
        return (1/n+1)
