import bigtree as bt
from bigtree import print_tree
import streamlit as st
import pprint
#need to use Chemistry_recommendations.Utils.[filename] to make it work in pycharm
# from Chemistry_recommendations.Utils.data_prep import Recommendation
# file_path = "Recommendations.xlsx"

#need to use Utils.[filename] to get the app to work within streamlit
from Utils.data_prep import Recommendation

file_path = "Utils/Recommendations.xlsx"
sheetname = "Amide_coupling_App_"

amide = Recommendation(file_path, sheetname)

# Build the tree for the reaction class
amide.build_nodes()
amide.build_recommendation()
amide.build_dict4tree()

# Build the tree for the reaction class
root_amide = bt.dict_to_tree(amide.leaves)



def show_page():

    # Define custom CSS styles
    st.write("<h1>Recommended methods to prepare amides</h1>", unsafe_allow_html = True)


    standard_conditions = root_amide.node_name

    st.write(f'For carboxylic acid which {standard_conditions} the following condition(s) are recommended:')

    results = bt.find(root_amide, lambda node: node.name == standard_conditions)

    # print best conditions (up to 3 conditions are returned)
    for i in range(1,4):
        i = str(i)
        item = results.get_attr(i)
        if item:
            with st.container():

                #print the recommendation for the reaction class
                st.markdown(f'{i} | {item.get("recommendation")}')
                # print(f'{i} | {item.get("recommendation")}')

                #print_additionnal_info(item) when it is available
                if item['ELN'] != '':
                    st.markdown(f"ELN reference: {item.get('ELN')}")
                else:
                    st.markdown("We unfortunately don't have any ELN reference to recommend. We are working on it!")
                if item.get('comments') != '':
                    st.markdown(f"Comment: {item.get('comments')}")
                if item.get('reference') != '':
                    st.markdown(f"Reference: [{item.get('reference')}]({item.get('link')})")



    # print('Standard conditions did not work because the carboxylic acid (choose from the list below):')
    alternatives = [i.name for i in root_amide.children]

    st.markdown("---")
    label_text = '<span style="font-size: 16px; font-weight: bold;">The standard conditions did not work because the carboxylic acid:</span>'

    container_style = 'display: flex; flex-direction: column; align-items: flex-start;'

    st.markdown(f'<div style="{container_style}">{label_text}', unsafe_allow_html=True)

    problem = st.selectbox(' ', ['Please choose an option'] + alternatives)
    st.markdown('</div>', unsafe_allow_html=True)

    for alternative in alternatives:
        if alternative == problem:
            st.write(f"For a carboxylic acid which {alternative}, here are alternative conditions which are recommended:")
            results = bt.find(root_amide, lambda node: node.name == alternative)
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
                            st.markdown("We unfortunately don't have any ELN reference to recommend. We are working on it!")

                        if item.get('comments') != '':
                            st.markdown(f"Comment: {item.get('comments')}")

                        if item.get('reference') != '':
                            st.markdown(f"Reference: [{item.get('reference')}]({item.get('link')})")
                        st.markdown("---")



# show_page()
# print('amide_page', __name__)