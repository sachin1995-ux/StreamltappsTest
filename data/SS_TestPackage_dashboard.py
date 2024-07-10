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
        st.success(f'Welcome {st.session_state["name"]}!, you have successfully logged in. Please navigate to the dashboard page to see the results.')
    else:
        st.info('Please login to access the dashboard.')

def register_user_page():
    st.write("This is the Register New User Page")
    try:
        (email_of_registered_user, username_of_registered_user, name_of_registered_user) = authenticator.register_user(pre_authorization=False)
        if email_of_registered_user:
            st.success('User registered successfully')
    except RegisterError as e:
        st.error(e)


# Dashboard Page
def dashboard_page():
    authenticator.logout()
    if st.session_state.get("authentication_status"):
        st.title("SmartSpend Campaign Monitoring Dashboard")
        with st.sidebar:
            st.header("Configuration")
            uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is  None:
            st.info(" Upload daily serving report through File Uploader", icon="ℹ️")
            file_path = 'data/Serving_Report_7_9_2024 (2).csv'  # Replace with the correct file path
            df = pd.read_csv(file_path)
        else:
            df = pd.read_csv(uploaded_file)
    
        # Convert 'Cost' and 'Revenue' to float after removing currency symbols
        df['Cost'] = df['Cost'].replace('[$,]', '', regex=True).astype(float)
        df['Revenue'] = df['Revenue'].replace('[$,]', '', regex=True).astype(float)
    
        # Calculate margin
        df['Margin'] = (df['Revenue'] - df['Cost']) / df['Revenue']
    
    
        df = df.rename(columns={'Package ID': 'packageId', 'CTR': 'ctr', 'VCR': 'vcr'})
        df['Impressions'] = df['Impressions'].str.replace(',', '').astype(int)
        df['Clicks'] = df['Clicks'].str.replace(',', '').astype(int)
        df['Completed Views'] = df['Completed Views'].str.replace(',', '').astype(int)
    
        package_ids = [9013, 9523, 9515, 9524, 9516, 9525, 9507, 9533, 9016, 9526]
    
        # Filter the DataFrame to include only the rows with packageId in the specified list
        df = df[df['packageId'].isin(package_ids)]
    
        df['Date'] = pd.to_datetime(df['Date']).dt.date
    
    
        # Load package mapping CSV
        package_mapping = pd.read_csv("data/SmartSpendTestPackageMapping.csv")
        df = df.merge(package_mapping, left_on='packageId', right_on='TraditionalPackage', how='left').drop_duplicates()
    
        cols = ['Date', 'packageId','Impressions', 'Clicks', 'Completed Views','ctr', 'vcr']
    
        st.write("Master Dataset", df)
    
    
        # Widgets
        if st.sidebar.button('Refresh Data'):
            st.experimental_rerun()
    
        date_range = st.sidebar.date_input("Select Date Range", [])
        package_selected = st.sidebar.selectbox("Select Package ID:", df["TraditionalPackage"].unique())
    
        graph_color = st.sidebar.color_picker('Pick a color for Traditional', '#ffc63e')
        graph_color_SS = st.sidebar.color_picker('Pick a color SmartSpend', '#F15B29')
    
        impression_threshold = st.sidebar.slider('Filter Impressions by Minimum Threshold', 0, 5000, 0)

    
        # Filter data by selected date range if specified
        if date_range:
            df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]
    
        # # Find the corresponding SmartSpend package
        campaignName = df[df["TraditionalPackage"] == package_selected]['CampaignName'].iloc[0]
        smartspend_package = df[df["TraditionalPackage"] == package_selected]['SmartSpendPackage'].iloc[0]
    
    
        st.write("SmartSpend packageId for selected traditional package:", smartspend_package)
    
        st.markdown(
            f"""<div style='font-weight: bold; color: #ffc63e;'>Campaign Name: {campaignName}</div>""",
            unsafe_allow_html=True
        )
    
        st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break
        # st.markdown("<br><br><br>", unsafe_allow_html=True)  # Adds three line breaks for more space
    
        # Filter data
        filtered_traditional = df[(df["TraditionalPackage"] == package_selected) & (df["Impressions"] >= impression_threshold)]
        filtered_smartspend = df[(df["packageId"] == smartspend_package) & (df["Impressions"] >= impression_threshold)]
    
    
    
        # Display selected data
        st.write("Filtered Data - Traditional Package", filtered_traditional[cols])
        st.write("Filtered Data - SmartSpend Package", filtered_smartspend[cols])
    
    
        # Convert 'Date' to datetime if not already
        filtered_traditional['Date'] = pd.to_datetime(filtered_traditional['Date'])
        filtered_smartspend['Date'] = pd.to_datetime(filtered_smartspend['Date'])
    
    
    
        # Add a 'Method' column
        filtered_traditional['Method'] = 'Traditional'
        filtered_smartspend['Method'] = 'SmartSpend'
    
        # Concatenate dataframes
        combined_df = pd.concat([filtered_traditional, filtered_smartspend])
    
        # Create the bar chart with hover data
        fig = px.bar(combined_df, x="Date", y="Impressions",
                     color='Method', barmode='group',
                     title="Daily Impression Comparison",
                     # labels={"VCR": "Video Completion Rate (%)", "Date": "Date"},
                    # color_discrete_map={'Traditional': '#ffc63e', 'SmartSpend': '#F15B29'}, # Custom colors
                     hover_data={"Date": "|%B %d, %Y", "Impressions": True})
    
        st.plotly_chart(fig, use_container_width=True)
    
        st.write(f"The total impressions for the selected traditional package is : {filtered_traditional['Impressions'].sum()}")
    
        st.write(f"The total impressions for the selected SmartSpend package is : {filtered_smartspend['Impressions'].sum()}")
    
    
    
        # Create the bar chart with hover data
        fig = px.bar(combined_df, x="Date", y="ctr",
                     color='Method', barmode='group',
                     title="Daily CTR Comparison",
                     labels={"CTR": "Click Through Rate (%)", "Date": "Date"},
                     hover_data={"Date": "|%B %d, %Y", "ctr": True})
    
        st.plotly_chart(fig, use_container_width=True)
    
        filtered_traditional_avg_ctr = round(filtered_traditional['Clicks'].sum()/filtered_traditional['Impressions'].sum()* 100,2)
        filtered_smartspend_avg_ctr = round(filtered_smartspend['Clicks'].sum()/filtered_smartspend['Impressions'].sum()* 100,2)
    
        st.write(f"The average CTR for the selected traditional package is : {filtered_traditional_avg_ctr}%")
        st.write(f"The average CTR for the selected SmartSpend package is : {filtered_smartspend_avg_ctr}%")
    
    
    
    
        # Create the bar chart with hover data
        fig = px.bar(combined_df, x="Date", y="vcr",
                     color='Method', barmode='group',
                     title="Daily VCR Comparison",
                     labels={"VCR": "Video Completion Rate (%)", "Date": "Date"},
                     hover_data={"Date": "|%B %d, %Y", "vcr": True})
    
        st.plotly_chart(fig, use_container_width=True)
    
    
        filtered_traditional_avg_vcr = round(filtered_traditional['Completed Views'].sum()/filtered_traditional['Impressions'].sum()* 100,2)
        filtered_smartspend_avg_vcr = round(filtered_smartspend['Completed Views'].sum()/filtered_smartspend['Impressions'].sum()* 100,2)
    
        st.write(f"The average VCR for the selected traditional package is: {filtered_traditional_avg_vcr}%")
        st.write(f"The average VCR for the selected SmartSpend package is: {filtered_smartspend_avg_vcr}%")
    
    
        st.markdown("<br>", unsafe_allow_html=True)  # Adds a line break
    
    
        st.write("###### Daily beakdown using Line Chart")
    
    
        # Create a line chart with Plotly Express
        fig = px.line(combined_df, x='Date', y='Margin', color='Method', symbol="Method",
                      title="Daily Margin Comparison - Line Chart",
                      labels={"Margin": "Margin Rate (%)", "Date": "Date"},
                      markers=True,  # Adds markers to the line chart
                      color_discrete_map={'Traditional': '#ffc63e', 'SmartSpend': '#F15B29'})  # Custom colors
                      # )
    
        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    
        filtered_traditional_avg_margin = round((filtered_traditional['Revenue'].sum() - filtered_traditional['Cost'].sum()) / (filtered_traditional['Revenue'].sum()) * 100,2)
        filtered_smartspend_avg_margin = round((filtered_smartspend['Revenue'].sum() - filtered_smartspend['Cost'].sum()) / (filtered_smartspend['Revenue'].sum()) * 100,2)
    
    
        st.write(f"The average Margin for the selected traditional package is: {filtered_traditional_avg_margin}%")
        st.write(f"The average Margin for the selected SmartSpend package is: {filtered_smartspend_avg_margin}%")
    
        # Create a line chart with Plotly Express
        fig = px.line(combined_df, x='Date', y='Impressions', color='Method', symbol="Method",
                      title="Daily Impression Comparison - Line Chart",
                      labels={"Impressions": "Daily Impression", "Date": "Date"},
                      markers=True,  # Adds markers to the line chart
                      color_discrete_map={'Traditional': '#ffc63e', 'SmartSpend': '#F15B29'})  # Custom colors
                      # )
    
        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    
        # Create a line chart with Plotly Express
        fig = px.line(combined_df, x='Date', y='ctr', color='Method', symbol="Method",
                      title="Daily CTR Comparison - Line Chart",
                      labels={"ctr": "Video Completion Rate (%)", "Date": "Date"},
                      markers=True,  # Adds markers to the line chart
                      color_discrete_map={'Traditional': '#ffc63e', 'SmartSpend': '#F15B29'})  # Custom colors
                      # )
    
        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    
        # Create a line chart with Plotly Express
        fig = px.line(combined_df, x='Date', y='vcr', color='Method', symbol="Method",
                      title="Daily VCR Comparison - Line Chart",
                      labels={"vcr": "Video Completion Rate (%)", "Date": "Date"},
                      markers=True,  # Adds markers to the line chart
                      color_discrete_map={'Traditional': '#ffc63e', 'SmartSpend': '#F15B29'})  # Custom colors
                      # )
    
        # Display the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("You are not logged in. Please login to view the dashboard.")

# Page selection logic
if page == "Login Page":
    login_page()
elif page == "Register New User":
    register_user_page()
elif page == "Dashboard":
    dashboard_page()
