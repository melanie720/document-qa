import streamlit as st
from openai import OpenAI, OpenAIError

# Show title and description.
st.title("📄 Mel's Document Q&A")
st.caption("Upload a text file and ask a question about it.")

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("Enter your OpenAI API Key:", type="password")

if not openai_api_key:
    st.info("Add your OpenAI API key and press Enter.", icon="🔑")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    try:
        client.models.list()

        # Let the user upload a file via `st.file_uploader`.
        uploaded_file = st.file_uploader("Document (.txt or .md)", type=("txt", "md"))

        # Ask the user for a question via `st.text_area`.
        question = st.text_area(
            "Your question",
            placeholder="Ex. What are the main points in this document?",
            disabled=not uploaded_file,
        )

        # Added a button:
        if st.button("Get answer", type="primary", disabled=not uploaded_file):
            if not question:
                st.warning("Type a question first.")
            else:
                # Process the uploaded file and question.
                document = uploaded_file.read().decode()
                messages = [
                    {
                        "role": "user",
                        "content": f"Here's a document: {document} \n\n---\n\n {question}",
                    }
                ]

                # Needed a spinner:
                with st.spinner("Reading your document...", show_time=True):
                    # Generate an answer using the OpenAI API.
                    stream = client.chat.completions.create(
                        model="gpt-5-nano",
                        messages=messages,
                        stream=True,
                    )

                    # Stream the response to the app using `st.write_stream`.
                    st.write_stream(stream)

    except OpenAIError:
        st.error("That key didn't work. Check it and try again.")