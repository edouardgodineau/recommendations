import bigtree as bt
import bigtree as bt
import streamlit as st
import pprint
#need to use Chemistry_recommendations.Utils.[filename] to make it work in pycharm
# from Chemistry_recommendations.Utils.data_prep import Recommendation
# file_path = "Recommendations.xlsx"

#need to use Utils.[filename] to get the app to work within streamlit
from Utils.data_prep import Recommendation
file_path = "Utils/Recommendations.xlsx"
sheetname = "Cyanation_App_"

cyanation = Recommendation(file_path, sheetname)
cyanation.build_nodes()
cyanation.build_recommendation()

# Build the tree for the reaction class
cyanation.build_dict4tree()
root_cyanation = bt.dict_to_tree(cyanation.leaves)








def show_page():

    # Define custom CSS styles
    with open('Utils/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


    st.write("<h1>Recommended methods to perform aryl halide cyanations</h1>", unsafe_allow_html = True)


    standard_conditions = root_cyanation.node_name

    results = bt.find(root_cyanation, lambda node: node.name == standard_conditions)

    st.write(f'The {standard_conditions} reaction conditions for cyanation are the following condition(s):')

    # print best conditions (up to 3 conditions are returned)
    for i in range(1, 4):
        i = str(i)
        item = results.get_attr(i)
        if item:

            with st.container():

                # print the recommendation for the reaction class
                st.markdown(f'<h1 class="container">{i} | {item.get("recommendation")}</h1>', unsafe_allow_html = True)
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

    alternatives = [i.name for i in root_cyanation.children]

    st.markdown("---")
    label_text = '<span style="font-size: 16px; font-weight: bold;">The standard conditions above did not work because the aryl halide is:</span>'

    container_style = 'display: flex; flex-direction: column; align-items: flex-start;'

    st.markdown(f'<div style="{container_style}">{label_text}', unsafe_allow_html=True)

    problem = st.selectbox(' ', ['Please choose an option'] + alternatives)
    st.markdown('</div>', unsafe_allow_html=True)


    for alternative in alternatives:
        if alternative == problem:
            st.write(f"For an aryl halide which {alternative}, here are alternative conditions which are recommended:")
            results = bt.find(root_cyanation, lambda node: node.name == alternative)
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

