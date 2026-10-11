# Scholarship Scout AI

A Streamlit app for scholarship discovery, eligibility-oriented searches, essay drafting grounded in the applicant's own writing, and application checklists.

## Features

- Search the web for scholarship leads using Tavily.
- Add filters such as location, education level, intended field, ethnicity/heritage eligibility terms, LGBTQ+ scholarships, disability-related scholarships, and lived-experience themes.
- Upload TXT, Markdown, PDF, or DOCX writing samples and notes.
- Draft essays using OpenAI, with instructions not to invent facts or exaggerate personal experiences.
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
OPENAI_API_KEY = "your-openai-api-key"
TAVILY_API_KEY = "your-tavily-api-key"
```

Never commit this file or put real API keys in source code. On Streamlit Community Cloud, add keys under your app's Settings / Secrets panel.

- OpenAI API: https://platform.openai.com/api-keys
- Tavily search API: https://app.tavily.com/

API usage may incur charges depending on provider plans and usage. The app cannot search live results or draft with GPT until the corresponding API key is configured.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py`, `requirements.txt`, `README.md`, and `.gitignore`.
3. Open https://share.streamlit.io/ and connect GitHub.
4. Create an app using your repository, branch `main`, and main file `app.py`.
5. Add `OPENAI_API_KEY` and `TAVILY_API_KEY` under the app's Secrets settings.
6. Deploy and test with non-sensitive sample information first.

## Privacy and responsible use

Ethnicity, LGBTQ+ identity, disability, trauma, and hardship can be sensitive. These filters are optional and should only be used when they help identify legitimate eligibility criteria or relevant opportunities. Do not invent or exaggerate identity, disability, trauma, hardship, accomplishments, or outcomes. Only upload documents you have permission to share, and review extracted text and generated drafts before using them.
