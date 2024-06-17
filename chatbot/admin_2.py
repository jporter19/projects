import streamlit as st
import chromadb
from langchain_community.embeddings.sentence_transformer import (SentenceTransformerEmbeddings,)
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


#--------------------------------------------  Collection Functions ------------------------------------------
#---------------------------------------- Change a Collection Name -------------------------------------
def change_name(new_name):
    try: 
        st.session_state.working_col.modify(name=new_name)
        return "Collection Rename Complete"
    except Exception as err:
        return "Collection Rename Failed: " + str(err)
#---------------------------------------- Delete a Collection -------------------------------------
def delete_collection():
    try:
        # st.session_state.db_client.delete_collection(st.session_state.working_col)
        return "Collection Deleted"
    except Exception as err:
        return "Collection Deleted Failed: " + str(err)
#---------------------------------------- Create a Collection -------------------------------------
def create_collection(db,new_col):
    try:
        db.get_collection(name=new_col)
        return "Collection Already Exists"
    except:
        try:
            db.create_collection(name=new_col, embedding_function=embeddings)
        except Exception as err:
            return "Collection Create Failed: " + str(err)
#---------------------------------------- Clear a Collection -------------------------------------
def clear_collection():
    return "Currently Unavailable"

#---------------------------------------- Collection Info -------------------------------------
def collection_stats(col):
    return col.count(), col.peek(2)

#---------------------------------------- List Collections in a DB -------------------------------------

def collection_delete_where(clause):
    return "Currently Unavailable"

def get_metadatas():
    return "Currently Unavailable"

def add_test_doc(col):
    col.add(
    documents=["lorem ipsum..", "doc2", "doc3"],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}],
    ids=["id1", "id2", "id3"]
)

# ------------------------------------------ Database ------------------------------------------
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






