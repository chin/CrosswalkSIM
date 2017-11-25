#when an auto enters
#spawn next auto (peds arrivals spawn ped arrivals)
#spawn its own exit event

from classes import stats as st

class auto:
    def __init__(self, arrivalTime, velocity, id):
    	self.arrivalTime = arrivalTime
    	self.velocity = velocity		#randomly decided speed
    	self.id = id					#ID number/index, determined when auto spawns. Eastbound even, Westbound odd

    def __str__(self):
        return "Auto: arrival time %s velocity %s id %s" %(self.arrivalTime,self.velocity,self.id)

    def exit_time_if_no_delay(self):
        S = 46 #street = 46 ft
        B = 330 #block = 330 ft
        
        dist = 7*B + 6*S
        time = dist/self.velocity
        exitTime = self.arrivalTime + time
        return exitTime
    
    def calculate_auto_delay(self, yellow_begins_time):
        print("Calculating delay")
        
        #DON'T FORGET: sum variance and means using welford's eq
        
        #determine if particular auto is delayed
    	#triggered on the YELLOW traffic signal in safety_signals class. 
        
        delay = None
        auto_length = 9 #9ft length of auto
        yellow_duration = 8 #8 sec yellow
        red_duration = 18 #18 sec red light
        
        B = 330
        S= 46
        crosswalk_width = 24
        sim_total_dist = 7*B + 6*S
        middle_of_crosswalk = sim_total_dist/2
        
        #Near end is to the left. The left side of simulation is distance/length 0
        #with increasing numbers towards the right
        crosswalk_far_end = middle_of_crosswalk + crosswalk_width/2
        crosswalk_near_end = middle_of_crosswalk - crosswalk_width/2
        
        #start at zero
        #travel happens starting at arrival time
        travel_time_before_yellow = yellow_begins_time - self.arrivalTime
        
        back_end_dist_yellow_ends = self.velocity * (travel_time_before_yellow + yellow_duration) - auto_length
        front_end_dist_red_ends = self.velocity * (travel_time_before_yellow + yellow_duration + red_duration)
        

        #Find two conditions:
        #Its back end will be past the farthest edge of the crosswalk in YELLOW seconds.
        #Its front end will have not reached the near edge of the crosswalk in (YELLOW + RED) seconds. 
        #If both of these conditions are false, the auto will be delayed; otherwise the auto is not delayed at the crosswalk.
      
        got_across_before_red = True
        arrived_after_light_green = True
                
        if (back_end_dist_yellow_ends < crosswalk_far_end): 
            got_across_before_red = False
        if (front_end_dist_red_ends > crosswalk_near_end):
            arrived_after_light_green = False

        if (not got_across_before_red and not arrived_after_light_green):
            delay = 0
            st.stats.track_statistics(delay, 'auto delay')
            return delay #not delayed
        
        #If the car is delayed, you have to calculate by how much
    
        vj = self.velocity
        a = 10 #ft/s/s acceleration
        bj = vj^2 / (2*a)
        tj = vj/a
        ej = self.arrivalTime
        w = 24 #ft wide crosswalk
        
        halt_at_crosswalk_time = ej + (7/2*B + 3*S - w/2 - bj)/vj + tj
        light_turns_green_time = yellow_begins_time + yellow_duration + red_duration
        
        time_at_full_speed = (7*B + 6*S - 2*bj) /vj
        time_changing_speed = 2*tj
        time_stopped = light_turns_green_time - halt_at_crosswalk_time
        
        total_time_if_delay = time_at_full_speed + time_changing_speed + time_stopped
        exit_time_if_delay = self.arrivalTime + total_time_if_delay
        
        delay = exit_time_if_delay - self.exit_time_if_no_delay()
        st.stats.track_statistics(delay, 'auto delay')
        return delay
        


        #If doing it with a list of red lights
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
        