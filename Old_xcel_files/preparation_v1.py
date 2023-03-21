from dataclasses import dataclass, field
import pandas as pd
from bigtree import dict_to_tree, print_tree


pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)

@dataclass
class ExcelData():
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
    df: pd.DataFrame = field(init=False)
    ranking: pd.Series = field(init=False)
    ELN: pd.Series = field(init=False)
    link: pd.Series = field(init=False)
    reference: pd.Series = field(init=False)
    comments: pd.Series = field(init=False)
    conditions_columns: list = field(init=False)
    conditions: pd.DataFrame = field(init=False)
    recommendation: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.df = pd.read_excel(io=self.file_path, sheet_name=self.sheetname)

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

    def build_recommendation(self):
        self.df['recommendation'] = self.conditions.apply(
            lambda x: ', '.join([str(i) for i in x if pd.notna(i) and str(i) != '']), axis=1)
        return self.df


@dataclass
class Tree:
    data: ExcelData
    tree_nodes: pd.Series = field(init=False)
    leaves_content = {}
    root = None


    def build_nodes(self):
        levels = []
        for level in range(1, 10):
            if hasattr(self.data, f"level{level}"):
                levels.append(getattr(self.data, f"level{level}"))
        df_concatenated = pd.concat(levels, axis=1)
        self.tree_nodes = df_concatenated.apply(lambda x: "/".join(x.dropna().astype(str)), axis=1)
        self.data.df['nodes'] = self.tree_nodes
        return self.data.df

    def build_dict4tree(self):
        for self.tree_nodes, group in self.data.df.groupby('nodes'):
            for index, row in group.iterrows():
                leaf = {}
                for col in self.data.df.columns:
                    attribute_name = col
                    ranking = row[attribute_name]
                    if not pd.isna(ranking):
                        leaf[attribute_name] = ranking
                self.leaves_content[str(self.tree_nodes)] = leaf

        return self.leaves_content

    def build_tree(self):
        self.root = dict_to_tree(self.leaves_content)
        return self.root

    def print_tree(self):
        print_tree(self.root)
        return




# file_path = "Recommendations.xlsx"
# sheetname = "Amide_coupling_App_"
#
# # Load data for the reaction class and build the recommendations
# amide = ExcelData(file_path, sheetname)
# amide.build_recommendation()
#
# # Build the tree for the reaction class
# Tree(amide).build_nodes()
# Tree(amide).build_dict4tree()
# # root = Tree(amide).build_tree()
# root = Tree(amide).build_tree()
# print_tree(root)





