import pickle
import streamlit as st
import pandas as pd
import sklearn


with open('knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)
with open('svm_model.pkl', 'rb') as f:
    svm_model = pickle.load(f)
with open('rf_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

def classification_predict(month, year, major, classificationCategory, eventCategory):
    
    original = pd.DataFrame(columns=['month', 'year', 'major_AERO', 'major_AREN', 'major_BAEN', 'major_BMEN',
       'major_CECN', 'major_CEEN', 'major_CHEN', 'major_CLEN', 'major_COMP',
       'major_CPEN', 'major_CPSC', 'major_CSCE', 'major_CVEN', 'major_ECEN',
       'major_ELEN', 'major_ENGE', 'major_ESET', 'major_ETID', 'major_EVEN',
       'major_IDIS', 'major_INEN', 'major_ISEN', 'major_ITDE', 'major_MEEN',
       'major_MMET', 'major_MSEN', 'major_MTDE', 'major_MXET', 'major_NUEN',
       'major_OCEN', 'major_PETE', 'major_TEAB', 'classificationCategory_FR',
       'classificationCategory_JR', 'classificationCategory_SO',
       'classificationCategory_SR', 'eventCategory_Community Building',
       'eventCategory_Professional Development',
       'eventCategory_Research and Development', 'eventCategory_Service'])
    df_pred = pd.DataFrame([[month, year, major, classificationCategory, eventCategory]], columns=['month','year','major', 'classificationCategory', 'eventCategory'])
    df_pred = pd.get_dummies(df_pred, columns=['major', 'classificationCategory', 'eventCategory'])
    df_pred = df_pred.reindex(original.columns, axis=1, fill_value=0)
    df_pred.fillna(0, inplace=True)
    pred1 = knn_model.predict_proba(df_pred)
    pred2 = rf_model.predict_proba(df_pred)
    pred3 = svm_model.predict_proba(df_pred)
    results = {"knn": pred1[0][0], "random forest": pred2[0][0], "svm": pred3[0][0]}
    return results



