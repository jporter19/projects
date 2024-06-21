
#%%  - these are the importers 
import streamlit as st  # Streamlit is a package used for simple websites
import chromadb         # Chroma Db is an open source vector database
from find_distances_closest_to_one import closest_index
from chroma_functions import db_collections
#from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.utils import embedding_functions
st.session_state.embeddings = embedding_functions.DefaultEmbeddingFunction()
#from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
#st.session_state.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

##%% ------------------------ Initialize Directory & Name for Primary DB ---------------------------
st.session_state.dbpath="b:\\python\\database\\booboo" # set the path to the DB
if 'col_choice' not in st.session_state:  #initialize selection of a collection
    st.session_state['col_choice']=None   # This could be set a default
    st.session_state.good = True # If None, then buttons are disabled


#%%
def clear_expanders():
    st.session_state['prompt_res'] = dict()

##%%  ------------------  Open an Existing Chroma DB as a Client  -----------------------------
st.session_state.run_client = chromadb.PersistentClient(path=st.session_state.dbpath)

# --------------------  This is a side bar collection pickter  ----------------------------
st.session_state.col_choice = st.selectbox("Pick a Collection",db_collections(st.session_state.run_client),index=None)
if st.session_state.col_choice == None:
    st.session_state.good = True # If None, then buttons are disabled
else:
    st.session_state.good = False

##%%  ---------If a Collection is selected create a chroma DB collection instance  ------------------
if st.session_state.col_choice:
    try:
        st.session_state.working_collection = st.session_state.run_client.get_collection(st.session_state.col_choice)
    except Exception as err:
        st.write(str(err))
resp_cnt = st.slider(min_value=1,max_value=10,label="Set the Number of Response")

##%%  --------------- Main Program  -------------------------------
if 'prompt_res' not in st.session_state:
    st.session_state['prompt_res']=dict()

# ------------- Display results in a container  ------------------
with st.container():  # using a container pushes the input to the top of the page
    st.subheader(f'Collection: [{st.session_state.col_choice}]',divider=True)
    prompt=(st.chat_input('What is your question?',key='input', disabled=st.session_state.good))
    if prompt: # if prompt has data then run this
        docs, res =[], []
        try:
            res = st.session_state.working_collection.query(query_texts=prompt,n_results=resp_cnt)
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
            prompt = prompt + ' -- Collection  \{'+st.session_state.col_choice+'\}'
            st.session_state.prompt_res.update({prompt:best_docs})
            st.button("clear", key='c', on_click=clear_expanders)
            for key in st.session_state.prompt_res:
                exp1=st.expander("output")
                with exp1: 
                    st.write(st.session_state.prompt_res[key])
        except:
            st.write("Please Select a Collection")

