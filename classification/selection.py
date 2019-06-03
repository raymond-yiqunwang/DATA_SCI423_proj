import pandas as pd
import math
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn import svm
from mpl_toolkits.mplot3d import Axes3D 
from sklearn.datasets import make_circles



data = pd.read_csv("../data/data_all_float.csv", header=0, index_col=None, sep=';')

properties = [ 'Thermal Conductivity', 'Specific Heat Capacity', 'Hardness, Vickers', 'Electrical Resistivity', 'Elongation at Break',
               'Bulk Modulus', 'Modulus of Elasticity', 'Shear Modulus', 'Poissons Ratio', 'Tensile Strength, Yield', 'Tensile Strength, Ultimate']

"""
elon, hard, tensile yield
elon, hard, tensile ult
tensile yield, hard, elon
tensile ult, hard, elon
tensile utl, hard, tensile yield
elon, tensile yield, hard
tensile yield, elon, tensile ult
elon, tensile ult, hard
tensile utl, elon, tensile yield
tensile yield, tensile ult, hard
tensile yield, tensile ult, elon
"""


stdscale = StandardScaler(copy=True, with_mean=True, with_std=True)

for i in range(len(properties)):
    for j in range(i+1, len(properties)):
        for k in range(len(properties)):
            if (k == i) or (k == j): continue
            # drop instances with NaN
            drop_instance = []
            for idx in data.index:
                if True in [math.isnan(x) for x in data.loc[idx, [properties[i], properties[j], properties[k]]]]:
                    drop_instance.append(idx)
            data_loc = data.drop(drop_instance)
            features = [properties[i], properties[j]]
            target = properties[k]
            X = stdscale.fit_transform(data_loc[features].values)
            y = stdscale.fit_transform(data_loc[target].values.reshape(-1, 1))
#    y = (y >= np.median(y)).astype(int)
            fig = plt.figure()
            axes = fig.add_subplot(111, projection = '3d')
            axes.scatter(X[:, 0], X[:, 1], y, depthshade = True)
            plt.xlabel(features[0])
            plt.ylabel(features[1])
            plt.title(target)
            plt.show()

    #plot data
#    ind = np.nonzero(y >= np.median(y))[0]
#    plt.plot(X[ind, 0], X[ind, 1], 'ro', markersize=4)
#    ind = np.nonzero(y < np.median(y))[0]
#    plt.plot(X[ind, 0], X[ind, 1], 'b^', markersize=4)
#    plt.xlabel(features[0])
#    plt.ylabel(features[1])
#    plt.title(targets[i])
#    plt.show()
