import streamlit as st
import pandas as pd
import check_duplicates as cd
import plotly.express as px
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#packages needed
#streamlit
#pandas
#plotly
#

#df = pd.read_csv("/Users/q.t./Documents/GitHub/Scrapping/wdr2-plylst (2).csv", sep=",")

# Connecting to SQL-Database

df = pd.read_csv("/Users/q.t./Documents/GitHub/StreamlitGithub/plylst_wdr2.csv", sep=",")

# Data Aggregation / Editing / Data Cleaning
# df["Datum"] = pd.to_datetime(df["Datum"], format="%Y-%m-%d %H:%M")
df['Datum'] = df['Datum'].map(lambda x: x.rstrip('Uhr'))
df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y,%H.%M ")
df["Jahr"] = df.Datum.dt.year
df["Monat"] = df.Datum.dt.month
df["Tag"] = df.Datum.dt.day
df["Stunde"] = df.Datum.dt.hour
df["Minute"] = df.Datum.dt.minute



st.title("Playlist Overview")

st.markdown("""
This web-application performs simple descriptive statistics of playlist data sets from radio station.
 * **Current radio stations on observation:** WDR2

 """)

st.sidebar.header("User Input Features")
#Sidebar - Year
unique_year = sorted(df.Jahr.unique())
select_year = st.sidebar.multiselect("Jahr",unique_year,unique_year)

#Sidebar - Month
df_sel_year = df[(df.Jahr.isin(select_year))]
unique_month = sorted(df.Monat.unique())
select_month = st.sidebar.multiselect("Monat",list(reversed(unique_month)),unique_month)

# Sidebar - Tag
df_select = df[(df.Monat.isin(select_month))]
unique_day = sorted(df_select.Tag.unique())
select_day = st.sidebar.multiselect("Tag", unique_day, unique_day)

# Filtering data

# df_select = df[(df.Monat.isin(select_month)) & (df.Tag.isin(select_day))]
df_select = df[(df.Tag.isin(select_day))]
st.write(df_select[["Datum", "Song", "Interpret"]])

st.table(df_select["Song"].value_counts().head())
st.table(df_select["Interpret"].value_counts().head())

# Descriptive Analysis

