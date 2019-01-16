from collections import defaultdict
import pandas as pd
import os

features = defaultdict(int)

ddir = "./scrape_data/data_raw/"
for filename in os.listdir(ddir):
    data = pd.read_csv(ddir+filename, header=0, index_col=0)
    for ind in data.index:
        features[ind] += 1


for ii in sorted(features.items(), key=lambda tup: tup[-1], reverse=True):
    print(ii)
