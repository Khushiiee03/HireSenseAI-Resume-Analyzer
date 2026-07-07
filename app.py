"""Streamlit entry point for HireSense AI."""

from __future__ import annotations

import streamlit as st

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
        "Upload a resume and job description to preview extracted text before AI analysis."
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


def render_upload_module() -> None:
    """Render Phase 2 resume and job description upload workflow."""
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


def main() -> None:
    configure_page()
    render_header()
    st.divider()
    render_upload_module()


if __name__ == "__main__":
    main()
