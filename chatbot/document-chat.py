
#%%  - these are the importers 
import streamlit as st  # Streamlit is a package used for simple websites
import chromadb         # Chroma Db is an open source vector database
from find_distances_closest_to_one import closest_index
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
st.session_state.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


# st.page_link('admin_2.py',label="Admin Page")
# st.page_link('pages/test2.py', label=":blue[test2 link]")
##%% ------------------------ Initialize Directory & Name for Primary DB ---------------------------
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

def clear_expanders():
    st.session_state['prompt_res'] = dict()

##%%  ------------------  Open an Existing Chroma DB as a Client  -----------------------------
run_client = chromadb.PersistentClient(path=st.session_state.dbpath)
try:
    run_client.get_collection(name="test")
except Exception as err:
    st.write(str(err))

#st.session_state.col_choice = run_client.get_collection("test")
# --------------------  This is a side bar collection pickter  ----------------------------
#st.session_state.col_choice = st.sidebar.selectbox("Pick a Collection",my_collections(run_client),index=None)
st.session_state.col_choice = st.selectbox("Pick a Collection",my_collections(run_client),index=None)

##%%  ---------If a Collection is selected Create a LangChain Chroma instance  ------------------
if st.session_state.col_choice:
    #working_collection = Chroma(collection_name=st.session_state.col_choice, embedding_function=st.session_state.embeddings, persist_directory=st.session_state.dbpath,)
    working_collection = run_client.get_collection(st.session_state.col_choice)
    # st.write(working_collection.query(query_texts="doc2"))
resp_cnt = st.slider(min_value=1,max_value=10,label="Set the Number of Response")

##%%  --------------- Main Program  -------------------------------
if 'prompt_res' not in st.session_state:
    st.session_state['prompt_res']=dict()

# ------------- Display results in a container  ------------------
with st.container():  # using a container pushes the input to the top of the page
    st.subheader(f'Collection: [{st.session_state.col_choice}]',divider=True)
    prompt=(st.chat_input('What is your question?'))
    if prompt: # if prompt has data then run this
        docs, res =[], []
        res = working_collection.query(query_texts=prompt,n_results=resp_cnt)
        if resp_cnt > len(res['ids']):
            resp_cnt = len(res['ids'])
        message="Query Results"
        #for doc in res:
        #    with st.expander(message): 
        #        st.write(doc.page_content)
        #        st.write(f'Chapter: {doc.metadata['chapter']}')
        #        st.write(f'Verse: {doc.metadata['verse']}')
        #        #st.button('See More',key=doc.index)
        docs = closest_index(res["distances"][0],2)
        best_docs = ''
        for d in docs:
            best_docs = best_docs + res["documents"][0][d]
            #best_docs = best_docs + res["documents"][0][d] +  f'  \n :blue[Source:] *{res["metadatas"][0][d].get('source')}*' +'\n\n'
            #best_docs = best_docs + res["documents"][0][d] +  '  '  + 'www.newadvent.org' 
            #st.write(res['documents'][0][d])  
            #st.write(res['metadatas'][0][d])
            #st.write(best_docs)
        #def print_response():
        prompt = prompt + ' -- Collection  \{'+st.session_state.col_choice+'\}'
        #st.session_state.st.session_state.prompt_res.update({prompt:best_docs[0]})
        #st.write(type(st.session_state.prompt_res))

        st.session_state.prompt_res.update({prompt:best_docs})
        #response = st.container(height=400)
        #with response:
        st.button("clear", key='c', on_click=clear_expanders)
        for key in st.session_state.prompt_res:
            #message = st.chat_message('user')
            #message.write(key)
            exp1=st.expander("output")
            with exp1: 
                st.write(st.session_state.prompt_res[key])
            #st.button(label="clear",key='exp_clear',on_click=clear_expanders, args=[st.session_state.exp1])

        #if st.session_state.clear==True:
            #st.write(st.session_state._clear)
    
            # st.write("IN the BUTTON")
            # st.session_state['prompt_res']=dict()
            #exp1.empty()
            #response.empty()
            #prompt=None
            #message=None
            #key = None
            #st.write(st.session_state.prompt_res)

