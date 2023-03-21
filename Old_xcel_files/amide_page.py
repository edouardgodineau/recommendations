import bigtree as bt
import streamlit as st
from Utils.data_preparation import *
#need to use Chemistry_recommendations.Utils.[filename] to make it work in pycharm
#need to use Utils.[filename] to get the app to work within streamlit

path = "Utils/Recommendations.xlsx"
# path = "Recommendations.xlsx"
sheetname = "Amide_coupling_App"

df = load_data(path, sheetname)
df = build_recommendation(df)
df = build_tree_nodes(df)
tree = build_dict(df)
root = bt.dict_to_tree(tree)


def print_additionnal_info(result):
    if result.get('eln') != '':
        print(f"ELN reference: {result.get('eln')}")
    else:
        print("We unfortunately don't have any ELN reference to recommend. We are working on it!")
    # if result.get('reference') != '':
    #     print(f"Literature reference: {result.get('reference')}")
    if result.get('comments') != '':
        print(f"Comment: {result.get('comments')}")

def show_page():

    # Define custom CSS styles
    st.write("<h1>Recommended methods to prepare amides</h1>", unsafe_allow_html = True)


    standard_conditions = root.node_name

    st.write(f'For carboxylic acid which {standard_conditions} the following condition(s) are recommended:')

    result = bt.find(root, lambda node: node.name == standard_conditions).get_attr('conditions#')
    for result in result:
        st.markdown(f"{result.get('rating')} | {result.get('recommendation')}")
        if result.get('eln') != '':
            st.markdown(f"ELN reference: {result.get('eln')}")
        else:
            st.markdown("We unfortunately don't have any ELN reference to recommend. We are working on it!")
        if result.get('comments') != '':
            st.markdown(f"Comment: {result.get('comments')}")
        if result.get('reference') != '':
            st.markdown(f"Reference: [{result.get('reference')}]({result.get('link')})")

    print('Standard conditions did not work because the carboxylic acid (choose from the list below):')
    alternatives_1 = [i.name for i in root.children]

    st.markdown("---")
    label_text = '<span style="font-size: 16px; font-weight: bold;">The standard conditions did not work because the carboxylic acid:</span>'

    container_style = 'display: flex; flex-direction: column; align-items: flex-start;'

    st.markdown(f'<div style="{container_style}">{label_text}', unsafe_allow_html=True)

    # problem = st.selectbox('', ["", *alternatives_1])
    problem = st.selectbox('', ['Please choose an option'] + alternatives_1)
    st.markdown('</div>', unsafe_allow_html=True)


    for alternative in alternatives_1:
        if alternative == problem:
            st.write(f"For a carboxylic acid which {alternative}, here are alternative conditions which are recommended:")
            results = bt.find(root, lambda node: node.name == alternative).get_attr('conditions#')
            for i in range(3):
                for result in results:
                    if i == result.get('rating')-1:
                        st.markdown(f"{result.get('rating')} | {result.get('recommendation')}")
                        if result.get('eln') != '':
                            st.markdown(f"ELN reference: {result.get('eln')}")
                            # st.code(f"Clone this eln: {result.get('eln')}")
                        else:
                            st.markdown("We unfortunately don't have any ELN reference to recommend. We are working on it!")
                        if result.get('comments') != '':
                            st.markdown(f"Comment: {result.get('comments')}")
                        if result.get('reference') != '':
                            st.markdown(f"Reference: [{result.get('reference')}]({result.get('link')})")
                        st.markdown("---")





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
print('amide_page', __name__)