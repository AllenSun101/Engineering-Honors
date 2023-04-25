import streamlit as st
import pandas as pd
import model_deploy 


def app():
    st.markdown("## Machine Learning")
    month = st.selectbox('month:', ["Jan","Feb","Mar","Apr","May","Aug","Sep","Oct","Nov"])
    year = st.selectbox('year (2-digit):', [2019, 2020, 2021, 2022, 2023, 2024])
    major = st.selectbox('major:', ['BAEN', 'BMEN', 'CHEN', 'CPEN', 'CPSC', 'CSCE', 'CVEN', 'ECEN', 'ELEN', 'ENGE', 'ESET', 'ETID', 'EVEN', 'IDIS', 'INEN', 'ISEN', 'ITDE', 'MEEN', 'MMET', 'MSEN', 'MTDE', 'MXET', 'NUEN', 'OCEN', 'PETE', 'TEAB'])
    classificationCategory = st.selectbox('classification:', ['Freshman', 'Sophomore', 'Junior', 'Senior'])
    eventCategory = st.selectbox("event category:", ["Community Building", "Professional Development", "Research and Development", "Service"])

    month_dict = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 
                'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    month = month_dict[month]
    year_dict = {2019: 19, 2020: 20, 2021: 21, 2022: 22, 2023: 23, 2024: 24}
    year = year_dict[year]
    class_dict = {"Freshman": "FR", "Sophomore": "SO", "Junior": "JR", "Senior": "SR"}
    classificationCategory = class_dict[classificationCategory]

    predictions = model_deploy.classification_predict(month, year, major, classificationCategory, eventCategory)
    st.write("### The estimated attendance probability is calculated below: ")
    st.write(f"From KNN model: {round(predictions['knn'],2)}")
    st.write(f"From random forest model: {round(predictions['random forest'],2)}")
    st.write(f"From SVM model: {round(predictions['svm'],2)}")

