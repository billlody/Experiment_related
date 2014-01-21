import xalglib
from differentialR import outputfile

def main():
    FileName1='TEST.txt'
    F1=open(FileName1)

    Field1, Voltage1=[], []
    Field2, Voltage2=[], []

    while 1:
        line=F1.readline()
        if not line:
            break
        parts=line.split('\t')
        if float(parts[0])>0:
            Field1.append(float(parts[0]))
            Voltage1.append(float(parts[1]))
        else:
            Field2.append(-float(parts[0]))
            Voltage2.append(float(parts[1]))

    FileName2='output1.dat'
    FileName3='output2.dat'
    outputfile(Field1, Voltage1, Voltage1, FileName2)
    outputfile(Field2, Voltage2, Voltage2, FileName3)

if __name__=="__main__":
    main()
