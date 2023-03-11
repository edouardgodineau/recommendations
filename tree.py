import pandas as pd
from bigtree import Node, print_tree, dict_to_tree, print_tree, dataframe_to_tree, find, findall
import bigtree as bt

import json
# with open('recommendations4amide.json', 'r') as f:
#     data = json.loads(f.read())

# data = pd.read_excel('Recommendations__.xlsx', sheet_name="Amide_coupling_tree")
with open('result_dict.json', 'r') as f:
    path = json.loads(f.read())


root = dict_to_tree(path)


# print_tree(root, attr_list=["conditions#"])

root_name = ['standard', 'decomposition', 'unreactive']

for amide_class in root_name:
    res = bt.find(root, lambda node: node.name ==amide_class).get_attr('conditions#')
    print(f"\nFor {amide_class} type of amide:")
    for res in res:
        print(f"rating: {res.get('rating')}\nrecommended condition: {res.get('recommendation')}")


import bigtree

import bigtree

# Assume root is the root node of the tree
import bigtree

# Assume root is the root node of the tree
# node_names = []
#
# def get_node_name(node):
#     node_names.append(node.name)
#
# nodes = root.findall('*')
# for node in nodes:
#     get_node_name(node)
#
# print(node_names)


import bigtree

import bigtree

# Assume root is the root node of the tree
import bigtree

# Assume root is the root node of the tree

# def get_node_name(node):
#     node_names.append(node.name)
#     for child in node.children:
#         get_node_name(child)

def get_node_name(node):
    node_names = [node.name]
    for child in node.children:
        node_names += get_node_name(child)
    return node_names

# node_names = []
node_names = get_node_name(root)

print(node_names)

