
#%%  - these are the importers 


import streamlit as st  # Streamlit is a package used for simple websites
from streamlit import session_state as ss
import chromadb         # Chroma Db is an open source vector database
import ptvsd
from find_distances_closest_to_one import closest_index
from chroma_functions import db_collections
from chromadb.utils import embedding_functions
ss.embeddings = embedding_functions.DefaultEmbeddingFunction()
#ptvsd.enable_attach(address=('localhost', 5678), redirect_output=True)
#ptvsd.wait_for_attach()
#breakpoint()
# Session State Variables (Document Chat)
    # embeddings : Default embedding function
    # col_choice : String value of User selected collection)
    # dbpath : Path to vector database
    # run_client : Vector DB client
    # disabled : Button enable/disable
    # working_collection : Active Vectore DB collection
    # prompt_res : 
# input keys (these are automatically session state variables):  
    # c
    # input


##%% ------------------------ Initialize Directory & Name for Primary DB ---------------------------
ss.dbpath="b:\\python\\database\\booboo" # set the path to the DB
##%%  ------------------  Open an Existing Chroma DB as a Client  -----------------------------
ss.run_client = chromadb.PersistentClient(path=ss.dbpath)

# initialize session state variables
if 'col_choice' not in ss:
    ss['col_choice']=None 
if 'working_collection' not in ss:
    ss['working_collection']=[]
if 'disabled' not in ss:  
    ss['disabled']=True
if 'prompt_res' not in ss:
    ss['prompt_res']=dict()
if 'OPTIONS' not in ss:
    ss['OPTIONS'] = db_collections(ss.run_client)
    ss.OPTIONS.insert(0,None)
    ss['selected']=None
#if '' not in ss:
   # ss['prompt_res']=dict() 

##%% 
def clear_expanders():
    ss['prompt_res'] = dict()

def val_flip():
    ss.selected = ss.col_index
    if ss.col_index == None:
        ss.disabled = True # If None, then buttons are disabled
    else:
        ss.disabled = False

# --------------------  This is a collection pickter  ----------------------------
ss.col_choice=st.selectbox("Pick a Collection",options=ss.OPTIONS,key='col_index', on_change=val_flip,index=ss.OPTIONS.index(ss.selected))

##%%  ---------If a Collection is selected create a chroma DB collection instance  ------------------
if ss.col_index:
    try:
        ss.working_collection = ss.run_client.get_collection(ss.col_index)
    except Exception as err:
        st.write(str(err))
resp_cnt = st.slider(min_value=1,max_value=10,label="Set the Number of Response")

# ------------- Display results in a container  ------------------
with st.container():  # using a container pushes the input to the top of the page
    st.subheader(f'Collection: [{ss.col_index}]',divider=True)
    prompt=(st.chat_input('What is your question?',key='input', disabled=ss.disabled))
    if prompt: # if prompt has data then run this
        docs, res =[], []   
        try:
            res = ss.working_collection.query(query_texts=prompt,n_results=resp_cnt)
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
            prompt = prompt + ' -- Collection  \{'+ss.col_index+'\}'
            ss.prompt_res.update({prompt:best_docs})
            st.button("clear", key='c', on_click=clear_expanders)
            for key in ss.prompt_res:
                exp1=st.expander("output")
                with exp1: 
                    #pass
                    st.write(ss.prompt_res[key])
        except:
            st.write("Please Select a Collection")

