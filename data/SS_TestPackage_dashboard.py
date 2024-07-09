


import streamlit as st
import pandas as pd
import plotly.express as px

import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # For better date handling on x-axis
import numpy as np  # Needed for numerical operations


st.title("SmartSpend Campaign Monitoring Dashboard")


# def set_theme():
#     theme = {
#         "base": "light",
#         "primaryColor": "#f63366",
#         "backgroundColor": "#ffffff",
#         "secondaryBackgroundColor": "#e0e0e0",
#         "textColor": "#262730",
#         "font": "sans serif"
#     }
    
#     st.set_page_config(page_title="Dashboard", layout="wide", theme=theme)

# set_theme()

# package_selected = st.sidebar.selectbox("Select Package ID:", df["PackageID"].unique())
# filtered_data = df[df["PackageID"] == package_selected]
# st.write("Filtered Data", filtered_data)

with st.sidebar:
    st.header("Configuration")
    uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is None:
    st.info(" Upload a file through config", icon="ℹ️")
    st.stop()

df = pd.read_csv(uploaded_file)
# Convert 'Cost' and 'Revenue' to float after removing currency symbols
df['Cost'] = df['Cost'].replace('[¤,]', '', regex=True).astype(float)
df['Revenue'] = df['Revenue'].replace('[¤,]', '', regex=True).astype(float)

# Calculate margin
df['Margin'] = (df['Revenue'] - df['Cost']) / df['Revenue']

df = df.rename(columns={'Package ID': 'packageId', 'CTR': 'ctr', 'VCR': 'vcr'})
df['Impressions'] = df['Impressions'].str.replace(',', '').astype(int)
df['Clicks'] = df['Clicks'].str.replace(',', '').astype(int)
df['Completed Views'] = df['Completed Views'].str.replace(',', '').astype(int)


# Load your campaign data
# df = pd.read_csv("/Users/sachin/Downloads/MonitoringDashboard_SmartSpend/SS_Packages_7_4_2024.csv")
# df = pd.read_csv("/Users/sachin/Downloads/Serving_Report_7_8_2024.csv")
df['Date'] = pd.to_datetime(df['Date']).dt.date

# Load package mapping CSV
# package_mapping = pd.read_csv("/Users/sachin/Downloads/MonitoringDashboard_SmartSpend/SmartSpendTestPackageMapping.csv")
package_mapping = pd.read_csv('data/SmartSpendTestPackageMapping.csv')
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



# uploaded_file = st.file_uploader("Upload your data CSV", type=["csv"])
# if uploaded_file is not None:
#     df = pd.read_csv(uploaded_file)

# Filter data by selected date range if specified
if date_range:
    df = df[(df['Date'] >= date_range[0]) & (df['Date'] <= date_range[1])]

# # Package selector - allows selection of Traditional or SmartSpend package
# package_selected = st.selectbox("Select packageId:", df["TraditionalPackage"].unique())

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


# st.write("Campaign Name :", campaignName)


# Filter data
filtered_traditional = df[(df["TraditionalPackage"] == package_selected) & (df["Impressions"] >= impression_threshold)]
filtered_smartspend = df[(df["packageId"] == smartspend_package) & (df["Impressions"] >= impression_threshold)]



# Display selected data
st.write("Filtered Data - Traditional Package", filtered_traditional[cols])
st.write("Filtered Data - SmartSpend Package", filtered_smartspend[cols])


# Data preparation
filtered_traditional['Date'] = pd.to_datetime(filtered_traditional['Date'])
filtered_smartspend['Date'] = pd.to_datetime(filtered_smartspend['Date'])

dates = np.arange(len(filtered_traditional['Date']))  # Position index for each date
bar_width = 0.1  # Adjust this width based on your preference



# Assuming the data preparation has already been done
# Convert 'Date' to datetime if not already
filtered_traditional['Date'] = pd.to_datetime(filtered_traditional['Date'])
filtered_smartspend['Date'] = pd.to_datetime(filtered_smartspend['Date'])



# Calculate positions for bar and line graphs
dates = np.arange(len(filtered_traditional['Date']))  # Position index for each date
bar_width = 0.1  # Adjust this width based on your preference


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



# # Impressions Comparison (Line Graph)
# st.write("###### Impressions Comparison Between Traditional and SmartSpend (Line Graph)")
# fig, ax = plt.subplots(figsize=(10, 4))
# ax.plot(filtered_traditional['Date'], filtered_traditional['Impressions'], label='Traditional', color='#ffc63e', marker='o')
# ax.plot(filtered_smartspend['Date'], filtered_smartspend['Impressions'], label='SmartSpend', color='#30363f', marker='o')
# ax.set_xticks(filtered_traditional['Date'])
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
# ax.set_xticklabels([label.strftime('%Y-%m-%d') for label in filtered_traditional['Date']], rotation=45)
# ax.legend()
# ax.set_title("Line Graph - Daily Impressions")
# plt.tight_layout()
# st.pyplot(fig)

# # Impressions Comparison (Bar Graph)
# st.write("###### Impressions Comparison Between Traditional and SmartSpend (Bar Graph)")
# fig, ax = plt.subplots(figsize=(10, 4))
# ax.bar(dates - bar_width/2, filtered_traditional['Impressions'], width=bar_width, color='#ffc63e', label='Traditional')
# ax.bar(dates + bar_width/2, filtered_smartspend['Impressions'], width=bar_width, color='#30363f', label='SmartSpend')
# ax.set_xticks(dates)
# ax.set_xticklabels([label.strftime('%Y-%m-%d') for label in filtered_traditional['Date']], rotation=45)
# ax.legend()
# ax.set_title("Bar Graph - Daily Impressions")
# plt.tight_layout()
# st.pyplot(fig)



# # Clicks Comparison (Line Graph)
# st.write("###### Clicks Comparison Between Traditional and SmartSpend (Line Graph)")
# fig, ax = plt.subplots(figsize=(10, 4))
# ax.plot(filtered_traditional['Date'], filtered_traditional['Clicks'], label='Traditional', color='#ffc63e', marker='o')
# ax.plot(filtered_smartspend['Date'], filtered_smartspend['Clicks'], label='SmartSpend', color='#30363f', marker='o')
# ax.set_xticks(filtered_traditional['Date'])
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
# ax.set_xticklabels([label.strftime('%Y-%m-%d') for label in filtered_traditional['Date']], rotation=45)
# ax.legend()
# ax.set_title("Line Graph - Daily Clicks")
# plt.tight_layout()
# st.pyplot(fig)


# # Completed Views Comparison (Line Graph)
# st.write("###### Completed Views Comparison Between Traditional and SmartSpend (Line Graph)")
# fig, ax = plt.subplots(figsize=(10, 4))
# ax.plot(filtered_traditional['Date'], filtered_traditional['Completed Views'], label='Traditional', color='#ffc63e', marker='o')
# ax.plot(filtered_smartspend['Date'], filtered_smartspend['Completed Views'], label='SmartSpend', color='#30363f', marker='o')
# ax.set_xticks(filtered_traditional['Date'])
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
# ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
# ax.set_xticklabels([label.strftime('%Y-%m-%d') for label in filtered_traditional['Date']], rotation=45)
# ax.legend()
# ax.set_title("Line Graph - Daily Completed Views")
# plt.tight_layout()
# st.pyplot(fig)


# Download Button
if st.download_button('Download Data', df.to_csv(), file_name='filtered_data.csv'):
    st.success('File successfully downloaded')

