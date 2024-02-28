import streamlit as st
from openai import OpenAI
import pandas as pd

# Set up the title of the app
st.title("Miami Dade College ChatGPT")

# Display the image at the top of the page
# st.image("https://lwfiles.mycourse.app/65a6a0bb6e5c564383a8b347-public/81791ed30dbcd226feec79d58591be68.png")
st.image("https://reddotmiami.com/wp-content/uploads/bfi_thumb/rdm17-sponsors-feature_miami-dade-college-ni0a0heylglji1208ljp6e0q3d88qq8jbo2h48yk4w.gif")
# Link to Trivera Tech website
st.markdown("For more information, visit [Trivera Tech](https://www.triveratech.com).")
# Get OpenAI API key
openai_api_key = st.sidebar.text_input('OpenAI API Key')

# Check if the OpenAI API key is valid
if not openai_api_key.startswith('sk-'):
    st.warning('Please enter your OpenAI API key!', icon='⚠️')
else:
    # Initialize the OpenAI client with the valid API key
    client = OpenAI(api_key=openai_api_key)

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Allow users to set parameters for the model
with st.sidebar:
    st.write("Set Model Parameters")
    temperature = st.slider("Temperature", 0.0, 2.0, 1.0)
    max_tokens = st.slider("Max Tokens", 1, 500, 256)
    top_p = st.slider("Top P", 0.0, 1.0, 1.0)
    frequency_penalty = st.slider("Frequency Penalty", 0.0, 2.0, 0.0)
    presence_penalty = st.slider("Presence Penalty", 0.0, 2.0, 0.0)

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
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
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

# Code to display the model data table within an expander
with st.expander("Model Information"):
    df_models = create_model_data_table()
    st.table(df_models)
# ... your existing imports and setup code ...

# Data policy and model endpoint compatibility expander
with st.expander("OpenAI API Data Usage Policy"):
    st.markdown("""
    **How we use your data**
    Your data is your data.

    As of March 1, 2023, data sent to the OpenAI API will not be used to train or improve OpenAI models (unless you explicitly opt in). One advantage to opting in is that the models may get better at your use case over time.

    To help identify abuse, API data may be retained for up to 30 days, after which it will be deleted (unless otherwise required by law). For trusted customers with sensitive applications, zero data retention may be available. With zero data retention, request and response bodies are not persisted to any logging mechanism and exist only in memory in order to serve the request.

    Note that this data policy does not apply to OpenAI's non-API consumer services like ChatGPT or DALL·E Labs.

    **Default usage policies by endpoint**

    | ENDPOINT | DATA USED FOR TRAINING | DEFAULT RETENTION | ELIGIBLE FOR ZERO RETENTION |
    | --- | --- | --- | --- |
    | /v1/chat/completions | No | 30 days | Yes, except image inputs |
    | /v1/files | No | Until deleted by customer | No |
    | ... | ... | ... | ... |
    | /v1/completions | No | 30 days | Yes |
    * Image inputs via the gpt-4-vision-preview model are not eligible for zero retention.

    * For the Assistants API, we are still evaluating the default retention period during the Beta. We expect that the default retention period will be stable after the end of the Beta.

    **Model endpoint compatibility**

    | ENDPOINT | LATEST MODELS |
    | --- | --- |
    | /v1/assistants | All models except gpt-3.5-turbo-0301 supported. |
    | ... | ... |
    This list excludes all of our deprecated models.

    For details, see our API data usage policies. To learn more about zero retention, get in touch with our sales team.
    """, unsafe_allow_html=True)

# Allow users to select the model
model_options = list(df_models["MODEL"])
# Find the index of 'gpt-3.5-turbo' in the model options list
default_index = model_options.index('gpt-3.5-turbo') if 'gpt-3.5-turbo' in model_options else 0
selected_model = st.sidebar.radio("Select the OpenAI model", model_options, index=default_index)


# Allow users to select the model
# model_options = list(df_models["MODEL"])
# selected_model = st.sidebar.radio("Select the OpenAI model", model_options)

# Update the model based on user selection
st.session_state["openai_model"] = selected_model
