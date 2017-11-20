
from classes import event
from enum import Enum
global event_list
global pedNum

#instead of storing walk light and traffic signal value
#track the states of that state diagram
#bottom is minGreenLight reqGreenLight, minGreenLightTime
#right is reqGreenLightWITHBUTTON, yellowOnExpire
#middle is "buttonReady" triggerImmediatelyOnButtonPress, yellowOnPress


class crosswalksignal(Enum):
    RED_WALK = 0
    YELLOW_NO_WALK = 1 
    GREEN_MANDATORY_PERIOD = 2
    GREEN_GO_YELLOW_ON_TIMER = 3
    GREEN_GO_YELLOW_ON_PRESS = 4

class safety_signals:
    def __init__(self, signal):
        self.safetySignal = crosswalksignal.GREEN_MANDATORY_PERIOD

    def change_signal( self, signal ):
        self.safetySignal = signal
       
    #definitions for functions changing the safety signals
    def button_press(self):
        if self.safetySignal is crosswalksignal.GREEN_GO_YELLOW_ON_PRESS:
            yellow_begins(self)
        
        elif self.safetySignal is crosswalksignal.GREEN_YELLOW_ON_TIMER:
            yellow_begins(self)
        
        elif self.safetySignal is crosswalksignal.YELLOW_NO WALK:
            pass

        elif self.safetySignal is crosswalksignal.RED_WALK:
            pass

        return self


    def ped_at_button(self):
        if self.safetySignal is crosswalksignal.RED_WALK:
            pass
            # check if can walk
        else:
            button_press(self)

    def yellow_begins(self):
        self.safetySignal = crosswalksignal.YELLOW_NO_WALK
        event_list.put( event( t + 8, event.event_type.YELLOW_EXPIRES, pedNum) )#yellow timer = 8s

        #this is when you calculate auto delay
        #TODO is this right?
        #-----------------------------------------------------??
        for a in auto_list:
            calculate_auto_delay

        return self

    def yellow_expires(self):
        red_begins(self)
        return self

    def red_expires(self):
        self.safetySignal = crosswalksignal.GREEN_MANDATORY_PERIOD
        green_begins(self)
        return self

    def red_begins(self):
        self.safetySignal = crosswalksignal.RED_WALK
        event_list.put( event( t + 18, event.event_type.RED_EXPIRES, pedNum ) )#red timer = 18s: pedestians can walk
        return self

    def green_begins(self):
        self.safetySignal = crosswalksignal.GREEN_MANDATORY_PERIOD
        event_list( event( t + 35, event.event_type.GREEN_EXPIRES, pedNum ) )#green timer = 35s
        return self

    def green_expires(self):
        if self.safetySignal is crosswalksignal.GREEN_MANDATORY_PERIOD:
            self.safetySignal = crosswalksignal.GREEN_GO_YELLOW_ON_PRESS
        elif self.safetySignal is crosswalksignal.GREEN_YELLOW_ON_TIMER:
            pass
        return self

   


