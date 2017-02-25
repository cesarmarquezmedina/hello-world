import pandas as pd
import matplotlib.pyplot as plt
from sklearn import svm
import scipy as sp
from time import time
import mysql.connector 

tiempo_inicial=time()

Ruta=50

def error(f, x, y):
       return sp.sum((f(x)-y)**2)

def trans_seg(string):
    segundos=int(string[-2:])
    minutos=int(string[-4:-2])
    if(len(string)==5):
        hora=int(string[0])
    else:
        hora=int(string[:2])
    return ((hora*3600)+(minutos*60)+segundos)
       

datos_in=pd.DataFrame([21.866505],columns=['X'])
datos_in['Y']=[-102.245071]
datos_in['Hora']=[64700]
datos_in['Dia']=[1]
datos_in['Festivo']=[1]
datos_in['Ruta']=[Ruta]


cnx = mysql.connector.connect(user='cesarmarquez', password='CESAR_2606952_*cmarquez',
                              host='urban-srv.isavanzados.com.mx',
                              database='Becarios'
                              )
cursor=cnx.cursor()
cursor.execute('Select * from Registro4')
df=cursor.fetchall()
cnx.close()
df=pd.DataFrame(df)
df.columns=['Ruta','Hora','X','Y','id']

#df=pd.read_csv('Rutas.csv')
print(df)

x=df['X']
y=df['Y']

aux=[]
time2=df['Hora']
tiempo=[]


for index,row in enumerate(time2):
    aux.append(row)
    aux2=str(aux[index])
    segundos=int(aux2[-2:])
    minutos=int(aux2[-4:-2])
    if(len(aux2)==7):
        hora=int(aux2[0])
    else:
        hora=int(aux2[:2])
    tiempo.append((hora*3600)+(minutos*60)+segundos)

aux=[]

for index in range(len(tiempo)-1):
    aux.append(tiempo[index+1]-tiempo[index])   

aux.insert(0,0)

dis=[]
vel=[]
status=[]

for index in range(1,len(x)):
    a=(x[index]-x[index-1])**2
    b=(y[index]-y[index-1])**2
    c=((a+b)**.5)*100
    c2=c*100
    dis.append(c2)
    
    velocidad=(c/aux[index])*3600
    if(velocidad<15):
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


camion=df[df['Status']==1]
pie=df[df['Status']==0]

#plt.plot(df['Hora'].head(32),df['Km/h'].head(32))
#plt.scatter(camion['Hora'],camion['Km/h'])
#plt.scatter(pie['Hora'],pie['Km/h'],color=(0,1,0))
#plt.show()

clf= svm.SVC(gamma=0.01,C=100)


clf.fit(df[['Ruta','X','Y']],df['Hora'])


#clf.fit(df['Km/h'].values.reshape(-1,1),df['Hora'])

pred=[]

xs=[21.85111,21.851191,21.941131,21.91009,21.852406]
ys=[-102.351197,-102.271743,-102.278511,-102.259641,-102.292171]

hora_pred=clf.predict(datos_in[['Ruta','X','Y']])

aux1=str(hora_pred[0])
#print(aux1)
hora1=trans_seg(aux1)

aux1=str(datos_in['Hora'][0])
#print(aux1)
hora0=trans_seg(aux1)

des=(hora0-hora1)

for a in range(5):
    aux1=clf.predict([[Ruta,xs[a],ys[a]]])[0]
    h=trans_seg(str(aux1))
    b=((h-hora0+des)/60)
    #print(b)
    pred.append(b)


pre=pd.DataFrame(pred,columns=['Prediccion'])

pre['X']=pd.DataFrame(xs)
pre['Y']=pd.DataFrame(ys)

"""
x=df[(df['Km/h']<10) & (df['Hora']<66000 )]['Hora']
y=df[(df['Km/h']<10) & (df['Hora']<66000 )]['Km/h']
x2=df[(df['Km/h']<10) & (df['Hora']>66000 )]['Hora']
y2=df[(df['Km/h']<10) & (df['Hora']>66000 )]['Km/h']
      
x2=x2.append(pd.DataFrame([max(x)]),ignore_index=True)
y2=y2.append(pd.DataFrame([y[max(y.index.values)]]),ignore_index=True)
      
d = sp.linspace(0,x.shape[0],x.shape[0])
d2 = sp.linspace(x2.shape[0]+x.shape[0],x.shape[0],x2.shape[0])

f1p = sp.polyfit(x2[0], d2, 1)
f1 = sp.poly1d(f1p)
ef1=error(f1, x2[0], d2)

f2p = sp.polyfit(x, d, 5)
f2 = sp.poly1d(f2p)
ef2=error(f2, x, d)

#if datos_in['Hora'][0]<max(x):
"""   

