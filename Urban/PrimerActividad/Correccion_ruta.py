import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector
from sklearn import svm

df1=pd.read_csv('Datos_muestra.csv')

cnx = mysql.connector.connect(user='cesarmarquez', password='CESAR_2606952_*cmarquez',
                              host='urban-srv.isavanzados.com.mx',
                              database='Urban'
                              )
cursor=cnx.cursor()

cursor.execute('Select * from Registro2')
df=cursor.fetchall()
cnx.close()

df=pd.DataFrame(df)
df.columns=['Ruta','Hora','X','Y','Id']




clf= svm.SVC(gamma=0.01,C=100)

clf.fit(df1[['X','Y']],df1.index.values)

df=df.tail(7)
df=df.head(3)

z=clf.predict(df[['X','Y']]) 

grafica=df1[min(z):max(z)+1]

plt.scatter(df['Y'],df['X'])
plt.scatter(grafica['Y'],grafica['X'])
plt.plot(df['Y'],df['X'])
plt.plot(grafica['Y'],grafica['X'])

plt.show()