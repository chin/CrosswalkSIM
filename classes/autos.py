#when an auto enters
#spawn next auto (peds arrivals spawn ped arrivals)
#spawn its own exit event

class autos:
    def __init__(self, arrivalTime, velocity, id):
    	self.arrivalTime = arrivalTime
    	self.velocity = velocity		#randomly decided speed
    	self.id = id					#ID number/index, determined when auto spawns. Eastbound even, Westbound odd

    def calculate_auto_delay(self):
        pass
        #determine if particular auto is delayed
    	#triggered on the YELLOW traffic signal in safety_signals class. Find two conditions:
	    #Its back end will be past the farthest edge of the crosswalk in YELLOW seconds.
	    #Its front end will have not reached the near edge of the crosswalk in (YELLOW + RED) seconds. 
		#If both of these conditions are false, the auto will be delayed; otherwise the auto is not delayed at the crosswalk.
        
        #HOW TO ORCHESTRATE THIS LOGIC:
        #remember in a separate list all the times that a red light turns on (maybe also when it turns off)
        #yellow light does not matter in computations
        #pedestrians but not cars are delayed by yellow button
        #yellow button matters ONLY to pedestrians
        #pedestrian signal puts values in a list
        #when an auto exits calculate when it would have been in crosswalk
        #see if any of those overlap any of the times in the red light list (and then perform delay calc)
        
        #leaving  crosswalk time < red light begin time
        #entry time > green light begin time (red light turns off / red light time+ red light duration)
        #entry time after green light begins
        
        #calculate when they exit the simulation***
        #constant speed when do they enter crosswalk and when does back of car leave the crosswalk
        
        #cars that are not delayed are added under welford
        #autoexithandler will keep track of values at end
        #exit time will also be kept track of - simulation current time is precisely that
        