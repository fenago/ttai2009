import streamlit as st
from openai import OpenAI
import pandas as pd

# Set up the title of the app
st.title("Trivera Tech ChatGPT for Prompt Engineering")

# Display the image at the top of the page
st.image("https://lwfiles.mycourse.app/65a6a0bb6e5c564383a8b347-public/4ef4ee108068d6f94365c6d2360b3a66.png")

# Get OpenAI API key
openai_api_key = st.sidebar.text_input('OpenAI API Key')

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

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

# Function to create and cache the model data table
@st.cache
def create_model_data_table():
    model_data = {
        "MODEL": [
            "gpt-4-0125-preview", "gpt-4-turbo-preview", "gpt-4-1106-preview", 
            "gpt-4-vision-preview", "gpt-4-1106-vision-preview", "gpt-4", 
            "gpt-4-0613", "gpt-4-32k", "gpt-4-32k-0613",
            "gpt-3.5-turbo-0125", "gpt-3.5-turbo", "gpt-3.5-turbo-1106", 
            "gpt-3.5-turbo-instruct", "gpt-3.5-turbo-16k", "gpt-3.5-turbo-0613", 
            "gpt-3.5-turbo-16k-0613", "dall-e-3", "dall-e-2", 
            "tts-1", "tts-1-hd", "text-embedding-3-large", 
            "text-embedding-3-small", "text-embedding-ada-002", 
            "text-moderation-latest", "text-moderation-stable", "text-moderation-007"
        ],
        "DESCRIPTION": [
            "New GPT-4 Turbo model reducing 'laziness' in task completion. Max 4,096 tokens.",
            "Alias for gpt-4-0125-preview.",
            "GPT-4 Turbo with improved instruction following and JSON mode. Max 4,096 tokens.",
            "GPT-4 with image understanding. Alias for gpt-4-1106-vision-preview.",
            "GPT-4 with image understanding. Max 4,096 tokens.",
            "Alias for gpt-4-0613. Continuous upgrades.",
            "GPT-4 snapshot from June 13th 2023. Improved function calling.",
            "Alias for gpt-4-32k-0613. Focused on GPT-4 Turbo.",
            "Snapshot of gpt-4-32k from June 13th 2023.",
            "Updated GPT-3.5 Turbo model. Fixes text encoding for non-English calls. Max 4,096 tokens.",
            "Alias for gpt-3.5-turbo-0613. Will upgrade to gpt-3.5-turbo-0125.",
            "GPT-3.5 Turbo with improved instruction following. Max 4,096 tokens.",
            "Similar to GPT-3 models. For legacy Completions endpoint.",
            "Legacy model, alias for gpt-3.5-turbo-16k-0613.",
            "Legacy snapshot of gpt-3.5-turbo from June 13th 2023.",
            "Legacy snapshot of gpt-3.5-16k-turbo from June 13th 2023.",
            "Latest DALL·E model with enhanced capabilities.",
            "Previous DALL·E model with 4x resolution improvement.",
            "Latest text-to-speech model, optimized for speed.",
            "Latest text-to-speech model, optimized for quality.",
            "Most capable embedding model for English and non-English tasks. 3,072 output dimensions.",
            "Improved performance over 2nd gen ada model. 1,536 output dimensions.",
            "Most capable 2nd generation embedding model. 1,536 output dimensions.",
            "Alias for text-moderation-007.",
            "Alias for text-moderation-007.",
            "Most capable moderation model across all categories."
        ],
        "CONTEXT WINDOW": [
            "128,000 tokens", "128,000 tokens", "128,000 tokens", 
            "128,000 tokens", "128,000 tokens", "8,192 tokens", 
            "8,192 tokens", "32,768 tokens", "32,768 tokens",
            "16,385 tokens", "4,096 tokens", "16,385 tokens", 
            "4,096 tokens", "16,385 tokens", "4,096 tokens", 
            "16,385 tokens", None, None, 
            None, None, None, 
            None, None, "32,768 tokens", 
            "32,768 tokens", "32,768 tokens"
        ],
        "TRAINING DATA": [
            "Up to Dec 2023", "Up to Dec 2023", "Up to Apr 2023", 
            "Up to Apr 2023", "Up to Apr 2023", "Up to Sep 2021", 
            "Up to Sep 2021", "Up to Sep 2021", "Up to Sep 2021",
            "Up to Sep 2021", "Up to Sep 2021", "Up to Sep 2021", 
            "Up to Sep 2021", "Up to Sep 2021", "Up to Sep 2021", 
            "Up to Sep 2021", "Nov 2023", "Nov 2022", 
            "Latest", "Latest", "Latest", 
            "Latest", "Latest", "Latest", 
            "Latest", "Latest"
        ]
    }
    return pd.DataFrame(model_data)

# Display the model data table
df_models = create_model_data_table()
st.table(df_models)

# Allow users to select the model
model_options = list(df_models["MODEL"])
selected_model = st.sidebar.radio("Select the OpenAI model", model_options)

# Update the model based on user selection
st.session_state["openai_model"] = selected_model
