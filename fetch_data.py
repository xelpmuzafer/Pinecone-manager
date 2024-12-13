import streamlit as st
from pinecone import Pinecone, ServerlessSpec
import pandas as pd
from SupabaseHandler import get_all_group_ids, get_keys

# Streamlit app title
st.title("Pinecone Document Viewer")


# Initialize Pinecone
api_key = st.text_input("Enter your Pinecone API Key", type="password", value="")
index_name = st.text_input("Enter your Pinecone Index Name", value="")

supabase_namespace = f"supabase/{index_name}_new"


list_of_source = get_all_group_ids(supabase_namespace)


# Create a dropdown to select a source with truncated options
def truncate_source(source, length=50):
    return source if len(source) <= length else "..." + source[-length:]

truncated_sources = [truncate_source(source) for source in list_of_source]
source_mapping = dict(zip(truncated_sources, list_of_source))
selected_truncated_source = st.selectbox("Select a Source", options=truncated_sources) if truncated_sources else None

selected_source = source_mapping.get(selected_truncated_source) if selected_truncated_source else None



vector_ids = get_keys(supabase_namespace, selected_source) if len(list_of_source) > 0 else []

if api_key and index_name:
    try:
        # Initialize Pinecone client
        pc = Pinecone(api_key=api_key)
        index = pc.Index(index_name)

        # Fetch list of all documents
        st.write("Fetching documents from Pinecone...")
       

        
        # Query the documents with pagination
        results = index.fetch(sorted(vector_ids))

        st.write(f"Total documents in the index: {len(results["vectors"].items())}")

        # Prepare data for display
        data = []
        for doc_id, doc in results["vectors"].items():
            page_content = doc['metadata'].get('text', "N/A")
         
            st.markdown(f"""
                <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; background-color: grey;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <code style="font-size: 14px;">{doc_id}</code>
                    </div>
                    <div style="margin-top: 10px;">{page_content}</div>
                </div>
            """, unsafe_allow_html=True)


        if len(data) == 0:
       
            st.write("No documents found for the given page number and limit.")

    except Exception as e:
        st.error(f"Error: {str(e)}")
else:
    st.write("Please provide the API Key, Environment, and Index Name to proceed.")
