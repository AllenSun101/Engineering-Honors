import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import data_management
import plot_revised

# Need to fix initialize bug
st.session_state.Semester = "All Semesters"
st.session_state.Event = "All Events"
st.session_state.Major = "All Majors"
st.session_state.Class = "All Classes"
st.session_state.X_axis = "Semester"


st.session_state.PrevAllSemesters = True



def app():

    # Check if session state exists
    if "Semester" not in st.session_state:
        st.session_state.Semester = "All Semesters"
        st.session_state.Event = "All Events"
        st.session_state.Major = "All Majors"
        st.session_state.Class = "All Classes"

    # Options Storage
    semesters = ["All Semesters"]
    events = ["All Events"]
    majors = ["All Majors"]
    class_years = ["All Classes"]
    
    st.markdown("## Attendance Visualization")

    # Create Columns for the widgets
    col1, col2, col3, col4 = st.columns(4)

    # Handle Updated Session Values
    # Moving between semesters
    if st.session_state.Semester != "All Semesters":
        data = data_management.get_data(st.session_state.Semester, "All Events", "All Majors", "All Classes", "Attendance")
        unique_events = pd.unique(data['event'])
        if st.session_state.Event not in unique_events:
            if st.session_state.Event != "All Events":
                st.session_state.Major = "All Majors"
                st.session_state.Class = "All Classes"
            st.session_state.Event = "All Events"
        major_class_attendance_data = data_management.get_data(st.session_state.Semester, st.session_state.Event, "All Majors", "All Classes", "Attendance")
        if st.session_state.Major not in pd.unique(major_class_attendance_data['major']):
            st.session_state.Major = "All Majors"
        if st.session_state.Class not in pd.unique(major_class_attendance_data['classification_year']):
            st.session_state.Class = "All Classes"
            

    elif st.session_state.Event != "All Events":
        if st.session_state.PrevAllSemesters:
            st.session_state.Semester = data_management.find_semester_from_event(st.session_state.Event, "Attendance")
        else:
            st.session_state.Event = "All Events"
        st.session_state.Major = "All Majors"
        st.session_state.Class = "All Classes"
        

    if st.session_state.Semester == "All Semesters" and st.session_state.Event == "All Events":
        st.session_state.PrevAllSemesters = True
    else:
        st.session_state.PrevAllSemesters = False
    

    # selectbox options never change
    semester_attendance_data = data_management.get_data("All Semesters", "All Events", "All Majors", "All Classes", "Attendance")
    semesters.extend(pd.unique(semester_attendance_data['semester']))
    
    # selectbox based on semester
    event_attendance_data = data_management.get_data(st.session_state.Semester, "All Events", "All Majors", "All Classes", "Attendance")
    events.extend(pd.unique(event_attendance_data['event']))
    st.session_state.Event = st.session_state.Event

    # selectboxes based on semester and event 
    major_class_attendance_data = data_management.get_data(st.session_state.Semester, st.session_state.Event, "All Majors", "All Classes", "Attendance")
    majors.extend(pd.unique(major_class_attendance_data['major']))
    if st.session_state.Major not in majors:
        st.session_state.Major = "All Majors"
    st.session_state.Major = st.session_state.Major
    
    class_years.extend(pd.unique(major_class_attendance_data['classification_year']))
    st.session_state.Class = st.session_state.Class


    # Display selectboxes
    selected_semester = col1.selectbox(label="Filter by Semester", options=semesters, key="Semester")

    selected_event = col2.selectbox(label="Filter by Event", options=events, key="Event")

    selected_major = col3.selectbox(label="Filter by Major", options=majors, key="Major")

    selected_year = col4.selectbox(label="Filter by Class", options=class_years, key="Class")

    x_axis = col1.selectbox(label="X Axis", options=['Semester', 'Event', 'Major', 'Class'], key="X_axis")


    # Query database based on session states
    attendance_data = data_management.get_data(st.session_state.Semester, st.session_state.Event, st.session_state.Major, st.session_state.Class, "Attendance")
    # print(attendance_data)


    #------------PLOT DATA HERE------------------
    # WATCH AND HANDLE EMPTY DATASET CASES!!!!!

    if attendance_data.empty:
        st.write("### Empty set of data")
    else:
        freq_dict = plot_revised.get_frequency(attendance_data, x_axis)
        plot_revised.plot(freq_dict, "Attendance By " + x_axis, x_axis, False)



