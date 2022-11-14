import pandas as pd
import numpy as np



def open_file(file_name):
    """
    @param file_name - name of workbook

    @return bundled dataframe of all sheets in workbook
    """
    return pd.ExcelFile(file_name)


def data_clean(file: str, a_start: int, a_end: int, r_start: int, r_end: int) -> dict:
    """
    @param file - name of workbook
    @param a_start - column to start on (inclusive)
    @param a_end - column to end on (non-inclusive)
    @param r_start - row to start on (inclusive)
    @param r_end - row to end on (non-inclusive)

    @return dict of dataframes for each attended (a) and registered (r) dataset (key=(sheet_name, a/r), value=dataframe)
    """
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
    """
    @param file_name - name of workbook

    @return bundled dataframe of all sheets in workbook
    """
    for ws in sheets:
        if ws[1] == "a":
            sheets[ws].to_csv("data/" + ws[0] + "_a.csv", index=False)
        else:
            sheets[ws].to_csv("data/" + ws[0] + "_r.csv", index=False)