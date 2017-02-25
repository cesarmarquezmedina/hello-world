import pandas as pd
import mysql.connector
import sys,json
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

try:
    data=json.loads(sys.argv[1])
except:
    print("Error")
    #sys.exit(1)

cnx = mysql.connector.connect(user='cesarmarquez', password='CESAR_2606952_*cmarquez',
                              host='urban-srv5937.cloudapp.net',
                              database='Scripts'
                              )

cursor=cnx.cursor()
cursor.execute('Select * from Rutas')
df=cursor.fetchall()
cnx.close()
df=pd.DataFrame(df)
df.columns=['Ruta','X','Y','Direccion']


#df=pd.read_csv('Rutas_ok.csv')

Rut=[10,20,40,1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,18,19,21,23,24,25]


#salidax=data[0]
#saliday=data[1]

#llegadax=data[2]
#llegaday=data[3]
salidax=[21.902744]
saliday=[-102.284860]

llegadax=[21.878641]
llegaday=[-102.301947]

num=0

dis=[]
dis2=[]
RutaSalida=[]
RutaSalida2=[]
RutaLlegada=[]
RutaLlegada2=[]

for index in range(df.shape[0]):
    dis.append(distancia(df['X'][index],salidax[num],df['Y'][index],saliday[num]))
    
    dis2.append(distancia(df['X'][index],llegadax[0],df['Y'][index],llegaday[0]))

df['Distancia']=pd.DataFrame(dis)
df['Distancia2']=pd.DataFrame(dis2)

for index in range(len(Rut)):
    
    aux=min(df[(df['Ruta']==Rut[index])&(df['Direccion']==1)]['Distancia'])
    aux2=min(df[(df['Ruta']==Rut[index])&(df['Direccion']==2)]['Distancia'])
    
    aux3=min(df[(df['Ruta']==Rut[index])&(df['Direccion']==1)]['Distancia2'])
    aux4=min(df[(df['Ruta']==Rut[index])&(df['Direccion']==2)]['Distancia2'])
    
    if(aux<250):
        RutaSalida.append(Rut[index])
    if(aux2<250):
        RutaSalida2.append(Rut[index])
        
    if(aux3<250):
        RutaLlegada.append(Rut[index])
    if(aux4<250):
        RutaLlegada2.append(Rut[index])
        
MismaRuta=False
TomarRuta=[]
hacia=[]

for index in range(len(RutaSalida)):
    for index2 in range(len(RutaLlegada)):
        if(RutaSalida[index]==RutaLlegada[index2]):
            MismaRuta=True
            TomarRuta.append(RutaSalida[index])
            hacia.append(1)
            
for index in range(len(RutaSalida2)):
    for index2 in range(len(RutaLlegada2)):
        if(RutaSalida2[index]==RutaLlegada2[index2]):
            MismaRuta=True
            TomarRuta.append(RutaSalida2[index])
            hacia.append(2)
Rutasd={}

if(MismaRuta):
    for index in range(len(TomarRuta)):
        aux=min(df[(df['Ruta']==TomarRuta[index])&(df['Direccion']==hacia[index])]['Distancia'])
        aux2=min(df[(df['Ruta']==TomarRuta[index])&(df['Direccion']==hacia[index])]['Distancia2'])
        num1=df[(df['Distancia']==aux)&(df['Ruta']==TomarRuta[index])&(df['Direccion']==hacia[index])].index.values[0]
        num2=df[(df['Distancia2']==aux2)&(df['Ruta']==TomarRuta[index])&(df['Direccion']==hacia[index])].index.values[0]
        print(num1,num2)
        if(num1<num2):
            
            Rutasd[len(Rutasd)+1]={'Ruta':TomarRuta[index],'Direccion':hacia[index],'index1':num1,'index2':num2+1}

