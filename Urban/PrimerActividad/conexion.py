import mysql.connector
import pandas as pd


cnx = mysql.connector.connect(user='cesarmarquez', password='CESAR_2606952_*cmarquez',
                              host='urban-srv.isavanzados.com.mx',
                              database='Urban'
                              )

#CREATE USER 'cesarmarquez2'@'201.166.183.181' IDENTIFIED BY 'CESAR_2606952_*cmarquez';
#GRANT ALL PRIVILEGES ON * . * TO 'cesarmarquez2'@'201.166.183.181';
#FLUSH PRIVILEGES;

cursor=cnx.cursor()
#cursor.execute('SELECT * FROM Rutas INTO OUTFILE "gente.txt"')
cursor.execute('load data local infile "~/Repositorios/Urban/Rutas_xy.csv" into table Rutas FIELDS TERMINATED BY ","')
#df=cursor.fetchall()
cnx.close()
#print(df)
df=pd.DataFrame(df)
df.columns=['Hora','Ruta','X','Y','Direccion','Dia','Festivo']