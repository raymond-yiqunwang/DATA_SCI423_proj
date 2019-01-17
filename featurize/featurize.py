from collections import defaultdict
import pandas as pd
import os

## select features and convert from strings to floating point numbers

features_dict = defaultdict(int)

ddir = "../scrape_data/data_raw/"
for filename in os.listdir(ddir):
    data = pd.read_csv(ddir+filename, header=0, index_col=0)
    for ind in data.index:
        features_dict[ind] += 1

print(' These are the potential features:')
for ii in sorted(features_dict.items(), key=lambda tup: tup[-1], reverse=True):
    if (ii[-1] > 100) and (ii[0] is not ' '):
        print(ii)
print('')

elem_list = ['Iron, Fe', 'Carbon, C', 'Sulfur, S', 'Silicon, Si', 'Phosphorous, P', 'Manganese, Mn', 'Chromium, Cr', 'Nickel, Ni', 'Molybdenum, Mo', 'Copper, Cu']

prop_list = ['Density', 'Hardness, Vickers', 'Thermal Conductivity', 'Specific Heat Capacity', 'CTE, linear', 'Electrical Resistivity', 'Elongation at Break',
             'Bulk Modulus', 'Modulus of Elasticity', 'Shear Modulus', 'Poissons Ratio', 'Tensile Strength, Yield', 'Tensile Strength, Ultimate']

feature_list = elem_list + prop_list
nfeature = len(feature_list)

# collect features from files
data_all_string = []
for filename in os.listdir(ddir):
    instance = ['0%']*len(elem_list) + ['NA']*len(prop_list) # initialize instance row
    data = pd.read_csv(ddir+filename, header=0, index_col=0)
    for ii in range(nfeature):
        if feature_list[ii] in data.index:
            instance[ii] = data.loc[feature_list[ii], 'Metric']
            if '\n' in instance[ii]: instance[ii] = instance[ii].replace('\n', ' ') # get rid of some unexpected '\n' in dataset
    if instance[0] is not 0: data_all_string.append(instance) # steel only

# convert to DataFrame and save to file
data_all_string = pd.DataFrame(data_all_string, index=None, columns=feature_list)
data_all_string.to_csv(path_or_buf="../data/data_all_string.csv", sep=';', index=False)

# define util function
def extract_float(string):
    if string is 'NA': return string # do not process non-available data
    num1 = ''
    num2 = ''
    curr = 0
    while not string[curr].isdigit(): # locate the first digit
        curr += 1
    # process the first float
    assert(string[curr].isdigit())
    while string[curr].isdigit():
        num1 += string[curr]
        curr += 1
        if curr == len(string): return float(num1)
    if string[curr] is '.':
        num1 += '.'
        curr += 1
        while string[curr].isdigit():
            num1 += string[curr]
            curr += 1
            if curr == len(string): return float(num1)
    # check if there is a second
    while string[curr].isspace():
        curr += 1
    if string[curr] is not '-':
        return float(num1)
    else: # process the second float
        curr += 1
    while string[curr].isspace():
        curr += 1
    assert(string[curr].isdigit())
    while string[curr].isdigit():
        num2 += string[curr]
        curr += 1
        if curr == len(string): return (float(num1) + float(num2)) / 2.0
    if string[curr] is '.':
        num2 += '.'
        curr += 1
        while string[curr].isdigit():
            num2 += string[curr]
            curr += 1
            if curr == len(string): return (float(num1) + float(num2)) / 2.0
    return (float(num1) + float(num2)) / 2.0


# convert string to float
data_all_float = pd.DataFrame(data=data_all_string, copy=True)
for ii in range(data_all_float.shape[0]):
    for jj in range(data_all_float.shape[1]):
        data_all_float.iloc[ii, jj] = extract_float(data_all_float.iloc[ii, jj])

# drop instances whose Fe weight is less than 50%
drop_list = []
for ii in data_all_float.index:
    if data_all_float.loc[ii, 'Iron, Fe'] < 80.:
        drop_list.append(ii)
data_all_float = data_all_float.drop(drop_list)

print('Shape of data: ', data_all_float.shape)
data_all_float.to_csv("../data/data_all_float.csv", sep=';', index=False)

