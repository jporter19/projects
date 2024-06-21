import streamlit as st
import datetime
#st.set_page_config(page_title="Add Documents", layout="centered", initial_sidebar_state="auto", menu_items={'Get Help':"mailto:jporter19@duck.com"})

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_chroma.vectorstores import Chroma
from langchain_core import documents
import chromadb 
from tkinter import filedialog as fd
if 'col_choice' not in st.session_state:
        st.switch_page("Document_Chat.py")
input_type = None
data = None
st.subheader(f'Data Load for Collection: "{st.session_state.col_choice}"')
input_type = st.selectbox("Data Upload",(".txt, .pdf or .epub","URL","YouTube"),index=None, placeholder="Choose File Type", disabled=st.session_state.good)
now = datetime.datetime.now()
today = now.strftime("%m/%d/%Y %H:%M")
if input_type == (".txt, .pdf or .epub"):
        filetypes = [
        ("PDF, TXT, EPUB Files", "*.pdf *.txt *.epub"),
        ("All Files", "*.*")]
        filename = fd.askopenfilename(filetypes=filetypes)
        loader = PyMuPDFLoader(filename)
        data = loader.load_and_split()  # load pdf
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
        #data[0].page_content
        #data[0].metadata
        #data[0].metadata['source']
        with st.form("New Data Input"):
                st.selectbox("Input Type", ("txt","pdf","epub","Youtube","html"),key='input_type')
                source=st.text_input("Source",key='src', value=data[0].metadata['source'])
                file=st.text_input("File Name:", value=data[0].metadata['file_path'])
                author=st.text_input("Author:",value=data[0].metadata['author'], placeholder="Enter Author's Name")
                title=st.text_input("Title:",value=data[0].metadata['title'])
                subject=st.text_input("Subject:",value=data[0].metadata['subject'])
                keywords=st.text_input("Key Words",value=data[0].metadata['keywords'], placeholder="Enter a comma seperated list of topics")
                create_date=st.text_input("Creation Date:",value=data[0].metadata['creationDate'],placeholder=str(today))
                #page=st.text_input("page:", value=str(data[0].metadata['source']))
                #total_pages=st.text_input("Total Pages", value=data[0].metadata['total_pages'])
                #creator=st.text_input("Creator:",value=str(data[0].metadata['creator']))
                #producer=st.text_input("producer:")
                #modDate=st.text_input("Last Updated:")
                #trapped=st.text_input("trapped") #  This is related to PDFs and means the document has been prepared for printing with trapping
                #encryption=st.text_input("encryption")
                #st.text_input("Tile:", key='tile')
                #st.text_area("Comment", key='comment')
                #st.checkbox("Favorite", key='source')
                st.form_submit_button("Submit Data Load")
        st.write(st.session_state.working_collection.count())
        st.write(len(data))
        #index+len(data) for doc in enumerate(data):
        #        st.write(in)

        #db3=Chroma.from_documents(documents=data,persist_directory=st.session_state.dbpath,collection_name=st.session_state.col_choice,embedding=st.session_state.embeddings)
        #result= db3.similarity_search("the furnace of Babylon that we heard about that Shadrach mesach and Abednego were thrown")
        #st.write(result)
