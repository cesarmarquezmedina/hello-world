import csv as csv
import numpy as np
archivo=csv.reader(open('vehicle.csv','rt',))
print(archivo)
data=[]

for index,row in enumerate(archivo):
    if index>0:
        data.append(row)
    else:
        a=row
    if index>8039:
        break
        
data=np.array(data)
data1=data.T
data1=data1[:5]
data1=data1.T
print(a[0])
print(a[1])
print(a[2])
print(a[3])
print(a[4])
print(data1)


