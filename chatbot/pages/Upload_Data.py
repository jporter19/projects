import streamlit as st
from streamlit import session_state as ss3
import datetime
#st.set_page_config(page_title="Add Documents", layout="centered", initial_sidebar_state="auto", menu_items={'Get Help':"mailto:jporter19@duck.com"})
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_chroma.vectorstores import Chroma
from langchain_core import documents
import chromadb 
from tkinter import filedialog as fd
# a collection needs to be selected to import
if 'col_choice' not in ss3:
        st.switch_page("Document_Chat.py")
input_type = None

def getfile():
        got_data=False
        #if 'f_data' not in ss:
        #        ss.f_date=[]
        if ss3.upload_type == (".txt, .pdf, .epub"):
                filetypes = [("PDF, TXT, EPUB Files", "*.pdf *.txt *.epub"),
                        ("All Files", "*.*")]
                filename = fd.askopenfilename(filetypes=filetypes)
                loader = PyMuPDFLoader(filename)
                data = loader.load_and_split()  # load pdf
                got_data=True
        elif ss3.upload_type == "YouTube":
                val = st.text_input("Enter URL to YouTube Video:")
                if val:
                        loader = YoutubeLoader.from_youtube_url(val, add_video_info=True)
                        data = loader.load()      
                        st.write("loading a youtube")
                        got_data=True
        elif ss3.upload_type == "URL":
                pass
                #val = st.text_input("Enter URL to Website:")
        else:
                pass
        if got_data:
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
                        #id_list=[]
                        id,doc,meta = [],[],[]
                        start_val = ss3.working_collection.count()
                        for index in range(len(data)):
                                id.append(str(index + start_val))
                                data[index].metadata['source']=source
                                data[index].metadata['file_path']=file
                                data[index].metadata['author']=author
                                data[index].metadata['title']=title
                                data[index].metadata['subject']=subject
                                data[index].metadata['keywords']=keywords
                                data[index].metadata['creationDate']=create_date
                                doc.append(data[index].page_content)
                                meta.append(data[index].metadata)
                        st.write(start_val)
                        with st.expander("range"):
                                for i in range(len(data)):
                                        st.write(i)
                        st.form_submit_button("Submit Data Load")
                st.write(id)
                ss3.working_collection.add(ids=id,documents=doc,metadatas=meta)
                #st.write(ss.working_collection.count())
                #st.write(ss.working_col.get(ids='30'))
                #st.write(data[0])
                st.divider()
        # st.write(data[1])
                #index+len(data) for doc in enumerate(data):
                #        st.write(in)

                #db3=Chroma.from_documents(documents=data,persist_directory=ss.dbpath,collection_name=ss.col_choice,embedding=ss.embeddings)
                #result= db3.similarity_search("the furnace of Babylon that we heard about that Shadrach mesach and Abednego were thrown")
                #st.write(result)

st.subheader(f'Data Load for Collection: "{ss3.col_choice}"')  # dynamic header
input_type = st.selectbox("Data Upload",(".txt, .pdf, .epub","URL","YouTube"),key='upload_type', index=None, placeholder="Choose File Type", on_change=getfile, disabled=ss3.disabled)
now = datetime.datetime.now()
today = now.strftime("%m/%d/%Y %H:%M")