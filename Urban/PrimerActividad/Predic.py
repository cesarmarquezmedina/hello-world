import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from sklearn import svm


def distancia(x,x1,y,y1):
    a=(x-x1)**2
    b=(y-y1)**2
    c=((a+b)**.5)*100000
    return c

def trans_seg(string):
    segundos=int(string[-2:])
    minutos=int(string[-4:-2])
    if(len(string)==5):
        hora=int(string[0])
    else:
        hora=int(string[:2])
    return ((hora*3600)+(minutos*60)+segundos)
    
df1=pd.read_csv('Rutas_ok.csv')

cnx = mysql.connector.connect(user='cesarmarquez', password='CESAR_2606952_*cmarquez',
                              host='urban-srv.isavanzados.com.mx',
                              database='Scripts'
                              )
cursor=cnx.cursor()

x=[21.888073] 
y=[-102.317065]
hora=[91100]

cursor.execute('Select * from Ruta40')

df=cursor.fetchall()

cnx.close()

df=pd.DataFrame(df)
df.columns=['Ruta','Hora','X','Y','Id']

clf= svm.SVC(gamma=0.01,C=100)

clf.fit(df[['X','Y','Hora']],df.index.values)

df1=pd.DataFrame(hora)
df1.columns=['Hora']
df1['X']=pd.DataFrame(x)
df1['Y']=pd.DataFrame(y)

z=clf.predict(df1[['X','Y','Hora']]) 

dis=distancia(x[0],df['X'][z[0]],y[0],df['Y'][z[0]])

#plt.plot(df['Y'],df['X'])

#plt.show()

print(df['X'][int(z)],df['Y'][int(z)],df['Hora'][int(z)])