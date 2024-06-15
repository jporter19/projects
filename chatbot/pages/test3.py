import streamlit as st
import chromadb

# get Chroma Collection Stats - currently 3 documents
def collection_stats(col):  
    return col.count(), col.peek(2)
# get list of collection - currently 1 collection
def db_collections(db):
    collections = []
    for i in range (db.count_collections()):
        collections.append(db.list_collections()[i].name)
    return collections
def change_check():
    st.write("in change_check") # this displays correctly
    st.session_state.change = True

#initialize variables
working_col = None
if 'change' not in st.session_state:
    st.session_state.change = False
working_db =chromadb.PersistentClient(path=st.session_state.dbpath)
pick = st.selectbox("Pick a Collection",db_collections(working_db),index=None,key='colpick', on_change=change_check)
if st.session_state.change:    # ----- THIS BREAKS BUTTON 
    working_col = working_db.get_collection(pick)
    st.session_state.change = False   # ----- THIS BREAKS BUTTON 
if working_col != None:
    st.write(f'outer: {working_col.count()}')   # this returns 'outer 3'
    col1, col2 = st.columns(2)
    if pick:
        st.write(f'if pick: {working_col.count()}')   # this returns 'if pick 3'
        with col1:
            st.write(f'column 1: {working_col.count()}')  # this returns 'column 1: 3'
            if st.button("Collection Stats"):
                # In current state - clicking this button resets the page 
                st.write("Hi there")  # This will only print when the if statement marked THIS BREAKS BUTTON is removed
                count, peek = collection_stats(working_col)


