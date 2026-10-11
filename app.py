import os
from io import BytesIO
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Scholarship Scout | Find Your Future", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

def secret(name):
    try:
        return st.secrets.get(name, os.getenv(name, ""))
    except Exception:
        return os.getenv(name, "")


DESCRIPTION_CHAR_LIMIT = 320

def limited_description(value, limit=DESCRIPTION_CHAR_LIMIT):
    """Keep scholarship previews compact so they stay inside their cards."""
    text = " ".join(str(value or "No preview available.").split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:-") + "…"

# Editorial, layered teal-and-ivory visual system inspired by the supplied references.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

/* Streamlit's selected app theme is exposed through CSS variables. Use them
   for surfaces and text, while keeping the Scholarship Scout teal identity. */
:root {
  --sc-teal:#075b53;
  --sc-teal-hover:#0b7167;
  --sc-light-paper:#eef1e9;
  --sc-light-card:#f8f8f1;
  --sc-light-sidebar:#dce7df;
  --sc-light-ink:#123f3a;
  --sc-light-muted:#506c66;
  --sc-dark-paper:#171c1c;
  --sc-dark-card:#222a29;
  --sc-dark-sidebar:#1d2524;
  --sc-dark-ink:#e7eee9;
  --sc-dark-muted:#b4c4bd;
  --sc-line-light:rgba(5,70,64,.24);
  --sc-line-dark:rgba(190,220,207,.22);
}
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
.stApp { background:var(--background-color); color:var(--text-color); }
[data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
  background:var(--background-color); color:var(--text-color);
}
[data-testid="stHeader"] { background:transparent; }
.block-container { max-width:1240px; padding-top:1.5rem; padding-bottom:4rem; }
h1,h2,h3,h4 { font-family:'Manrope',sans-serif !important; color:var(--text-color) !important; letter-spacing:-.035em; }
p, label, .stMarkdown, [data-testid="stMarkdownContainer"], [data-testid="stWidgetLabel"] { color:var(--text-color); }
[data-testid="stCaptionContainer"], .small-note { color:var(--secondary-text-color) !important; }

div[data-testid="stSidebar"] {
  background:var(--secondary-background-color);
  border-right:1px solid var(--sc-line-light);
}
div[data-testid="stSidebar"] h2, div[data-testid="stSidebar"] label,
div[data-testid="stSidebar"] p, div[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
  color:var(--text-color);
}

div[data-testid="stTextInput"] input, div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] div[data-baseweb="select"], div[data-testid="stNumberInput"] input {
  border-radius:14px !important;
  background:var(--secondary-background-color) !important;
  border-color:var(--sc-line-light) !important;
  color:var(--text-color) !important;
}
div[data-testid="stTextInput"] input::placeholder, div[data-testid="stTextArea"] textarea::placeholder {
  color:var(--secondary-text-color) !important; opacity:1 !important;
}
[data-baseweb="select"] *, [data-baseweb="popover"] * { color:var(--text-color); }

