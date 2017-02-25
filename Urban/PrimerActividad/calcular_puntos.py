import pandas as pd
import mysql.connector
import math

def distancia(x,x1,y,y1):
    a=(x-x1)**2
    b=(y-y1)**2
    c=((a+b)**.5)*100000
    return c

def angulo(x,y):
    if(y==0):
        if(x<0):
            ang=180
        else:
            ang=0
    else:
        ang=math.degrees(math.atan(x/y))
        if(y>0):
            if(x<0):
                ang=360-ang    
        else:
            if(x<0):
                ang=ang+180
            else:
                ang=180-ang  
    return(ang)

cnx = mysql.connector.connect(user='cesarmarquez', password='CESAR_2606952_*cmarquez',
                              host='urban-srv5937.cloudapp.net',
                              database='Scripts'
                              )

cursor=cnx.cursor()
cursor.execute('Select * from Rutas')
df3=cursor.fetchall()
cursor.execute('Select * from camiones_rutas')
df2=cursor.fetchall()
cursor.execute('Select * from Paradas')
df=cursor.fetchall()
cnx.close()

df3=pd.DataFrame(df3)
df3.columns=['Ruta','X','Y','Direccion']
df2=pd.DataFrame(df2)
df2.columns=['id_rutas','Ruta','Direccion','index']
df2.pop('index')
df=pd.DataFrame(df)
df.columns=['id','X','Y']
angu=[]

for index in range(df2.shape[0]):
    dis=[]
    parada=df2['id_rutas'][index]
    ruta=df2['Ruta'][index]
    direccion=df2['Direccion'][index]
    xparada=float(df[df['id']==parada]['X'])
    yparada=float(df[df['id']==parada]['Y'])
    a=df3[(df3['Ruta']==ruta)&(df3['Direccion']==direccion)]
    a=a.reset_index()
    for index2 in range(a.shape[0]):
        dis.append(distancia(xparada,a['X'][index2],yparada,a['Y'][index2]))
        a['Distancia']=pd.DataFrame(dis)
    num=min(a['Distancia'])
    indexpunto=int(a[a['Distancia']==num]['index'])
    xpunto=float(a[a['index']==indexpunto]['X'])
    ypunto=float(a[a['index']==indexpunto]['Y'])
    if(indexpunto!=a['index'][0]):
        xpuntoant=float(a[a['index']==indexpunto-1]['X'])
        ypuntoant=float(a[a['index']==indexpunto-1]['Y'])
        xref=xpunto-xparada
        yref=ypunto-yparada
        xref2=xpuntoant-xparada
        yref2=ypuntoant-yparada
        ang1=angulo(xref,yref)
        ang2=angulo(xref2,yref2)
        if(abs(ang1-ang2)>160):
            angu.append(indexpunto-1)
        else:
            angu.append(indexpunto)
            
    else:
        angu.append(indexpunto)
            
df2['index']=pd.DataFrame(angu)

cnx.connect()
cursor=cnx.cursor()
cursor.execute('truncate table camiones_rutas')
cnx.commit()
for index in range(df2.shape[0]):
    cursor.execute('insert into camiones_rutas values('+str(df2['id_rutas'][index])+','+str(df2['Ruta'][index])+','+str(df2['Direccion'][index])+','+str(df2['index'][index])+')')
    
cnx.commit()
cnx.close()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
