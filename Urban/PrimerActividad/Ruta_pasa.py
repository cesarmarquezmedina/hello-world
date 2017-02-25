#https://dlegorreta.wordpress.com/tag/matplotlib/

import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from time import time
#df=pd.read_csv('Rutas_xy.csv')

tiempo_inicial=time()
cnx = mysql.connector.connect(user='cesarmarquez', password='CESAR_2606952_*cmarquez',
                              host='urban-srv.isavanzados.com.mx',
                              database='Urban'
                              )
cursor=cnx.cursor()
cursor.execute('Select * from Rutas')
df=cursor.fetchall()
cnx.close()
df=pd.DataFrame(df)
df.columns=['Hora','Ruta','X','Y','Direccion','Dia']

Rut=[50,42,2,39,20]
x=[21.854529,21.873724,21.873595,21.879764,21.888263]
y=[-102.259909,-102.270931,-102.281692,-102.295299,-102.296156]
num=2
grafica=[]

for a in range(5):
    X=[]
    Y=[]
    Ruta=[]
    R=Rut[a]

    for row in df['X']:
        X.append(row)
        
    for row in df['Y']:
        Y.append(row)
    
    for row in df['Ruta']:
        Ruta.append(row)

    dis=[]

    for index in range(len(X)):
        a=(X[index]-x[num])**2
        b=(Y[index]-y[num])**2
        c=((a+b)**.5)*100
        c2=c*100
        dis.append(c2)

    Rutas=pd.DataFrame(Ruta,columns=['Ruta'])
    Rutas['X']=pd.DataFrame(X)
    Rutas['Y']=pd.DataFrame(Y)
    Rutas['Distancia']=pd.DataFrame(dis)

    distancia=Rutas[Rutas['Ruta']==R]['Distancia']
    punto=Rutas[Rutas['Distancia']==min(distancia)]
    print(punto)
    if min(distancia)<100:
        grafica.append(R)

for a in range(len(grafica)):
    X=df[df['Ruta']==grafica[a]]['X']
    Y=df[df['Ruta']==grafica[a]]['Y']
    plt.plot(Y,X)
    
plt.scatter([-102.221879,-102.366247,-102.366247,-102.221879],[21.840073,21.840073,21.951886,21.951886])
plt.scatter(y[num],x[num])
plt.show()
tiempo_final=time()

tiempo=tiempo_final-tiempo_inicial

print(tiempo)


