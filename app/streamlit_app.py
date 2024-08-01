import streamlit as st
import requests

st.markdown(
    """
    <style>
    /* Set the background color for the entire app */
    .reportview-container, .main, .block-container {
        background-color: rgba(185, 181, 240, 1) !important;
    }
    
    /* Customize sidebar background */
    .sidebar .sidebar-content {
        background-color: rgba(185, 181, 240, 1) !important;
    }

    .centered-image {
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .centered-image img {
        max-width: 100%;
        height: auto;
    }

    .stButton button:hover {
        background-color: #45a049; /* Darker green on hover */
    }

    /* Customize header section background */
    header, .st-emotion-cache-12fmjuu {
        background: rgba(185, 181, 240, 1) !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Define API URLs
RAG_API_URL = "http://127.0.0.1:9000/rag"
CLASSIFICATION_API_URL = "http://127.0.0.1:9000/classification"

st.title("Infiheal-Mental Health Chatbot By Shashank")
st.image("screenshots/healo.png",width=300)
# Sidebar for navigation
st.sidebar.title("Navigation")
option = st.sidebar.selectbox(
    "Choose a page:",
    ["RAG Model", "Classification Model"]
)

if option == "RAG Model":
    st.header("RAG Model Interaction")

    # Text area for user input
    prompt = st.text_area("Enter your prompt:", "What is the impact of mental health on sleep?")

    if st.button("Generate Response"):
        if prompt:
            with st.spinner("Generating response..."):
                # Send the request to the RAG API
                response = requests.post(RAG_API_URL, json={"prompt": prompt})
                if response.ok:
                    result = response.json()
                    st.write("**Response:**")
                    st.write(result.get("response", "No response generated."))
                    st.write("**Loaded Articles:**")
                    for article in result.get("articles", []):
                        st.write(f"- {article}")
                else:
                    st.write("Error:", response.text)
        else:
            st.write("Please enter a prompt to generate a response.")

elif option == "Classification Model":
    st.header("Classification Model Interaction")

    # Text area for user input
    texts = st.text_area("Enter texts to classify, separated by newline:", "I am unable to sleep for long hours\nsleep disorder")

    if st.button("Classify Texts"):
        if texts:
            # Convert multiline text input into a list
            text_list = texts.split('\n')
            with st.spinner("Classifying texts..."):
                # Send the request to the Classification API
                response = requests.post(CLASSIFICATION_API_URL, json={"texts": text_list})
                if response.ok:
                    results = response.json()
                    st.write("**Predictions:**")
                    for result in results:
                        text = result.get("text")
                        predicted_class = result.get("predicted_class")
                        class_label = result.get("class_label")
                        st.write(f"Text: {text} - Predicted Class: {predicted_class} ({class_label})")
                else:
                    st.write("Error:", response.text)
        else:
            st.write("Please enter some texts to classify.")
