import os
import datetime
import openai
import streamlit as st

# Display the image at the top of the page
st.image("https://lwfiles.mycourse.app/65a6a0bb6e5c564383a8b347-public/4ef4ee108068d6f94365c6d2360b3a66.png")

# Sidebar for OpenAI API Key
openai_api_key = st.sidebar.text_input('OpenAI API Key')

def transcribe(audio_file):
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript

def save_audio_file(audio_bytes, file_extension):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"
    with open(file_name, "wb") as f:
        f.write(audio_bytes)
    return file_name

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = transcribe(audio_file)
    return transcript["text"]

def main():
    st.title("Whisper Transcription")

    # Upload Audio tab
    audio_file = st.file_uploader("Upload Audio", type=["mp3", "mp4", "wav", "m4a"])
    if audio_file:
        file_extension = audio_file.type.split('/')[1]
        audio_file_name = save_audio_file(audio_file.read(), file_extension)

        if st.button("Transcribe"):
            transcript_text = transcribe_audio(audio_file_name)
            st.header("Transcript")
            st.write(transcript_text)

            with open("transcript.txt", "w") as f:
                f.write(transcript_text)

            st.download_button("Download Transcript", transcript_text, file_name="transcript.txt")

if __name__ == "__main__":
    main()


