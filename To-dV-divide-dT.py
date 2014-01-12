import xalglib
from differentialR import drange
from differentialR import outputfile

def main():
    FileName1='1stP-0.7V-5.516Hz(output).dat'
    FileName2='1stP-0.7V-5.516Hz-VoltageDiff-ThermalE.dat'
    F1=open(FileName1)
    F2=open(FileName2)
    F1.readline()
    for i in range(7):
        F2.readline()

    T1, dT=[], []
    while 1:
        line1=F1.readline()
        if not line1:
            break
        parts=line1.split('\t')
        T1.append(float(parts[0]))
        dT.append(float(parts[1]))

    T2, dV=[], []
    while 1:
        line2=F2.readline()
        if not line2:
            break
        parts=line2.split(' ')
        T2.append(float(parts[3]))
        dV.append(float(parts[8]))

    p1=xalglib.polynomialfit(T1, dT, 9)
    p2=xalglib.polynomialfit(T2, dV, 9)

    T_low=max(min(T1), min(T2))
    T_high=min(max(T1), max(T2))
    Temperature=drange(T_low, T_high, 0.1)

    result=[]
    for i in range(len(Temperature)):
        v=xalglib.barycentriccalc(p2[1], Temperature[i]) / xalglib.barycentriccalc(p1[1], Temperature[i])
        result.append(v)

    outputfile(Temperature, result, result, FileName1[:17]+"(dv-dt)(output).dat")


if __name__=="__main__":
    main()
