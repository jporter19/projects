import chromadb
import streamlit as ss

#--------------------------------------------  Collection Functions ------------------------------------------
# This is designed to work with a Streamlit Button.  A Chroma db client is recieved as an argument, and a new collection name is
# referenced from session state.  

def create_col(db):
    try:
        db.create_collection(ss.col_nm)
        ss.resp = "New Collection Created"
    except:
        ss.resp = "This Collection Already Exists" 
        
def rename_col(col):
    col.modify(ss.renamer)
# -----------------------------   Set Working Collection -------------------------------
# set the working collection to the name passed in colpick 
def set_collection(db):
    try:
        ss.working_collection=db.get_collection(ss.colpick)
        ss.resp = "Collection Set" 
    except:
        ss.working_collection = None
        ss.resp = "Error getting collection from Chroma" 


#---------------------------------------- Delete a Collection -------------------------------------
def del_collection(db,to_del):
    ss.working_collection = []
    db.delete_collection(to_del)
    '''if ss.col_choice:
        val=ss.col_choice
        ss.col_choice=None
        db.delete_collection(val)
        ss.resp =  "Collection Deleted"
    else:
        ss.resp =  "No Collection Selected"'''

#---------------------------------------- Clear a Collection -------------------------------------
def clear_data(col):
    
    pass


#---------------------------------------- Collection Info -------------------------------------
def collection_stats(col):
    if col == None:
        ss.resp =  "Collection Count Failed: " + str(err)
    try:
        cnt=col.count()
    except:
        ss.resp =  "Collection Count Failed: " + str(err)
    try:
        peek=col.peek(2)
    except:
        ss.resp =  "Collection Peek Failed: " + str(err)
    return cnt, peek

#---------------------------------------- List Collections in a DB -------------------------------------

def collection_delete_where(col,clause):
    ss.resp =  "Currently Unavailable"

def get_metadatas():
    ss.resp =  "Currently Unavailable"

def add_test_doc(col):
    col.add(
    documents=["lorem ipsum..", "doc2", "doc3"],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}],
    ids=["id1", "id2", "id3"])
    ss.resp =  "Three docuemnts added to collection"
    
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
  