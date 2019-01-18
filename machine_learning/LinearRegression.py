import numpy as np
import pandas as pd
import sys
import operator
import math
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import *
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


data = pd.read_csv("../data/data_all_float.csv", header=0, index_col=None, sep=';')

# drop 'CTE, linear' for more instances to study
drop_feature = ['CTE, linear'] 
data = data.drop(labels=drop_feature, axis=1)

# drop instances with NaN
drop_instance = []
for idx in data.index:
    if True in [math.isnan(x) for x in data.loc[idx, data.columns.values]]:
        drop_instance.append(idx)
data = data.drop(drop_instance)
print('The shape of data after modification: ', data.shape)

hyper_params = [{
    'fit_intercept': (False, True),
}]

stdscale = StandardScaler()

target = 'Tensile Strength, Yield'
X = data.drop(target, axis=1).values
y = data[target].values

# standardize features
X = stdscale.fit_transform(X)
y = stdscale.fit_transform(y.reshape(-1, 1))

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75, test_size=0.25, random_state=0)

regressor = linear_model.LinearRegression()

grid_clf = GridSearchCV(regressor, cv=5, param_grid=hyper_params,
                        verbose=0, n_jobs=8, scoring='r2')

grid_clf.fit(X_train, y_train.ravel())


"""

    train_score_mse = mean_squared_error(stdscal.inverse_transform(y_train),stdscal.inverse_transform(grid_clf.predict(X_train)))
    test_score_mse = mean_squared_error(stdscal.inverse_transform(y_test),stdscal.inverse_transform(grid_clf.predict(X_test)))

    sorted_grid_params = sorted(grid_clf.best_params_.items(), key=operator.itemgetter(0))

    # print results
    out_text = '\t'.join([data_name.split('/')[-1][:-7], 'linear-regression',
                          str(sorted_grid_params).replace('\n',','), str(train_score_mse), str(test_score_mse)])

    print(out_text)
    sys.stdout.flush()
"""
