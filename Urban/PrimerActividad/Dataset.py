#http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.dropna.html

import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp

def error(f, x, y):
       return sp.sum((f(x)-y)**2)

df=pd.read_csv('Dataset.csv')
df=df.dropna(thresh=5)
df=df.reset_index()
df.pop('index')
x=df['X']
y=df['Y']

aux=[]
time=df['Hora']
tiempo=[]

for index,row in enumerate(time):
    aux.append(row)
    aux2=str(aux[index])
    segundos=int(aux2[-2:])
    minutos=int(aux2[-4:-2])
    if(len(aux2)==4):
        hora=int(aux2[0])
    else:
        hora=int(aux2[0:2])
    tiempo.append((hora*3600)+(minutos*60)+segundos)

aux=[]

for index in range(len(tiempo)-1):
    aux.append(tiempo[index+1]-tiempo[index])   

aux.insert(0,0)

aux2=[]
aux3=[]
for row in x: 
    aux2.append(row)

for row in y:
    aux3.append(row)


dis=[]
vel=[]
status=[]
for index in range(1,len(aux2)):
    a=(x[index]-x[index-1])**2
    b=(y[index]-y[index-1])**2
    c=((a+b)**.5)*100
    c2=c
    if index==1:
        dis.append(c2)
    else:
        dis.append(c2+dis[index-2])
    velocidad=(c/aux[index])*3600
    if(velocidad<10):
        status.append(0)
    else:
        status.append(1)
    vel.append(velocidad)
    
status.insert(0,0)
status=pd.DataFrame(status)

dis.insert(0,0)
vel.insert(0,0)
df['Km/h']=pd.DataFrame(vel)
df['Distancia']=pd.DataFrame(dis)
df['Status']=pd.DataFrame(status)
#plt.plot(x.head(43),y.head(43))
df=df.head(30)
camion=df[df['Status']==1]
pie=df[df['Status']==0]

x=df[df['Km/h']<10]['Hora']
y=df[df['Km/h']<10]['Km/h']

f2p = sp.polyfit(x, y, 1)
f2 = sp.poly1d(f2p)
ef2=error(f2, x, y)

fx = sp.linspace(min(x),max(x), 5900)
plt.plot(fx, f2(fx), linewidth=3,color = (0,1,0))
#plt.plot(df['Hora'].head(32),df['Km/h'].head(32))
plt.scatter(camion['Hora'],camion['Km/h'])
plt.scatter(pie['Hora'],pie['Km/h'],color=(0,1,0))
plt.show()










