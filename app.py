import streamlit as st
import os
from rag import load_and_chunk, build_vectorstore, load_vectorstore, retrieve_context, ask_groq

# Page Config
st.set_page_config(
    page_title="AskMyNotes",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AskMyNotes")
st.caption("Upload a document and ask questions about it.")


# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] 

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "file_processed" not in st.session_state:
    st.session_state.file_processed = False 


# Sidebar - file upload
with st.sidebar:
    st.header("📁 Upload Your Document")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "md", "docx", "csv", "html", "jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        temp_path = f"./temp_{uploaded_file.name}"

        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        if not st.session_state.file_processed:
            with st.spinner("Processing your document..."):
                try:
                    chunks = load_and_chunk(temp_path)
                    st.session_state.vectorstore = build_vectorstore(chunks)
                    st.session_state.file_processed = True
                    st.session_state.chat_history = [] 
                    st.success(f"Ready! Ask me anything about **{uploaded_file.name}**")
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

    if st.session_state.file_processed:
        if st.button("Upload New Document"):
            st.session_state.file_processed = False
            st.session_state.vectorstore = None
            st.session_state.chat_history = []
            st.rerun()

    st.divider()
    st.markdown("**Supported formats:**")
    st.markdown("PDF, TXT, MD, DOCX, CSV, HTML, JPG, PNG")

# Chat interface

if not st.session_state.file_processed:
    st.info("👈 Upload a document in the sidebar to get started.")

else:
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_question = st.chat_input("Ask a question about your document...")

    if user_question:
        with st.chat_message("user"):
            st.markdown(user_question)

        st.session_state.chat_history.append({
            "role": "user",
            "content": user_question
        })

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    context = retrieve_context(st.session_state.vectorstore, user_question)
                    answer = ask_groq(user_question, context)
                    st.markdown(answer)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })
                except Exception as e:
                    st.error(f"Error getting answer: {str(e)}")