import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import streamlit_authenticator as stauth
import hashlib

# import yaml
# import streamlit as st
# from yaml.loader import SafeLoader
# import streamlit_authenticator as stauth
# from streamlit_authenticator.utilities.exceptions import (CredentialsError,
#                                                           ForgotError,
#                                                           LoginError,
#                                                           RegisterError,
#                                                           ResetError,
#                                                           UpdateError) 

# # Loading config file
# with open('/Users/sachin/Downloads/config.yaml', 'r', encoding='utf-8') as file:
#     config = yaml.load(file, Loader=SafeLoader)

# # Creating the authenticator object
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['pre-authorized']
# )

pg = st.navigation([st.Page("/Users/sachin/Downloads/MonitoringDashboard_SmartSpend/Register New User.py"), 
    st.Page("/Users/sachin/Downloads/MonitoringDashboard_SmartSpend/Login Page.py"),
    st.Page("/Users/sachin/Downloads/MonitoringDashboard_SmartSpend/Update User Details.py")])
pg.run()





# # Creating a login widget
# try:
#     authenticator.login()
# except LoginError as e:
#     st.error(e)

# if st.session_state["authentication_status"]:
#     authenticator.logout()
#     st.write(f'Welcome *{st.session_state["name"]}*')
# elif st.session_state["authentication_status"] is False:
#     st.error('Username/password is incorrect')
# elif st.session_state["authentication_status"] is None:
#     st.warning('Please enter your username and password')

# # # Creating a password reset widget
# # if st.session_state["authentication_status"]:
# #     try:
# #         if authenticator.reset_password(st.session_state["username"]):
# #             st.success('Password modified successfully')
# #     except ResetError as e:
# #         st.error(e)
# #     except CredentialsError as e:
# #         st.error(e)

# # # # Creating a new user registration widget
# # try:
# #     (email_of_registered_user,
# #         username_of_registered_user,
# #         name_of_registered_user) = authenticator.register_user(pre_authorization=False)
# #     if email_of_registered_user:
# #         st.success('User registered successfully')
# # except RegisterError as e:
# #     st.error(e)

# # # # Creating a forgot password widget
# # try:
# #     (username_of_forgotten_password,
# #         email_of_forgotten_password,
# #         new_random_password) = authenticator.forgot_password()
# #     if username_of_forgotten_password:
# #         st.success('New password sent securely')
# #         # Random password to be transferred to the user securely
# #     elif not username_of_forgotten_password:
# #         st.error('Username not found')
# # except ForgotError as e:
# #     st.error(e)

# # # # Creating a forgot username widget
# # try:
# #     (username_of_forgotten_username,
# #         email_of_forgotten_username) = authenticator.forgot_username()
# #     if username_of_forgotten_username:
# #         st.success('Username sent securely')
# #         # Username to be transferred to the user securely
# #     elif not username_of_forgotten_username:
# #         st.error('Email not found')
# # except ForgotError as e:
# #     st.error(e)

# # # # Creating an update user details widget
# # if st.session_state["authentication_status"]:
# #     try:
# #         if authenticator.update_user_details(st.session_state["username"]):
# #             st.success('Entries updated successfully')
# #     except UpdateError as e:
# #         st.error(e)

# # # Saving config file
# # with open('/Users/sachin/Downloads/config.yaml', 'w', encoding='utf-8') as file:
# #     yaml.dump(config, file, default_flow_style=False)



# # if st.session_state["authentication_status"]:
# #     # Dashboard code
# #     st.title("SmartSpend Campaign Monitoring Dashboard")
# #     with st.sidebar:
# #         st.header("Configuration")
# #         uploaded_file = st.file_uploader("Choose a file")
# #         if uploaded_file is not None:
# #             df = pd.read_csv(uploaded_file)
# #         else:
# #             st.info("Upload daily serving report through File Uploader", icon="ℹ️")
