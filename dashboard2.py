import streamlit as st
import pandas as pd

def app():
    st.markdown("## Engineering Honors Alternate Page")
    col1, col2, col3 = st.columns(3)
    col1.selectbox(label="Filter by Event", options=["Event 2022"])
    col2.selectbox(label="Filter by Major", options=["Major 2022"])
    col3.selectbox(label="Filter by Class", options=["Class 2022"])
    
    

