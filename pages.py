import pandas as pd
import numpy as np
import re

pd.set_option('display.max_columns', None)
data = pd.read_excel('Recommendations__.xlsx', sheet_name="Amide_coupling_App")


def format_data(df: pd.DataFrame) -> pd.DataFrame:
    equiv = [col for col in df.columns if "equiv" in col]
    unit = [col for col in df.columns if "unit" in col]
    for col in equiv:
        df[col] = " ("+ df[col].astype(str) + " eq.)" if df[col].notna().all() else ""
    for col in unit:
        df[col] = " " + df[col].astype(str) if df[col].notna().all() else ""
    return df

data = format_data(data)


def build_pairs(df: pd.DataFrame) -> list:
    """
    Build pairs of columns from a dataframe
    :param df: dataframe
    :return: list of pairs
    """
    params = [col.split('_')[0] for col in df.columns if "_equiv" in col or "_value" in col]
    cols = []
    for param in params:
        param_value_unit = [col for col in df.columns if param in col]
        cols.append(param_value_unit)
    return cols


def prepare_params(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare parameters for the recommendation
    :param df: dataframe
    :return: dictionary of parameters
    """
    params = build_pairs(df)

    for param in params:
        to_drop = [col for col in param if col not in param[0]]

        df[param[0]] = df[param].apply(lambda x: ''.join(x.dropna().astype(str)), axis=1)
        if "_value" in param[0]:
            col = re.sub("_value", "", param[0])
            df[col] = df[param[0]]
            to_drop.append(param[0])

        df = df.drop(to_drop, axis=1)
    return df


data = prepare_params(data)
print(data)




# # View the resulting column pairs
#
# # data['recommendation'] = data[cols].apply(lambda x: ', '.join(x.dropna().astype(str)), axis=1)
# data['recommendation'] = data[cols].apply(lambda x: ', '.join([str(i) for i in x if pd.notna(i) and str(i) != 'nan']), axis=1)
#
# print(data['recommendation'].head())

# df = data.recommendation
# df.to_json('recommendations4amide.json')
#
#
# import json
#
#
# with open('recommendations4amide.json', 'r') as f:
#     data = json.loads(f.read())
#
# amide1 = []
# for i in range(3):
#     reco = f'Top{i+1} condition: {data[str(i)]}'
#     amide1.append(reco)
#
# print(amide1)


