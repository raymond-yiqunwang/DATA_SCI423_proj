import pandas as pd
import os

ddir = "./scrape_data/data_raw/"
for filename in os.listdir(ddir):
    data = pd.read_csv(ddir+filename)
    print(data.shape)
