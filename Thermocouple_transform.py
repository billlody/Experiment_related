import xalglib
import math
import os.path
from differentialR import outputfile

class Thermocouple:
    def __init__(self):
        self.diffT=1.0
        self.Temperature=[]
        self.mVolt=[]
        self.s=None
    # calculate value of voltage difference
    def find_value(self, Tinitial, volt):
        if volt<0.0 or Tinitial < 0.0 or Tinitial > 350.0:
            raise Exception('Check','Value')
        start=xalglib.spline1dintegrate(self.s, Tinitial)
        self.diffT=1.0
        final=xalglib.spline1dintegrate(self.s, Tinitial+self.diffT)
        diffV=final-start
        while math.fabs(diffV-volt)>0.5:
            if diffV>volt:
                self.diffT=self.diffT / 2.0
            else:
                self.diffT=self.diffT * 1.5
            final=xalglib.spline1dintegrate(self.s, Tinitial+self.diffT)
            diffV=final-start
    # read data to Temperature and temperature difference
    def read_data(self, T, V):
        factor=1000
        result=[]
        for i in range(len(T)):
            Volt=float(V[i])*1000000/factor
            self.find_value(float(T[i]), Volt)
            result.append(self.diffT)
        return T, result
    # save thermalcouple data
    def read_thermalC(self):
        try:
            F1=open('Sensitivity AuFe-Chromel Thermocouple.DAT')
            while 1:
                line=F1.readline()
                if not line:
                    break
                parts=line.split(' ')
                self.Temperature.append(parts[0])
                self.mVolt.append(parts[1])
        finally:
            F1.close()
            self.s = xalglib.spline1dbuildlinear(self.Temperature, self.mVolt)

class FileData:
    def __init__(self, NFile):
        self.FileName=NFile
        self.F=open(self.FileName)
        self.splitp=' '
        self.Xoutput=[]
        self.Youtput=[]
        self.data=[()]
    def check(self):
        line=self.F.readline()
        if line[0]=='T':
            self.splitp='\t'
        else:
            for i in range(6):
                line=self.F.readline()
            self.splitp=' '        
    def input(self, Xn, Yn):
        self.check()
        while 1:
            line=self.F.readline()
            if not line:
                break
            parts=line.split(self.splitp)
            self.Xoutput.append(float(parts[Xn]))
            self.Youtput.append(float(parts[Yn])) 
        print(str(len(self.Xoutput)) + " data input")
    def output_list(self):
        return self.Xoutput, self.Youtput
    def output_tuple_l(self):
        self.data=zip(self.Xoutput, self.Youtput)
        return self.data

def main():
    FileName='NernstE-output-dT-2P.dat'
    Fobject=FileData(FileName)
    Fobject.input(0, 1)
    T, CVolt=Fobject.output_list()

    TC=Thermocouple()
    TC.read_thermalC()  
    print(str(len(T))+" data input")
    Temp, diffT=[], []
    Temp, diffT=TC.read_data(T, CVolt)
    # output to a file
    Fname=Fobject.FileName[:-4]
    Fname=Fname+"(test).dat"
    SpecificH=[1/x for x in diffT]
    outputfile(Temp, diffT, SpecificH, Fname, 'Temperature', 'DeltaTemperature', 'SpecificH')
        
if __name__ =="__main__":
    main()
