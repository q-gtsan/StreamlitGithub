import streamlit as st

# Custom imports
from multipage import MultiPage
import firstPage, playlistPage_streamlit

# Create an instance of the app
app = MultiPage()

# Title of the main page
st.title("Data Portfolio")
# Add all your applications (pages) here
app.add_page("Main", firstPage.app)
app.add_page("Playlist_Project", playlistPage_streamlit.app)

# The main app
app.run()
