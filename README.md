# Scholarship Scout AI

A Streamlit app for scholarship discovery, eligibility-oriented searches, essay drafting grounded in the applicant's own writing, and application checklists.

## Features

- Search the web for scholarship leads using Tavily.
- Add filters such as location, education level, intended field, ethnicity/heritage eligibility terms, LGBTQ+ scholarships, disability-related scholarships, and lived-experience themes.
- Upload TXT, Markdown, PDF, or DOCX writing samples and notes.
- Draft essays using Google Gemini, with instructions not to invent facts or exaggerate personal experiences.
- Download generated essay drafts and track a basic application checklist.

## Important limitations

- Search results are leads, not verified scholarship listings. Confirm eligibility, award amounts, deadlines, and application instructions on the official sponsor website.
- Essay generation helps improve relevance and clarity; it cannot guarantee an award.
- This version does not automatically submit applications or bypass CAPTCHAs or website restrictions.
- Sensitive filters are optional. Search queries and essay materials are sent to the configured third-party providers when those features are used. Avoid uploading information you do not want processed externally.
- This starter version does not save a profile or database to a server. Session data may be lost when the session ends.
- Check each scholarship's policy on AI assistance and disclose it when required.

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Configure API keys

Create `.streamlit/secrets.toml` locally:

```toml
GEMINI_API_KEY = "your-openai-api-key"
TAVILY_API_KEY = "your-tavily-api-key"
```

Never commit this file or put real API keys in source code. On Streamlit Community Cloud, add keys under your app's Settings / Secrets panel.

- Google Gemini API: https://platform.openai.com/api-keys
- Tavily search API: https://app.tavily.com/

API usage may incur charges depending on provider plans and usage. The app cannot search live results or draft with GPT until the corresponding API key is configured.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, `README.md`, and `.gitignore`.
3. Open https://share.streamlit.io/ and connect GitHub.
4. Create an app using your repository, branch `main`, and main file `app.py`.
5. Add `GEMINI_API_KEY` and `TAVILY_API_KEY` under the app's Secrets settings.
6. Deploy and test with non-sensitive sample information first.

## Privacy and responsible use

Ethnicity, LGBTQ+ identity, disability, trauma, and hardship can be sensitive. These filters are optional and should only be used when they help identify legitimate eligibility criteria or relevant opportunities. Do not invent or exaggerate identity, disability, trauma, hardship, accomplishments, or outcomes. Only upload documents you have permission to share, and review extracted text and generated drafts before using them.\n\n
## Writing sample library

The Essay Studio lets you upload TXT, Markdown, PDF, or DOCX samples, save extracted text under a name, and select saved samples for later drafts. Selected samples are combined as writing-style and factual references.

This starter implementation stores extracted text in `app_data/writing_samples/` on the app filesystem and excludes that folder from Git with `.gitignore`. On Streamlit Community Cloud, local files are not guaranteed to survive app replacement, rebuilds, or infrastructure resets. For dependable multi-session storage in production, use a database or object storage service and add authentication so each user can access only their own samples. Uploaded writing can contain sensitive personal details, so avoid public repositories and do not commit `app_data/`.\n\n
## Brag sheet library

The Essay Studio also supports a reusable brag sheet, resume, or activities-and-achievements document. Upload TXT, Markdown, PDF, or DOCX, save its extracted text to your brag sheet library, and select it for later essays. Selected brag sheet content is provided to the essay model as user-supplied factual context alongside selected writing samples.

As with writing samples, local filesystem storage on Streamlit Community Cloud is not guaranteed to survive app replacement or infrastructure resets. For durable, account-specific storage, add authentication and an external database or object storage. Do not commit private brag sheets or writing samples to GitHub.\n\n
## User profile

The app includes a reusable profile form for education, location, intended major, goals, activities, leadership, community service, awards, projects, and optional scholarship context. Saved profile details are used as context for search and essay drafts.

This starter app is a single-user prototype: the profile is stored in `app_data/user_profile.json` on the local app filesystem. It is not a secure multi-user account system, and Streamlit Cloud local files may not survive resets. Before opening this app to multiple users, implement authentication and per-user database storage. Do not collect sensitive identifiers or commit `app_data/` to GitHub.


## Google Gemini setup

1. Create an API key in [Google AI Studio](https://aistudio.google.com/).
2. In Streamlit Community Cloud, open your app's Settings → Secrets.
3. Add `GEMINI_API_KEY = "your-key-here"`.
4. Save and restart the app. Never commit real API keys to GitHub.

The free Gemini API tier has rate and usage limits that can change. Check Google's current terms before public launch.


## Google AI Studio setup

1. Create an API key at [Google AI Studio](https://aistudio.google.com/).
2. In Streamlit Community Cloud, open your app's Settings → Secrets.
3. Add `GEMINI_API_KEY = "your-key-here"`.
4. Save and restart the app. Never commit real API keys to GitHub.

The Gemini free tier has usage and rate limits that can change. Check Google's current terms before public launch.
