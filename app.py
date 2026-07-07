"""Streamlit entry point for HireSense AI."""

from __future__ import annotations

import streamlit as st


def configure_page() -> None:
    """Configure Streamlit page metadata."""
    st.set_page_config(
        page_title="HireSense AI",
        page_icon="HS",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def render_home() -> None:
    """Render the Phase 1 landing screen."""
    st.title("HireSense AI")
    st.subheader("AI Resume Analyzer")
    st.write(
        "Upload and analyze resumes against job descriptions with AI-powered ATS insights."
    )


def main() -> None:
    configure_page()
    render_home()


if __name__ == "__main__":
    main()
