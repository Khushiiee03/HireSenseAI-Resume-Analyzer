# HireSense AI

HireSense AI is an AI-powered Resume Screening and ATS Analysis web application. It will help recruiters and job seekers compare resumes against job descriptions, generate ATS insights, and provide AI-powered hiring recommendations using Google's Gemini AI.

## Phase 1 Status

This phase creates the project foundation:

- Streamlit application entry point
- Production-oriented folder structure
- Dependency manifest
- Environment variable example
- Git-ready project files

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
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── assets/
├── modules/
├── output/
└── resumes/
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

## Environment Variables

| Variable | Description |
| --- | --- |
| `GOOGLE_API_KEY` | Google Gemini API key used by the `google-genai` SDK. |

## Roadmap

- Resume PDF upload
- Job description PDF/TXT upload
- Text extraction
- Gemini-powered resume and job description comparison
- ATS score generation
- Matching and missing skills analysis
- Resume summary, strengths, weaknesses, suggestions, and hiring recommendation
