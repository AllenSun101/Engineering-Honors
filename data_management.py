import sqlite3
import pandas as pd


# Initially create SQL Table, feed spreadsheets into them
con = sqlite3.connect('eh_data.db')


# Create tables if not already created
con.execute('''CREATE TABLE IF NOT EXISTS attendance_data
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            semester VARCHAR(50) NOT NULL,
            major VARCHAR(50) NOT NULL,
            classification VARCHAR(50) NOT NULL, 
            event VARCHAR(50) NOT NULL,
            attended INTEGER NOT NULL)''')

con.execute('''CREATE TABLE IF NOT EXISTS registration_data
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            semester VARCHAR(50) NOT NULL,
            major VARCHAR(50) NOT NULL,
            classification VARCHAR(50) NOT NULL,
            event VARCHAR(50) NOT NULL,
            registered INTEGER NOT NULL)''')

con.close()


# Inserting data
def add_data(file_name, semester):
    con = sqlite3.connect('eh_data.db')

    cur = con.cursor()
    file_path = "data/" + file_name

    sheets = pd.read_excel(file_path, sheet_name=None)

    # Get individual sheets
    for event in sheets:
        event_sheet = pd.read_excel(file_path, sheet_name=event)

        # Process attendance data and insert to database
        attended = event_sheet[['Attended', 'Major', 'Classification']]
        attended = attended.dropna()

        for i in range(len(attended)):
            try:
                major = attended['Major'][i]
                classification = get_class_year(semester, attended['Classification'][i])
                attend_status = int(attended['Attended'][i])
                cur.execute("INSERT INTO attendance_data (semester, major, classification, attended, event) VALUES (?, ?, ?, ?, ?)"
                         , (semester, major, classification, attend_status, event))
            except:
                print("Attend Error")
                continue

        # Process registration data and insert to database
        registered = event_sheet[['Registered', 'Major.1', 'Classification.1']]
        registered = registered.dropna()
        registered['Registered'] = registered['Registered'].replace("Yes", 1)
        registered['Registered'] = registered['Registered'].replace("No", 0)

        for i in range(len(registered)):
            try:
                major = registered['Major.1'][i]
                classification = get_class_year(semester, registered['Classification.1'][i])
                register_status = int(registered['Registered'][i])
                cur.execute("INSERT INTO registration_data (semester, major, classification, registered, event) VALUES (?, ?, ?, ?, ?)"
                         , (semester, major, classification, register_status, event))
            except:
                print("Register Error")
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

    if semester == "All Semesters" and event == "All Events" and major == "All Majors" and classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data")
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data")

    elif semester == "All Semesters" and event == "All Events" and classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE major = ?", (major,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE major = ?", (major,))

    elif semester == "All Semesters" and event == "All Events" and major == "All Majors":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE classification = ?", (classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE classification = ?", (classification,))
        
    elif semester == "All Semesters" and event == "All Events":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE major = ? AND classification = ?", (major, classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE major = ? classification = ?", (major, classification,))

    elif event == "All Events" and major == "All Majors" and classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ?", (semester,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE semester = ?", (semester))

    elif event == "All Events" and major == "All Majors":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND classification = ?", (semester, classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND classification = ?", (semester, classification,))

    elif event == "All Events" and classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND major = ?", (semester, major,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND major = ?", (semester, major,))

    elif event == "All Events":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND major = ? AND classification = ?", (semester, major, classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND major = ? AND classification = ?", (semester, major, classification,))

    elif major == "All Majors" and classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND event = ?", (semester, event,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND event = ?", (semester, event,))

    elif major == "All Majors":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND event = ? AND classification = ?", (semester, event, classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND event = ? AND classification = ?", (semester, event, classification,))
        
    elif classification == "All Classes":
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND event = ? AND major = ?", (semester, event, major,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND event = ? AND major = ?", (semester, event, major,))
   
    else:
        if data_type == "Attendance":
            cur.execute("SELECT * FROM attendance_data WHERE semester = ? AND event = ? AND major = ? AND classification = ?", (semester, event, major, classification,))
        elif data_type == "Registration":
            cur.execute("SELECT * FROM registration_data WHERE semester = ? AND event = ? AND major = ? AND classification = ?", (semester, event, major, classification,))
   
    results = pd.DataFrame(cur.fetchall())
    con.close()

    # Handle empty datasets
    if results.empty:
        return results

    # Otherwise, assign columns
    results.columns = ['id', 'semester', 'major', 'classification', 'event', 'attended']
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


