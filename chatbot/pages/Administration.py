import streamlit as st
from streamlit import session_state as ss2
import chromadb
from chromadb.utils import embedding_functions
#ss2.embeddings = embedding_functions.DefaultEmbeddingFunction()
from chroma_functions import *

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

dbpath = "b:\\python\\database\\booboo"
db_client=chromadb.PersistentClient(path=dbpath)

#------------------------   Initialize Variables  ------------------
#if 'db_client' not in ss:

if 'selected' not in ss2:
    st.write('TRUE')
else:
    st.write('FALSE')

if 'working_collection' not in ss2:
    ss2['working_collection']=[]
if 'resp' not in ss2:
    ss2['resp'] = None
if 'confirmation' not in ss2:
    ss2.confirmation = False
if 'col_count' not in ss2:
    ss2.col_count = None
if 'selected' not in ss2:
    ss2.selected = None
ss2.col_count = ss2.working_collection.count()

def val_flip():
    ss2.selected = ss2.colpick
    if ss2.colpick == None:
        ss2.disabled = True # If None, then buttons are disabled
    else:
        ss2.working_collection = ss2.run_client.get_collection(ss2.colpick)
        ss2.col_count = ss2.working_collection.count()
        ss2.disabled = False

@st.experimental_dialog("Confirmation")
def confirm_msg(msg):
    st.write(msg)
    if st.button("Confirm",key='confirm_delete'):
        ss2.confirmation = True
        st.rerun()
    if st.button("Cancel",key='cancelled'):
        ss2.confirmation = False
        st.rerun()

st.title("Application Manager")
st.divider()
st.subheader("Database Management")
st.divider()

col1, col2 = st.columns([1,3])
version, setting = None, []
# setting = []
with col1:
    if st.button("DB Stats",key='db_stats'):
        version,setting = db_stats(db_client)
with col2:
    expand_1 = st.expander("Database Stats")
    with expand_1:
        if version and setting:
           pass
           st.write("Version:" + str(version))
           st.write(setting)
with col1:
    if st.button("DB Reset"):
        resp = db_reset(db_client)
        col2.write(resp)
st.divider()
st.subheader(f'Active Collection: [{ss2.col_choice}], Document Count: {ss2.col_count}')  # Populate section title
ss2.col_choice=st.selectbox("Pick a Collection",options=ss2.OPTIONS,key='colpick', on_change=val_flip,index=ss2.OPTIONS.index(ss2.selected))
#ss2.col_index = st.selectbox("Change Collection",db_collections(db_client),index=ss2.col_index, key='colpick',on_change=set_collection, args=[db_client])

#if ss2.col_choice:
#    ss2.disabled = False
#else:
#    ss2.disabled = True
if ss2.disabled == False:
    with st.expander("Collection Information"):
        ss2.col_count=str(ss2.working_collection.count())
        st.write("Document Count:" + ss2.col_count)
        st.write(ss2.working_collection.peek(4))
# pick a collection and get collection from db
st.divider() 
col1, col2 = st.columns([1,3])
with col1:
    st.button("Delete Current Collection",key='del_col', disabled=ss2.disabled, on_click=del_collection, args=[db_client,ss2.col_choice])
    if st.button("Create Collection",key='makecol'):
        with col2:
            new_name= st.text_input("Enter Collection Name",key='col_nm',placeholder=None, on_change=create_col, args=[db_client])
            st.write(ss2.resp)
    if st.button("Rename Collection", disabled=ss2.disabled):
        with col2:
            data=st.text_input("Enter New Name for Collection",key='renamer',placeholder=None, on_change=rename_col, args=[ss2.working_collection])
    if st.button("Add Test Documents", key='add_test_data', disabled=ss2.disabled, on_click=add_test_doc, args=[ss2.working_collection]):
        col2.write(ss2.resp)
    if st.button("Clear All Data", key='clear_data', disabled=ss2.disabled, on_click=clear_data, args=[ss2.working_collection]):
        col2.write(ss2.resp)


# ss





