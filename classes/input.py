import sys
import os
from enum import Enum
import math
from tkinter.constants import BUTT
from random import expovariate # exponenial(lamb)

#imported from SIM during initialization
autoTracefile = None
pedTracefile = None
buttonTracefile = None

#local variables
lineInAutoTrace = 0
lineInPedTrace= 0
lineInButtonTrace = 0
rp = 60/6 #ped arrival rate in both directions
ra = 60/8 #auto arrival rate

    
class traceType(Enum):
    AUTO = 0
    PED = 1
    BUTTON = 2

class input:
    def getNextAutoInterarrival(self):
        u = self.input.readNextUniformInTrace(self, traceType.AUTO)
        print("u: ", u)
        u = float(u)
        print("u: ", u)
        return -1*ra*math.log(1.0 - u)
    
    def getNextPedInterarrival(self):
        u = self.input.readNextUniformInTrace(self,traceType.PED)
        print("u: ", u)
        u = float(u)
        print("u: ", u)
        return -1*rp*math.log(1.0 - u)
    
    #Uniform(25,35) 
    def getNextAutoSpeed(self):
        u = self.input.readNextUniformInTrace(self, traceType.AUTO)
        u = float(u)
        a = 25
        b = 35
        mph = a + u * (b - a)
        #ftpersec = 1.46667*mph
        #return ftpersec
        return mph;
        
    #Uniform(2.6,4.1)
    def getNextPedSpeed(self):
        u = self.input.readNextUniformInTrace(self, traceType.PED)
        u = float(u)
        a = 2.6
        b = 4.1
        return a + u * (b - a)
    
    def getNext_ButtonTracefile_UniformRand(self):
        #TODO CONVERT TO PROBABILITY VALUE CORRECTLY
        #THIS WILL ALWAYS RETURN UNIFORM 0,1
        #YOU WILL NEED TO INTREPRET IT BASED ON STATE OF CROSSWALK
        u = self.input.readNextUniformInTrace(self, traceType.BUTTON)
        u = float(u)
        return u
    
    #DO NOT CALL THIS DIRECTLY
    #call using the above methods to get random values
    def readNextUniformInTrace(self, traceCurrent):
        if not isinstance(traceCurrent, traceType):
            raise TypeError('Must be a trace type enum type')
        
        uniformRand = ""
        global autoTracefile
        global pedTracefile
        global buttonTracefile
        global lineInAutoTrace
        global lineInPedTrace
        global lineInButtonTrace
        
        if traceCurrent == traceType.AUTO:
            uniformRand = self.input.readFile(self, autoTracefile)
            lineInAutoTrace+= 1
        elif traceCurrent == traceType.PED:
            uniformRand = self.input.readFile(self, pedTracefile)
            lineInPedTrace+= 1
        elif traceCurrent == traceType.BUTTON:
            uniformRand = self.input.readFile(self, buttonTracefile)
            lineInButtonTrace+= 1
        
        if (uniformRand == 0):
            print("Uniform value not returned")
            sys.exit(1)
        
        return uniformRand

    def closeFiles(self):
        autoTracefile.close()
        pedTracefile.close()
        buttonTracefile.close()
        print("Files closed")
        

    def readFile(self, filename):
        #filehandle = open(filename)
        #print(filehandle.read())
        #filehandle.close()
        
        #relativeFilename = filename;
        #fileDir = os.path.dirname(os.path.realpath('__file__'))
        #filename = os.path.join(fileDir, filename)
        
        line = filename.readline()
        
        if len(line.strip()) == 0 :
            raise Exception('File ended prematurely:', filename)

            
        return line
        
    def testRandomValues(self):
    
        numTests = 5
        
        print("Auto test")
        for i in range (0,numTests*2):
            if i % 2 == 0: #even 
                print('Interarrival', self.input.getNextAutoInterarrival(self), end='  ')
            else: #odd
                print('Speed', self.input.getNextAutoSpeed(self))
    
        print("\nPed test")
        for i in range (0,numTests*2):
            if i % 2 == 0: #even 
                print('Interarrival', self.input.getNextPedInterarrival(self), end='  '),
            else: #odd
                print('Speed', self.input.getNextPedSpeed(self))
    
        print("\nUniform button press values")
        for i in range (0,numTests):
            print(self.input.getNext_ButtonTracefile_UniformRand(self))
            
        print("\nReturning to beginning of input files.\n\n")
        
        #Refresh bookmarks
        global lineInAutoTrace
        global lineInPedTrace
        global lineInButtonTrace
        lineInAutoTrace  =0
        lineInPedTrace   =0
        lineInButtonTrace=0
