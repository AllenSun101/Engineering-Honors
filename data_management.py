import sqlite3
import pandas as pd
import regex as re 


# Initially create SQL Table, feed spreadsheets into them
con = sqlite3.connect('eh_data.db')


# Create tables if not already created
con.execute('''CREATE TABLE IF NOT EXISTS registration_data
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            semester VARCHAR(50) NOT NULL,
            major VARCHAR(50) NOT NULL,
            classificationYear VARCHAR(50) NOT NULL, 
            classificationCategory VARCHAR(50) NOT NULL,
            event VARCHAR(50) NOT NULL,
            eventCategory VARCHAR(50) NOT NULL,
            undatedEvent VARCHAR(50) NOT NULL,
            month VARCHAR(50) NOT NULL,
            year VARCHAR(50) NOT NULL,
            attended INTEGER NOT NULL)''')

con.execute('''CREATE TABLE IF NOT EXISTS attendance_data
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            semester VARCHAR(50) NOT NULL,
            major VARCHAR(50) NOT NULL,
            classificationYear VARCHAR(50) NOT NULL, 
            classificationCategory VARCHAR(50) NOT NULL,
            event VARCHAR(50) NOT NULL,
            eventCategory VARCHAR(50) NOT NULL,
            undatedEvent VARCHAR(50) NOT NULL,
            month VARCHAR(50) NOT NULL,
            year VARCHAR(50) NOT NULL,
            registered INTEGER NOT NULL)''')

con.close()


# Inserting data
def add_data(file_name, semester, event_categories):
    con = sqlite3.connect('eh_data.db')

    cur = con.cursor()
    file_path = "data/" + file_name

    sheets = pd.read_excel(file_path, sheet_name=None)

    # Keeps track of index in event counter
    event_category_counter = 0

    # Get individual sheets
    for event in sheets:
        # Get pandas dataframe for event sheet
        event_sheet = pd.read_excel(file_path, sheet_name=event)

        # Handle event name and date
        modified_event = extract_date_and_remove_from_column(event)
        month = modified_event[0]
        year = modified_event[1]
        undated_event = modified_event[2]

        # Handle event categories
        event_category = event_categories[event_category_counter]
        event_category_counter += 1


        # Process registration data and insert to database
        registered = event_sheet[['Attended', 'Major', 'Classification']]
        registered = registered.dropna()

        # Cycle through entries for registration data
        for i in range(len(registered)):
            try:
                major = registered['Major'][i]
                classification = get_class_year(semester, registered['Classification'][i])
                classification_category = registered['Classification'][i][0:2]
                attend_status = int(registered['Attended'][i])

                # Insert into database
                cur.execute("INSERT INTO registration_data (semester, major, classificationYear, classificationCategory, attended, event, eventCategory, undatedEvent, month, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                         , (semester, major, classification, classification_category, attend_status, event, event_category, undated_event, month, year))
            except:
                # print("Register Error")
                continue

        # Process attendance data and insert to database
        attended = event_sheet[['Registered', 'Major.1', 'Classification.1']]
        attended = attended.dropna()
        attended['Registered'] = attended['Registered'].replace("Yes", 1)
        attended['Registered'] = attended['Registered'].replace("No", 0)

        # Cycle through entries for attendance data
        for i in range(len(attended)):
            try:
                major = attended['Major.1'][i]
                classification = get_class_year(semester, attended['Classification.1'][i])
                classification_category = attended['Classification.1'][i][0:2]
                register_status = int(attended['Registered'][i])

                # Insert into database
                cur.execute("INSERT INTO attendance_data (semester, major, classificationYear, classificationCategory, registered, event, eventCategory, undatedEvent, month, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                         , (semester, major, classification, classification_category, register_status, event, event_category, undated_event, month, year))
            except:
                #print("Attend Error")
                continue

    con.commit()
    con.close()


# Delete data for semester
def delete_data(semester):
    con = sqlite3.connect('eh_data.db')
    cur = con.cursor()
    cur.execute("DELETE FROM attendance_data WHERE semester = ?", (semester, ))
    cur.execute("DELETE FROM registration_data WHERE semester = ?", (semester, ))
    con.commit()
    con.close()


# Querying data for streamlit application
def get_data(semester, event, major, classification, data_type):
    con = sqlite3.connect('eh_data.db')
    cur = con.cursor()

    # Get data depending on selectbox specifications (parameters)
    if semester == "All Semesters" and event == "All Events" and major == "All Majors" and classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data")
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data")

    elif semester == "All Semesters" and event == "All Events" and classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE major = ?", (major,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE major = ?", (major,))

    elif semester == "All Semesters" and event == "All Events" and major == "All Majors":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE classificationYear = ?", (classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE classificationYear = ?", (classification,))
        
    elif semester == "All Semesters" and event == "All Events":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE major = ? AND classificationYear = ?", (major, classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE major = ? AND classificationYear = ?", (major, classification,))

    elif event == "All Events" and major == "All Majors" and classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE semester = ?", (semester,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ?", (semester,))

    elif event == "All Events" and major == "All Majors":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND classificationYear = ?", (semester, classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND classificationYear = ?", (semester, classification,))

    elif event == "All Events" and classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND major = ?", (semester, major,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND major = ?", (semester, major,))

    elif event == "All Events":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND major = ? AND classificationYear = ?", (semester, major, classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND major = ? AND classificationYear = ?", (semester, major, classification,))

    elif major == "All Majors" and classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND event = ?", (semester, event,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND event = ?", (semester, event,))

    elif major == "All Majors":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND event = ? AND classificationYear = ?", (semester, event, classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND event = ? AND classificationYear = ?", (semester, event, classification,))
        
    elif classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND event = ? AND major = ?", (semester, event, major,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND event = ? AND major = ?", (semester, event, major,))
   
    else:
        if data_type == "Attendance":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND event = ? AND major = ? AND classificationYear = ?", (semester, event, major, classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND event = ? AND major = ? AND classificationYear = ?", (semester, event, major, classification,))
   
    results = pd.DataFrame(cur.fetchall())
    con.close()

    # Handle empty datasets
    if results.empty:
        return results

    # Otherwise, assign columns
    if data_type == "Attendance":
        results.columns = ['id', 'semester', 'major', 'classification_year', 'classification_category', 'event', 'event_category', 'undated_event', 'month', 'year', 'attended']
    elif data_type == "Registration":
        results.columns = ['id', 'semester', 'major', 'classification_year', 'classification_category', 'event', 'event_category', 'undated_event', 'month', 'year', 'registered']
    return results


