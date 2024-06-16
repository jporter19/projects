import streamlit as st

with st.form("New Data Input"):
    st.selectbox("Input Type", ("txt","pdf","epub","Youtube","html"),key='input_type')
    st.text_input("File Name:", key='file_name')
    st.text_input("Author:", key='author', placeholder="Enter Author's Name")
    st.text_input("Tile:", key='tile')
    st.date_input("Load Date:", key='load_date')
    st.text_area("Comment", key='comment')
    st.text_input("Tags", key='tags', placeholder="Enter a comma seperated list of topics")
    # st.checkbox("Favorite", key='source')
    st.form_submit_button("Submit Data Load")