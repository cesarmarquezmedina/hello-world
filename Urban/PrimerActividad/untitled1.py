#https://github.com/mGalarnyk/Python_Tutorials/blob/master/Time_Series/Part1_Time_Series_Data_BasicPlotting.ipynb

import pandas as pd
import pandas_datareader.data as web #conda install -c anaconda pandas-datareader=0.2.1
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import pylab as pl
import scipy as sp
from sklearn.linear_model import LinearRegression

def error(f, x, y):
       return sp.sum((f(x)-y)**2)
       
google = web.DataReader('GOOG', data_source = 'google', start = '3/14/2009', end = '4/14/2016')
google = google.drop('Volume', axis = 1 )
google['Ticks'] = range(0,len(google.index.values))
#se toma de decima parte de lops datos 
one_tenth = google.sample(frac = .1,random_state=np.random.randint(10))
#se quita el encabezado de los indices y se reacomodan de menor a mayor
one_tenth.index.name = None
one_tenth = one_tenth.sort_values(by=['Ticks'], ascending=[True])

#se reseta el index para que sea el de la fecha 
google = google.reset_index()
google.head(3)

google['Rolling_Mean'] = google['Open'].rolling(window = 80).mean()
#print(google.head(5))
filt_google = google[(google['Ticks'] >= 800) & (google['Ticks'] <= 1200)]
#se crea el modelo para la prediccion
model = LinearRegression().fit(filt_google[['Ticks']], filt_google[['Rolling_Mean']])
m = model.coef_[0]
b = model.intercept_
#print ('y = ', round(m[0],2), 'x + ', round(b[0],2))
#se crean predicciones a partir de datos proporcionados
predictions = model.predict(filt_google[['Ticks']])
#print(predictions[0:5])
#se crea un data frame para las predicciones 
predictions= pd.DataFrame(data=predictions,index=filt_google.index.values,columns=['Pred'])

joined_df=filt_google.join(predictions,how='inner')

#se calcula el error de las predicciones en comparacion del valor real
r_squared = sklearn.metrics.r2_score(joined_df['Rolling_Mean'],joined_df['Pred'],multioutput='uniform_average')
#print(r_squared)
texto='Prediction error '+str(r_squared)

x=joined_df['Ticks'].head(100)
y=joined_df['Rolling_Mean'].head(100)

fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
#print("Model parameters: %s" %  fp1)

#f(x) = 2.59619213 * x + 989.02487106

f1 = sp.poly1d(fp1)
ef1=error(f1, x, y)

f2p = sp.polyfit(x, y, 7)
f2 = sp.poly1d(f2p)
ef2=error(f2, x, y)


fx = sp.linspace(min(x.index.values),max(x.index.values)+10, 100) # generate X-values for plotting
plt.plot(fx, f1(fx), linewidth=3,color = (0,0,0))
plt.plot(fx, f2(fx), linewidth=3,color = (0,1,0))
plt.legend(["d="+str(f1.order)+" Error="+str(ef1),"d="+str(f2.order)+" Error="+str(ef2)], loc="upper left")
plt.scatter(x,y,color = (1,0,0))
plt.autoscale(tight=True)
plt.show()
fx = sp.linspace(max(x.index.values),max(x.index.values)+10)
pred=f2(fx)
print("\n\nPrediccion")
print(pred)

print("\n\nDatos")
print(joined_df.head(10))

#fig = plt.figure();
#ax = fig.add_subplot(111);

#ax.plot(joined_df['Ticks'], joined_df['Rolling_Mean'], color = (0,0,0), linewidth = 4, alpha = .9, label = 'Prediction');
#ax.plot(joined_df['Ticks'], joined_df['Pred'], color = (1,0,0), label = texto);
#ax.set_title('Rolling Mean vs Linear Regression')
#ax.set_xlabel('Ticks')
#ax.set_ylabel('Price')
#ax.legend(loc='lower right');



"""fig, axes = plt.subplots(nrows = 1, ncols = 3, figsize = (15,5));
axes[0].plot('Ticks', 'Open', data = google);
axes[0].set_title('Original');
axes[1].plot('Ticks', 'Open', data = one_tenth);
axes[1].set_title('Sampled');
axes[2].plot('Ticks', 'Rolling_Mean', data = google);
axes[2].set_title('Smoothed (Rolling_Mean)');"""