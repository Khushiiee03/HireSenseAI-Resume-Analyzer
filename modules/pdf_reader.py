"""Document text extraction utilities for uploaded resume and job files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

import fitz


SUPPORTED_JOB_DESCRIPTION_TYPES = {"pdf", "txt"}
SUPPORTED_RESUME_TYPES = {"pdf"}


@dataclass(frozen=True)
class ExtractionResult:
    """Result returned by document extraction helpers."""

    text: str
    error: str | None = None

    @property
    def is_successful(self) -> bool:
        return self.error is None and bool(self.text.strip())


def get_file_extension(file_name: str) -> str:
    """Return a normalized file extension without the leading dot."""
    return Path(file_name).suffix.lower().lstrip(".")


def extract_text_from_pdf(pdf_file: BinaryIO) -> ExtractionResult:
    """Extract text from a PDF upload using PyMuPDF."""
    try:
        pdf_bytes = pdf_file.read()
        if not pdf_bytes:
            return ExtractionResult(text="", error="The uploaded PDF is empty.")

        with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf_document:
            page_text = [page.get_text("text") for page in pdf_document]

        extracted_text = "\n".join(page_text).strip()
        if not extracted_text:
            return ExtractionResult(
                text="",
                error="No readable text was found in this PDF. It may be scanned or image-only.",
            )

        return ExtractionResult(text=extracted_text)
    except fitz.FileDataError:
        return ExtractionResult(text="", error="The uploaded file is not a valid PDF.")
    except Exception as exc:
        return ExtractionResult(
            text="",
            error=f"Could not extract text from the PDF: {exc}",
        )


def extract_text_from_txt(txt_file: BinaryIO) -> ExtractionResult:
    """Extract text from a TXT upload."""
    try:
        txt_bytes = txt_file.read()
        if not txt_bytes:
            return ExtractionResult(text="", error="The uploaded TXT file is empty.")

        for encoding in ("utf-8", "utf-8-sig", "latin-1"):
            try:
                extracted_text = txt_bytes.decode(encoding).strip()
                break
            except UnicodeDecodeError:
                continue
        else:
            return ExtractionResult(text="", error="The TXT file encoding is not supported.")

        if not extracted_text:
            return ExtractionResult(text="", error="No readable text was found in this TXT file.")

        return ExtractionResult(text=extracted_text)
    except Exception as exc:
        return ExtractionResult(
            text="",
            error=f"Could not extract text from the TXT file: {exc}",
        )


def extract_text_from_upload(uploaded_file: BinaryIO, allowed_types: set[str]) -> ExtractionResult:
    """Extract text from an uploaded file when its type is allowed."""
    file_name = getattr(uploaded_file, "name", "")
    extension = get_file_extension(file_name)

    if extension not in allowed_types:
        supported_types = ", ".join(sorted(allowed_types)).upper()
        return ExtractionResult(
            text="",
            error=f"Unsupported file type. Please upload one of: {supported_types}.",
        )

    uploaded_file.seek(0)
    if extension == "pdf":
        return extract_text_from_pdf(uploaded_file)

    uploaded_file.seek(0)
    if extension == "txt":
        return extract_text_from_txt(uploaded_file)

    return ExtractionResult(text="", error="Unsupported file type.")


def build_text_preview(text: str, max_characters: int = 2500) -> str:
    """Return a bounded text preview for the Streamlit UI."""
    clean_text = text.strip()
    if len(clean_text) <= max_characters:
        return clean_text

    return f"{clean_text[:max_characters].rstrip()}\n\n... Preview truncated ..."
