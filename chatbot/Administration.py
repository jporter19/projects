import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
st.session_state.embeddings = embedding_functions.DefaultEmbeddingFunction()
from chroma_functions import *

dbpath = "b:\\python\\database\\booboo" 
#------------------------   Initialize Variables  ------------------
#if 'db_client' not in st.session_state:

db_client=chromadb.PersistentClient(path=dbpath)

#db_client.create_collection(new_name)
if 'col_choice' not in st.session_state:
    st.session_state.col_choice = None
if 'working_col' not in st.session_state:
    st.session_state.working_col = st.empty()
if 'resp' not in st.session_state:
    st.session_state.resp = None
if 'confirmation' not in st.session_state:
    st.session_state.confirmation = False
if 'disable' not in st.session_state:
    st.session_state.disable = True

@st.experimental_dialog("Confirmation")
def confirm_msg(msg):
    st.write(msg)
    if st.button("Confirm",key='confirm_delete'):
        st.session_state.confirmation = True
        st.rerun()
    if st.button("Cancel",key='cancelled'):
        st.session_state.confirmation = False
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
st.subheader(f'Collection Management - Active Collection: [{st.session_state.col_choice}]')  # Populate section title
st.session_state.col_choice = st.selectbox("Pick a Collection",db_collections(db_client),index=None, key='colpick',on_change=set_collection, args=[db_client])
if st.session_state.col_choice:
    st.session_state.disable = False
else:
    st.session_state.disable = True
# pick a collection and get collection from db
st.divider() 
col1, col2 = st.columns([1,3])
with col1:
    st.button("Delete Current Collection",key='del_col', disabled=st.session_state.disable, on_click=del_collection, args=[db_client])
    if st.button("Create Collection",key='makecol'):
        with col2:
            new_name= st.text_input("Enter Collection Name",key='col_nm',placeholder=None, on_change=create_col, args=[db_client])
            st.write(st.session_state.resp)
    if st.button("Collection Stats", disabled=st.session_state.disable):
        count=0
        if st.session_state.working_col == None:
            col2.write("No Collections Selected")
        else:
            count, peek = collection_stats(st.session_state.working_col)
        if count  > 0:
            with col2:
                with st.expander("Collection Information"):
                    st.write("Document Count:" + str(count))
                    st.write(peek)
    if st.button("Rename Collection", disabled=st.session_state.disable):
        with col2:
            data=st.text_input("Enter New Name for Collection",key='renamer',placeholder=None, on_change=rename_col, args=[st.session_state.working_col])
    if st.button("Add Test Documents", key='add_test_data', disabled=st.session_state.disable, on_click=add_test_doc, args=[st.session_state.working_col]):
        col2.write(st.session_state.resp)


# st.session_state

# '''



