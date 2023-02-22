import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
from multipage import MultiPage
from dashboard1 import app as dasbhoard1_app
from dashboard2 import app as dashboard2_app

# Create an instance of the app 
app = MultiPage()

# Title of the main page
st.set_page_config(layout="wide")
app.add_page("Main", dasbhoard1_app)
app.add_page("Alternative", dashboard2_app)

# The main app
app.run()

