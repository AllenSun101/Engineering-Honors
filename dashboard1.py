import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def app():
    st.markdown("## Engineering Honors Main Demo")
    col1, col2, col3, col4 = st.columns(4)
    col1.selectbox(label="Filter by Semester", options=["Fall 2022"])
    col2.selectbox(label="Filter by Event", options=["Event 2022"])
    col3.selectbox(label="Filter by Major", options=["Major 2022"])
    col4.selectbox(label="Filter by Class", options=["Class 2022"])

    temp_data = pd.read_excel("data/Fall 2019 Event Info (Data Project).xlsx", sheet_name="(12.11.19) Study pectacular")
    
    st.write(" ")
    st.write(" ")
    st.write(" ")


    col1, col2 = st.columns([7, 3])
    with col1:
        st.bar_chart(temp_data, x="Major", y="Attended")

    labels = temp_data["Major"].dropna().unique()
    sizes = [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2]

    with col2:
        fig, ax = plt.subplots(figsize=(5,4))
        ax.pie(sizes, labels=labels)
        st.pyplot(fig)


    

