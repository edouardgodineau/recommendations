import pandas as pd
import re
import bigtree as bt
import pprint


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
# data = pd.read_excel('Recommendations__.xlsx', sheet_name="Amide_coupling_App")
path = 'Recommendations__.xlsx'
sheetname = "Amide_coupling_App"
def load_data(path: str, sheetname:str)-> pd.DataFrame:
    data = pd.read_excel(io=path, sheet_name=sheetname)
    return data

def format_data(df: pd.DataFrame) -> pd.DataFrame:
    equiv = [col for col in df.columns if "equiv" in col]
    unit = [col for col in df.columns if "unit" in col]
    # remaining = ['reference', 'link', 'ELN', 'Comments']

    for idx, row in df.iterrows():
        for col in equiv:
            df.loc[idx, col] = " (" + str(df.loc[idx, col]).replace('nan', '') + " eq.)" if pd.notna(df.loc[idx, col]) else ""

        for col in unit:
            df.loc[idx, col] = str(df.loc[idx, col]).replace('nan', '') if pd.notna(df.loc[idx, col]) else ""
        # for col in remaining:
        #     df.loc[idx, col] = str(df.loc[idx, col]).replace('nan', '') if pd.notna(df.loc[idx, col]) else ""
            # df.loc[idx, col] = "" if pd.notna(df.loc[idx, col]) else df.loc[idx, col]
    return df



def build_pairs(df: pd.DataFrame) -> list:
    """
    Build pairs of columns from a dataframe
    :param df: dataframe
    :return: list of pairs
    """
    df = format_data(df)
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


def build_recommendation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build recommendation
    :param df: dataframe
    :return: dataframe
    """
    df = prepare_params(df)

    additionnal_info = ['Level_1', 'Level_2','Level_3', 'reaction', 'conditions#', 'results', 'reference', 'link', 'ELN', 'Comments']
    cols = [col for col in df.columns if col not in additionnal_info]
    df['recommendation'] = df[cols].apply(lambda x: ', '.join([str(i) for i in x if pd.notna(i) and str(i) != '']), axis=1)
    return df

def get_node_name(node):
    node_names = [node.name]
    for child in node.children:
        node_names += get_node_name(child)
    return node_names




# recommended_cols = ['reaction', 'results', 'conditions#', 'recommendation', 'reference', 'link', 'ELN', 'Comments']
# out = df[recommended_cols]
#
# out.to_json('recommendations4amide.json')
# out.to_csv('recommendations4amide.csv', sep='\t', index=False)


def build_tree_nodes(df: pd.DataFrame) -> pd.DataFrame:
    levels = [col for col in df.columns if "Level" in col]
    df['tree'] = df[levels].apply(lambda x: '/'.join(x.dropna().astype(str)), axis=1)
    return df


def build_dict(df: pd.DataFrame) -> dict:
    """
    Build dictionary of recommendations
    :param df: dataframe
    :return: dictionary
    """
    result_dict = {}
    for tree, group in df.groupby('tree'):
        conditions_list = []
        for index, row in group.iterrows():
            rating = row['conditions#']
            recommendation = row['recommendation']
            eln = row['ELN'] if pd.notna(row['ELN']) else ""
            comments = row['Comments'] if pd.notna(row['Comments']) else ""
            reference = row['reference'] if pd.notna(row['reference']) else ""
            link = row['link'] if pd.notna(row['link']) else ""
            conditions_list.append({'rating': rating, 'recommendation': recommendation,'eln':eln, 'comments': comments, 'reference': reference, 'link': link})
        result_dict[tree] = {'conditions#': conditions_list}
    return result_dict

df = load_data(path, sheetname)
df = build_recommendation(df)
df = build_tree_nodes(df)
tree = build_dict(df)
root = bt.dict_to_tree(tree)

# node_name = get_node_name(root)
# print(node_name)
# for i in root.children:
#     print(i.name)
#     for j in i.children:
#         print(j.name)

# print(root.descendants)