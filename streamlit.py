import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
from multipage import MultiPage
from dashboard1 import app as dasbhoard1_app
from dashboard2 import app as dashboard2_app
from dashboard1_new import app as dashboard1_new_app
from manage_data_dashboard import app as manage_data
from machine_learning import app as machine_learning

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.set_page_config(layout="wide")
app.add_page("Main", dasbhoard1_app)
app.add_page("Attendance Analytics", dashboard1_new_app)
app.add_page("Turnout Rates", dashboard2_app)
app.add_page("Machine Learning", machine_learning)
app.add_page("Manage Data", manage_data)

# add page for data insertion/manipulation

# The main app
app.run()

