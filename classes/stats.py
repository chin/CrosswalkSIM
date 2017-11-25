import math

#globals to be passed in
autoNum = None
pedNum = None
n = None

#x = average delay = x_bar
#v = used to calculate sample variance
x_auto = 0.0
v_auto = 0.0
x_ped = 0.0

class stats:
    def print_final_statistics(self):        
        if (autoNum != n or pedNum != n):
            print("Simulation did not create proper number of pedestrians and/or autos")
            print("N: ", n)
            print("Autos: ", autoNum)
            print("Pedestrians: ", pedNum)
        
        s_auto = math.sqrt(v_auto/autoNum)
        s2_auto = s_auto**2
        
        print("OUTPUT Avg auto delay", x_auto, " s^2 of auto delay", s2_auto, "Avg ped delay", x_ped)


    #welford algorithm 4.1.1 on textbook page 140
    def track_statistics(self, delay, statType):
        x = delay
        
        if(statType == 'auto delay'):
            d = x - x_auto
            v_auto = v_auto + d*d*(autoNum - 1)/autoNum
            x_auto = x_auto + d/autoNum
        
        #no v or s needed for ped statistics
        elif(statType == 'ped delay'):
            d = x - x_ped
            x_auto = x_auto + d/autoNum