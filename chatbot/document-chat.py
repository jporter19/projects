
#%%  - these are the importers 
import streamlit as st  # Streamlit is a package used for simple websites
import chromadb         # Chroma Db is an open source vector database
from langchain_chroma.vectorstores import Chroma
from pprint import pprint  # pprint is a bit better than print
from chromadb.config import Settings
from tqdm.autonotebook import tqdm, trange
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
st.session_state.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.document_loaders import YoutubeLoader
from tkinter import filedialog as fd
import re   # re is regular expressions for pattern matching

st.page_link('B:/code/projects/chatbot/admin_2.py',label="Admin Page")
st.page_link('pages/test2.py', label=":blue[test2 link]")
#%% - this is a path to the primary database, each database can have multiple collections
st.session_state.dbpath="b:\\python\\database\\booboo" # set the path to the DB
if 'col_choice' not in st.session_state:  #initialize selection of a collection
    st.session_state['col_choice']=None   # This could be set a default

#%%
# This function will produce a distinct list of collection to be displayed in drop down
def my_collections(db):
    collections = []
    for i in range (db.count_collections()):
        collections.append(db.list_collections()[i].name)
    return collections

#%%  ------------------  Open an Existing Chroma DB as a Client  -----------------------------
run_client = chromadb.PersistentClient(path=st.session_state.dbpath)

try:
    run_client.get_collection(name="test")
    st.write("success")
except Exception as err:
    st.write(str(err))

#st.session_state.col_choice = run_client.get_collection("test")
if run_client.count_collections() > 0:
# --------------------  This is a side bar collection pickter  ----------------------------
    st.session_state.col_choice = st.sidebar.selectbox("Pick a Collection",my_collections(run_client))
#else:
#    collections(runclient,"Add")
#%%  ---------If a Collection is selected Create a LangChain Chroma instance  ------------------
if st.session_state.col_choice:
    st. session_state.db = Chroma(persist_directory=st.session_state.dbpath,collection_name=st.session_state.col_choice,embedding_function=st.session_state.embeddings)
resp_cnt = st.sidebar.slider(min_value=1,max_value=10,label="Set the Number of Response")
########### - Testing - ###########
# st.write(db._collection.count())


#%%  --------------- Main Program  -------------------------------
if 'prompt_res' not in st.session_state:
    st.session_state['prompt_res']=dict()

# Setup tabs 
tab1, tab2 = st.tabs(["Query","Admin"]) 

with tab1:
    # ------------- Display results in a container  ------------------
    with st.container():  # using a container pushes the input to the top of the page
        st.subheader(f'Collection: [{st.session_state.col_choice}]',divider=True)
        prompt=(st.chat_input('What is your question?'))
        if prompt: # if prompt has data then run this
            res = db.similarity_search_with_relevance_scores(prompt,resp_cnt)
            resp_cnt = len(res)
            i=1
            for doc in res:
                # st.write(doc)
                if i==1:
                    message = f"Best Result: {i}" 
                else: message = f"Result: {i}"
                with st.expander(message):
                    st.write(doc[0].page_content)
                    st.write(f'Source: {doc[0].metadata['source']}')
                    st.button('See More',key=doc.index)
                i=i+1

            #best_docs = ''
            #for d in docs:
            #    best_docs = best_docs + res["documents"][0][d] +  f'  \n :blue[Source:] *{res["metadatas"][0][d].get('source')}*' +'\n\n'
            #    best_docs = best_docs + res["documents"][0][d] +  '  '  + 'www.newadvent.org'   
            #    st.write(best_docs)
            #prompt = prompt + ' -- Collection  \{'+st.session_state.col_choice+'\}'
            #st.session_state.prompt_res.update({prompt:best_docs[0]})
            #st.session_state.prompt_res.update({prompt:best_docs})
            #response = st.container(height=600)
            #with response:
             #   for key in st.session_state.prompt_res:
              #      message = st.chat_message('user')
              #      message.write(key)
               #     mycont=st.container(height=250, border=True)
                #    with mycont: st.write(st.session_state.prompt_res[key])
with tab2:
   st.write("Content TBD")
