from collections import defaultdict
import pandas as pd
import os

features_all = defaultdict(int)

ddir = "./scrape_data/data_raw/"
for filename in os.listdir(ddir):
    data = pd.read_csv(ddir+filename, header=0, index_col=0)
    for ind in data.index:
        features_all[ind] += 1

print(' These are the potential features:')
for ii in sorted(features_all.items(), key=lambda tup: tup[-1], reverse=True):
    if (ii[-1] > 100) and (ii[0] is not ' '):
        print(ii)
