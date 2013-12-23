import xalglib
import math
import os.path    

def find_value(Tinitial, volt, s):
    if volt<0 and Tinitial < 0 and Tinitial > 350:
        raise Exception('Check','Value')
    start=xalglib.spline1dintegrate(s, Tinitial)
    diffT=1
    final=xalglib.spline1dintegrate(s, Tinitial+diffT)
    diffV=final-start
    while math.fabs(diffV-volt)>0.0001:
        if diffV>volt:
            diffT=diffT / 2
        else:
            diffT=diffT * 1.5
        final=xalglib.spline1dintegrate(s, Tinitial+diffT)
        diffV=final-start
    return diffT

def read_data(T, V, s):
    factor=100
    result=[]
    for i in range(len(T)):
        Volt=float(V[i])*1000000/factor
        result.append(find_value(float(T[i]), Volt, s))
    return T, result

def read_thermalC():
    Temperature, mVolt=[],[]
    try:
        F=open('Sensitivity AuFe-Chromel Thermocouple.dat')
        while 1:
            line=F.readline()
            if not line:
                break
            parts=line.split(' ')
            Temperature.append(parts[0])
            mVolt.append(parts[1])
    finally:
        F.close()
    return Temperature, mVolt

def main():
    F=open('1stP-1stThermocouple-0.2v-912.4Hz-HeatC(normal).dat')
    for i in range(7):
        line=F.readline()

    T, CVolt = [], []

    while 1:
        line=F.readline()
        if not line:
            break
        parts=line.split(' ')
        T.append(parts[3])
        CVolt.append(parts[5])

    Temperature, uVolt=read_thermalC()  
    s = xalglib.spline1dbuildlinear(Temperature, uVolt)

    print(str(len(T))+" data input")

    Temp, diffT=read_data(T, CVolt, s)
    # output to a file
    Fname=F.name[:-4]
    Fname=Fname+"(output).dat"
    Foutput=open(Fname, 'w')
    Foutput.write('Temperature') 
    Foutput.write('\t')
    Foutput.write('DeltaTemperature')
    Foutput.write('\t')
    Foutput.write('HeatCapacity')
    Foutput.write('\n')
    for i in range(len(Temp)):
        Foutput.write(str(Temp[i]))
        Foutput.write('\t')
        Foutput.write(str(diffT[i]))
        Foutput.write('\t')
        Foutput.write(str(1/diffT[i]))
        Foutput.write('\n')
        
if __name__ =="__main__":
    main()
