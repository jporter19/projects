import chromadb
import streamlit as st

#--------------------------------------------  Collection Functions ------------------------------------------
# This is designed to work with a Streamlit Button.  A Chroma db client is recieved as an argument, and a new collection name is
# referenced from session state.  

def create_col(db):
    try:
        db.create_collection(st.session_state.col_nm)
        st.session_state.resp = "New Collection Created"
    except:
        st.session_state.resp = "This Collection Already Exists" 
        
def rename_col(col):
    col.modify(st.session_state.renamer)
# -----------------------------   Set Working Collection -------------------------------
# set the working collection to the name passed in colpick 
def set_collection(db):
    try:
        st.session_state.working_col=db.get_collection(st.session_state.colpick)
        st.session_state.resp = "Collection Set" 
    except:
        st.session_state.working_col = None
        st.session_state.resp = "Error getting collection from Chroma" 


#---------------------------------------- Delete a Collection -------------------------------------
def del_collection(db):
    st.session_state.working_collection = st.empty()
    db.delete_collection(st.session_state.col_choice)
    '''if st.session_state.col_choice:
        val=st.session_state.col_choice
        st.session_state.col_choice=None
        db.delete_collection(val)
        st.session_state.resp =  "Collection Deleted"
    else:
        st.session_state.resp =  "No Collection Selected"'''

#---------------------------------------- Clear a Collection -------------------------------------


#---------------------------------------- Collection Info -------------------------------------
def collection_stats(col):
    if col == None:
        st.session_state.resp =  "Collection Count Failed: " + str(err)
    try:
        cnt=col.count()
    except:
        st.session_state.resp =  "Collection Count Failed: " + str(err)
    try:
        peek=col.peek(2)
    except:
        st.session_state.resp =  "Collection Peek Failed: " + str(err)
    return cnt, peek

#---------------------------------------- List Collections in a DB -------------------------------------

def collection_delete_where(col,clause):
    st.session_state.resp =  "Currently Unavailable"

def get_metadatas():
    st.session_state.resp =  "Currently Unavailable"

def add_test_doc(col):
    col.add(
    documents=["lorem ipsum..", "doc2", "doc3"],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}],
    ids=["id1", "id2", "id3"])
    st.session_state.resp =  "Three docuemnts added to collection"
    
def db_collections(db):
    collections = []
    for i in range (db.count_collections()):
        collections.append(db.list_collections()[i].name)
    return collections

def db_reset(db):
    try:
        db.reset()
        return "DB Reset Complete"
    except Exception as err:
        return "DB Reset Failed: " + str(err)

def db_stats(db):
    return db.get_version(), db.get_settings()
  