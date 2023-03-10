import pandas as pd
import numpy as np

data = pd.read_excel('Recommendations__.xlsx', sheet_name="Amide_coupling_App")
# print(data.head())
data['amine_equiv_'] = data.amine_equiv.apply(lambda x: str(x))
# data['recommendation'] = data.carboxylic_acid + '(1 equiv.), ' +\
#                          data.amine + '(' + data.amine_equiv_ +' equiv.),'+ data.base + data.Column1 + data.coupling_agent +

for col in data.select_dtypes(np.number):
col_ = f'{col}_'
if "equiv" in col:
    data[col] = data[col].apply(lambda x: '(' + str(x) + ' eq.)')
else:
    data[col] = data[col].apply(lambda x: str(x))

# print(data.dtypes)


cols_recommended = ['carboxylic_acid',
                'carboxylic_acid_equiv',
                'amine',
                'amine_equiv',
                'base',
                'base_equiv',
                'coupling_agent',
                'coupling_agent_equiv',
                'Solvent',
                'Temperature',
                'Reference',
                'ELN',
                'Comments'
                ]

prefixes = {}

# Loop through each column name
for col_name in cols_recommended:
# Extract the prefix of the column name
prefix = col_name.split('_')[0]

# Add the column name to the prefix dictionary
if prefix in prefixes:
    prefixes[prefix].append(col_name)
else:
    prefixes[prefix] = [col_name]

# Create a list of pairs from the prefix dictionary
column_pairs = [v for v in prefixes.values()]

cols = []
for v in column_pairs:
data[v[0]] = data[v].apply(lambda x: " ".join(x.astype(str)), axis=1)
cols.append(v[0])

# View the resulting column pairs

# data['recommendation'] = data[cols].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
data['recommendation'] = data[cols].apply(lambda x: ', '.join([str(i) for i in x if pd.notna(i) and str(i) != 'nan']), axis=1)


df = data.recommendation
df.to_json('recommendations4amide.json')


import json


with open('recommendations4amide.json', 'r') as f:
data = json.loads(f.read())

amide1 = []
for i in range(3):
reco = f'Top{i+1} condition: {data[str(i)]}'
amide1.append(reco)

print(amide1)

def proce