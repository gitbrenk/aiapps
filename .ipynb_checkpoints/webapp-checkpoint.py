# Run with "python -m streamlit run webapp.py"
import streamlit as st
from dotenv import load_dotenv
import anthropic
from pypdf import PdfReader

load_dotenv()
client = anthropic.Anthropic()

st.title("Chat with your document")

uploaded = st.file_uploader("Upload a PDF or text file", type=["pdf", "txt", "md"])
if not uploaded:
    st.info("Upload a file to start.")
    st.stop()

# Read the file once, and start a fresh chat when a new file is uploaded
if st.session_state.get("doc_name") != uploaded.name:
    if uploaded.name.lower().endswith(".pdf"):
        text = "\n".join(page.extract_text() or "" for page in PdfReader(uploaded).pages)
    else:
        text = uploaded.read().decode("utf-8", errors="ignore")
    st.session_state.doc_name = uploaded.name
    st.session_state.doc_text = text
    st.session_state.history = []

system = (
    "Answer questions using the document below. If the answer isn't in it, say so.\n\n"
    f"<document>\n{st.session_state.doc_text}\n</document>"
)

# Show the conversation so far
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        c = msg["content"]
        st.markdown(c if isinstance(c, str) else "".join(b.text for b in c if b.type == "text"))

if question := st.chat_input("Ask about the document"):
    st.session_state.history.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with client.messages.stream(
            model="claude-opus-5-5",
            max_tokens=4096,
            system=system,
            messages=st.session_state.history,
        ) as stream:
            st.write_stream(stream.text_stream)
            reply = stream.get_final_message()
    st.session_state.history.append({"role": "assistant", "content": reply.content})