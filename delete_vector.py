import streamlit as st
from pinecone import Pinecone, ServerlessSpec
from SupabaseHandler import delete_record_by_key
# Streamlit app title
st.title("Pinecone Vector Deletion")

# Initialize Pinecone
api_key = st.text_input("Enter your Pinecone API Key", type="password", value="")
index_name = st.text_input("Enter your Pinecone Index Name", value="")

# Input for the vector ID to delete
vector_id_to_delete = st.text_input("Enter the Vector ID to Delete", value="")

if st.button("Delete Vector"):
    if api_key and index_name and vector_id_to_delete:
        try:
            # Initialize Pinecone client
            pc = Pinecone(api_key=api_key)
            index = pc.Index(index_name)

            # Delete the vector
            st.write(f"Attempting to delete vector with ID: {vector_id_to_delete}")
            index.delete(ids=[vector_id_to_delete])
            supabase_namespace = f"supabase/{index_name}_new"
            delete_record_by_key(supabase_namespace, vector_id_to_delete)

            

            st.success(f"Successfully deleted vector with ID: {vector_id_to_delete}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please provide all required fields: API Key, Index Name, and Vector ID.")
