import xalglib
import math
import os.path    

# average data with 101
def average_data(data, num):
    initiallist=data[:(2*num+1)]
    l=[sum(x) for x in zip(*initiallist)]
    T=[l[0]/(2*num+1)]
    R=[l[1]/(2*num+1)]
    for i in range(len(data)-2*num-1):
        mark=i+num+1
        l[0]+=data[mark+num][0]-data[mark-num][0]
        l[1]+=data[mark+num][1]-data[mark-num][1]
        T.append(l[0]/(2*num+1))
        R.append(l[1]/(2*num+1))
    return T, R

def calc_factor(width, thickness, length):
    result=1000.0 * width * thickness / length
    return result    

def drange(start, stop, step):
    r=start
    result=[]
    while r<stop:
        result.append(r)
        r += step
    return result

# output file, temperature, resistivity, 1st order der, file name
def outputfile(x, y1, y2, Fname):
    Foutput=open(Fname, 'w')
    Foutput.write('Temperature') 
    Foutput.write('\t')
    Foutput.write('Resistivity(ohm * mm)')
    Foutput.write('\t')
    Foutput.write('1st order derivative')
    Foutput.write('\n')
    for i in range(len(x)):
        Foutput.write(str(x[i]))
        Foutput.write('\t')
        Foutput.write(str(y1[i]))
        Foutput.write('\t')
        Foutput.write(str(y2[i]))
        Foutput.write('\n')
    Foutput.close()

def main():
    F=open('1stP-1mA-7.32Hz-ResistivityF.dat')
    for i in range(7):
        line=F.readline()

    T, R = [], []
    result=[]
    # factor should be the width, thickness and length of the sample
    factor=calc_factor(0.543, 0.018, 0.536)

    while 1:
        line=F.readline()
        if not line:
            break
        parts=line.split(' ')
        Temperary=float(parts[3]), float(parts[7])
        result.append(Temperary)

    result_S=sorted(result, key=lambda tup: tup[0])

    T, R=average_data(result_S, 50)

    p=xalglib.polynomialbuild(T, R)
    xT=drange(min(T), max(T), 0.1)
    volt, diff=[], []
    for x in xT:
        v, dv=xalglib.barycentricdiff1(p, x)
        volt.append(v)
        diff.append(dv)
    print(volt[100], diff[100])
    print(str(len(T))+" data input")

    # output to a file
    Fname=F.name[:-4]
    Fname=Fname+"(output).dat"
    outputfile(xT, volt, diff, Fname)

if __name__ =="__main__":
    main()
