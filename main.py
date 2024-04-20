import streamlit as st
import base64

@st.cache_resource()
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    print("setting background")
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = """
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    """ % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

st.set_page_config(initial_sidebar_state="collapsed")
set_png_as_page_bg('webb.png')

st.markdown("<h1 style='text-align: center; color: black;'>Baklava Recommender System</h1>", unsafe_allow_html=True)

if st.session_state.get('mode') is None:
    print("hello")
    col1, col2 = st.columns(2)
    if col1.button('Random Baklava', use_container_width=True):
        st.session_state.mode = 'random'
        st.rerun()

    if col2.button('Category Baklava', use_container_width=True):
        st.session_state.mode = 'category_selection'
        st.rerun()

elif st.session_state.mode == 'random':
    st.write('Random Baklava')
elif st.session_state.mode == 'category_selection':
    _,col,__ =st.columns([0.2,0.6,0.2])
    values = col.multiselect('Select Category', ['Baklava', 'Baklava2', 'Baklava3'])
    if col.button('Submit'):
        st.session_state.mode = 'category_results'
        st.rerun()
elif st.session_state.mode == 'category_results':
    st.write('Category Results')
else:
    st.write('Invalid mode')

    
