import streamlit as st
import pandas as pd
import data_management
import sqlite3
 
st.session_state.file_submit = False
st.session_state.reset = True

def app():
    st.markdown("## Add and Delete Data")
    col1, col2 = st.columns([6, 4])
    
    with col1:
        # Selectbox of user options 
        option = st.selectbox(label="Select a Command", options=["Select Option", "Add Data", "Delete Data"])

        if option == "Add Data":
            # Create form for uploading files 
            with st.form("data form"):
                file = st.text_input(label="Enter the name of the file you would like to add or delete")
                semester = st.text_input(label="Enter the semester of the spreadsheet")
                if st.session_state.reset:
                    change_key = True
                st.write("File example: Spring 2022 Event Info (Data Project).xlsx")
                st.write("Note: Semester should be in the format 'Season Year'. For example: Fall 2022")
                submit = st.form_submit_button("Submit")

                # If submit button pressed
                if submit:
                    st.session_state.file_submit = True
                    print("submitted")

            # If first submit button pressed 
            if st.session_state.file_submit:
                categories = []
                file_path = "data/" + file

                # Attempt to find the file or indicate failure
                try:
                    sheets = pd.read_excel(file_path, sheet_name=None)

                    # Create form for category selects
                    with st.form("Categorization form"):
                        # For each event, create selectbox and add to category 
                        for event in sheets:
                            st.write(event)
                            selectbox = st.selectbox(label="Select category", options=["Research and Development", "Service", "Community Building", "Professional Development"], key=event)
                            categories.append(selectbox)
                        second_submit = st.form_submit_button("Submit Categorizations")
                        
                        # TODO- handle second submit
                        if second_submit:
                            st.write("submitted again")
                            print(categories)
                            data_management.add_data(file, semester, categories)
                            # data_management.add_data("Spring 2022 Event Info (Data Project).xlsx", Spring 2022)
                            st.session_state.file_submit = False
                except:
                    st.write("Could not load the file. Please ensure the file name and data formatting is correct")

        elif option == "Delete Data":
            with st.form("data form"):
                con = sqlite3.connect('eh_data.db')
                cur = con.cursor()

                # Get list of all semesters
                cur.execute("SELECT semester from attendance_data")
                current_semesters = pd.DataFrame(cur.fetchall())

                # Display list of existing semesters
                if not current_semesters.empty:
                    current_semesters.columns = ['semester',]
                    current_semesters = pd.unique(current_semesters['semester'])
                    st.write("Existing semesters:")
                    for current_semester in current_semesters:
                        st.write(current_semester)

                # Input semester to delete
                semester = st.text_input(label="Enter the semester of data to delete")
                submit = st.form_submit_button("Submit")
                if submit:
                    try:
                        data_management.delete_data(semester)
                        st.write("Successfully deleted semester from the database!")
                    except:
                        st.write("Error occurred in the deletion process. Ensure that input is valid.")
        
        # If default option
        elif option == "Select Option":
            # File Format Instructions
            st.write("File Formatting:")
            st.write("Format files with like the example files in the 'data' folder.")
            st.write("Sheetnames should be in the format: 'm.dd.yyyy (event_name)'")
            st.write("For each sheet, column whitespace does not matter, but ordering and names should follow the same format.")
            st.write("Add all data files to the 'data' folder.")
    

# FR-change on plot
# Plot textsize
# Aggregation Table- SQL commands after inserting data
# Submit Form Handling
# No data bug
