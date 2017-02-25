#http://scikit-learn.org/stable/modules/generated/sklearn.svm.libsvm.fit.html
#información hacerca del kernel
#http://scikit-learn.org/stable/tutorial/basic/tutorial.html
#http://pybonacci.org/2015/01/14/introduccion-a-machine-learning-con-python-parte-1/

import matplotlib.pyplot as plt
from sklearn import datasets 
from sklearn import svm

digits= datasets.load_digits()

#print(digits.data)
#print(digits.target)
#print(digits.images[0])


clf= svm.SVC(gamma=0.01,C=100)

number=-17
number2=-32

x,y=digits.data[:number],digits.target[:number]

#print(digits.target[:number])
clf.fit(x,y)

f,axarr = plt.subplots(1,2, sharex=True)
axarr[0].imshow(digits.images[number],cmap=plt.cm.gray_r,interpolation="nearest")
axarr[0].set_title('Prediction 1')
axarr[1].imshow(digits.images[number2],cmap=plt.cm.gray_r,interpolation="nearest")
axarr[1].set_title('Prediction 2')
print('Prediccion:',clf.predict(digits.data[number].reshape(1,-1)),clf.predict(digits.data[number2].reshape(1,-1)))

