import pandas as pd
import math
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.model_selection import GridSearchCV, train_test_split
from mpl_toolkits.mplot3d import Axes3D 
from sklearn.datasets import make_circles

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


data = pd.read_csv("../data/data_all_float.csv", header=0, index_col=None, sep=';')
data = data[['Hardness, Vickers', 'Elongation at Break', 'Tensile Strength, Yield']]

features = ['Hardness, Vickers', 'Elongation at Break']
target = ['Tensile Strength, Yield']

# drop instances with NaN
drop_instance = []
for idx in data.index:
    if True in [math.isnan(x) for x in data.loc[idx]]:
        drop_instance.append(idx)
data = data.drop(drop_instance)

stdscale = StandardScaler(copy=True, with_mean=True, with_std=True)
X = data.drop(target, axis=1).values
y = data[target].values.reshape(-1, 1)

X = stdscale.fit_transform(X)
y = stdscale.fit_transform(y)

hyper_params = [{
    'kernel' : ('linear',),
}]



#X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, test_size=0.25, random_state=0)
#regressor = svm.SVC()
#grid_clf = GridSearchCV(regressor, cv=5, param_grid=hyper_params,
#                        verbose=1, n_jobs=2, scoring='r2')
#grid_clf.fit(X_train, y_train.ravel())
#X1 = X[:, 0].reshape((-1, 1))
#X2 = X[:, 1].reshape((-1, 1))
#X3 = (X1**2 + X2**2)
#X = np.hstack((X, X3))
#svc = svm.SVC(kernel = 'linear')
#svc.fit(X, y)
#w = svc.coef_
#b = svc.intercept_

#grid_clf.predict(X_test)

# plot results
fig = plt.figure()
# plot data
axes2 = fig.add_subplot(111, projection = '3d')
ind = np.nonzero(y >= 1)[0]
axes2.scatter(X[ind, 0], X[ind, 1], y[ind], depthshade = True)
ind = np.nonzero(y < 1)[0]
axes2.scatter(X[ind, 0], X[ind, 1], y[ind], depthshade = True)
# separating hyperplane
#x1 = X[:, 0].reshape(-1, 1)
#x2 = X[:, 1].reshape(-1, 1)
#x1, x2 = np.meshgrid(x1, x2)
#x3 = -(w[0][0]*x1 + w[0][1]*x2 + b) / w[0][2]
#axes1 = fig.gca(projection = '3d')
#axes1.plot_surface(x1, x2, x3, alpha = 0.01)
plt.xlabel(features[0])
plt.ylabel(features[1])
plt.title(target)
plt.show()

#fig = plt.figure()
#axes = fig.add_subplot(111, projection = '3d')
#axes.scatter(X[:, 0], X[:, 1], y, depthshade = True)
#plt.xlabel(features[0])
#plt.ylabel(features[1])
#plt.title(target)
#plt.show()

    #plot data
#ind = np.nonzero(y >= 1)[0]
#plt.plot(X[ind, 0], X[ind, 1], 'ro', markersize=4)
#ind = np.nonzero(y < 1)[0]
#plt.plot(X[ind, 0], X[ind, 1], 'b^', markersize=4)
#plt.xlabel(features[0])
#plt.ylabel(features[1])
#plt.title(target[0])
#plt.show()
