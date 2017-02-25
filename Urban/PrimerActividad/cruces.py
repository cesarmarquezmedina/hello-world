import pandas as pd
import mysql.connector
from time import time

ini=time()


def distancia(x,x1,y,y1):
    a=(x-x1)**2
    b=(y-y1)**2
    c=((a+b)**.5)*100000
    return c

def Checar(df1,df2):
    for indexx in range(min(df1.index.values),max(df1.index.values)+1):
        for indexy in range(min(df2.index.values),max(df2.index.values)+1):
            aprox=distancia(df1['X'][indexx],df2['X'][indexy],df1['Y'][indexx],df2['Y'][indexy])
                
            if (aprox<100):
                return(True,indexx,indexy)
                
    return (False,0,0)
    
cnx = mysql.connector.connect(user='cesarmarquez', password='CESAR_2606952_*cmarquez',
                              host='urban-srv5937.cloudapp.net',
                              database='Scripts'
                              )

cursor=cnx.cursor()
cursor.execute('truncate table cruces')
cnx.commit()
cursor.execute('Select * from Rutas')
df=cursor.fetchall()
cnx.close()
df=pd.DataFrame(df)
df.columns=['Ruta','X','Y','Direccion']


Rut=[10,20,40,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,18,19,21,23,24,25]

no=[]

for ruta in Rut:
    x1=df[(df['Ruta']==ruta)&(df['Direccion']==1)]
    for ruta2 in Rut:
        x2=df[(df['Ruta']==ruta2)&(df['Direccion']==1)]
        ok,index3,index4=Checar(x1,x2)
        if(ok):
            no.append([ruta,ruta2,1,1,index3,index4])
        #print(Checar(x1,x2),ruta,ruta2)
    for ruta2 in Rut:
        x2=df[(df['Ruta']==ruta2)&(df['Direccion']==2)]
        ok,index3,index4=Checar(x1,x2)
        if(ok):
            no.append([ruta,ruta2,1,2,index3,index4])
        
for ruta in Rut:
    x1=df[(df['Ruta']==ruta)&(df['Direccion']==2)]
    for ruta2 in Rut:
        x2=df[(df['Ruta']==ruta2)&(df['Direccion']==1)]
        ok,index3,index4=Checar(x1,x2)
        if(ok):
            no.append([ruta,ruta2,2,1,index3,index4])
        #print(Checar(x1,x2),ruta,ruta2)
    for ruta2 in Rut:
        x2=df[(df['Ruta']==ruta2)&(df['Direccion']==2)]
        ok,index3,index4=Checar(x1,x2)
        if(ok):
            no.append([ruta,ruta2,2,2,index3,index4])
dp=pd.DataFrame(no)
dp.columns=['Ruta1','Ruta2','direccion1','direccion2','index1','index2']

cnx.connect()
cursor=cnx.cursor()   
                       
for a in range(dp.shape[0]):
    
    cursor.execute('insert into cruces values('+str(dp['Ruta1'][a])+','+str(dp['Ruta2'][a])+','+str(dp['direccion1'][a])+','+str(dp['direccion2'][a])+','+str(dp['index1'][a])+','+str(dp['index2'][a])+')')

cnx.commit()
cnx.close()
fin=time()
print('Tiempo: ',fin-ini)
        
