import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from time import time

df=pd.read_csv('Rutas_ok.csv')

"""tiempo_inicial=time()
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
"""

Rut=[10,7]
x=[21.854529,21.873724,21.873595,21.879764,21.888263]
y=[-102.259909,-102.270931,-102.281692,-102.295299,-102.296156]
puntox=[21.920094]
puntoy=[-102.261723]

num=2
grafica=[]
grafica2=[]
X=[]
Y=[]
Ruta=[]

for row in df['X']:
    X.append(row)
    
for row in df['Y']:
    Y.append(row)
    
for row in df['Ruta']:
    Ruta.append(row)

dis=[]
dis2=[]

for index in range(len(X)):
    a=(X[index]-x[num])**2
    b=(Y[index]-y[num])**2
    c=((a+b)**.5)*100
    c2=c*100
    dis.append(c2)
    
    d=(X[index]-puntox[0])**2
    e=(Y[index]-puntoy[0])**2
    f=((d+e)**.5)*100
    f2=f*100
    dis2.append(f2)

df['Distancia']=pd.DataFrame(dis)
df['Distancia2']=pd.DataFrame(dis2)

for a in range(5):
    R=Rut[a]
    
    distancia=df[df['Ruta']==R]['Distancia']
    distancia2=df[df['Ruta']==R]['Distancia2']
    
    punto2=df[df['Distancia2']==min(distancia2)]
    punto=df[df['Distancia']==min(distancia)]
    print(punto[['Ruta','Distancia']])
    print(punto2[['Ruta','Distancia2']])
    
    if min(distancia)<70:
        grafica.append(R)
    if min(distancia2)<10:
        grafica2.append(R)

#graficas importantes
"""for a in range(len(grafica)):
    X=df[df['Ruta']==grafica[a]]['X']
    Y=df[df['Ruta']==grafica[a]]['Y']
    plt.plot(Y,X)

for a in range(len(grafica2)):
    X=df[df['Ruta']==grafica2[a]]['X']
    Y=df[df['Ruta']==grafica2[a]]['Y']
    plt.scatter(Y,X)
"""

plt.scatter(-102.261723,21.920094)	    

plt.scatter([-102.221879,-102.366247,-102.366247,-102.221879],[21.840073,21.840073,21.951886,21.951886])
plt.scatter(y[num],x[num])

camion=False
Rutas=[]

for a in range(len(grafica)):
    for b in range(len(grafica2)):
        if grafica[a]==grafica2[b]:
            camion=True
            Rutas.append(grafica[a])

check=True
if(camion):
    print("La ruta "+str(Rutas[0]))
    check=False
else:
    punto=[]
    punto2=[]
    dis=[]
    ruta1=[]
    ruta2=[]
    for a in range(len(grafica)):
        ch=False
        X=df[df['Ruta']==grafica[a]]['X']
        Y=df[df['Ruta']==grafica[a]]['Y']
        for b in range(len(grafica2)):
            if(ch):
                break
            X1=df[df['Ruta']==grafica2[b]]['X']
            Y1=df[df['Ruta']==grafica2[b]]['Y']
            for c in range(min(X.index.values),max(X.index.values)+1):
                if(ch):
                    break
                for d in range(min(X1.index.values),max(X1.index.values)+1):
                    v=(X[c]-X1[d])**2
                    f=(Y[c]-Y1[d])**2
                    r=((v+f)**.5)*100
                    r2=r*100
                    #print(r)
                
                    if r2<50:
                        ch=True
                        punto.append(d)
                        punto2.append(c)
                        ruta1.append(grafica[a])
                        ruta2.append(grafica2[b])
                        
                        break
if (check):
    if (len(ruta2)>1):
        print("Tienes las siguientes opciones:\n")
        for a in range(len(ruta2)):
            print(str(a+1)+"- Tomar la ruta "+str(ruta1[a])+" Y despues tomar la ruta "+str(ruta2[a])+"\n")
                
    res=int(input("Elige tu opcion: "))
    
    X=df[df['Ruta']==ruta1[res-1]]['X']
    Y=df[df['Ruta']==ruta1[res-1]]['Y']
    
    plt.plot(Y,X)
    
    X=df[df['Ruta']==ruta2[res-1]]['X'][punto[res-1]:]
    Y=df[df['Ruta']==ruta2[res-1]]['Y'][punto[res-1]:]
    plt.plot(Y,X)
    
    plt.scatter(df['Y'][punto[res-1]],df['X'][punto[res-1]])
else:
    X=df[df['Ruta']==Rutas[0]]['X']
    Y=df[df['Ruta']==Rutas[0]]['Y']
    plt.plot(Y,X)

plt.show()
#tiempo=tiempo_final-tiempo_inicial

#print(tiempo)


