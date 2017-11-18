
from classes import event

from enum import Enum


#instead of storing walk light and traffic signal value
#track the states of that state diagram
#bottom is minGreenLight reqGreenLight, minGreenLightTime
#right is reqGreenLightWITHBUTTON, yellowOnExpire
#middle is "buttonReady" triggerImmediatelyOnButtonPress, yellowOnPress


#                 READ!
#----------------------------------------------------------!!!!-----------------------------------------------------
#-------------Keith basically told me how to do this
#-------------he said don't use the below ones, we want to have
#-------------an enum for every possible state in the state machine picture
#-------------separate ones will be a big problem for us!!


#GET RID OF THESE:


#class crosswalksignal(Enum):
#    NO_WALK = 0
#    WALK = 1

#class trafficlight(Enum):
#    RED = 0
#    YELLOW = 1
#    GREEN = 2


#WE WANT:

class crosswalksignal(Enum):
    RED_WALK = 0
    YELLOW_NO_WALK = 1 
    GREEN_MANDATORY_PERIOD = 2
    GREEN_GO_YELLOW_ON_TIMER = 3
    GREEN_GO_YELLOW_ON_PRESS = 4

class safety_signals:
    def __init__(self, crosswalk_signal, traffic_signal, timer):
        self.crosswalk_signal = crosswalksignal(crosswalk_signal) #WALK || NO_WALK
        self.traffic_signal = trafficsignal(traffic_light) #RED || YELLOW || GREEN

    #definitions for functions changing the safety signals
    def button_press(self):
        if self.traffic_signal is trafficlight.GREEN:
            pass
            #if green timer expired
                #yellow_begins(self)
            #else
                #green timer decrementing so in rightmost blue state
        if self.traffic_signal is trafficlight.YELLOW:
            #trigger yellow timer = 8s
            pass

        if self.traffic_signal is trafficlight.RED:
            #if red timer not expired do nothing
            pass

        return self


    def ped_at_button(self):
        if self.traffic_signal is trafficlight.RED:
            pass
            #walk
        else:
            button_press(self)

    def yellow_begins(self):
        self.traffic_signal = trafficlight.YELLOW
        #yellow timer = 8s

        #this is when you calculate auto delay
        #TODO is this right?
        #-----------------------------------------------------??
        for a in auto_list:
            calculate_auto_delay

        return self

    def yellow_expires(self):
        self.crosswalk_signal = crosswalksignal.WALK
        self.traffic_signal = trafficlight.RED

    def red_expires(self):
        self.crosswalk_signal = crosswalksignal.NO_WALK
        self.traffic_signal = trafficlight.GREEN
        green_begins(self)
        return self

    def red_begins(self):
        self.crosswalk_signal = crosswalksignal.WALK
        # red timer = 18s: pedestians can walk
        return self

    def green_begins(self):
        self.traffic_signal = trafficlight.GREEN
        #green timer = 35s
        return self

    def green_expires(self):
        return self

   


