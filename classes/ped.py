from classes import stats as st

class ped:
    B = 330
    S = 46
    w = 24
    dist = B + S + w

    def __init__(self, arrivalTime, velocity, id):
        self.arrivalTime = arrivalTime
        self.velocity = velocity        #randomly decided speed
        self.id = id                    #ID number/index, determined when ped spawns. Eastbound even, Westbound odd


    def calculate_ped_delay(self, exitTime):
        time = exitTime - self.arrivalTime
        minTime = self.dist/self.velocity
        D_p = time - minTime
        st.stats.track_statistics(D_p, 'ped delay')
        return D_p 
        
    def exit_time_if_no_delay(self):
        time = self.dist/self.velocity
        exitTime = self.arrivalTime + time
        return exitTime
    
    def can_cross(self):
        return (( self.w/self.velocity ) >= 0 )

    def exit_time(self):
        retrun ( self.w/self.velocity )
