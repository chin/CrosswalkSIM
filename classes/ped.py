
class ped:
    B = 330
    S = 46
    w = 24
    dist = B + S + w

    def __init__(self, arrivalTime, velocity, id):
        self.arrivalTime = arrivalTime
        self.velocity = velocity        #randomly decided speed
        self.id = id                    #ID number/index, determined when ped spawns. Eastbound even, Westbound odd


    def calculate_ped_delay(self, exiTime):
        time = exitTime - self.arrivalTime
        minTime = dist/self.velocity
        D_p = time - minTime
        return D_p 
        
    def exit_time_if_no_delay(self):
        time = dist/self.velocity
        exitTime = self.arrivalTime + time
        return exitTime

    
