# ---- Imports 
import streamlit as st
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
st.write(st.session_state.dbpath)
#client = chromadb.PersistentClient(b:\)
# ---- Functions
def collection_stats(col):
    return col.count(), col.peek(2)
def db_collections(db):
    collections = []
    for i in range (db.count_collections()):
        collections.append(db.list_collections()[i].name)
    return collections
def change_name(col):
    try: 
        st.text_input('Enter the New Name', key='new_name')
        col.modify(name=str(st.session_state.new_name))
        return "Collection Rename Complete"
    except Exception as err:
        return "Collection Rename Failed: " + str(err)
def change_check():
    st.session_state.change = True

# ---- Initialize vars
show_expander=[False,False,False,False]
dbpath = st.session_state.dbpath  # name of the vector database
if 'change' not in st.session_state:
    st.session_state.change = False


hiphop_db =chromadb.PersistentClient(path=st.session_state.dbpath)
pick = st.selectbox("Pick a Collection",db_collections(hiphop_db),index=None,key='colpick', on_change=change_check)
if st.session_state.change:
    st.write("MUST BE IN HERE")
    hiphop = hiphop_db.get_collection(pick)
    #st.write(working_col.count())
    st.session_state.change = False

# ---- Select working Collection name

col1, col2, col3, col4 = st.columns(4)
def display():
    st.session_state

# working_col is a 
if pick:
    with col1:
        st.write(hiphop.count())  # thi
        if st.button("Collection Stats", key='stats'):
            st.write(hiphop.count())
            #count, peek = collection_stats(working_col)
            show_expander[0]=True
    if show_expander[0]:
        with st.expander("Collection Information"):
            st.write("Document Count:" + str(count))
            st.write(peek)
    with col2:
        if st.button("Rename Collection", key='rename'):
            resp = change_name(hiphop)
    if show_expander[1]:
        with st.expander("Collection Information"):
            st.write("Document Count:" + str(count))
            st.write("This is different data")






