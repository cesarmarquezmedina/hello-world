import pandas as pd
import mysql.connector 
import sys, json

cnx = mysql.connector.connect(user='cesarmarquez', password='CESAR_2606952_*cmarquez',
                              host='urban-srv5937.cloudapp.net',
                              database='Scripts'
                              )
cursor=cnx.cursor()
cursor.execute('Select * from estados')
df=cursor.fetchall()

cnx.close()

df=pd.DataFrame(df)
df.columns=['Estado','X','Y','X2','Y2']

try:
    
    data=json.loads(sys.argv[1])
    
except:
    print("Error")
    #sys.exit(1)

    
x=20.607950
y=-100.174194

#x=float(data[0])
#y=float(data[1])

estado={}
for index in range(df.shape[0]):
    x1=df['X'][index]
    x2=df['X2'][index]
    y1=df['Y'][index]
    y2=df['Y2'][index]
    if((x>=(min(x1,x2)))&(x<=(max(x1,x2)))):
        if((y>=(min(y1,y2)))&(y<=(max(y1,y2)))):
            estado['Estado']={'Nombre':df['Estado'][index]}
            break

print (json.dumps(estado))