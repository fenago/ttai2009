import streamlit as st
from openai import OpenAI
import pandas as pd

# Set up the title of the app
st.title("ChatGPT-like clone")

# Display the image at the top of the page
st.image("https://lwfiles.mycourse.app/65a6a0bb6e5c564383a8b347-public/4ef4ee108068d6f94365c6d2360b3a66.png")

# Table of models
model_data = {
    "MODEL": ["gpt-4-0125-preview", "gpt-4-turbo-preview", "gpt-4-1106-preview", "gpt-4-vision-preview", "gpt-4-1106-vision-preview", "gpt-4", "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613"],
    "DESCRIPTION": [
        "New GPT-4 Turbo The latest GPT-4 model intended to reduce cases of “laziness” where the model doesn’t complete a task. Returns a maximum of 4,096 output tokens.",
        "Currently points to gpt-4-0125-preview.",
        "GPT-4 Turbo model featuring improved instruction following, JSON mode, reproducible outputs, parallel function calling, and more. Returns a maximum of 4,096 output tokens. This is a preview model.",
        "GPT-4 with the ability to understand images, in addition to all other GPT-4 Turbo capabilities. Currently points to gpt-4-1106-vision-preview.",
        "GPT-4 with the ability to understand images, in addition to all other GPT-4 Turbo capabilities. Returns a maximum of 4,096 output tokens. This is a preview model version.",
        "Currently points to gpt-4-0613. See continuous model upgrades.",
        "Snapshot of gpt-4 from June 13th 2023 with improved function calling support.",
        "Currently points to gpt-4-32k-0613. See continuous model upgrades. This model was never rolled out widely in favor of GPT-4 Turbo.",
        "Snapshot of gpt-4-32k from June 13th 2023 with improved function calling support. This model was never rolled out widely in favor of GPT-4 Turbo."
    ],
    "CONTEXT WINDOW": ["128,000 tokens"] * 9,
    "TRAINING DATA": ["Up to Dec 2023"] * 4 + ["Up to Apr 2023"] * 2 + ["Up to Sep 2021"] * 3
}
df_models = pd.DataFrame(model_data)
st.table(df_models)

# Allow users to select the model
model_options = list(df_models["MODEL"])
selected_model = st.sidebar.radio("Select the OpenAI model", model_options)

# Get OpenAI API key
openai_api_key = st.sidebar.text_input('OpenAI API Key')

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Update the model based on user selection
st.session_state["openai_model"] = selected_model

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input for new message
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Generate the response from the model
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
