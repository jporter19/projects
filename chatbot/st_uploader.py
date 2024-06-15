import streamlit as st
import pymupdf

def process_file(f,f_type):
    if f:
        f.seek(0,0)
        docs = pymupdf.open(stream=f.read(),filetype=f_type)
        st.write(f"length is {len(docs)}")
        for page in docs:
            text = page.get_text().encode("utf8")
            # text = page.get_text()
            st.write(text)

input_type = None
col1, col2 = st.columns([2,3])
with col1:
    input_type = st.selectbox("Data Upload",("txt","pdf","epub","URL","YouTube"),index=None, placeholder="Choose File Type")
with col2:
    if input_type in ("txt","pdf","epub"):
        val = st.file_uploader("enter:", type=[input_type],accept_multiple_files=False, label_visibility = "hidden", disabled=False)
        process_file(val,input_type)
    elif input_type == "YouTube":
        val = st.text_input("Enter URL to YouTube Video:")
        st.write(val)
    elif input_type == "URL":
        val = st.text_input("Enter URL to Website:")
        st.write(val)
    else:
        val = None
       # val = st.file_uploader("enter:", label_visibility = "hidden", disabled=True)



