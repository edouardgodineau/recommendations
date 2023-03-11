import streamlit as st
import os
import sys

# # my_dir = os.path.join('Multipage_app')
# # Multipage_app/main.py
# sys.path.append(os.path.join('recommendations', 'Multipage_app'))

parent_dir = os.path.abspath(os.path.join(os.getcwd(), ".."))

# add the parent directory to the system path
sys.path.append(parent_dir)

from Multipage_app.amide_page import show_page

st.write("<h1>Recommended methods to prepare amides</h1>", unsafe_allow_html = True)

show_page()