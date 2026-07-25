# AI Germany Job Hunter

A resume analysis tool that scores your resume against multiple job descriptions, flags missing skills, and generates a tailored cover letter for each application. Built around German-market job hunting, but the core logic isn't tied to any one country.

## What it does

Upload a resume and a batch of job description files, and the app runs two passes:

1. **Local skill matching**: a quick TF-IDF/keyword pass that scores every job against your resume before any AI call happens, so you can filter out weak matches for free.
2. **AI analysis**: for the jobs you select, an LLM (via Groq's Llama 3.3) scores match quality, ATS compatibility, and interview probability, then returns resume improvements, a learning plan, and a fully written cover letter.

Everything gets saved as JSON per job, plus a ranked CSV summary.

## Project structure

```
.
├── app.py                          # Streamlit UI
├── main.py                         # CLI entry point (batch mode, no UI)
├── requirements.txt
├── .env
├── .gitignore
├── features/
│   ├── cover_letter_generator.py   # Renders/downloads the generated cover letter (Streamlit)
│   ├── cover_letter.py             # Rewrites/humanizes a cover letter into a target style
│   └── resume_optimizer.py         # Produces an optimized resume summary/experience/skills as JSON
├── models/
│   ├── analyzer.py                 # Builds the analysis prompt, calls a provider
│   ├── job_loader.py               # Loads job description .txt files
│   ├── job_ranker.py               # TF-IDF/cosine similarity ranking of jobs against a resume
│   ├── job_reader.py               # Reads/parses individual job description files
│   ├── resume_reader.py            # Extracts text from a resume PDF
│   └── skill_matcher.py            # Local (non-AI) resume-to-job matching
├── prompts/
│   └── recruiter_prompt.txt        # The recruiter-persona prompt sent to the LLM
├── providers/
│   └── groq_provider.py            # Groq (Llama 3.3 70B) client wrapper
├── services/
│   └── analysis_service.py         # Orchestrates the full pipeline end to end
└── utils/
    ├── csv_writer.py               # Saves ranked results as CSV
    └── report_writer.py            # Saves results as JSON
```

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=your_key_here
```

## Usage

### Web UI

```bash
streamlit run app.py
```

1. Upload your resume (PDF) and one or more job description files (`.txt`).
2. Click **Analyze Jobs** to run the local skill match.
3. Review the skill match table and select which jobs to send for AI analysis. Jobs scoring 50%+ locally are pre-selected.
4. Click **Analyze Selected Jobs** to get match/ATS/interview scores, strengths, resume improvements, a learning plan, ATS tips, and a generated cover letter for each one.
5. Download any cover letter directly from its expander.

### CLI / batch mode

```bash
python main.py
```

Reads `data/resume.pdf` and every file in `data/jobs/`, analyzes all of them against `prompts/recruiter_prompt.txt`, and prints a ranked summary to the terminal. Full results land in `data/reports/`.

## Output

For each job, `data/reports/<company>.json` contains:

| Field | Description |
|---|---|
| `match_score` | 0-100, overall fit |
| `ats_score` | 0-100, ATS compatibility |
| `interview_probability` | 0-100 |
| `strengths` | What already matches the role |
| `missing_skills` | Gaps relative to the job description |
| `resume_improvements` | Specific edits to make |
| `learning_plan` | Skills worth picking up |
| `professional_summary` | Rewritten summary line |
| `improved_experience` | Rewritten experience bullets |
| `keywords` | Keywords to include for ATS |
| `ats_tips` | ATS-specific formatting/content tips |
| `cover_letter` | Full personalized cover letter (400-500 words) |

`data/reports/job_ranking.json` and `job_ranking.csv` hold all results sorted by `match_score`, highest first.

## Notes on the cover letter prompt

The recruiter prompt enforces a few hard constraints worth knowing about if you're editing it:

- No placeholders like `[Company Name]` or `[Your Name]`. The actual company name is used, pulled from the job description.
- No invented experience, skills, or achievements beyond what's in the resume.
- No em dashes, emojis, bullet points, or markdown in the letter itself.
- A blocklist of common AI-sounding phrases ("I am thrilled," "leverage my skills," "fast-paced environment," and similar) to keep the tone from reading as generated.

## Roadmap / ideas

- Support additional resume formats beyond PDF.
- Add a second AI provider as a fallback if Groq rate-limits.
- Persist analysis history across sessions instead of re-running per upload.

## Author

- LinkedIn: https://www.linkedin.com/in/maanapriyanshurajput/
- Portfolio: https://maanajipriyanshu.github.io/insights-by-priyanshu/
- GitHub: https://github.com/maanajipriyanshu
- Instagram: https://instagram.com/maanapriyanshurajput