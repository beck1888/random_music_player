from manager import * # Interacts with the JSON songs file and validate pw
import streamlit as st  # Streamlit website
from random import choice  # Pick a random song from a list
from PIL import Image  # Load the favicon
from configs import *  # Custom page styles
import time  # Show instructions only temporarily

# Load favicon
favicon = Image.open('favicon.png')

# Name tab and show favicon
st.set_page_config(page_title="Music player", page_icon=favicon)

# Import and apply the custom styling configs
page_configs = [remove_st_ui, no_anchors, hide_settings, hide_enter_to_submit]
for custom_style in page_configs:
    st.markdown(custom_style, unsafe_allow_html=True)

# Make a songs list based on the JSON file
songs_dict = dict(get_songs())
songs = list(songs_dict.keys())

# Check if a song has already been selected, if not, pick a random one
if 'song_name' not in st.session_state:
    st.session_state.song_name = choice(songs)

# Get the URL of the title
url = songs_dict[st.session_state.song_name]

# Shows the song name on the top of the page
st.title("Now playing: '" + st.session_state.song_name + "'")

# Set the now_playing song to own var for use later
now_playing = st.session_state.song_name

# Loads the video
st.video(url)

# Create three columns for content alignment
col1, col2, col3 = st.columns([1,2,1])

# Places control buttons
with col1:
    # Refresh button
    if st.button("🔄 New song"):
        # Pick a new random song and update the session state
        st.session_state.song_name = choice(songs)
        st.rerun()

# Open in YouTube button
with col3:  # Even though in col 3, must come first to be seen
    st.link_button("📺 See on YouTube", url)

# Form for adding a song
with st.form("Add a song to the list", clear_on_submit=True):
    st.subheader("📝 Add your own music")

    user_input_title = st.text_input("Song name")
    user_input_url = st.text_input("Full YouTube URL to the song")
    user_password_guess = st.text_input("Password", type='password')
    st.text("A password is required so only authorized people may add songs.")
    if st.form_submit_button('Add song'):
        if is_correct_password(user_password_guess) is True:
            add_song(user_input_title, user_input_url)
            st.success("Song added!", icon="✅")
            st.balloons()
        else:
            st.error("Wrong password. Your song has not been added.")

# Form for removing the current song from the playlist
with st.form("Remove a song from the list", clear_on_submit=True):
    st.subheader("🗑️ Remove a song from the list")

    song_name_pop = st.selectbox("Pick a song to remove", list(get_songs()), index=None, placeholder="Click the dropdown or type here...")
    user_password_guess = st.text_input("Password", type='password')
    st.text("A password is required so only authorized people may remove songs.")
    if st.form_submit_button("Remove song"):
        if is_correct_password(user_password_guess) is True:
            remove_status = remove_song(song_name_pop)
            if remove_status == 'complete':
                st.success("Song removed!", icon="✅")
            else:
                st.error("That song isn't in this playlist")
        else:
            st.error("Wrong password. The current song has not been deleted.")

# List all the songs in the playlist
index = 1
st.title("🎧 Songs in this playlist:")
for song in get_songs():
    st.text(f"{str(index)}) {song}")
    index += 1