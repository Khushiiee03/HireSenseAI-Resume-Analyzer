"""Streamlit entry point for HireSense AI."""

from __future__ import annotations

import streamlit as st

from modules.ai_analyzer import AnalysisResult, analyze_resume
from modules.pdf_reader import (
    SUPPORTED_JOB_DESCRIPTION_TYPES,
    SUPPORTED_RESUME_TYPES,
    ExtractionResult,
    build_text_preview,
    extract_text_from_upload,
)


def configure_page() -> None:
    """Configure Streamlit page metadata."""
    st.set_page_config(
        page_title="HireSense AI",
        page_icon="HS",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_header() -> None:
    """Render the application header."""
    st.title("HireSense AI")
    st.subheader("AI Resume Analyzer")
    st.write(
        "Upload a resume and job description to generate ATS insights with Gemini AI."
    )


def render_extraction_result(title: str, result: ExtractionResult | None) -> None:
    """Render a text extraction preview or a helpful error."""
    st.markdown(f"### {title}")

    if result is None:
        st.info("Upload a file to see the extracted text preview.")
        return

    if result.error:
        st.warning(result.error)
        return

    st.text_area(
        label=f"{title} Preview",
        value=build_text_preview(result.text),
        height=280,
        disabled=True,
    )
    st.caption(f"Extracted {len(result.text):,} characters.")


def render_analysis_result(result: AnalysisResult | None) -> None:
    """Render Gemini analysis output or a user-friendly error."""
    st.markdown("### AI Resume Analysis")

    if result is None:
        st.info("Upload both files successfully, then run the analysis.")
        return

    if result.error:
        st.error(result.error)
        return

    st.markdown(result.markdown)


def render_upload_module() -> None:
    """Render resume and job description upload plus AI analysis workflow."""
    resume_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=sorted(SUPPORTED_RESUME_TYPES),
        help="Upload a text-based resume PDF.",
    )

    job_description_file = st.file_uploader(
        "Upload Job Description (PDF or TXT)",
        type=sorted(SUPPORTED_JOB_DESCRIPTION_TYPES),
        help="Upload a text-based PDF or plain text job description.",
    )

    resume_result = None
    job_description_result = None

    if resume_file is not None:
        resume_result = extract_text_from_upload(resume_file, SUPPORTED_RESUME_TYPES)

    if job_description_file is not None:
        job_description_result = extract_text_from_upload(
            job_description_file,
            SUPPORTED_JOB_DESCRIPTION_TYPES,
        )

    resume_column, job_column = st.columns(2)
    with resume_column:
        render_extraction_result("Resume Text", resume_result)

    with job_column:
        render_extraction_result("Job Description Text", job_description_result)

    can_analyze = (
        resume_result is not None
        and job_description_result is not None
        and resume_result.is_successful
        and job_description_result.is_successful
    )

    st.divider()

    if not can_analyze:
        render_analysis_result(None)
        return

    if st.button("Analyze Resume", type="primary"):
        with st.spinner("Analyzing resume against the job description..."):
            analysis_result = analyze_resume(
                resume_result.text,
                job_description_result.text,
            )
        render_analysis_result(analysis_result)
    else:
        render_analysis_result(None)


def main() -> None:
    configure_page()
    render_header()
    st.divider()
    render_upload_module()


if __name__ == "__main__":
    main()
