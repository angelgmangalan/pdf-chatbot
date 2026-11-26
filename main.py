import hashlib
import tempfile
from pathlib import Path

import streamlit as st


st.set_page_config(page_title="PDF Chatbot")
st.title("PDF Chatbot")
st.caption("Upload a PDF and ask questions about its contents. Answers use local Ollama.")
st.session_state.setdefault("messages", [])

@st.cache_resource
def get_rag():
    import rag

    return rag


uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    file_id = hashlib.sha256(file_bytes).hexdigest()

    if st.button("Index PDF", type="primary"):
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
                temp_file.write(file_bytes)
                temp_path = temp_file.name

            with st.spinner("Reading and indexing the PDF..."):
                rag = get_rag()
                rag.load_pdf(temp_path)

            st.session_state["indexed_file_id"] = file_id
            st.session_state["indexed_file_name"] = uploaded_file.name
            st.session_state["messages"] = []
            st.success(f"Indexed {len(rag.chunks)} text chunks.")
        except Exception as exc:
            st.error(f"Could not index this PDF: {exc}")
        finally:
            if temp_path is not None:
                Path(temp_path).unlink(missing_ok=True)

indexed = (
    uploaded_file is not None
    and st.session_state.get("indexed_file_id") == file_id
)

if st.session_state.get("indexed_file_id") and not indexed:
    st.warning("Index the currently selected PDF before asking questions.")
elif st.session_state.get("indexed_file_name"):
    st.caption(f"Indexed document: {st.session_state['indexed_file_name']}")

for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Ask a question about the PDF",
    disabled=not indexed,
)

if question:
    st.session_state["messages"].append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Finding an answer..."):
            try:
                rag = get_rag()
                answer = rag.ask(question)
                st.markdown(answer)
                st.session_state["messages"].append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as exc:
                st.error(f"Could not answer the question: {exc}")
