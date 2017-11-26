import sys
import os
from enum import Enum
import math

#imported from SIM during initialization
autoTracefile = ""
pedTracefile = ""
buttonTracefile = ""

#local variables
lineInAutoTrace = 0
lineInPedTrace= 0
lineInButtonTrace = 0
rp = 3 #ped arrival rate in one direction
ra = 4 #auto arrival rate

    
class traceType(Enum):
    AUTO = 0
    PED = 1
    BUTTON = 2

class input:
    def getNextAutoInterarrival(self):
        u = self.input.readNextUniformInTrace(self, traceType.AUTO)
        u = float(u)
        return -2*ra*math.log(1.0 - u)
    
    def getNextPedInterarrival(self):
        u = self.input.readNextUniformInTrace(self,traceType.PED)
        u = float(u)
        return -2*rp*math.log(1.0 - u)
    
    #Uniform(25,35) 
    def getNextAutoSpeed(self):
        u = self.input.readNextUniformInTrace(self, traceType.AUTO)
        u = float(u)
        a = 25
        b = 35
        return a + u * (b - a)
        
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
        
        uniformRand = 0
        global autoTracefile
        global pedTracefile
        global buttonTracefile
        global lineInAutoTrace
        global lineInPedTrace
        global lineInButtonTrace
        
        if traceCurrent == traceType.AUTO:
            uniformRand = self.input.readFile(self, autoTracefile, lineInAutoTrace)
            lineInAutoTrace+= 1
        elif traceCurrent == traceType.PED:
            uniformRand = self.input.readFile(self, pedTracefile, lineInPedTrace)
            lineInPedTrace+= 1
        elif traceCurrent == traceType.BUTTON:
            uniformRand = self.input.readFile(self, buttonTracefile, lineInButtonTrace)
            lineInButtonTrace+= 1
        
        if (uniformRand == 0):
            print("Uniform value not returned")
            sys.exit(1)
        
        return uniformRand


    def readFile(self, filename, lineInFile):
        #filehandle = open(filename)
        #print(filehandle.read())
        #filehandle.close()
        
        relativeFilename = filename;
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(fileDir, filename)
        
        try:
            #i starts at 0
            with open(filename) as fp:
                for i, line in enumerate(fp):
                    if i == lineInFile:
                        #print(line)
                        break
            
            
            if len(line.strip()) == 0 :
                raise Exception('File ended prematurely:', relativeFilename)
            
            return line
    
        except IOError:
            print("Could not read file:", relativeFilename)
            sys.exit(1)
        except Exception as err:
            print(err.args[0], err.args[1])
            sys.exit(1)
        
        
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