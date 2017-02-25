#http://stackoverflow.com/questions/14047979/executing-python-script-in-php-and-exchanging-data-between-the-two

import pandas as pd
import matplotlib.pyplot as plt
import scipy as sp
from time import time
import mysql.connector 
from sklearn import svm

df1=pd.read_csv('Rutas_ok.csv')

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
cursor.execute('Select * from Ruta20')
df=cursor.fetchall()
cnx.close()
df=pd.DataFrame(df)
df.columns=['Ruta','Hora','X','Y','id']

aux2=tiempo_pas(df)

df['Tiempo']=pd.DataFrame(aux2)
dis=[]
print(df)
df1=df.tail(27)
df=df.head(103)
plt.plot(df['Y'],df['X'])
df=df[df['Tiempo']>40].reset_index()
plt.plot(df1['Y'],df1['X'])
df = df.drop('index', 1)


"""
clf= svm.SVC(gamma=0.01,C=100)

clf.fit(df1[(df1['Ruta']==40)&(df1['Direccion']==1)][['X','Y']],df1[(df1['Ruta']==40)&(df1['Direccion']==1)][['X','Y']].index.values)

z=clf.predict(df[['X','Y']][:1]) 

z2=clf.predict(df[['X','Y']][1:2])

if (z<z2):
    plt.plot(df1[(df1['Ruta']==40)&(df1['Direccion']==1)]['Y'][z[0]:],df1[(df1['Ruta']==40)&(df1['Direccion']==1)]['X'][z[0]:])
    print('1')
else:
    plt.plot(df1[(df1['Ruta']==40)&(df1['Direccion']==2)]['Y'][z[0]:],df1[(df1['Ruta']==40)&(df1['Direccion']==2)]['X'][z[0]:])    
    print('2')
    
plt.scatter(df['Y'][:1],df['X'][:1])
"""
plt.scatter([-102.221879,-102.366247,-102.366247,-102.221879],[21.840073,21.840073,21.951886,21.951886])

plt.show()












