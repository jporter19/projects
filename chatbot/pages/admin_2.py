import streamlit as st
import chromadb

if "dbpath" not in st.session_state:
    st.switch_page("document-chat.py")
    
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
def create_collection(new_col):
    st.write(f"In Create {new_col}")
    try:
        st.session_state.db_client.get_collection(name=new_col)
        return "Collection Already Exists"
    except:
        try:
            st.write("RUNNING CREATE")
            st.session_state.db_client.create_collection(name=new_col, embedding_function=st.session_state.embeddings)
        except Exception as err:
            return "Collection Create Failed: " + str(err)
#---------------------------------------- Clear a Collection -------------------------------------
def clear_collection():
    return "Currently Unavailable"

#---------------------------------------- Collection Info -------------------------------------
def collection_stats():
    return st.session_state.working_col.count(), st.session_state.working_col.peek(2)

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

# ------------------------------------------ Database ------------------------------------------
def db_collections():
    collections = []
    for i in range (st.session_state.db_client.count_collections()):
        collections.append(st.session_state.db_client.list_collections()[i].name)
    return collections

def db_reset():
    try:
        st.session_state.db_client.reset()
        return "DB Reset Complete"
    except Exception as err:
        return "DB Reset Failed: " + str(err)

def db_stats():
    return st.session_state.db_client.get_version(), st.session_state.db_client.get_settings()
  

#------------------------   Initialize Variables  ------------------
dbpath = st.session_state.dbpath  # name of the vector database
if 'db_client' not in st.session_state:
    st.session_state.db_client=chromadb.PersistentClient(path=dbpath)
#st.write(db_collections(st.session_state.db_client))
# add_test_doc(working_col)
# collection_stats(working_col)   
#st.write("count:" + str(working_col.count()))
#st.write(db_client
#.list_collections())
st.title("Application Manager")
st.divider()
st.subheader("Database Management")
st.divider()
col1, col2 = st.columns([1,3])
version = None
setting = []
with col1:
    if st.button("DB Stats"):
        version,setting = db_stats()
with col2:
    expand_1 = st.expander("Database Stats")
    with expand_1:
        if version and setting:
            st.write("Version:" + str(version))
            st.write(setting)
with col1:
    if st.button("DB Reset"):
        resp = db_reset()
        with col2:
            st.write(resp)

st.divider()
st.session_state['working_col'] = None
st.subheader(f'Collection Management [{st.session_state.working_col}]')
# Choose a collection
def rerun():
    st.session_state.working_col = st.session_state.db_client.get_collection(st.session_state.colpick)
st.session_state.pick = st.selectbox("Pick a Collection",db_collections(),index=None,key='colpick', on_change=rerun)
st.divider()
col1, col2 = st.columns([1,3])
with col1:
    if st.button("Delete Collection"):
        with col2:
            collect_nm = st.selectbox("Pick a Collection",db_collections(),index=None,)
            if collect_nm != None:
                resp = delete_collection(collect_nm)
                st.write(resp)
    if st.button("Create Collection"):
        new_name = None
        new_name = st.text_input("Enter Collection Name")
        if not new_name:
            st.stop()
        resp = create_collection(new_name)
        st.write(resp)
    if st.button("Collection Stats"):
        count, peek = collection_stats()
        with col2:
            with st.expander("Collection Information"):
                st.write("Document Count:" + str(count))
                st.write(peek)
    if st.button("Rename Collection"):
        rename = None
        rename = st.text_input("Enter New Name for Collection")
        if not rename:
            st.stop()
        try:
            resp = change_name(rename)
            st.write(resp)
        except Exception as err:
            with col2:
                st.write(str(err))

    if st.button("Add Test Documents"):
        resp = add_test_doc()
        with col2:
            st.write(resp)







