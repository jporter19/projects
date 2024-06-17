import streamlit as st
if 'msg' not in st.session_state:
    st.session_state = ''

# Display a parameter
@st.experimental_dialog("Message")
def modal_dialog(var):
    st.write(var)
    st.session_state.msg = "complete"
    return "complete"

# confirm or cancel
@st.experimental_dialog("Confirmation")
def confirm_msg(msg):
    st.write(msg)
    if st.button("Confirm",key='confirm1'):
        return "Confirm"
    if st.button("Cancel",key='cancel1'):
        return "Cancel"

if st.button("Say Hello",key='greeting'):
    msg=modal_dialog("Hello")

    st.write(msg)
#if st.button("Confirm",key='confirm2'):
#   msg = confirm_msg("Pleas e Confirm")
#    st.write(msg)


'''


@st.experimental_dialog("Collection Management")
def collections(action):
    if action == "Delete":
        collection = st.text_input(f"Enter the name of the collection to {action}")
        if st.button("Submit"):
            st.write(f"Collection '{collection}' has been DELETED")
            #db.delete_collection(collection)
    elif action == "Add":
        collection = st.text_input(f"Enter the name of the collection to {action}")
        if st.button("Submit"):
            st.write(f"Collection '{collection}' has been CREATED")
            #db.create_collection(collection)
    else:
        st.write("Error: Invalid Action")
  
st.write("Add or delete a collection")
if st.button("Add a New Collection"):
    collections("Add")
elif st.button("Delete a Collection"):
    collections("Delete")
else:
    if st.button("Cancel"):
        st.write("CANCELLED")
        '''