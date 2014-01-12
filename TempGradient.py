from differentialR import xalglib
from differentialR import drange
from differentialR import outputfile

def main():
    FileName1='1stP-0.7V-5.516Hz-1ndTCouple-ThermalE(output).dat'
    FileName2='1stP-0.7V-5.516Hz-2ndTCouple-ThermalE(output).dat'
    F1=open(FileName1)
    F2=open(FileName2)
    F1.readline()
    F2.readline()

    T1, dT1=[], []
    while 1:
        line1=F1.readline()
        if not line1:
            break
        parts=line1.split('\t')
        T1.append(float(parts[0]))
        dT1.append(float(parts[1]))

    T2, dT2=[], []
    while 1:
        line2=F2.readline()
        if not line2:
            break
        parts=line2.split('\t')
        T2.append(float(parts[0]))
        dT2.append(float(parts[1]))

    p1=xalglib.polynomialfit(T1, dT1, 9)
    p2=xalglib.polynomialfit(T2, dT2, 9)
    T_low=max(min(T1), min(T2))
    T_high=min(max(T1), max(T2))
    Temperature=drange(T_low, T_high, 0.1)

    result=[]
    for i in range(len(Temperature)):
        v=xalglib.barycentriccalc(p1[1], Temperature[i])-xalglib.barycentriccalc(p2[1], Temperature[i])
        result.append(v)

    outputfile(Temperature, result, result, FileName1[:17]+"(output).dat")

if __name__=="__main__":
    main()
