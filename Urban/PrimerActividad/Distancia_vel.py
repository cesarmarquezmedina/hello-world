import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
from time import time
import mysql.connector 


def trans_seg(string):
    segundos=int(string[-2:])
    minutos=int(string[-4:-2])
    if(len(string)==5):
        hora=int(string[0])
    else:
        hora=int(string[:2])
    return ((hora*3600)+(minutos*60)+segundos)
    
def distancia(x,x1,y,y1):
    a=(x-x1)**2
    b=(y-y1)**2
    c=((a+b)**.5)*100
    return c
    
def tiempo_pas(df1):
    aux=[]
    tiempo=[]
    for index,row in enumerate(df1['Hora']):
        aux.append(row)
        tiempo.append(trans_seg(str(aux[index])))
    aux=[]
    for index in range(len(tiempo)-1):
        aux.append(tiempo[index+1]-tiempo[index]) 
        
    aux.insert(0,0)
    return aux
    
def error(f, x, y):
       return sp.sum((f(x)-y)**2)
       
cnx = mysql.connector.connect(user='cesarmarquez', password='CESAR_2606952_*cmarquez',
                              host='urban-srv.isavanzados.com.mx',
                              database='Scripts'
                              )
cursor=cnx.cursor()
cursor.execute('Select * from Ruta40')
df=cursor.fetchall()
cnx.close()
df=pd.DataFrame(df)
df.columns=['Ruta','Hora','X','Y','id']

aux2=tiempo_pas(df)

df['Tiempo']=pd.DataFrame(aux2)
dis=[]
df=df[df['Tiempo']>40].reset_index()

df = df.drop('index', 1)

for index in range(min(df.index.values),max(df.index.values)):
    dis.append(distancia(df['X'][index],df['X'][index+1],df['Y'][index],df['Y'][index+1]))


dis.insert(0,0)

df['Distancia']=pd.DataFrame(dis)

aux2=tiempo_pas(df)

df = df.drop('Tiempo', 1)

df['Tiempo']=pd.DataFrame(aux2)

df['Velocidad']=(df['Distancia']/df['Tiempo'])*3600

aux=[]
aux2=[]
aux2.append(0)
aux.append(0)
df['Tiempo']=df['Tiempo']
for index in range(min(df.index.values),max(df.index.values)):
      aux.append(df['Tiempo'][index+1]+aux[index])  
      aux2.append(df['Distancia'][index+1]+aux2[index])

""" 
plt.plot(aux,aux2)

f2p = sp.polyfit(aux, aux2, 2)
f2 = sp.poly1d(f2p)
ef2=error(f2, aux, aux2)

fx = sp.linspace(min(aux),max(aux)+400, 200) # generate X-values for plotting
plt.plot(fx, f2(fx), linewidth=3,color = (0,0,0))
"""

plt.plot(df['Hora'],df['Distancia'])

    
    
    
    