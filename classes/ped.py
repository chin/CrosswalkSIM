from classes import stats as st

#variable instead of class
ped_list = []

class ped:
    B = 330
    S = 46
    w = 46
    dist = B + S + w
    button = B + S

    def __init__(self, arrivalTime, velocity, id):
        self.arrivalTime = arrivalTime
        self.velocity = velocity        #randomly decided speed
        self.id = id                    #ID number/index, determined when ped spawns. Eastbound even, Westbound odd

    def calculate_ped_delay(self, exitTime):
        minTime = self.exit_time_if_no_delay() #self.dist/self.velocity
        D_p = exitTime - minTime
        st.stats.track_statistics(st, D_p, 'ped delay')
        print("Ped delay: ped num - %s arrival %.2f exit %.2f min time %.2f delay %.2f" %(self.id, self.arrivalTime, exitTime, minTime, D_p))
        return D_p 
        
    def exit_time_if_no_delay(self):
        time = self.dist/self.velocity
        exitTime = self.arrivalTime + time
        return exitTime
    
    def can_cross(self, time_left):
        return ( time_left -( self.w/self.velocity ) >= 0 ) # need to compare to the time left in the light

    def exit_time(self):
        return ( self.w/self.velocity )

    def ped_at_button(self, sim_time):
        if ( self.arrivalTime +(self.button/self.velocity) ) <= sim_time:
            return True
        else:
            return False

    def __lt__(self, rhs):
        return (self.arrivalTime +(self.button/self.velocity)) < (rhs.arrivalTime +(rhs.button/rhs.velocity))