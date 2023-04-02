import streamlit as st
import pandas as pd
import data_management


def app():
    st.markdown("## Add and Delete Data")
    col1, col2 = st.columns([6, 4])
    with col1:
        option = st.selectbox(label="Select a Command", options=["Select Option", "Add Data", "Delete Data"])
        if option == "Add Data":
            with st.form("data form"):
                file = st.text_input(label="Enter the name of the file you would like to add or delete")
                semester = st.text_input(label="Enter the semester of the spreadsheet")
                st.write("File example: Spring 2022 Event Info (Data Project).xlsx")
                st.write("Note: Semester should be in the format 'Season Year'. For example: Fall 2022")
                submit = st.form_submit_button("Submit")
                if submit:
                    try:
                        data_management.add_data(file, semester)
                        # data_management.add_data("Spring 2022 Event Info (Data Project).xlsx", Spring 2022)
                        st.write("Successfully uploaded the files to database!")
                    except:
                        st.write("Could not load the file. Please ensure the file name and data formatting is correct")
        elif option == "Delete Data":
            with st.form("data form"):
                # Display list of existing semesters?
                semester = st.text_input(label="Enter the semester of data to delete")
                submit = st.form_submit_button("Submit")
                if submit:
                    try:
                        data_management.delete_data(semester)
                        st.write("Successfully deleted semester from the database!")
                    except:
                        st.write("Error occurred in the deletion process. Ensure that input is valid.")

        


    
    

