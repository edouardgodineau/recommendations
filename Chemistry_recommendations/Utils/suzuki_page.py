import bigtree as bt
import streamlit as st
from Utils.data_preparation import *
#need to use Chemistry_recommendations.Utils.[filename] to make it work in pycharm
#need to use Utils.[filename] to get the app to work within streamlit



path = "Utils/Recommendations__.xlsx"
# path = "Recommendations__.xlsx"
sheetname = "Suzuki_App"

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
    st.write("<h1>Recommended methods to perform Suzuki Cross couplings</h1>", unsafe_allow_html = True)


    standard_conditions = root.node_name

    st.write(f'The {standard_conditions} reaction conditions for Suzuki cross couplings are the following condition(s):')

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

    alternatives_1 = [i.name for i in root.children]

    st.markdown("---")
    label_text = '<span style="font-size: 16px; font-weight: bold;">The standard conditions above did not work because the:</span>'

    container_style = 'display: flex; flex-direction: column; align-items: flex-start;'

    st.markdown(f'<div style="{container_style}">{label_text}', unsafe_allow_html=True)

    # problem = st.selectbox('', ["", *alternatives_1])
    problem = st.selectbox('', ['Please choose an option'] + alternatives_1)
    st.markdown('</div>', unsafe_allow_html=True)


    for alternative in alternatives_1:
        if alternative == problem:
            st.write(f"If the {alternative}, here are alternative conditions which are recommended:")
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

