import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import glob


# Streamlit app reruns every time a selectbox option is changed
# However, the selectbox options will not be reset to default

def app():

    # Options Storage
    semesters = ["All Semesters"]
    events = ["All Events"]
    majors = ["All Majors"]
    class_years = ["All Classes"]

    # Get Excel files, extract semester/event information and add to list
    path = "data/"
    semester_files = glob.glob(path + "*.xlsx")

    for file_name in semester_files:
        workbook_semester = " ".join(file_name.split("\\")[1].split(" ")[0:2])
        semesters.append(workbook_semester)
        file = pd.read_excel(file_name, sheet_name=None)
        for workbook_event in file:
            events.append(workbook_event)

    st.markdown("## Engineering Honors Main")

    # Create Columns for the widgets
    col1, col2, col3, col4 = st.columns(4)

    # SEMESTER SELECTBOX
    selected_semester = col1.selectbox(label="Filter by Semester", options=semesters)

    # EVENT SELECTBOX
    # If All Semesters is selected, keep the fully-rendered options
    if selected_semester == "All Semesters":
        selected_event = col2.selectbox(label="Filter by Event", options=events)
    # Otherwise, only render the specific semester events
    else:
        events = ["All Events"]
        selected_datafile_name = "data/" + selected_semester + " Event Info (Data Project).xlsx"
        selected_datafile = pd.read_excel(selected_datafile_name, sheet_name=None)
        for event_entry in selected_datafile:
            events.append(event_entry)
        selected_event = col2.selectbox(label="Filter by Event", options=events)

    # MAJOR SELECTBOX
    majors = getMajorOptions(selected_semester, selected_event)    
    # Collect all unique engineering codes
    col3.selectbox(label="Filter by Major", options=majors)

    # CLASS SELECTBOX
    # Get all years from every dataset if "all semesters" is selected
    if selected_semester == "All Semesters":
        for semester in semesters:
            if semester == "All Semesters":
               continue
            year = semester.split(" ")[1] 
            if year not in class_years:
                class_years.append(year)
        # Find the latest year
        latest_year = 0
        for year in class_years:
            if year == "All Classes":
                continue
            if int(year) > int(latest_year):
                latest_year = int(year)
        # To account for current students, add 4 years to the lastest 
        for i in range(1, 5):
            class_years.append(str(latest_year + i))
    else:
        year = selected_semester.split(" ")[1]
        season = selected_semester.split(" ")[0]
        start = year
        if season == "Fall":
            # start with the next calendar year
            start = str(int(start) + 1)
        # Add 4 years to the start for all graduation years
        for i in range(4):
            class_years.append(str(int(start) + i))
    selected_year = col4.selectbox(label="Filter by Class", options=class_years)


    # Template Stuff- Ignore/Delete everything below

    temp_data = pd.read_excel("data/Fall 2019 Event Info (Data Project).xlsx", sheet_name="(12.11.19) Study pectacular")
    
    st.write(" ")
    st.write(" ")
    st.write(" ")


    col1, col2 = st.columns([7, 3])
    with col1:
        st.bar_chart(temp_data, x="Major", y="Attended")

    labels = temp_data["Major"].dropna().unique()
    # Made up data for the pie chart 
    sizes = [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2]

    with col2:
        fig, ax = plt.subplots(figsize=(5,4))
        ax.pie(sizes, labels=labels)
        st.pyplot(fig)


def getMajorOptions(semesters, events):
    unique_majors = []
    # All Semesters, All Events
    if semesters == "All Semesters":
        path = "data/"
        semester_files = glob.glob(path + "*.xlsx")
        for selected_datafile_name in semester_files:
            sheets = pd.read_excel(selected_datafile_name, sheet_name=None)
            for sheetname in sheets:
                df = pd.read_excel(selected_datafile_name, sheet_name=sheetname)
                df = df["Major"].dropna()
                for major in df:
                    if major not in unique_majors:
                        unique_majors.append(major)
    else:
        # Specific Semester, All Events
        selected_datafile_name = "data/" + semesters + " Event Info (Data Project).xlsx"
        if events == "All Events":
            sheets = pd.read_excel(selected_datafile_name, sheet_name=None)
            for sheetname in sheets:
                df = pd.read_excel(selected_datafile_name, sheet_name=sheetname)
                df = df["Major"].dropna()
                for major in df:
                    if major not in unique_majors:
                        unique_majors.append(major)
        # Specific Semester and Events
        else:
            sheetname = pd.read_excel(selected_datafile_name, sheet_name=events)
            df = sheetname["Major"].dropna()
            for major in df:
                if major not in unique_majors:
                    unique_majors.append(major)
    # Sort alphabetically, add All Majors option to front (default option)
    unique_majors = sorted(unique_majors)
    unique_majors.insert(0, "All Majors")
    return unique_majors

