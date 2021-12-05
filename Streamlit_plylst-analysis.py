import streamlit as st
import pandas as pd


# Connecting to SQL-Database

df = pd.read_csv("plylst_wdr2.csv", sep=",")

# Data Aggregation / Editing / Data Cleaning
# df["Datum"] = pd.to_datetime(df["Datum"], format="%Y-%m-%d %H:%M")
df['Datum'] = df['Datum'].map(lambda x: x.rstrip('Uhr'))
df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y,%H.%M ")
df["Interpret"] = df.Interpret.astype("category")
df["Song"] = df.Song.astype("category")
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
#Showing Data
# df_select = df[(df.Monat.isin(select_month)) & (df.Tag.isin(select_day))]

df_select = df[(df.Tag.isin(select_day))]
st.header("Overall table of selected playlist")
st.write("Data Dimension: "+str(df_select.shape[0]) + ' rows and 3 columns')
st.write(df_select[["Datum", "Song", "Interpret"]])

st.header("Most played Song")
st.table(df_select["Song"].value_counts().head())
st.header("Most played Artist")
st.table(df_select["Interpret"].value_counts().head())
st.header("Most played Artist and Song")
df_group = df_select.groupby(["Interpret"]).Song.value_counts().sort_index(ascending=False).sort_values(ascending=False)
st.table(df_group.head(30))

# Descriptive Analysis

