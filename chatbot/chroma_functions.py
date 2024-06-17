import chromadb
#--------------------------------------------  Collection Functions ------------------------------------------
#---------------------------------------- Change a Collection Name -------------------------------------
def change_name(col,new_name):
    try: 
        col.modify(name=new_name)
        return "Collection Rename Complete"
    except Exception as err:
        return "Collection Rename Failed: " + str(err)
#---------------------------------------- Delete a Collection -------------------------------------
def delete_collection(db,col):
    try:
        db.delete_collection(col)
        return "Collection Deleted"
    except Exception as err:
        return "Collection Deleted Failed: " + str(err)
#---------------------------------------- Create a Collection -------------------------------------
def create_collection(db,col,new_name,embeddings):
    try:
        db.get_collection(name=new_name)
        return "Collection Already Exists"
    except:
        try:
            db.create_collection(name=new_name, embedding_function=embeddings)
        except Exception as err:
            return "Collection Create Failed: " + str(err)
#---------------------------------------- Clear a Collection -------------------------------------

#---------------------------------------- Collection Info -------------------------------------
def collection_stats(col):
    return col.count(), col.peek(2)

#---------------------------------------- List Collections in a DB -------------------------------------

def collection_delete_where(clause):
    return "Currently Unavailable"

def get_metadatas():
    return "Currently Unavailable"

def add_test_doc():
    st.session_state.working_col.add(
    documents=["lorem ipsum..", "doc2", "doc3"],
    metadatas=[{"chapter": "3", "verse": "16"}, {"chapter": "3", "verse": "5"}, {"chapter": "29", "verse": "11"}],
    ids=["id1", "id2", "id3"]
)