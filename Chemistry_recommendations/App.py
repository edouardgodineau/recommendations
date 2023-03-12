import base64
import os
import streamlit as st

parent_dir = os.path.abspath(os.path.join(os.getcwd(), ""))
st.set_page_config(page_title="Chemistry Recommendations",
                   page_icon=':book:',
                   layout="wide",
                   initial_sidebar_state="expanded")

with st.container():
    st.header('App for troubleshooting reactions')
    st.subheader("You will find here:")
    st.markdown("- tips and tricks for performing efficiently chemistry")
    st.markdown("- classical protocols for a variety of classical reactions. A resource to quickly check what to try next if a reaction does not work")

with st.container():
    st.write("---")
    _, col2, _, col4, _, col6, _ = st.columns(7)
    with col2:
        # st.subheader("Sustainability in Chemistry Sharepoint", style={"font-size": "24px", "font-weight": "bold"}
        st.markdown(f'<h1 style="color:#5F7800;font-size:20px; text-align: center">{"Sustainability in Chemistry Sharepoint"}</h1>', unsafe_allow_html=True)
        # image_file = open('Utils/images/shutterstock_1345050239.jpg', 'rb')
        # image_bytes = image_file.read()
        # # st.image(image_bytes, width=200, caption="[Sustainability in Chemistry Sharepoint](https://syngenta.sharepoint.com/sites/sustchem)")
        url = "https://syngenta.sharepoint.com/sites/sustchem"
        file_path = "Utils/images/shutterstock_1345050239.jpg"
        link = f'<a href={url} target="_blank"><img src="data:image/jpeg;base64,{base64.b64encode(open(file_path, "rb").read()).decode()}" alt="Clickable image" width="200"></a>'
        st.markdown(link, unsafe_allow_html=True)

    with col4:
        st.markdown(f'<h1 style="color:#5F7800;font-size:20px; text-align: center">{"Stein Research Chemistry"}</h1>', unsafe_allow_html=True)
        url = "https://syngenta.sharepoint.com/sites/sustchem"
        file_path = "Utils/images/Stein_research_chemistry.PNG"
        link = f'<a href={url} target="_blank"><img src="data:image/png;base64,{base64.b64encode(open(file_path, "rb").read()).decode()}" alt="Clickable image" width="200"></a>'
        st.markdown(link, unsafe_allow_html=True)

    with col6:
        url = "https://reagents.acsgcipr.org/reagent-guides"
        file_path = "Utils/images/ACS_reagent_guide.JPG"
        st.markdown(f'<h1 style="color:#5F7800;font-size:20px; text-align: center">{"ACS Reagent Guide"}</h1>', unsafe_allow_html=True)
        link = f'<a href={url} target="_blank"><img src="data:image/png;base64,{base64.b64encode(open(file_path, "rb").read()).decode()}" alt="Clickable image" width="200"></a>'
        st.markdown(link, unsafe_allow_html=True)


with st.container():
    _, col2, col3, _ = st.columns(4)


    with col2:

        url = "https://syngenta.sharepoint.com/sites/sustchem/Public/Forms/AllItems.aspx?id=%2Fsites%2Fsustchem%2FPublic%2FGreen%20Chemistry%20Poster%2Epdf&parent=%2Fsites%2Fsustchem%2FPublic"
        st.markdown(
            f'<h1  style="color:#5F7800;font-size:20px; text-align: center">{"Syngenta Digital Poster"}</h1>', unsafe_allow_html=True)
        file_path = "Utils/images/Digital_poster.PNG"
        link = f'<a target="_blank"><img src="data:image/png;base64,{base64.b64encode(open(file_path, "rb").read()).decode()}" title="{url}" alt="Clickable image" width="300"></a>'
        st.markdown(link, unsafe_allow_html=True)

    with col3:
        st.markdown(f'<h1 style="color:#5F7800;font-size:20px; text-align: center">{"Solvent Guide"}</h1>',unsafe_allow_html=True)
        url = "https://syngenta.sharepoint.com/:x:/r/sites/sustchem/_layouts/15/Doc.aspx?sourcedoc=%7B691390FA-470A-44A8-BA03-F04887CF7D6E%7D&file=Solvent%20Sustainability%20Guide.xlsx&_DSL=1&action=default&mobileredirect=true"
        file_path = "Utils/images/Solvent guide.JPG"
        link = f'<a target="_blank"><img src="data:image/png;base64,{base64.b64encode(open(file_path, "rb").read()).decode()}" alt="Clickable image" width="300"></a>'
        st.markdown(link, unsafe_allow_html=True)