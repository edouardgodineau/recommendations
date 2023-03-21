from dataclasses import dataclass, field
import pandas as pd
import bigtree as bt


# pd.set_option('display.max_columns', None)
# pd.set_option('display.width', 2000)


@dataclass
class Recommendation:
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
    data: pd.DataFrame = field(init=False)
    tree_nodes: pd.Series = field(init=False)
    nodes_unique = None
    recommendation = None
    leaves = None

    def __post_init__(self):
        self.data = pd.read_excel(io=self.file_path, sheet_name=self.sheetname)


        for n in range(1, 10):
            level = "level" + str(n)
            Level_n = "Level_" + str(n)
            if Level_n in self.data.columns and not self.data[Level_n].isnull().all():
                setattr(self, level, self.data[Level_n])
        self.data = self.data.fillna('')
        self.ranking = self.data['ranking']
        self.reference = self.data['reference']
        self.ELN = self.data['ELN']
        self.link = self.data['link']
        self.comments = self.data['comments']
        self.static_cols = [col for col in self.data.columns if "Level" in col] + ['ranking', 'reference', 'ELN', 'link', 'comments']
        self.conditions_columns = [col for col in self.data.columns if col not in self.static_cols]
        self.conditions = self.data[self.conditions_columns]

        return self

    def build_nodes(self):
        levels = []
        for level in range(1, 10):
            if hasattr(self, f"level{level}"):
                levels.append(getattr(self, f"level{level}"))
        df_concatenated = pd.concat(levels, axis=1)
        self.tree_nodes = df_concatenated.apply(lambda x: "/".join(x.dropna().astype(str)), axis=1)
        self.data['nodes'] = self.tree_nodes
        self.nodes_unique = list(set([self.tree_nodes[idx] for idx in self.data.index]))
        return self

    def build_recommendation(self):
        self.data['recommendation'] = self.conditions.apply(
            lambda x: ', '.join([str(i) for i in x if pd.notna(i) and str(i) != '']), axis=1)
        self.recommendation = self.data['recommendation']
        return self


    def build_dict4tree(self)  -> dict:
        self.leaves = {}
        for node in self.nodes_unique:
            list_of_recommendations = {}

            for idx, row in self.data.iterrows():

                if self.tree_nodes[idx] == node:
                    list_of_recommendations[str(self.ranking[idx])] = {
                                                    self.recommendation.name: self.recommendation[idx],
                                                    self.reference.name: self.reference[idx],
                                                    self.ELN.name: self.ELN[idx],
                                                    self.link.name: self.link[idx],
                                                    self.comments.name: self.comments[idx],
                                                    }
                    print(node)
                    print(list_of_recommendations)

            self.leaves[node] = list_of_recommendations
        return self.leaves