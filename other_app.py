import streamlit as st
import pytube as pt
import whisper

# Display the image at the top of the page
st.image("https://lwfiles.mycourse.app/65a6a0bb6e5c564383a8b347-public/4ef4ee108068d6f94365c6d2360b3a66.png")

# Sidebar for OpenAI API Key
openai_api_key = st.sidebar.text_input('OpenAI API Key')

# Using tabs for different functionalities
tab1, tab2 = st.tabs(["Whisper", "Other Functionality"])

# Whisper tab
with tab1:
    st.header("Whisper - YouTube Video Transcription")
    
    # User input for YouTube URL
    youtube_url = st.text_input("Enter YouTube Video URL")
    
    # Dropdown for Model Size
    model_size = st.selectbox("Select Model Size", ["tiny", "base", "small", "medium", "large"])

    # Button to transcribe
    if st.button("Transcribe"):
        if youtube_url:
            try:
                # Downloading the video
                yt = pt.YouTube(youtube_url)
                stream = yt.streams.filter(only_audio=True)[0]
                stream.download(filename="audio.mp3")

                # Loading the Whisper model
                model = whisper.load_model(model_size)

                # Transcribing the audio file
                result = model.transcribe("audio.mp3")

                # Displaying the transcription
                st.text_area("Transcription", result["text"], height=250)
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Other Functionality tab
with tab2:
    st.header("Other Functionality")
    # ... Code for other functionalities ...

# ... Additional code for the app ...
