import streamlit as st
import os
import sys
# from main import show_page
parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))
st.set_page_config(page_title="Multipage App",
                   layout="wide",
                   initial_sidebar_state="expanded")


st.title('App for troubleshooting reactions')
st.markdown("Find here:")
st.markdown("- tips and tricks for performing efficiently chemistry")
st.markdown("- classical protocols for a variety of classical reactions. A resource to quickly check what to try next if a reaction does not work")
# st.sidebar.success('Select a page from the sidebar')
# show_page()