import streamlit as st
import pages
import json

def show_page():
    # Define custom CSS styles

    with open('recommendations4amide.json', 'r') as f:
        data = json.loads(f.read())

    amide1 = []
    for i in range(3):
        reco = f'Top{i + 1} condition: {data[str(i)]}'
        amide1.append(reco)

    st.sidebar.selectbox('Menu', ('Amide formation', 'Suzuki reactions', 'C-N couplings (Buchwald, Ullmann, Chan-Lam...)'))
    st.title("Recommendations for reaction conditions for making amides")
    st.write('please choose from the list which type of amide starting material you are working with:')

    amide = (
        "Please estimate the reactivity of the carboxylic acid you are working with",
        "normal",
        "unreactive",
        "highly sensitive",
    )


    amide = st.selectbox("Amide type", amide)

    if amide == "normal":
        st.write("For carboxylic adic having a normal reactivity, here are 3 conditions which are recommended:")
        st.markdown(amide1[0])
        st.markdown(amide1[1])
        st.markdown(amide1[2])

    if amide == "unreactive":
        st.write("For carboxylic adic having a normal reactivity, here are 3 conditions which are recommended:")
        st.markdown("Top condition1: ")
        st.markdown("Top condition2: ")
        st.markdown("Top condition3: ")

    if amide == "highly sensitive":
        st.write("Here are 3 conditions we recommend for you")
        st.markdown("1. Acid chloride, Amine 1.1 equiv., K2CO3 or NEt3 3.0 equiv., -, ACN or ethyl acetate, RT")
        st.markdown("3. Acid, Amine 1.1 equiv., NMI 3.0 equiv., TCFH 2.0 equiv., ACN or ethyl acetate, RT, Clone this eln: 22-6615\nCheck out this [Org. Lett. 2020, 22, 5737](https://doi.org/10.1021/acs.orglett.0c01676)")
        st.markdown("3.")

show_page()