else:
    
    #Ruta Salida1
    for index in range(len(RutaSalida)):
        xs=df[(df['Ruta']==RutaSalida[index])&(df['Direccion']==1)]
              
        aux=min(df[(df['Ruta']==RutaSalida[index])&(df['Direccion']==1)]['Distancia'])
        num1=df[(df['Ruta']==RutaSalida[index])&(df['Distancia']==aux)&(df['Direccion']==1)].index.values[0]
        
        
        for index2 in range(len(RutaLlegada)):
            xll=df[(df['Ruta']==RutaLlegada[index2])&(df['Direccion']==1)]
                    
            aux2=min(df[(df['Ruta']==RutaLlegada[index2])&(df['Direccion']==1)]['Distancia2'])
            num2=df[(df['Ruta']==RutaLlegada[index2])&(df['Distancia2']==aux2)&(df['Direccion']==1)].index.values[0]        
            
            ok,index3,index4=Checar(xs,xll)
            
            if((ok)&(num1<index3)&(index4<num2)):
                Rutasd[len(Rutasd)+1]={'Ruta1':RutaSalida[index],'Direccion':1,'index1':num1,'index2':index3+1,'Ruta2':RutaLlegada[index2],'Direccion2':1,'index3':index4,'index4':num2+1}
                
                
            
        for index2 in range(len(RutaLlegada2)):
            xll=df[(df['Ruta']==RutaLlegada2[index2])&(df['Direccion']==2)]
                        
            aux2=min(df[(df['Ruta']==RutaLlegada2[index2])&(df['Direccion']==2)]['Distancia2'])
            num2=df[(df['Ruta']==RutaLlegada2[index2])&(df['Distancia2']==aux2)&(df['Direccion']==2)].index.values[0]
            
            ok,index3,index4=Checar(xs,xll)
            
            if((ok)&(num1<index3)&(index4<num2)):
                Rutasd[len(Rutasd)+1]={'Ruta1':RutaSalida[index],'Direccion':1,'index1':num1,'index2':index3+1,'Ruta2':RutaLlegada2[index2],'Direccion2':2,'index3':index4,'index4':num2+1}
                
                
    #Ruta Salida2
    for index in range(len(RutaSalida2)):
        xs=df[(df['Ruta']==RutaSalida2[index])&(df['Direccion']==2)]
              
        aux=min(df[(df['Ruta']==RutaSalida2[index])&(df['Direccion']==2)]['Distancia'])
        num1=df[(df['Ruta']==RutaSalida2[index])&(df['Distancia']==aux)&(df['Direccion']==2)].index.values[0]
        
        
        for index2 in range(len(RutaLlegada)):
            xll=df[(df['Ruta']==RutaLlegada[index2])&(df['Direccion']==1)]
                        
            aux2=min(df[(df['Ruta']==RutaLlegada[index2])&(df['Direccion']==1)]['Distancia2'])
            num2=df[(df['Ruta']==RutaLlegada[index2])&(df['Distancia2']==aux2)&(df['Direccion']==1)].index.values[0]
            
            ok,index3,index4=Checar(xs,xll)
            
            if((ok)&(num1<index3)&(index4<num2)):
                
                Rutasd[len(Rutasd)+1]={'Ruta1':RutaSalida2[index],'Direccion':2,'index1':num1,'index2':index3+1,'Ruta2':RutaLlegada[index2],'Direccion2':1,'index3':index4,'index4':num2+1}
                
            
        for index2 in range(len(RutaLlegada2)):
            xll=df[(df['Ruta']==RutaLlegada2[index2])&(df['Direccion']==2)]
                        
            aux2=min(df[(df['Ruta']==RutaLlegada2[index2])&(df['Direccion']==2)]['Distancia2'])
            num2=df[(df['Ruta']==RutaLlegada2[index2])&(df['Distancia2']==aux2)&(df['Direccion']==2)].index.values[0]
                                
            ok,index3,index4=Checar(xs,xll)
                        
            if((ok)&(num1<index3)&(index4<num2)):
                
                Rutasd[len(Rutasd)+1]={'Ruta1':RutaSalida2[index],'Direccion':2,'index1':num1,'index2':index3+1,'Ruta2':RutaLlegada2[index2],'Direccion2':2,'index3':index4,'index4':num2+1}

fin=time()
print('Tiempo: ',fin-ini)
#print (Rutasd)
        
