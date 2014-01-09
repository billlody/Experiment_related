# unfinished
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

# output file, temperature, resistivity, temperature, 1st order der, file name
def outputfile(x1, y1, y2, Fname):
    Foutput=open(Fname, 'w')
    Foutput.write('Temperature') 
    Foutput.write('\t')
    Foutput.write('Resistivity(ohm * mm)')
    Foutput.write('\t')
    Foutput.write('1st order derivative')
    Foutput.write('\n')
    for i in range(len(x1)):
        Foutput.write(str(x1[i]))
        Foutput.write('\t')
        Foutput.write(str(y1[i]))
        Foutput.write('\t')
        Foutput.write(str(y2[i]))
        Foutput.write('\n')
    Foutput.close()

def take_deriv(T, R):
    dR=[]
    temp=T[0], (R[1]-R[0])
    dR.append(temp)
    for i in range(len(T)-2):
        temp1=(R[i+1]-R[i]) / (T[i+1]-T[i])
        temp2=(R[i+2]-R[i+1]) / (T[i+2]-T[i+1])
        temp=T[i+1], (temp1*0.5 + temp2*0.5)
        dR.append(temp)
    temp=T[-1], ((R[-1]-R[-2])/(T[-1]-T[-2]))
    dR.append(temp)
    return dR

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
    dR=take_deriv(T, R)
    T_d, R_d=average_data(dR, 50)

    # output to a file
    Fname=F.name[:-4]
    Fname=Fname+"(output)1.dat"
    outputfile(T, R, R, Fname)
    Fname=F.name[:-4]
    Fname=Fname+"(output)2.dat"
    outputfile(T_d, R_d, R_d, Fname)

if __name__ =="__main__":
    main()
