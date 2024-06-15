import streamlit as st
#st.set_page_config(page_title="Add Documents", layout="centered", initial_sidebar_state="auto", menu_items={'Get Help':"mailto:jporter19@duck.com"})

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_chroma.vectorstores import Chroma
from tkinter import filedialog as fd
st.write(st.session_state.col_choice)
input_type = None
data = None
input_type = st.selectbox("Data Upload",(".txt, .pdf or .epub","URL","YouTube"),index=None, placeholder="Choose File Type")

if input_type == (".txt, .pdf or .epub"):
        filetypes = [
        ("PDF, TXT, EPUB Files", "*.pdf *.txt *.epub"),
        ("All Files", "*.*")]
        filename = fd.askopenfilename(filetypes=filetypes)
        loader = PyMuPDFLoader(filename)
        data = loader.load_and_split()  # load pdf
        #st.write(data)
elif input_type == "YouTube":
        val = st.text_input("Enter URL to YouTube Video:")
        if val:
                loader = YoutubeLoader.from_youtube_url(val, add_video_info=True)
                data = loader.load()      
                st.write("loading a youtube")
        #st.write(data)
elif input_type == "URL":
        val = st.text_input("Enter URL to Website:")
        st.write(val)
else:
        val = None
if data:
        #st.write(data)
        db3=Chroma.from_documents(documents=data,persist_directory=st.session_state.dbpath,collection_name=st.session_state.col_choice,embedding=st.session_state.embeddings)
        result= db3.similarity_search("the furnace of Babylon that we heard about that Shadrach mesach and Abednego were thrown")
        st.write(result)




