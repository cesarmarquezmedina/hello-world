import pandas as pd
import mysql.connector

def distancia(x,x1,y,y1):
    a=(x-x1)**2
    b=(y-y1)**2
    c=((a+b)**.5)*100000
    return c

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
df=pd.DataFrame(df)
df.columns=['id','X','Y']

rutas=list(set(df3['Ruta']))
paradas=[]
for index in rutas:
    for direccion in (1,2):
        aux=df2[(df2['Ruta']==index)&(df2['Direccion']==direccion)]
        aux=aux.reset_index()
        for index2 in rutas:
            if(index!=index2):
                for direccion2 in (1,2):
                    aux2=df2[(df2['Ruta']==index2)&(df2['Direccion']==direccion2)]
                    aux2=aux2.reset_index()
                    for index3 in range(aux.shape[0]):
                        for index4 in range(aux2.shape[0]):
                            x1=float(df[df['id']==aux['id_rutas'][index3]]['X'])
                            y1=float(df[df['id']==aux['id_rutas'][index3]]['Y'])
                            x2=float(df[df['id']==aux2['id_rutas'][index4]]['X'])
                            y2=float(df[df['id']==aux2['id_rutas'][index4]]['Y'])
                            if(distancia(x1,x2,y1,y2)<250):
                                 paradas.append((index,index2,direccion,direccion2,aux['id_rutas'][index3],aux2['id_rutas'][index4])) 
                                 
cnx.connect()
cursor=cnx.cursor()
cursor.execute('truncate table transbordos')
cnx.commit()           
for index in range(len(paradas)):
    cursor.execute('insert into transbordos values('+str(paradas[index][0])+','+str(paradas[index][1])+','+str(paradas[index][2])+','+str(paradas[index][3])+','+str(paradas[index][4])+','+str(paradas[index][5])+')')     

cnx.commit()
cnx.close()            