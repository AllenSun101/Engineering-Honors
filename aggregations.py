import pandas as pd

def getCount(dataFrame, cName: str):
    col1 = dataFrame[cName].value_counts().index
    col2 = list(dataFrame[cName].value_counts())
    return pd.DataFrame({cName: col1, "Counts": col2})