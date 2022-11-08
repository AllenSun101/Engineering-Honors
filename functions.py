import pandas as pd
import numpy as np

def open_file(file_name):
    return pd.ExcelFile(file_name)


def data_clean(file, a_start, a_end, r_start, r_end):
    sheets = dict()
    for sheet in file.sheet_names:
        whole_sheet = pd.read_excel(file, sheet)
        attendance = whole_sheet.iloc[:, a_start:a_end]
        attendance = attendance.dropna()
        registered = whole_sheet.iloc[:, r_start:r_end]
        registered = registered.replace("Yes", 1)
        registered = registered.replace("No", 0)
        registered = registered.dropna()
        registered["Registered"] = registered["Registered"].astype(int)
        sheets[(sheet, "a")] = attendance
        sheets[(sheet, "r")] = registered
    return sheets

def create_csvs(sheets):
    for ws in sheets:
        if ws[1] == "a":
            sheets[ws].to_csv("data/" + ws[0] + "_a.csv", index=False)
        else:
            sheets[ws].to_csv("data/" + ws[0] + "_r.csv", index=False)