def get_class_year(semester, classification):
    season = semester.split(" ")[0]
    year = int(semester.split(" ")[1])
    classification_symbol = classification[0:2]
    if season == "Fall":
        classes = {"FR": year + 4, "SO": year + 3, "JR": year + 2, "SR": year + 1}
    elif season == "Spring":
        classes = {"FR": year + 3, "SO": year + 2, "JR": year + 1, "SR": year}
    class_year = classes[classification_symbol]
    return class_year


def find_semester_from_event(event, data_type):
    con = sqlite3.connect('eh_data.db')
    cur = con.cursor()

    if data_type == "Attendance":
        cur.execute("SELECT semester FROM attendance_data WHERE event = ?", (event,))
    elif data_type == "Registration":
        cur.execute("SELECT semester FROM registration_data WHERE event = ?", (event,))

    semester = cur.fetchone()
    con.close() 
    return semester[0]


def extract_date_and_remove_from_column(event):
    # Define a regular expression to match the date information in the text column
    pattern = r'\((\d{1,2})[./](\d{1,2}|[.&]\d{1,2})[./](\d{2}|\d{4})\)'
    
    # Define a function to extract the date information and remove it from the string
    def extract_date_and_remove(string):
        match = re.search(pattern, string)
        if match:
            month = int(match.group(1))
            year = int(match.group(3))
            text = string[:match.start()] + string[match.end():]
            return (month, year, text)
        else:
            return None
    
    # Apply the extract_date_and_remove function to the string to create a tuple with the extracted date information and modified text
    modified_event_data = extract_date_and_remove(event)
    
    return modified_event_data
    