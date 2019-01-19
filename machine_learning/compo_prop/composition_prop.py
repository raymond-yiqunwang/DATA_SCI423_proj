import numpy as np
import pandas as pd
import sys
import operator
import math

import xgboost
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import *

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)


data = pd.read_csv("../../data/data_all_float.csv", header=0, index_col=None, sep=';')

# drop 'CTE, linear' for more instances to study
drop_feature = ['Density', 'CTE, linear']
for ifeature in drop_feature:
    data = data.drop(labels=ifeature, axis=1)


hyper_params = [{
    'n_estimators' : (10, 50, 100, 250, 500, 1000,),
    'learning_rate' : (0.0001,0.01, 0.05, 0.1, 0.2,),
    'gamma' : (0,0.1,0.2,0.3,0.4,),
    'max_depth' : (6,),
    'subsample' : (0.5, 0.75, 1,),
}]

stdscale = StandardScaler()

properties = [ 'Thermal Conductivity', 'Specific Heat Capacity', 'Hardness, Vickers', 'Electrical Resistivity', 'Elongation at Break',
               'Bulk Modulus', 'Modulus of Elasticity', 'Shear Modulus', 'Poissons Ratio', 'Tensile Strength, Yield', 'Tensile Strength, Ultimate']

elements = ['Iron, Fe', 'Carbon, C', 'Sulfur, S', 'Silicon, Si', 'Phosphorous, P', 'Manganese, Mn', 'Chromium, Cr', 'Nickel, Ni', 'Molybdenum, Mo', 'Copper, Cu']

for target in properties:
    print('current target: ', target)
    
    # drop instances with NaN
    drop_instance = []
    for idx in data.index:
        if math.isnan(data.loc[idx, target]):
            drop_instance.append(idx)
    data_loc = data.drop(drop_instance)
    X = data_loc[elements].values
    y = data_loc[target].values
    
    print('Shape of dataset:')
    print(X.shape)
    
    # standardize features
    X = stdscale.fit_transform(X)
    y = stdscale.fit_transform(y.reshape(-1, 1))
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, test_size=0.25, random_state=0)
    
    regressor = xgboost.XGBRegressor()
    
    grid_clf = GridSearchCV(regressor, cv=5, param_grid=hyper_params,
                            verbose=1, n_jobs=8, scoring='r2')
    
    grid_clf.fit(X_train, y_train.ravel())
    
    train_score_mse = mean_squared_error(stdscale.inverse_transform(y_train), stdscale.inverse_transform(grid_clf.predict(X_train)))
    test_score_mse = mean_squared_error(stdscale.inverse_transform(y_test), stdscale.inverse_transform(grid_clf.predict(X_test)))
    
    sorted_grid_params = sorted(grid_clf.best_params_.items(), key=operator.itemgetter(0))
    
    # print results
    out_txt = '\t'.join(['algorithm: ', str(sorted_grid_params).replace('\n', ','), str(train_score_mse), str(test_score_mse)])
    print('best score:')
    print(grid_clf.best_score_)
    print('test score:')
    print(grid_clf.score(X_test, y_test))
    
    print(out_txt)
    print("")
    sys.stdout.flush()