.stButton > button, .stDownloadButton > button, .stLinkButton > a {
  border-radius:999px !important; border:1px solid var(--sc-teal) !important;
  background:var(--sc-teal) !important; color:#f4f4eb !important;
  font-weight:700 !important; padding:.65rem 1.2rem !important;
  transition:transform .15s ease, background .15s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover, .stLinkButton > a:hover {
  background:var(--sc-teal-hover) !important; transform:translateY(-1px);
}
button[kind="secondary"] { background:transparent !important; color:var(--text-color) !important; }

[data-testid="stTabs"] [data-baseweb="tab-list"] {
  gap:.5rem; background:var(--secondary-background-color); padding:.45rem; border-radius:999px;
}
[data-testid="stTabs"] button[role="tab"] {
  border-radius:999px; color:var(--text-color) !important; padding:.65rem 1.1rem;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  background:var(--sc-teal) !important; color:#f4f4eb !important;
}
[data-testid="stVerticalBlockBorderWrapper"] {
  background:var(--secondary-background-color); color:var(--text-color);
  border:1px solid var(--sc-line-light); border-radius:24px;
  box-shadow:0 10px 28px rgba(0,54,49,.06);
}
[data-testid="stVerticalBlockBorderWrapper"] p,
[data-testid="stVerticalBlockBorderWrapper"] h1,
[data-testid="stVerticalBlockBorderWrapper"] h2,
[data-testid="stVerticalBlockBorderWrapper"] h3,
[data-testid="stVerticalBlockBorderWrapper"] label { color:var(--text-color); }
[data-testid="stAlert"] { border-radius:18px; }
div[data-testid="stMetric"] {
  background:var(--secondary-background-color); color:var(--text-color);
  padding:1rem; border-radius:18px; border:1px solid var(--sc-line-light);
}
.hero {
  position:relative; overflow:hidden; padding:clamp(1.5rem,4vw,3.5rem);
  border-radius:34px; color:#f2f2e8;
  background:radial-gradient(circle at 85% 12%,rgba(121,190,166,.25),transparent 28%),
             linear-gradient(135deg,#003d39 0%,#075e56 60%,#0b7167 100%);
  box-shadow:0 20px 45px rgba(0,53,49,.18); margin-bottom:1.3rem;
}
.hero:after {
  content:"✦"; position:absolute; right:5%; bottom:-65px; font-size:240px;
  line-height:1; color:rgba(224,239,226,.08); transform:rotate(-12deg); pointer-events:none;
}
.eyebrow { font-size:.76rem; font-weight:800; letter-spacing:.22em; text-transform:uppercase; color:#a9d6c5; margin-bottom:1rem; }
.hero h1 { color:#f2f2e8 !important; max-width:850px; }
.hero p { color:#d0e3d8 !important; max-width:650px; font-size:1.05rem; line-height:1.65; }
.hero-pill { display:inline-block; border:1px solid rgba(229,241,230,.5); border-radius:999px; padding:.4rem .85rem; margin:.25rem .25rem 0 0; color:#edf2e8; font-size:.8rem; }
.section-kicker { color:var(--sc-teal-hover); font-size:.75rem; font-weight:800; letter-spacing:.18em; text-transform:uppercase; }
.panel-title { font-size:1.35rem; font-weight:800; letter-spacing:-.04em; }
.result-url { font-size:.82rem; color:var(--sc-teal-hover); overflow-wrap:anywhere; word-break:break-word; max-width:100%; }
[data-testid="stVerticalBlockBorderWrapper"] { min-width:0; }
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"],
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] p {
  max-width:100%; overflow-wrap:anywhere; word-break:break-word;
}
.small-note { font-size:.85rem; }
hr { border-color:var(--sc-line-light); }
footer { visibility:hidden; }

/* Dark theme overrides preserve readable contrast for surfaces and decorative labels. */
@media (prefers-color-scheme: dark) {
  div[data-testid="stSidebar"] { border-right-color:var(--sc-line-dark); }
  [data-testid="stVerticalBlockBorderWrapper"], div[data-testid="stMetric"] { border-color:var(--sc-line-dark); }
  .section-kicker, .result-url { color:#8fd5c1 !important; }
  hr { border-color:var(--sc-line-dark) !important; }
}
@media (max-width:700px) {
  .block-container { padding-left:1rem; padding-right:1rem; }
  .hero { border-radius:24px; }
  h1 { font-size:2.7rem !important; }
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ✦ Scholarship Scout")
    st.caption("FIND YOUR FUTURE")
    st.markdown("---")
    st.markdown("### Your search")
    location = st.text_input("Location", placeholder="New Jersey, United States")
    education = st.selectbox("Education level", ["High school senior", "High school student", "Undergraduate", "Graduate", "Trade / vocational", "Other"])
    field = st.text_input("Major or career", placeholder="Biomedical engineering")
    graduation_year = st.text_input("Graduation year", placeholder="2027")
    min_award = st.number_input("Minimum award ($)", min_value=0, value=0, step=500)
    max_award = st.number_input("Maximum award ($, 0 = any)", min_value=0, value=0, step=1000)
    st.markdown("---")
    st.markdown("### Optional eligibility themes")
    st.caption("Use only details you're comfortable sharing.")
    ethnicity = st.text_input("Ethnicity / heritage", placeholder="Only if relevant")
    lgbtq = st.selectbox("LGBTQ+ scholarships", ["No preference", "Include relevant scholarships", "Prioritize relevant scholarships"])
    disability = st.selectbox("Disability / neurodiversity", ["No preference", "Include relevant scholarships", "Prioritize relevant scholarships"])
    adversity = st.multiselect("Experiences and interests", [
        "Adversity / overcoming obstacles", "Family or financial hardship", "Trauma or recovery",
        "Disability or chronic barriers", "LGBTQ+ experiences", "First-generation student",
        "Community service", "Leadership", "Academic persistence", "Women in STEM"
    ])
    struggles = st.text_area("Other keywords", placeholder="Optional search terms, no need to share details.")
    count = st.slider("Results to find", 5, 20, 10)
    st.markdown("---")
    st.caption("✦ Your story belongs to you. Review every answer before using it.")

st.markdown("""
<div class="hero">
  <div class="eyebrow">Scholarship discovery · Personal essay studio</div>
  <h1>Your story.<br> Your next opportunity.</h1>
  <p>Find scholarships that fit your goals and experiences. Turn your own notes and writing into thoughtful, personal application drafts without losing your voice.</p>
  <span class="hero-pill">✦ Personalized search</span>
  <span class="hero-pill">✦ Your voice, not a template</span>
  <span class="hero-pill">✦ One organized workspace</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-kicker">YOUR WORKSPACE</div>', unsafe_allow_html=True)
tab_search, tab_essay, tab_tracker, tab_resources, tab_feedback = st.tabs(["✦ Discover", "✎ Essay studio", "▤ My checklist", "↗ Resources", "⚑ Report a bug"])

def search_web(query, limit=10):
    key = secret("TAVILY_API_KEY")
    if not key:
        return None, "Add TAVILY_API_KEY in Streamlit Secrets to enable live internet search."
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=key)
        response = client.search(query=query, search_depth="advanced", max_results=limit, include_answer=False)
        return response.get("results", []), None
    except Exception as e:
        return None, f"Search failed: {e}"

def make_search_query():
    parts = [
        "scholarships official application",
        location, education, field, graduation_year, ethnicity,
        "LGBTQ scholarship" if lgbtq != "No preference" else "",
        "disability neurodiversity scholarship" if disability != "No preference" else "",
        " ".join(adversity), struggles,
        f"scholarship award ${min_award} or more" if min_award else "",
        f"scholarship maximum ${max_award}" if max_award else "",
    ]
    return " ".join(p.strip() for p in parts if p and p.strip())

def extract_document(uploaded):
    if uploaded is None:
        return ""
    suffix = Path(uploaded.name).suffix.lower()
    data = uploaded.getvalue()
    try:
        if suffix in [".txt", ".md"]:
            return data.decode("utf-8", errors="replace")[:30000]
        if suffix == ".pdf":
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(data))
            return "\n".join(page.extract_text() or "" for page in reader.pages)[:30000]
        if suffix == ".docx":
            from docx import Document
            doc = Document(BytesIO(data))
            return "\n".join(p.text for p in doc.paragraphs)[:30000]
    except Exception as e:
        st.warning(f"Could not read {uploaded.name}: {e}")
    return ""

def draft_with_gemini(prompt, source_text, profile_text, scholarship_text, details=None):
    """Generate a scholarship essay using Google's Gemini API."""
    key = secret("GEMINI_API_KEY")
    if not key:
        return None, "Add GEMINI_API_KEY in Streamlit Community Cloud → Settings → Secrets. Create a key at Google AI Studio."
    details = details or {}
    word_limit = int(details.get("word_limit") or 500)

    def safe(value, limit=12000):
        return str(value or "").strip()[:limit]

    instructions = f"""You are an excellent scholarship essay coach. Write a specific, coherent first draft that directly answers the scholarship prompt. Do not write a generic template or checklist instead of an essay. Never invent events, results, awards, identities, hardship, feelings, numbers, or responsibilities. Use only supplied facts. If crucial details are missing, use a concise [ADD A SPECIFIC DETAIL] placeholder. Do not paste filenames, document headings, field labels, or raw metadata into the essay. Use writing samples to understand the applicant's natural voice, but do not deliberately reproduce grammar errors. Avoid clichés, repetition, inflated language, and generic claims. Focus on a clear central idea, concrete evidence, reflection, and connection to the scholarship. Aim for approximately {word_limit} words and do not exceed it by more than 5%. Return the essay followed by a short 'Facts to verify' section."""
    user_content = f"""SCHOLARSHIP PROMPT AND CRITERIA:
{safe(scholarship_text, 5000)}

WHAT THE APPLICANT WANTS TO EMPHASIZE:
{safe(prompt, 3000)}

APPLICANT PROFILE AND GOALS:
{safe(profile_text, 5000)}

SPECIFIC DETAILS PROVIDED:
- Goal: {safe(details.get('goal'), 2000)}
- Service/volunteering: {safe(details.get('service'), 2000)}
- Specific experience: {safe(details.get('example'), 3000)}
- Actions taken: {safe(details.get('action'), 2000)}
- Actual impact: {safe(details.get('impact'), 2000)}
- Lesson learned: {safe(details.get('lesson'), 2000)}
- Future plans: {safe(details.get('future'), 2000)}
- How scholarship helps: {safe(details.get('need'), 2000)}
- Example of natural phrasing: {safe(details.get('voice'), 1500)}

WRITING SAMPLES/NOTES (background only; never paste headings or metadata):
{safe(source_text, 14000)}

Write in a thoughtful high-school student's voice, grounded only in the facts above. For service essays, explain what the applicant actually did, why it mattered, what they learned, and how they will continue. Do not claim outcomes the applicant did not provide."""
    try:
        from google import genai
        client = genai.Client(api_key=key)
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=instructions + "\n\n" + user_content,
        )
        result = (getattr(response, "text", None) or "").strip()
        if not result:
            return None, "Gemini returned an empty response. Try again or use the offline template."
        return result, None
    except Exception as e:
        message = str(e)
        if "429" in message or "RESOURCE_EXHAUSTED" in message:
            return None, "Gemini's free-tier quota or rate limit has been reached. Try again later or use the offline template."
        if "API_KEY_INVALID" in message or "invalid api key" in message.lower() or "permission" in message.lower():
            return None, "Gemini could not authenticate this key. Check GEMINI_API_KEY in Streamlit Secrets and Google AI Studio."
        return None, f"Gemini drafting failed: {message[:400]}"


def draft_without_ai(prompt, source_text, profile_text, scholarship_text, details=None, word_limit=500):
    """Create a cleaner, fact-grounded essay draft without an external AI API."""
    details = details or {}

    def clean(value):
        value = str(value or "").replace("\\n", " ").replace("\n", " ")
        return re.sub(r"\s+", " ", value).strip(" \t\r\n-•")

    def sentence(value):
        value = clean(value)
        if not value:
            return ""
        return value if value[-1] in ".!?" else value + "."

    # Pull useful content from samples without including headings, field labels,
    # or entire document headers in the essay.
    ignored_starts = (
        "school:", "class year:", "intended major:", "possible minor",
        "college interests:", "basic information", "brag sheet", "who i am",
        "education:", "location:", "field:", "graduation year:",
        "selected themes:", "other user-provided keywords:",
        "writing sample:", "--- writing sample:"
    )
    candidates = []
    for line in re.split(r"[\n\r]+", str(source_text or "")):
        line = clean(line)
        if not line or len(line) < 28 or line.lower().startswith(ignored_starts):
            continue
        if line.endswith(":") or (line.isupper() and len(line) < 80):
            continue
        if line not in candidates:
            candidates.append(line)
    for line in re.split(r"[\n\r]+", str(profile_text or "")):
        line = clean(line)
        if len(line) >= 28 and not line.lower().startswith(ignored_starts) and line not in candidates:
            candidates.append(line)

    prompt_text = clean(scholarship_text)
    task_text = clean(prompt)
    goal = clean(details.get("goal"))
    example = clean(details.get("example"))
    action = clean(details.get("action"))
    impact = clean(details.get("impact"))
    lesson = clean(details.get("lesson"))
    future = clean(details.get("future"))
    need = clean(details.get("need"))
    voice = clean(details.get("voice"))
    service = clean(details.get("service"))
    word_limit = int(details.get("word_limit") or word_limit)

    # Prefer user-entered facts. Only use sample-derived text when no better
    # detail exists, and never paste metadata or raw document labels into prose.
    if not example and candidates:
        example = candidates[0]
    if not lesson:
        lesson = "I learned that consistent, practical help can make a difference to people facing difficult circumstances"
    if not goal:
        goal = "continue my education and use what I learn to contribute to my community"
    if not future:
        future = "keep serving my community while developing the skills to make a meaningful contribution"
    if not need:
        need = "help cover educational expenses and make it easier to focus on my studies"

    paragraphs = []
    if service or "volunteer" in (task_text + " " + prompt_text).lower() or "hungry" in (task_text + " " + prompt_text).lower():
        opening = (
            "Service matters to me because meeting a community's needs often begins with practical, consistent action. "
            + (sentence(service) + " " if service else "")
            + "I want to support efforts that help people access essentials, including reliable food, while treating every person with dignity."
        )
    else:
        opening = (
            "I am applying for this scholarship because it would support my education and the goals I am working toward. "
            + "My goal is to " + goal.rstrip(".") + "."
        )
    paragraphs.append(opening)

    if example:
        p2 = "One experience that connects to this commitment is " + sentence(example)
        if action:
            p2 += " In that work, " + sentence(action)
        if impact:
            p2 += " The result was " + sentence(impact)
        paragraphs.append(p2)
    else:
        paragraphs.append(
            "A meaningful example from my own experience would help show this commitment. "
            "[Add one specific volunteering experience: where you served, what you did, and who benefited.]"
        )

    paragraphs.append(
        "That experience has taught me " + sentence(lesson).lower().rstrip(".")
        + ". It has helped me understand that service is not only about wanting to help; it is also about listening, following through, and doing work that responds to real needs."
    )

    if voice:
        paragraphs.append("In my own words, " + sentence(voice))
    if future:
        paragraphs.append(
            "I want to carry this lesson into the future by " + future.rstrip(".")
            + ". My education will help me build the knowledge and judgment to do that thoughtfully."
        )
    else:
        paragraphs.append("I want to carry this lesson into the future through my education and continued community involvement.")

    paragraphs.append(
        "This scholarship would " + need.rstrip(".") + ". "
        + "With that support, I could keep working toward my goals while making time for the learning and service that matter to me."
    )

    draft = "\n\n".join(paragraphs)
    count = len(draft.split())
    if word_limit and count > word_limit:
        draft += f"\n\n[Revision note: This draft is about {count} words. Trim it to the scholarship's {word_limit}-word limit.]"
    else:
        draft += f"\n\n[Revision note: About {count} words. Add specific, accurate details and check the sponsor's word limit.]"
    draft += (
        "\n\n--- BEFORE SUBMITTING ---\n"
        "• Replace any generic wording with details only you can provide.\n"
        "• Verify every statement and remove anything that is not accurate.\n"
        "• Read aloud and revise phrases that do not sound like you.\n"
        "• Check the scholarship sponsor's rules about writing assistance."
    )
    return draft

def draft_with_gpt(prompt, source_text, profile_text, scholarship_text):
    key = secret("OPENAI_API_KEY")
    if not key:
        return None, "Add OPENAI_API_KEY in Streamlit Secrets to enable AI essay drafting."
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        instructions = (
            "You are a thoughtful scholarship essay coach. Help the applicant present real experiences clearly, "
            "specifically, and compellingly. Do not invent facts, awards, diagnoses, identities, hardships, or outcomes. "
            "Do not exaggerate trauma. If details are missing, use [ADD YOUR DETAIL] placeholders. Match the exact prompt "
            "and word limit. Preserve the applicant's voice based on their supplied writing sample. Explain how the draft "
            "answers the selection criteria, but never promise or guarantee an award."
        )
        user_content = f"""SCHOLARSHIP PROMPT / REQUIREMENTS:
{scholarship_text}

APPLICANT PROFILE (user-provided):
{profile_text}

APPLICANT'S WRITING SAMPLE / NOTES:
{source_text}

TASK:
{prompt}

Write a strong, authentic draft grounded only in supplied facts. After the draft, list facts to verify and briefly explain how the response aligns with the stated criteria. Do not include irrelevant private information."""
        response = client.responses.create(model="gpt-4.1-mini", instructions=instructions, input=user_content)
        return response.output_text, None
    except Exception as e:
        return None, f"Drafting failed: {e}"

with tab_search:
    if "saved_scholarships" not in st.session_state:
        st.session_state["saved_scholarships"] = []
    left, right = st.columns([1.45, 1], gap="large")
    with left:
        st.markdown('<div class="section-kicker">01 / MATCH WITH PURPOSE</div>', unsafe_allow_html=True)
        st.markdown("## Find opportunities that fit")
        st.write("Search scholarship pages using your goals and chosen eligibility themes. Verify deadlines and criteria with the official sponsor.")
        if st.button("Search scholarships ↗", type="primary", key="search_button"):
            query = make_search_query()
            st.session_state["last_query"] = query
            with st.spinner("Searching the web for scholarship leads..."):
                results, error = search_web(query, count)
            if error:
                st.warning(error)
            else:
                st.session_state["scholarship_results"] = results
                st.success(f"Found {len(results)} search results.")
        if st.session_state.get("last_query"):
            st.caption("Current search: " + st.session_state["last_query"])
    with right:
        with st.container(border=True):
            st.markdown('<div class="section-kicker">YOUR SEARCH SNAPSHOT</div>', unsafe_allow_html=True)
            st.markdown("### Built around you")
            st.write(f"**Education:** {education}")
            st.write(f"**Field:** {field or 'Add a major or career in the sidebar'}")
            st.write(f"**Location:** {location or 'Any location'}")
            st.write(f"**Themes:** {', '.join(adversity) if adversity else 'No experience themes selected'}")
            st.caption("Sensitive filters are optional and are used to make search queries more relevant.")
    results = st.session_state.get("scholarship_results", [])
    for i, item in enumerate(results, 1):
        with st.container(border=True):
            a, b = st.columns([5, 1])
            with a:
                st.markdown(f"### {i:02d} · {item.get('title', 'Scholarship result')}")
                st.write(limited_description(item.get("content", "No preview available.")))
                st.markdown(f'<div class="result-url">{item.get("url", "")}</div>', unsafe_allow_html=True)
            with b:
                if item.get("url"):
                    st.link_button("Open ↗", item["url"], key=f"open_result_{i}")
                saved_urls = [saved.get("url") for saved in st.session_state["saved_scholarships"]]
                if item.get("url") in saved_urls:
                    st.button("✓ Saved", key=f"saved_result_{i}", disabled=True)
                else:
                    if st.button("＋ Save", key=f"save_result_{i}"):
                        st.session_state["saved_scholarships"].append({
                            "title": item.get("title", "Scholarship result"),
                            "url": item.get("url", ""),
                            "content": item.get("content", ""),
                        })
                        st.rerun()
    if results:
        st.info("These are search leads, not verified awards. Confirm eligibility, award amount, deadlines, and AI-use rules on the sponsor's official website.")

    st.markdown("---")
    st.markdown('<div class="section-kicker">YOUR SHORTLIST</div>', unsafe_allow_html=True)
    st.markdown("## Saved scholarships")
    saved_scholarships = st.session_state.get("saved_scholarships", [])
    if not saved_scholarships:
        st.caption("Your saved scholarships will appear here. Save results to build your shortlist.")
    else:
        st.caption(f"{len(saved_scholarships)} scholarship(s) saved in this session.")
        for idx, saved in enumerate(saved_scholarships):
            with st.container(border=True):
                c1, c2, c3 = st.columns([5, 1, 1])
                with c1:
                    st.markdown(f"### {saved['title']}")
                    st.write(limited_description(saved.get("content", "")))
                    st.markdown(f'<div class="result-url">{saved.get("url", "")}</div>', unsafe_allow_html=True)
                with c2:
                    if saved.get("url"):
                        st.link_button("Open ↗", saved["url"], key=f"open_saved_{idx}")
                with c3:
                    if st.button("Remove", key=f"remove_saved_{idx}"):
                        st.session_state["saved_scholarships"].pop(idx)
                        st.rerun()
        export_text = "\\n\\n".join(
            f"{s['title']}\\n{s.get('url', '')}\\n{s.get('content', '')}" for s in saved_scholarships
        )
        st.download_button("Export saved scholarships ↓", export_text, file_name="saved-scholarships.txt", mime="text/plain")

with tab_essay:
    st.markdown('<div class="section-kicker">02 / WRITE IN YOUR OWN VOICE</div>', unsafe_allow_html=True)
    st.markdown("## Essay studio")
    st.write("Generate a personalized scholarship essay with Google Gemini, or use the offline template without an API key. Gemini sends the text you provide to Google for processing.")
    with st.container(border=True):
        uploaded_files = st.file_uploader(
            "Upload multiple writing samples or notes",
            type=["txt", "md", "pdf", "docx"],
            accept_multiple_files=True,
            key="writing_samples",
            help="Select several files at once. Their extracted text will be combined as reference material for your essay draft."
        )
        writing_sections = []
        if uploaded_files:
            for uploaded_file in uploaded_files:
                extracted = extract_document(uploaded_file)
                if extracted.strip():
                    writing_sections.append(
                        f"--- WRITING SAMPLE: {uploaded_file.name} ---\\n{extracted.strip()}"
                    )
            writing_sample = "\\n\\n".join(writing_sections)
            st.success(
                f"Loaded {len(uploaded_files)} file(s), with {len(writing_sample):,} characters of readable text."
            )
            with st.expander("Preview extracted writing samples"):
                if writing_sample:
                    st.text(writing_sample[:8000])
                    if len(writing_sample) > 8000:
                        st.caption("Preview shortened. The essay studio can use the combined extracted text.")
                else:
                    st.warning("No readable text was extracted from these files.")
        else:
            writing_sample = ""
        essay_profile = st.text_area("Background and goals (optional)", placeholder="Your intended major, career goals, responsibilities, projects, or other relevant context.", height=100)
        scholarship_prompt = st.text_area("Scholarship prompt and criteria", placeholder="Paste the exact question and selection criteria.", height=130)
        task = st.text_area("Main message", placeholder="Example: Show my commitment to volunteering and helping fight hunger.", height=70)
        with st.expander("Add details to make the draft more specific"):
            service_detail = st.text_area("What service or volunteering have you done?", placeholder="Organization, event, food drive, meal distribution, or other service. Include only true details.", height=75)
            example_detail = st.text_area("One specific experience", placeholder="What did you personally do? Describe one real moment or responsibility.", height=85)
            action_detail = st.text_area("What actions did you take?", placeholder="Your role, tasks, hours, people you worked with, or problem you helped solve.", height=70)
            impact_detail = st.text_area("What changed because of your work?", placeholder="Use real outcomes if you know them. Do not guess numbers.", height=65)
            lesson_detail = st.text_area("What did you learn?", placeholder="A lesson or value you took from the experience.", height=65)
            future_detail = st.text_area("How will you continue this work?", placeholder="Connect your future plans to service, education, or your career.", height=65)
            need_detail = st.text_area("How would the scholarship help?", placeholder="Tuition, books, transportation, supplies, or another real education expense.", height=65)
            voice_detail = st.text_area("A sentence in your own voice (optional)", placeholder="Write a sentence the way you would naturally say it.", height=55)
            word_limit_detail = st.number_input("Target word limit", min_value=100, max_value=2000, value=500, step=50)
        gemini_consent = st.checkbox("I agree to send the prompt, writing samples, and details I entered to Google Gemini. I will avoid sharing sensitive information I do not want processed.")
        st.caption("Uploaded writing and essay details are sent to Google only if you choose Gemini. The offline template does not call an AI service.")
        ai_col, template_col = st.columns(2)
        with ai_col:
            create_gemini = st.button("Generate with Gemini ✦", type="primary", use_container_width=True)
        with template_col:
            create_template = st.button("Use free template", use_container_width=True)

        profile_text = "\n".join([
            f"Education: {education}", f"Location: {location}", f"Field: {field}",
            f"Graduation year: {graduation_year}", f"Selected themes: {', '.join(adversity)}",
            f"Other user-provided keywords: {struggles}", essay_profile
        ])
        details = {
            "goal": essay_profile, "service": service_detail, "example": example_detail,
            "action": action_detail, "impact": impact_detail, "lesson": lesson_detail,
            "future": future_detail, "need": need_detail, "voice": voice_detail,
            "word_limit": word_limit_detail,
        }
        if create_gemini:
            if not gemini_consent:
                st.error("Please confirm before sending your writing and details to Google Gemini.")
            elif not scholarship_prompt.strip():
                st.error("Add the scholarship prompt first.")
            else:
                with st.spinner("Gemini is drafting your essay..."):
                    result, error = draft_with_gemini(task, writing_sample, profile_text, scholarship_prompt, details)
                if error:
                    st.error(error)
                else:
                    st.session_state["essay_draft"] = result
                    st.success("Your Gemini essay draft is ready. Review and personalize it before submitting.")
        if create_template:
            if not scholarship_prompt.strip():
                st.error("Add the scholarship prompt first.")
            else:
                with st.spinner("Building a structured starter..."):
                    st.session_state["essay_draft"] = draft_without_ai(task, writing_sample, profile_text, scholarship_prompt, details)
                st.success("Your offline template draft is ready. No AI service was called.")
    if st.session_state.get("essay_draft"):
        st.markdown("### Your draft")
        st.text_area("Edit before using", value=st.session_state["essay_draft"], height=380, key="editable_draft")
        st.download_button("Download essay draft ↓", st.session_state["editable_draft"], file_name="scholarship-essay-draft.txt", mime="text/plain")
        st.warning("Read it carefully, verify every claim, and follow the scholarship's rules about AI assistance.")

with tab_tracker:
    st.markdown('<div class="section-kicker">03 / KEEP MOVING</div>', unsafe_allow_html=True)
    st.markdown("## Application checklist")
    st.write("A simple checklist for keeping each application organized.")
    items = [
        "Confirm eligibility on the official website", "Verify deadline and time zone",
        "Read the scholarship's AI-use policy", "Request recommendation letters",
        "Prepare transcript and required documents", "Proofread each answer for accuracy",
        "Submit the application yourself", "Save the confirmation email or receipt"
    ]
    cols = st.columns(2)
    for idx, item in enumerate(items):
        with cols[idx % 2]:
            st.checkbox(item, key=f"check_{idx}")
    st.caption("This starter checklist is kept in the current session and is not yet saved to a permanent account.")

with tab_resources:
    st.markdown('<div class="section-kicker">04 / TRUSTED STARTING POINTS</div>', unsafe_allow_html=True)
    st.markdown("## Scholarship resources")
    resources = [
        ("CareerOneStop Scholarship Finder", "https://www.careeronestop.org/Toolkit/Training/find-scholarships.aspx"),
        ("Federal Student Aid", "https://studentaid.gov/"),
        ("BigFuture Scholarship Search", "https://bigfuture.collegeboard.org/pay-for-college/scholarship-search"),
        ("Scholarship America", "https://scholarshipamerica.org/students/"),
        ("Fastweb", "https://www.fastweb.com/"),
    ]
    for name, url in resources:
        with st.container(border=True):
            st.markdown(f"### {name}")
            st.link_button("Visit resource ↗", url)
    st.caption("Be cautious of scams. Legitimate scholarships should not require you to pay to apply.")

st.markdown("---")
st.markdown('<div class="small-note">SCHOLARSHIP SCOUT AI · Built to help you find opportunities and tell your story with care. No essay can guarantee an award. Review all generated content before submitting.</div>', unsafe_allow_html=True)

with tab_feedback:
    st.markdown('<div class="section-kicker">05 / HELP IMPROVE SCHOLARSHIP SCOUT</div>', unsafe_allow_html=True)
    st.markdown("## Found a bug?")
    st.write(
        "Help make Scholarship Scout better for everyone. If something looks wrong, "
        "a button does not work, a scholarship result seems inaccurate, or the essay "
        "studio behaves unexpectedly, please report it using the form below."
    )
    with st.container(border=True):
        st.markdown("### Submit a bug report")
        st.write("Please describe what you were doing, what you expected to happen, and what happened instead.")
        st.link_button(
            "Report a bug ↗",
            "https://forms.gle/8dAjyHSHFBrBv1tZ9",
            type="primary",
            use_container_width=True,
        )
        st.caption(
            "Please do not include passwords, API keys, or sensitive personal information "
            "in your report. If possible, include the page or feature where the issue occurred."
        )

