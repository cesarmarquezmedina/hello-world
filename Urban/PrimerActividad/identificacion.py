import pandas as pd 
import matplotlib.pyplot as plt

df=pd.read_csv('Dataset.csv')
df=df.head(32)

x=df['X']
y=df['Y']

plt.plot(x,y)
print(df)