"""
plt.plot(x,d)
plt.plot(x2[0],d2)

fx = sp.linspace(min(x),max(x),50000)
fx2= sp.linspace(min(x2[0]),max(x2[0]),50000)
plt.plot(fx, f2(fx), linewidth=3,color = (0,1,0))
plt.plot(fx2, f1(fx2), linewidth=3,color = (0,1,0))
#plt.scatter(camion['Hora'],camion['Km/h'])
#plt.scatter(pie['Hora'],pie['Km/h'],color=(0,1,0))
"""

#x=df[(df['Ruta']==Ruta) & (df['Direccion']==2)][['X','Y']]
#x2=df[(df['Ruta']==Ruta) & (df['Direccion']==2) & (df['Hora']<=hora_pred[0])][['X','Y']]

y=df['X']
x=df['Y']
#y2=x2['X']
#x2=x2['Y']
"""
plt.scatter(x,y)
#plt.plot(x2,y2,linewidth=5)

#plt.plot(x2,y2,color=(1,0,0))
plt.scatter([-102.221879,-102.366247,-102.366247,-102.221879],[21.840073,21.840073,21.951886,21.951886])

plt.scatter(pre['Y'],pre['X'],color=(0,1,0))
plt.text(pre['Y'][0],pre['X'][0]+.001,str(pre['Prediccion'][0]))
plt.text(pre['Y'][1],pre['X'][1]-.01,str(pre['Prediccion'][1]))
plt.text(pre['Y'][2],pre['X'][2]+.001,str(pre['Prediccion'][2]))
plt.text(pre['Y'][3],pre['X'][3]+.001,str(pre['Prediccion'][3]))
plt.text(datos_in['Y'][0]+.001,datos_in['X'][0]+.001,'0')

plt.show()
"""
f2p = sp.polyfit(df['Hora'].head(5),df['Km/h'].head(5), 7)
f2 = sp.poly1d(f2p)
ef2=error(f2,df['Hora'].head(5),df['Km/h'].head(5))
#print(ef2)

fx = sp.linspace(min(df['Hora'].head(5)),max(df['Hora'].head(5)),15)
#plt.plot(fx, f2(fx), linewidth=3,color = (0,1,0))

plt.scatter([-102.221879,-102.366247,-102.366247,-102.221879],[21.840073,21.840073,21.951886,21.951886])

plt.scatter(df[df['Status']==1]['Y'],df[df['Status']==1]['X'])
plt.scatter(df[df['Status']==0]['Y'],df[df['Status']==0]['X'],color=(0,1,0))

tiempo_final=time()

tiempo=tiempo_final-tiempo_inicial

#print(tiempo)
t=True


count=1
hed=2
bo=False
aux=0
while (count<30):
    
    f2p = sp.polyfit(df['Hora'].head(hed),df['Km/h'].head(hed), 3)
    f2 = sp.poly1d(f2p)
    ef2=error(f2,df['Hora'].head(hed),df['Km/h'].head(hed))
    if(ef2>5):
            
        f2p = sp.polyfit(df['Hora'].head(hed-1),df['Km/h'].head(hed-1), 3)
        f2 = sp.poly1d(f2p)
        fx = sp.linspace(min(df['Hora'].head(hed-1)),max(df['Hora'].head(hed-1)),15)
        ef2=error(f2,df['Hora'].head(hed-1),df['Km/h'].head(hed-1))
        
        #plt.plot(fx, f2(fx))
        #print(df)
        df=df.tail(df.shape[0]-hed+2)
        #print(df)
        hed=1
        if count==29:
            aux=1
            
    if (aux==0)&(count==29):
        bo=True
            
    hed=hed+1
    count=count+1

if bo==True:
    fx = sp.linspace(min(df['Hora'].head(hed-1)),max(df['Hora'].head(hed-1)),15)
    plt.plot(fx, f2(fx), linewidth=3)




