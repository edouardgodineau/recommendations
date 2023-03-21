import re

import pandas as pd

# import bigtree as bt
# import pprint


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)



def load_data(path: str, sheetname:str)-> pd.DataFrame:
    data = pd.read_excel(io=path, sheet_name=sheetname)
    return data

def format_data(df: pd.DataFrame) -> pd.DataFrame:
    equiv = [col for col in df.columns if "equiv" in col]
    unit = [col for col in df.columns if "unit" in col]

    for idx, row in df.iterrows():
        for col in equiv:
            df.loc[idx, col] = " (" + str(df.loc[idx, col]).replace('nan', '') + " eq.)" if pd.notna(df.loc[idx, col]) else ""

        for col in unit:
            df.loc[idx, col] = str(df.loc[idx, col]).replace('nan', '') if pd.notna(df.loc[idx, col]) else ""

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

from dataclasses import dataclass, field


@dataclass
class ExcelData:
    file_path: str
    sheetname: str
    level1: pd.Series = field(init=False)
    level2: pd.Series = field(init=False)
    level3: pd.Series = field(init=False)
    level4: pd.Series = field(init=False, default=None)
    level5: pd.Series = field(init=False, default=None)
    level6: pd.Series = field(init=False, default=None)
    level7: pd.Series = field(init=False, default=None)
    level8: pd.Series = field(init=False, default=None)
    level9: pd.Series = field(init=False, default=None)
    ranking: pd.Series = field(init=False)

    def __post_init__(self):
        self.df = pd.read_excel(io=self.file_path, sheet_name=self.sheetname)
        self.columns = self.df.columns
        for n in range(1,10):
            level = "level"+str(n)
            Level_n = "Level_"+str(n)
            if "Level_"+str(n) in self.df.columns:
                setattr(self, level, self.df[Level_n])
        self.ranking = self.df['ranking']
        self.reference = self.df['reference']
        self.ELN = self.df['ELN']
        self.link = self.df['link']
        self.comments = self.df['Comments']
        static_cols = ['Level_1', 'Level_2', 'Level_3','ranking', 'reference', 'ELN', 'link', 'Comments']
        self.conditions_columns = [col for col in self.df.columns if col not in static_cols]
        self.conditions = self.df[self.conditions_columns]
        self.recommendation = None

@dataclass
class Recommendation:
    df: ExcelData

    def build_recommendation(self):
        self.df.recommendation = self.df.conditions.apply(lambda x: ', '.join([str(i) for i in x if pd.notna(i) and str(i) != '']), axis=1)
        return self.df


@dataclass
class Tree:
    df: ExcelData
    tree: pd.Series = field(init=False)

    def build_nodes(self):
        levels = []
        for level in range(1, 10):
            if hasattr(self.df, f"level{level}"):
                levels.append(getattr(self.df, f"level{level}"))
        df_concatenated = pd.concat(levels, axis=1)
        self.df.tree = df_concatenated.apply(lambda x: ".".join(x.dropna().astype(str)), axis=1)
        return self.df.tree



file_path = "../Chemistry_recommendations/Utils/Recommendations.xlsx"
sheetname = "Amide_coupling_App_"

amide = ExcelData(file_path, sheetname)
print(Tree(amide).build_nodes())
# print(amide.df.columns)



