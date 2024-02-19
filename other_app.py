import os
import datetime
import openai
import streamlit as st
import whisper

# Display the image at the top of the page
st.image("https://lwfiles.mycourse.app/65a6a0bb6e5c564383a8b347-public/4ef4ee108068d6f94365c6d2360b3a66.png")

# Sidebar for OpenAI API Key
openai_api_key = st.sidebar.text_input('OpenAI API Key')

def transcribe_audio(file_path, model_type="base"):
    """
    Transcribe the audio file using Whisper.

    :param file_path: Path to the audio file.
    :param model_type: Type of Whisper model to use.
    :return: Transcribed text.
    """
    model = whisper.load_model(model_type)
    result = model.transcribe(file_path)
    return result["text"]

def save_audio_file(audio_bytes, file_extension):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"
    with open(file_name, "wb") as f:
        f.write(audio_bytes)
    return file_name

def main():
    st.title("Whisper Transcription")

    audio_file = st.file_uploader("Upload Audio", type=["mp3", "mp4", "wav", "m4a"])
    model_type = st.selectbox("Choose Whisper Model", ["tiny", "base", "small", "medium", "large"], index=1)

    if audio_file:
        file_extension = audio_file.type.split('/')[1]
        audio_file_name = save_audio_file(audio_file.read(), file_extension)

        if st.button("Transcribe"):
            transcript_text = transcribe_audio(audio_file_name, model_type)
            st.header("Transcript")
            st.write(transcript_text)

            with open("transcript.txt", "w") as f:
                f.write(transcript_text)

            st.download_button("Download Transcript", transcript_text, file_name="transcript.txt")

if __name__ == "__main__":
    main()

