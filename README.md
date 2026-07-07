# HireSense AI

HireSense AI is an AI-powered Resume Screening and ATS Analysis web application. It helps recruiters and job seekers compare resumes against job descriptions, generate ATS insights, and provide AI-powered hiring recommendations using Google's Gemini AI.

## Phase 3 Status

This phase adds Gemini AI resume analysis:

- Resume PDF upload
- Job description PDF or TXT upload
- PyMuPDF-based PDF text extraction
- TXT text extraction with common encoding support
- Extracted resume and job description previews
- Gemini-powered ATS analysis using the `google-genai` SDK
- User-friendly handling for missing keys, invalid keys, API failures, network errors, and empty inputs

The app does not use the deprecated `google.generativeai` package.

## Analysis Output

Gemini returns clean Markdown with:

- ATS Score
- Overall Match Percentage
- Matching Skills
- Missing Skills
- Strengths
- Weaknesses
- Resume Summary
- Suggestions for Improvement
- Final Hiring Recommendation: Strong Match, Moderate Match, or Weak Match

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
|   +-- ai_analyzer.py
|   +-- pdf_reader.py
+-- output/
|   +-- .gitkeep
+-- resumes/
    +-- .gitkeep
```

## Create a Gemini API Key

1. Open Google AI Studio: https://aistudio.google.com/
2. Sign in with your Google account.
3. Open the API key section.
4. Create a new Gemini API key.
5. Keep the key private. Do not commit it to GitHub.

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
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. Run the Streamlit app.

   ```bash
   python -m streamlit run app.py
   ```

## Current Workflow

1. Upload a resume as a PDF.
2. Upload a job description as a PDF or TXT file.
3. Review the extracted text previews.
4. Click `Analyze Resume`.
5. Review the Gemini-generated ATS analysis and hiring recommendation.

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `GEMINI_API_KEY` | Yes | Gemini API key used by the `google-genai` SDK. |
| `GEMINI_MODEL` | No | Optional model override. Defaults to `gemini-2.5-flash`. |

## Roadmap

- Structured result parsing
- Plotly charts for ATS scoring and skill gaps
- Exportable reports
- Saved analysis history
