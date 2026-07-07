"""Gemini-powered resume analysis for HireSense AI."""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import errors, types


DEFAULT_MODEL = "gemini-2.5-flash"


@dataclass(frozen=True)
class AnalysisResult:
    """Result returned by the AI resume analyzer."""

    markdown: str = ""
    error: str | None = None

    @property
    def is_successful(self) -> bool:
        return self.error is None and bool(self.markdown.strip())


def _get_api_key() -> str | None:
    """Load the Gemini API key from the local environment."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    return api_key or None


def _build_prompt(resume_text: str, job_description: str) -> str:
    """Create the analysis prompt sent to Gemini."""
    return f"""
You are HireSense AI, an expert resume screening and ATS analysis assistant.

Analyze the resume against the job description. Return only clean Markdown.
Do not include JSON, code fences, or extra preamble.

Use this exact structure:

# HireSense AI Resume Analysis

## ATS Score
- Score: [0-100]/100
- Rationale: [brief reason]

## Overall Match Percentage
- Match: [0-100]%

## Matching Skills
- [skill]

## Missing Skills
- [skill]

## Strengths
- [strength]

## Weaknesses
- [weakness]

## Resume Summary
[concise professional summary]

## Suggestions for Improvement
- [actionable suggestion]

## Final Hiring Recommendation
**[Strong Match / Moderate Match / Weak Match]**

Recommendation rationale: [brief reason]

Scoring guidance:
- Strong Match: 80-100
- Moderate Match: 55-79
- Weak Match: 0-54

Resume:
{resume_text}

Job Description:
{job_description}
""".strip()


def analyze_resume(resume_text: str, job_description: str) -> AnalysisResult:
    """Analyze resume text against a job description using Google Gemini."""
    clean_resume = resume_text.strip()
    clean_job_description = job_description.strip()

    if not clean_resume:
        return AnalysisResult(error="Resume text is empty. Upload a readable resume PDF.")

    if not clean_job_description:
        return AnalysisResult(
            error="Job description text is empty. Upload a readable PDF or TXT job description."
        )

    api_key = _get_api_key()
    if api_key is None:
        return AnalysisResult(
            error=(
                "Gemini API key is missing. Add GEMINI_API_KEY to your .env file "
                "and restart the Streamlit app."
            )
        )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
            contents=_build_prompt(clean_resume, clean_job_description),
            config=types.GenerateContentConfig(
                temperature=0.2,
                top_p=0.9,
                max_output_tokens=4096,
            ),
        )

        analysis_markdown = (response.text or "").strip()
        if not analysis_markdown:
            return AnalysisResult(
                error="Gemini returned an empty analysis. Please try again."
            )

        return AnalysisResult(markdown=analysis_markdown)
    except errors.ClientError as exc:
        status_code = getattr(exc, "code", None) or getattr(exc, "status_code", None)
        if status_code in {400, 401, 403}:
            return AnalysisResult(
                error=(
                    "Gemini rejected the request. Check that GEMINI_API_KEY is valid "
                    "and has access to the Gemini API."
                )
            )

        return AnalysisResult(error=f"Gemini request failed: {exc}")
    except errors.ServerError:
        return AnalysisResult(
            error="Gemini is temporarily unavailable. Please try again in a moment."
        )
    except errors.APIError as exc:
        return AnalysisResult(error=f"Gemini API request failed: {exc}")
    except (httpx.HTTPError, requests.RequestException):
        return AnalysisResult(
            error="Network error while contacting Gemini. Check your internet connection."
        )
    except Exception as exc:
        return AnalysisResult(error=f"Unexpected analysis error: {exc}")
