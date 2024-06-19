import chromadb
import streamlit as st 
import sys
sys.path.append('b:\\code\\projects\\chatbot\\pages')
from chroma_functions import create_collection, delete_collection, change_name, db_collections

if 'col_choice' not in st.session_state:
    st.session_state['col_choice']=None
st.session_state

run_client = chromadb.PersistentClient("b:\\python\\database\\booboo")
try:
    run_client.get_collection(name="test")
except Exception as err:
    st.write(str(err))

create_collection(run_client,"john")
st.selectbox("Pick a Collection",db_collections(run_client),key='col_picker',index=None)
st.write(st.session_state.col_picker)

