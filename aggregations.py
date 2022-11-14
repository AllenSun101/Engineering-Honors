import pandas as pd

def getCount(dataFrame, cName: str):
    """
    @param dataFrame - the dataframe to pull from
    @param cName - the column to pull data from

    @return dataframe constructed from given dataframe and column name
    """
    col1 = dataFrame[cName].value_counts().index
    col2 = list(dataFrame[cName].value_counts())
    return pd.DataFrame({cName: col1, "Counts": col2})