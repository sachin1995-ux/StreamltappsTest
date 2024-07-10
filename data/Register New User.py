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

st.write("Register New User")

# Creating a new user registration widget
try:
    (email_of_registered_user,
        username_of_registered_user,
        name_of_registered_user) = authenticator.register_user(pre_authorization=False)
    if email_of_registered_user:
        st.success('User registered successfully')
except RegisterError as e:
    st.error(e)

