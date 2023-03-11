import streamlit as st
from pages import *
import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.absolute()).split("/src")[0]+ "/src")


df = load_data(path, sheetname)
df = build_recommendation(df)
df = build_tree_nodes(df)
tree = build_dict(df)
root = bt.dict_to_tree(tree)

node_name = get_node_name(root)
# print(node_name)

def print_additionnal_info(result):
    if result.get('eln') == '':
        print("We unfortunately don't have any ELN reference to recommend. We are working on it!")
    else:
        print(f"ELN reference: {result.get('eln')}")
    if result.get('reference') != '':
        print(f"Literature reference: {result.get('reference')}")
    if result.get('comments') != '':
        print(f"Comment: {result.get('comments')}")

def show_page():

    # Define custom CSS styles
    standard_conditions = root.node_name
    # print(f'For carboxylic acid which {standard_conditions} the following condition(s) are recommended:')
    st.write(f'For carboxylic acid which {standard_conditions} the following condition(s) are recommended:')

    result = bt.find(root, lambda node: node.name == standard_conditions).get_attr('conditions#')
    # for result in result:
    #     print(f"{result.get('rating')} | recommended condition: {result.get('recommendation')}")
    #     print_additionnal_info(result)
    for result in result:
        st.markdown(
            f"{result.get('rating')} | recommended condition: {result.get('recommendation')}\n{print_additionnal_info(result)}")

    print('Standard conditions did not work because:')
    alternatives_1 = [i.name for i in root.children]

    problem = st.selectbox("Problem observed", alternatives_1)
    # problem = 'decomposes'

    # if amide == "normal":
    # # st.write("For carboxylic adic having a normal reactivity, here are 3 conditions which are recommended:")
    # #     st.markdown(amide1[0])
    # #     st.markdown(amide1[1])
    # #     st.markdown(amide1[2])


    for alternative in alternatives_1:
        if alternative == problem:
            st.write(f"For a carboxylic acid which {alternative}, here are 3 conditions which are recommended:")
            result = bt.find(root, lambda node: node.name == alternative).get_attr('conditions#')
            for result in result:
                st.markdown(f"{result.get('rating')} | recommended condition: {result.get('recommendation')}\n{print_additionnal_info(result)}")

                # if result.get('eln') == '':
                #     print("We unfortunately don't have any ELN reference to recommend. We are working on it!")
                # else:
                #     print(f"ELN reference: {result.get('eln')}")
                # if result.get('reference') != '':
                #     print(f"Literature reference: {result.get('reference')}")
                # if result.get('comments') != '':
                #     print(f"Comment: {result.get('comments')}")



    # st.write(f'For amides {amide_classes[0]}, the following condition(s) are recommended:')
    #
    # amide = (
    #     "Please estimate the reactivity of the carboxylic acid you are working with",
    #     "normal",
    #     "unreactive",
    #     "highly sensitive",
    # )
    #
    #
    # amide = st.selectbox("Amide type", amide)
    #
    # if amide == "normal":
    #     st.write("For carboxylic adic having a normal reactivity, here are 3 conditions which are recommended:")
    #     st.markdown(amide1[0])
    #     st.markdown(amide1[1])
    #     st.markdown(amide1[2])
    #
    # if amide == "unreactive":
    #     st.write("For carboxylic adic having a normal reactivity, here are 3 conditions which are recommended:")
    #     st.markdown("Top condition1: ")
    #     st.markdown("Top condition2: ")
    #     st.markdown("Top condition3: ")
    #
    # if amide == "highly sensitive":
    #     st.write("Here are 3 conditions we recommend for you")
    #     st.markdown("1. Acid chloride, Amine 1.1 equiv., K2CO3 or NEt3 3.0 equiv., -, ACN or ethyl acetate, RT")
    #     st.markdown("3. Acid, Amine 1.1 equiv., NMI 3.0 equiv., TCFH 2.0 equiv., ACN or ethyl acetate, RT, Clone this eln: 22-6615\nCheck out this [Org. Lett. 2020, 22, 5737](https://doi.org/10.1021/acs.orglett.0c01676)")
    #     st.markdown("3.")

show_page()