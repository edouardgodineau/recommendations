import pprint

import bigtree as bt
import bigtree as bt
import streamlit as st

#need to use Chemistry_recommendations.Utils.[filename] to make it work in pycharm
# from Chemistry_recommendations.Utils.data_prep import Recommendation
# file_path = "Recommendations.xlsx"

#need to use Utils.[filename] to get the app to work within streamlit
from Utils.data_prep import Recommendation
file_path = "Utils/Recommendations.xlsx"


sheetname = "Suzuki_App_"
# # Load data for the reaction class and build the recommendations
suzuki = Recommendation(file_path, sheetname)


# Build the tree for the reaction class
suzuki.build_nodes()
suzuki.build_recommendation()
suzuki_dict = suzuki.build_dict4tree()
# # Build the tree for the reaction class

root_suzuki = bt.dict_to_tree(suzuki_dict)

def show_page():

    # Define custom CSS styles
    st.write("<h1>Recommended methods to perform Suzuki Cross couplings</h1>", unsafe_allow_html = True)


    standard_conditions = root_suzuki.node_name

    results = bt.find(root_suzuki, lambda node: node.name == standard_conditions)

    st.write(f'The {standard_conditions} reaction conditions for Suzuki cross couplings are the following condition(s):')

    # print best conditions (up to 3 conditions are returned)
    for i in range(1, 4):
        i = str(i)
        item = results.get_attr(i)
        if item:
            with st.container():

                # print the recommendation for the reaction class
                st.markdown(f'{i} | {item.get("recommendation")}')
                # print(f'{i} | {item.get("recommendation")}')

                # print_additionnal_info(item) when it is available
                if item['ELN'] != '':
                    st.markdown(f"ELN reference: {item.get('ELN')}")
                else:
                    st.markdown("We unfortunately don't have any ELN reference to recommend. We are working on it!")
                if item.get('comments') != '':
                    st.markdown(f"Comment: {item.get('comments')}")
                if item.get('reference') != '':
                    st.markdown(f"Reference: [{item.get('reference')}]({item.get('link')})")

    # print('Standard conditions did not work because the carboxylic acid (choose from the list below):')
    alternatives = [i.name for i in root_suzuki.children]

    st.markdown("---")
    label_text = '<span style="font-size: 16px; font-weight: bold;">The standard conditions above did not work because the:</span>'

    container_style = 'display: flex; flex-direction: column; align-items: flex-start;'

    st.markdown(f'<div style="{container_style}">{label_text}', unsafe_allow_html=True)

    # problem = st.selectbox('', ["", *alternatives_1])
    problem = st.selectbox(' ', ['Please choose an option'] + alternatives)
    st.markdown('</div>', unsafe_allow_html=True)

    for alternative in alternatives:
        if alternative == problem:
            st.write(
                f"For a carboxylic acid which {alternative}, here are alternative conditions which are recommended:")
            results = bt.find(root_suzuki, lambda node: node.name == alternative)
            for i in range(1, 4):
                i = str(i)
                item = results.get_attr(i)
                if item:
                    with st.container():

                        # print the recommendation for the reaction class
                        st.markdown(f'{i} | {item.get("recommendation")}')

                        if item['ELN'] != '':
                            st.markdown(f"ELN reference: {item.get('ELN')}")
                        else:
                            st.markdown(
                                "We unfortunately don't have any ELN reference to recommend. We are working on it!")

                        if item.get('comments') != '':
                            st.markdown(f"Comment: {item.get('comments')}")

                        if item.get('reference') != '':
                            st.markdown(f"Reference: [{item.get('reference')}]({item.get('link')})")
                        st.markdown("---")


