# HireSense AI

HireSense AI is an AI-powered Resume Screening and ATS Analysis web application. It helps recruiters and job seekers compare resumes against job descriptions, generate ATS insights, and provide AI-powered hiring recommendations using Google's Gemini AI.

## Phase 2 Status

This phase adds the upload and text extraction workflow:

- Resume PDF upload
- Job description PDF or TXT upload
- PyMuPDF-based PDF text extraction
- TXT text extraction with common encoding support
- Extracted resume preview
- Extracted job description preview
- Graceful handling for empty, invalid, scanned, or unsupported files

AI analysis is intentionally not included yet.

## Tech Stack

- Backend: Python 3.13
- Frontend: Streamlit
- AI SDK: `google-genai`
- PDF Processing: PyMuPDF
- Data Processing: Pandas
- Charts: Plotly
- Environment Variables: python-dotenv

## Project Structure

```text
HireSense_Ai/
+-- app.py
+-- requirements.txt
+-- README.md
+-- .env.example
+-- .gitignore
+-- assets/
|   +-- .gitkeep
+-- modules/
|   +-- __init__.py
|   +-- pdf_reader.py
+-- output/
|   +-- .gitkeep
+-- resumes/
    +-- .gitkeep
```

## Setup

1. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies.

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Create a local `.env` file from `.env.example`.

   ```bash
   copy .env.example .env
   ```

4. Add your Gemini API key to `.env`.

   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key_here
   ```

5. Run the Streamlit app.

   ```bash
   python -m streamlit run app.py
   ```

## Current Workflow

1. Upload a resume as a PDF.
2. Upload a job description as a PDF or TXT file.
3. Review the extracted text previews.
4. Fix invalid, empty, scanned, or unsupported files before continuing to later phases.

## Environment Variables

| Variable | Description |
| --- | --- |
| `GOOGLE_API_KEY` | Google Gemini API key used by the `google-genai` SDK in later AI analysis phases. |

## Roadmap

- Gemini-powered resume and job description comparison
- ATS score generation
- Matching and missing skills analysis
- Resume summary, strengths, weaknesses, suggestions, and hiring recommendation
