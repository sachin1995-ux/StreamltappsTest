import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import streamlit_authenticator as stauth
import hashlib

import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities.exceptions import (CredentialsError,
                                                          ForgotError,
                                                          LoginError,
                                                          RegisterError,
                                                          ResetError,
                                                          UpdateError) 

# Loading config file
with open('/Users/sachin/Downloads/config.yaml', 'r', encoding='utf-8') as file:
    config = yaml.load(file, Loader=SafeLoader)

    # Creating the authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

st.write("Update User Details")

# # Creating a forgot password widget
try:
    (username_of_forgotten_password,
        email_of_forgotten_password,
        new_random_password) = authenticator.forgot_password()
    if username_of_forgotten_password:
        st.success('New password sent securely')
        # Random password to be transferred to the user securely
    elif not username_of_forgotten_password:
        st.error('Username not found')
except ForgotError as e:
    st.error(e)


# # Creating an update user details widget
if st.session_state["authentication_status"]:
    try:
        if authenticator.update_user_details(st.session_state["username"]):
            st.success('Entries updated successfully')
    except UpdateError as e:
        st.error(e)

# Saving config file
with open('/Users/sachin/Downloads/config.yaml', 'w', encoding='utf-8') as file:
    yaml.dump(config, file, default_flow_style=False)


