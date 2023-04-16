import streamlit as st
import pandas as pd
import data_management
import sqlite3
 
st.session_state.file_submit = False

def app():
    st.markdown("## Add and Delete Data")
    col1, col2 = st.columns([6, 4])
    with col1:
        # Selectbox of options for data management
        option = st.selectbox(label="Select a Command", options=["Select Option", "Add Data", "Delete Data"])

        if option == "Add Data":
            # If both file and category forms have been submitted
            st.write(st.session_state.file_submit)
            st.write(st.session_state.category_submit)
            if st.session_state.file_submit and st.session_state.category_submit:
                st.write("Done")

            # Create form for uploading files 
            with st.form("data form"):
                file = st.text_input(label="Enter the name of the file you would like to add or delete")
                semester = st.text_input(label="Enter the semester of the spreadsheet")
                st.write("File example: Spring 2022 Event Info (Data Project).xlsx")
                st.write("Note: Semester should be in the format 'Season Year'. For example: Fall 2022")
                submit = st.form_submit_button("Submit")

                # If submit button pressed
                if submit:
                    st.session_state.file_submit = True
                    print("submitted")

            # If submitted 
            if st.session_state.file_submit:
                categories = []
                file_path = "data/" + file

                # try to find the file or indicate failure
                try:
                    sheets = pd.read_excel(file_path, sheet_name=None)

                    # Create form for category selects
                    with st.form("Categorization form"):

                        # for all events in spreadsheet, create selectbox and add to category 
                        for event in sheets:
                            st.write(event)
                            selectbox = st.selectbox(label="Select category", options=["Research and Development", "Service", "Community Building", "Professional Development"], key=event)
                            categories.append(selectbox)
                        second_submit = st.form_submit_button("Submit Categorizations")
                        if second_submit:
                            st.write("submitted again")
                            print(categories)
                            st.session_state.category_submit = True
                except:
                    st.write("Could not load the file. Please ensure the file name and data formatting is correct")

                    # add to state
                    #try:
                     #   data_management.add_data(file, semester)
                        # data_management.add_data("Spring 2022 Event Info (Data Project).xlsx", Spring 2022)
                     #   st.write("Successfully uploaded the files to database!")
                    #except:
                    #    st.write("Could not load the file. Please ensure the file name and data formatting is correct")
        
        elif option == "Delete Data":
            with st.form("data form"):
                con = sqlite3.connect('eh_data.db')
                cur = con.cursor()
                cur.execute("SELECT semester from attendance_data")
                current_semesters = pd.DataFrame(cur.fetchall())
                if not current_semesters.empty:
                    current_semesters.columns = ['semester',]
                    current_semesters = pd.unique(current_semesters['semester'])
                    st.write("Existing semesters:")
                    for current_semester in current_semesters:
                        st.write(current_semester)
                semester = st.text_input(label="Enter the semester of data to delete")
                submit = st.form_submit_button("Submit")
                if submit:
                    try:
                        data_management.delete_data(semester)
                        st.write("Successfully deleted semester from the database!")
                    except:
                        st.write("Error occurred in the deletion process. Ensure that input is valid.")
        
        elif option == "Select Option":
            # File Format
            st.write("File format Information")
            st.write("Format files with <>")
            st.write("Example file below:")

        
# session state
# classification extras

    
    

