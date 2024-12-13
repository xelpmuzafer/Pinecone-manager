import streamlit as st

pg = st.navigation([st.Page("delete_vector.py"), st.Page("fetch_data.py")])
pg.run()