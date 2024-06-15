import streamlit as st

# Display a parameter
@st.experimental_dialog("Message")
def modal_dialog(var):
    st.write(var)
modal_dialog("boy oh boy")


# confirm or cancel
@st.experimental_dialog("Confirmation")
def confirm_msg(msg):
    st.write(msg)
    st.button("Confirm")
    st.button("Cancel")
confirm_msg("Confirm Deletion?")

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