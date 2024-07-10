import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import streamlit_authenticator as stauth
import hashlib

st.write(st.__version__)

# Define page navigation using sidebar selectbox
page = st.sidebar.selectbox("Choose a page", ["Login Page", "Register New User"])

# Define function for each page
def login_page():
    st.write("This is the Login Page")

def register_user_page():
    st.write("This is the Register New User Page")
    # Your registration logic here

# Display pages based on user selection
if page == "Login Page":
    login_page()
elif page == "Register New User":
    register_user_page()
