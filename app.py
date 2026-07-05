import streamlit as st
from modules.pdf_reader import extract_text_from_pdf

st.set_page_config(
    page_title="HireSense AI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 HireSense AI")

st.write("Welcome to the AI-Powered Resume Screening System!")

st.header("Upload Resume")

uploaded_resume = st.file_uploader(
    "Choose a Resume (PDF)",
    type=["pdf"]
)

st.header("Upload Job Description")

uploaded_job = st.file_uploader(
    "Choose a Job Description (PDF or TXT)",
    type=["pdf", "txt"]
)

if st.button("Analyze Resume"):

    if uploaded_resume is not None:

        resume_text = extract_text_from_pdf(uploaded_resume)

        st.subheader("Extracted Resume Text")

        st.write(resume_text)

    else:

        st.warning("Please upload a resume first.")