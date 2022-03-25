import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

##Tasks:
##Multiselect of top Artist and their songs
##Recoding: https://pythonwife.com/seaborn-with-streamlit/ (Frame)
# Connecting to SQL-Database
def app():
    #df = pd.read_csv("/Users/q.t./Documents/GitHub/StreamlitGithub/plylst_wdr2.csv", sep=",")
    #df = pd.read_csv("/Users/q.t./Documents/GitHub/StreamlitGithub/plylst_ndr2.csv", sep=",",index_col=0)
    # df = pd.read_csv("plylst_wdr2.csv", sep=",")

    # Data Aggregation / Editing / Data Cleaning
    # df["Datum"] = pd.to_datetime(df["Datum"], format="%Y-%m-%d %H:%M")
    df['Datum'] = df['Datum'].map(lambda x: x.rstrip('Uhr'))
    #wdr2
    df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y,%H.%M ")
    #ndr2
    #df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y, %H:%M")

    df["Interpret"] = df.Interpret.astype("category")
    df["Song"] = df.Song.astype("category")
    df["Jahr"] = df.Datum.dt.year
    df["Monat"] = df.Datum.dt.month
    df["Monat_Name"] = df.Datum.dt.strftime('%B')
    df["Tag"] = df.Datum.dt.day
    df["Stunde"] = df.Datum.dt.hour
    df["Minute"] = df.Datum.dt.minute
    df["Tag_name"] = df.Datum.dt.strftime('%a')



    st.title("Playlist Project")

    st.markdown("""
    This web-application performs simple descriptive statistics of playlist data from specific radio station.
     * **Current radio stations on observation:** WDR2
     
    Engaging following questions: 
    
    * How are the are the artist distribute? 
    * What are the most frequent artists overall, monthly, weekly 
    * What are the most frequent songs overall, monthly, weekly
    * What are the record labels of the most frequent artists respectively songs 
    * Does the dataset show seasonal trends
    * Does the dataset show patters on what time the most frequent artists (Top 10) are being played
    
    
     """)

    st.sidebar.header("User Input Features")

    #Dataframe

    #unique_df = list(df_ndr2,df_wdr2)
    #df = st.sidebar.multiselect("Data",unique_df,unique_df)



    #Sidebar - Year
    unique_year = sorted(df.Jahr.unique())
    select_year = st.sidebar.multiselect("Year",unique_year,unique_year)

    #Sidebar - Month
    df_sel_year = df[(df.Jahr.isin(select_year))]
    unique_month = sorted(df_sel_year.Monat_Name.unique())
    select_month = st.sidebar.multiselect("Month",list(reversed(unique_month)),unique_month)

    # Sidebar - Tag
    df_select = df_sel_year[(df_sel_year.Monat_Name.isin(select_month))]
    unique_day = sorted(df_select.Tag.unique())
    select_day = st.sidebar.multiselect("Day", unique_day, unique_day)

    # Actual DataFrame

    df_select = df[(df.Tag.isin(select_day))]

    # Filtering data

    # Overview

    st.subheader("Overview of Dataset")
    st.write("Data Dimension: "+str(df.shape[0]) + ' rows and 3 columns')
    st.write("First Entry: "+str(df.Datum.min()) +".")
    st.write("Last Entry: "+str(df.Datum.max())+".")
    st.write("Most played artist: "+str(df.Interpret.value_counts().reset_index()["index"][0]) +
             ". Count: " +str(df.Interpret.value_counts().reset_index()["Interpret"][0]))

    df_Song_most = df.groupby(["Song"]).Interpret.value_counts().reset_index(level="Song")
    df_Song_most.columns = ["Song", "Count"]
    df_Song_most = df_Song_most.sort_values(by="Count", ascending=False)
    st.write("Most played song: "+str(df_Song_most.Song[0])+" - "+str(df_Song_most.index[0]) +
             ". Count: "+str(df_Song_most.Count[0]))

    ##Highlights

    st.subheader("Most played Song")
    df_Song_played = df_select["Song"].value_counts().head(15)
    df_Song_played = df_Song_played.reset_index()
    df_Song_played.columns = ["Song", "Count"]
    st.table(df_Song_played)

    st.subheader("Most played Artist")
    df_Artist_played = df_select["Interpret"].value_counts().head(15)
    df_Artist_played = df_Artist_played.reset_index()
    df_Artist_played.columns = ["Artist", "Count"]
    st.table(df_Artist_played)

    st.subheader("Most played Artist and Song")
    df_Song_most["Artist"] = df_Song_most.index
    df_Song_most = df_Song_most.reindex(columns=['Artist', 'Song', 'Count'])
    df_Song_most.reset_index(drop=True, inplace=True)
    st.table(df_Song_most.head(15))

    ##Multiselect of top Artist and their songs



    # Descriptive Analysis
    st.subheader("Descriptive Analysis")
    # Distribution
    df_group_artist = df["Interpret"].value_counts().reset_index()
    df_group_artist.columns = ["Interpret", "Number of times artists are broadcast"]
    fig = plt.figure(figsize=(20, 6))
    g = sns.countplot(x="Number of times artists are broadcast", data=df_group_artist)
    label = np.sort(df_group_artist["Number of times artists are broadcast"].unique())
    g.set_xticklabels(labels=label, rotation=35,
                      ha="right")  # `ha` is just shorthand for horizontalalignment, which can also be used.
    g.set_ylabel("Sum of artists")
    st.pyplot(fig)

    st.markdown("""
    As expected the majority of the artists are being broadcast once. Further, data shows that only a few artists are 
    played more often (at least 25 times). Here, the artists Ed Sheeran (531), Ava Max (334), 
    Pink (323), Michael Patrick Kelly (296) and Adele (275) are having the most airtime. 
    
    """)


    st.subheader("Most played Artist as strip plot")
    first_0 = df_select["Interpret"].value_counts().head(1).reset_index()
    first_1 = first_0["index"][0]
    st.write("Most played Artist: "+str(first_1))
    ts_first = df_select[df_select["Interpret"] == first_1][["Datum", "Song","Stunde","Tag_name"]]
    ts_first_cnt_0 = ts_first["Stunde"].value_counts()
    ts_first_cnt_1 = ts_first_cnt_0.reset_index()

    fig = plt.figure(figsize=(12, 6))
    sns.barplot(x = "index", y = "Stunde", data = ts_first_cnt_1)
    #print(ts_first_cnt_1.columns)
    st.pyplot(fig)

    fig = plt.figure(figsize=(12, 9))
    sns.stripplot(x = "Tag_name", y = "Stunde", data = ts_first)
    st.pyplot(fig)
