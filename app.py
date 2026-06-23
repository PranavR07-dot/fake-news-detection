import streamlit as st
import joblib

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="TruthLens – Fake News Detector",
    page_icon="🔍",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600&display=swap');

/* ── Root palette ── */
:root {
    --bg:        #0D0F14;
    --surface:   #14171F;
    --border:    #1E2330;
    --accent:    #5B8BF5;
    --real:      #22C55E;
    --fake:      #EF4444;
    --muted:     #6B7280;
    --text:      #E8EAF0;
    --subtext:   #9CA3AF;
}

/* ── Base overrides ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 1.5rem 4rem !important; max-width: 720px; }

/* ── Brand header ── */
.brand {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    margin-bottom: 2.5rem;
}
.brand-icon {
    font-size: 2.2rem;
    line-height: 1;
}
.brand-name {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    letter-spacing: -0.5px;
    color: var(--text);
    margin: 0;
    line-height: 1.1;
}
.brand-name span { color: var(--accent); }
.brand-tagline {
    font-size: 0.85rem;
    color: var(--subtext);
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin: 0;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: var(--border);
    margin: 0 0 2rem 0;
}

/* ── Label above textarea ── */
.input-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--subtext);
    margin-bottom: 0.5rem;
}

/* ── Textarea ── */
textarea {
    background-color: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
    transition: border-color 0.2s;
    resize: vertical;
}
textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(91,139,245,0.15) !important;
    outline: none !important;
}
textarea::placeholder { color: var(--muted) !important; }

/* ── Char hint ── */
.char-hint {
    font-size: 0.75rem;
    color: var(--muted);
    text-align: right;
    margin-top: 0.3rem;
}

/* ── Analyse button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 2.2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: opacity 0.18s, transform 0.12s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Result card ── */
.result-card {
    border-radius: 12px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.8rem;
    border: 1.5px solid;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}
.result-card.real {
    background: rgba(34,197,94,0.07);
    border-color: rgba(34,197,94,0.35);
}
.result-card.fake {
    background: rgba(239,68,68,0.07);
    border-color: rgba(239,68,68,0.35);
}
.result-icon { font-size: 1.8rem; line-height: 1; }
.result-label {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    line-height: 1.1;
    margin: 0 0 0.2rem 0;
}
.result-card.real .result-label { color: var(--real); }
.result-card.fake .result-label { color: var(--fake); }
.result-desc { font-size: 0.84rem; color: var(--subtext); margin: 0; }

/* ── Confidence bar ── */
.conf-section { margin-top: 1.4rem; }
.conf-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.45rem;
}
.conf-title {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--subtext);
}
.conf-value {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: var(--text);
}
.conf-track {
    background: var(--border);
    border-radius: 999px;
    height: 6px;
    overflow: hidden;
}
.conf-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.7s cubic-bezier(.4,0,.2,1);
}
.conf-fill.real { background: var(--real); }
.conf-fill.fake { background: var(--fake); }

/* ── Footer note ── */
.footer-note {
    text-align: center;
    font-size: 0.75rem;
    color: var(--muted);
    margin-top: 3rem;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# ── Load model ────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    model = joblib.load("model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")
    return model, vectorizer

model, vectorizer = load_model()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="brand">
    <div class="brand-icon">🔍</div>
    <h1 class="brand-name">Truth<span>Lens</span></h1>
    <p class="brand-tagline">AI-powered news credibility analysis</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="input-label">Paste article or headline</p>', unsafe_allow_html=True)

news = st.text_area(
    label="news_input",
    label_visibility="collapsed",
    placeholder="Paste a news article, headline, or any text you want to verify…",
    height=200,
    key="news_input",
)

word_count = len(news.split()) if news.strip() else 0
st.markdown(f'<p class="char-hint">{word_count} words</p>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
predict_btn = st.button("Analyse Article")

# ── Prediction ────────────────────────────────────────────────────────────────
if predict_btn:
    if not news.strip():
        st.markdown("""
        <div class="result-card fake">
            <span class="result-icon">⚠️</span>
            <div>
                <p class="result-label" style="color:#F59E0B">No text entered</p>
                <p class="result-desc">Paste or type some text above before analysing.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Analysing…"):
            vec = vectorizer.transform([news])
            prediction = model.predict(vec)[0]
            raw_score  = model.decision_function(vec)[0]

        is_real   = (prediction == 1)
        label     = "Real News"     if is_real else "Fake News"
        icon      = "✅"            if is_real else "❌"
        css_cls   = "real"          if is_real else "fake"
        desc      = ("This article appears credible based on linguistic patterns."
                     if is_real else
                     "This article shows patterns commonly found in misinformation.")

        # Normalise confidence to 0–100 %
        capped = min(abs(raw_score), 3.0)
        conf_pct = round((capped / 3.0) * 100)

        st.markdown(f"""
        <div class="result-card {css_cls}">
            <span class="result-icon">{icon}</span>
            <div>
                <p class="result-label">{label}</p>
                <p class="result-desc">{desc}</p>
            </div>
        </div>

        <div class="conf-section">
            <div class="conf-header">
                <span class="conf-title">Model Confidence</span>
                <span class="conf-value">{conf_pct}%</span>
            </div>
            <div class="conf-track">
                <div class="conf-fill {css_cls}" style="width:{conf_pct}%"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<p class="footer-note">
    TruthLens uses a machine-learning classifier trained on labelled news datasets.<br>
    Results are probabilistic — always verify with primary sources.
</p>
""", unsafe_allow_html=True)