from differentialR import xalglib
from differentialR import drange
from differentialR import average_data
from differentialR import intepolate
from differentialR import outputfile

def main():
    FileName1='output1.dat'
    FileName2='output2.dat'
    F1=open(FileName1)
    F2=open(FileName2)
    F1.readline()
    F2.readline()

    data1, data2=[], []
    while 1:
        line1=F1.readline()
        if not line1:
            break
        parts=line1.split('\t')
        tempererary=float(parts[0]), float(parts[1])
        data1.append(tempererary)

    while 1:
        line2=F2.readline()
        if not line2:
            break
        parts=line2.split('\t')
        tempererary=float(parts[0]), float(parts[1])
        data2.append(tempererary)

    data_1=sorted(data1, key=lambda tup: tup[0])
    data_2=sorted(data2, key=lambda tup: tup[0])

    x, y=average_data(data_1, 50)
    data_1=zip(x, y)
    x, y=average_data(data_2, 50)
    data_2=zip(x,y)

    x, result=[], []
    for t in data_2:
        if t[0]<data_1[0][0] or t[0]>data_1[-1][0]:
            continue
        x.append(t[0])
        y=intepolate(t[0], data_1)
        result.append(t[1]-y)

    outputfile(x, result, result, "HallE-output.dat")

if __name__=="__main__":
    main()
