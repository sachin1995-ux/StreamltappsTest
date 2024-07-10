import streamlit as st
import pandas as pd
import plotly.express as px
import hashlib
import yaml
import streamlit_authenticator as stauth

# Load configuration
with open('data/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.safe_load(file)

# Initialize authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

# Define page navigation using sidebar selectbox
page = st.sidebar.selectbox("Choose a page", ["Login Page", "Register New User", "Dashboard"])

# Login Page
def login_page():
    st.write("This is the Login Page")
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)

    if st.session_state.get("authentication_status"):
        st.success(f'Welcome {st.session_state["name"]}')
    else:
        st.info('Please login to access the dashboard.')

# Register New User Page
def register_user_page():
    st.write("This is the Register New User Page")
    # Registration logic here

# Dashboard Page
def dashboard_page():
    if st.session_state.get("authentication_status"):
        st.title("SmartSpend Campaign Monitoring Dashboard")
        uploaded_file = st.sidebar.file_uploader("Choose a file")
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
        else:
            st.info("Upload a file to display data.")
            return

        # Data processing example
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        st.write(df.head())
    else:
        st.error("You are not logged in. Please login to view the dashboard.")

# Page selection logic
if page == "Login Page":
    login_page()
elif page == "Register New User":
    register_user_page()
elif page == "Dashboard":
    dashboard_page()
