import streamlit as st
import time
import threading
from pipeline import run_research_pipeline
from pipeline import extract_text

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AgentForge",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --border:    #1e1e2e;
    --accent:    #7c6af7;
    --accent2:   #e94560;
    --accent3:   #00d9b8;
    --text:      #e8e8f0;
    --muted:     #6b6b8a;
    --success:   #00d9b8;
}

/* Base */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { background: var(--surface) !important; }

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid var(--accent);
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    margin-bottom: 1.5rem;
    font-family: 'JetBrains Mono', monospace;
}
.hero h1 {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.8rem, 6vw, 5rem) !important;
    font-weight: 800 !important;
    line-height: 1.05 !important;
    letter-spacing: -0.03em !important;
    margin: 0 0 1rem !important;
    background: linear-gradient(135deg, #fff 30%, var(--accent) 70%, var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero p {
    font-size: 0.9rem;
    color: var(--muted);
    max-width: 500px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
}

/* ── Input area ── */
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.85rem 1.1rem !important;
    transition: border-color 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(124,106,247,0.15) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #5a4fd6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2.2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100%;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Pipeline step cards ── */
.step-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    margin-bottom: 0.9rem;
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    transition: border-color 0.3s;
    position: relative;
    overflow: hidden;
}
.step-card.active  { border-color: var(--accent); }
.step-card.done    { border-color: var(--success); }
.step-card.waiting { opacity: 0.45; }

.step-card.active::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(124,106,247,0.06), transparent);
    pointer-events: none;
}

.step-icon {
    font-size: 1.4rem;
    min-width: 2rem;
    text-align: center;
    margin-top: 0.1rem;
}
.step-label {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--text);
    margin-bottom: 0.25rem;
}
.step-desc {
    font-size: 0.75rem;
    color: var(--muted);
    line-height: 1.5;
}
.step-status {
    margin-left: auto;
    font-size: 0.7rem;
    font-family: 'JetBrains Mono', monospace;
    padding: 0.2rem 0.6rem;
    border-radius: 999px;
}
.step-status.running { background: rgba(124,106,247,0.2); color: var(--accent); }
.step-status.done    { background: rgba(0,217,184,0.15);  color: var(--success); }
.step-status.waiting { background: rgba(107,107,138,0.15); color: var(--muted); }

/* ── Result panels ── */
.result-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.6rem;
    margin-top: 1rem;
}
.result-panel h3 {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin: 0 0 1rem !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.result-panel h3 span.dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent);
}
.result-panel .content {
    font-size: 0.88rem;
    line-height: 1.8;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Feedback panel ── */
.feedback-panel {
    background: linear-gradient(135deg, rgba(233,69,96,0.07), rgba(124,106,247,0.07));
    border: 1px solid rgba(233,69,96,0.3);
    border-radius: 14px;
    padding: 1.6rem;
    margin-top: 1rem;
}

/* ── Divider ── */
.divider { border-top: 1px solid var(--border); margin: 2rem 0; }

/* ── Spinner override ── */
[data-testid="stSpinner"] > div { border-top-color: var(--accent) !important; }

/* ── Expander ── */
[data-testid="stExpander"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    color: var(--muted) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* Tab styling */
[data-baseweb="tab-list"] { background: var(--surface) !important; border-radius: 10px; border: 1px solid var(--border); padding: 4px; gap: 4px; }
[data-baseweb="tab"] { font-family: 'Syne', sans-serif !important; font-size: 0.82rem !important; font-weight: 700 !important; color: var(--muted) !important; border-radius: 8px !important; }
[aria-selected="true"][data-baseweb="tab"] { background: var(--accent) !important; color: #fff !important; }
</style>
""", unsafe_allow_html=True)


# ── Helper: render a pipeline step ───────────────────────────────────────────
def render_step(icon, label, desc, state_key):
    """state_key: 'waiting' | 'active' | 'done'"""
    status_label  = {"waiting": "queued", "active": "running…", "done": "complete"}[state_key]
    card_class    = f"step-card {state_key}"
    status_class  = {"waiting": "waiting", "active": "running", "done": "done"}[state_key]
    st.markdown(f"""
    <div class="{card_class}">
        <div class="step-icon">{icon}</div>
        <div>
            <div class="step-label">{label}</div>
            <div class="step-desc">{desc}</div>
        </div>
        <span class="step-status {status_class}">{status_label}</span>
    </div>
    """, unsafe_allow_html=True)


# ── Session state defaults ────────────────────────────────────────────────────
st.session_state.setdefault("result", None)
st.session_state.setdefault("error", None)
st.session_state.setdefault("running", False)
st.session_state.setdefault("current_step", 0)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">Multi-Agent · AI Research Pipeline</div>
    <h1>ResearchMind</h1>
    <p>Drop a topic. Four specialised agents search, scrape, write, and critique — so you get a polished research report in minutes.</p>
</div>
""", unsafe_allow_html=True)


# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], gap="small")
with col_input:
    topic = st.text_input(
        label="topic",
        label_visibility="collapsed",
        placeholder="e.g.  Quantum computing in drug discovery …",
        disabled=st.session_state.running,
        key="topic_input",
    )
with col_btn:
    run_clicked = st.button(
        "Run →" if not st.session_state.running else "Running…",
        disabled=st.session_state.running or not topic.strip(),
    )

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


# ── Pipeline columns ──────────────────────────────────────────────────────────
col_pipeline, col_results = st.columns([1, 2], gap="large")

STEPS = [
    ("🔍", "Search Agent",  "Queries the web for recent, authoritative sources"),
    ("📄", "Reader Agent",  "Scrapes the most relevant URL for deep content"),
    ("✍️", "Writer Agent",  "Synthesises findings into a structured report"),
    ("🧐", "Critic Agent",  "Reviews the draft and returns actionable feedback"),
]

with col_pipeline:
    st.markdown('<p style="font-family:Syne,sans-serif;font-size:0.72rem;letter-spacing:0.15em;text-transform:uppercase;color:#6b6b8a;margin-bottom:0.8rem;">Pipeline</p>', unsafe_allow_html=True)
    step_placeholders = [st.empty() for _ in STEPS]

    def draw_steps(active_idx):
        for i, (icon, label, desc) in enumerate(STEPS):
            state = "done" if i < active_idx else ("active" if i == active_idx else "waiting")
            with step_placeholders[i]:
                render_step(icon, label, desc, state)

    # Initial render
    if st.session_state.result:
        draw_steps(4)   # all done
    elif st.session_state.running:
        draw_steps(st.session_state.current_step or 0)
    else:
        draw_steps(-1)  # all waiting


# ── Run the pipeline ──────────────────────────────────────────────────────────
if run_clicked and topic.strip():
    st.session_state.running     = True
    st.session_state.result      = None
    st.session_state.error       = None
    st.session_state.current_step = 0

    # Monkey-patch print to capture step progress via session state is tricky;
    # instead we'll drive steps with a progress placeholder and rerun.
    # We run the pipeline directly and update steps between stages.

    with col_results:
        progress_ph = st.empty()

    try:
        from agents import build_reader_agent, build_search_agent, critic_chain, writer_chain

        state = {}

        # ── Step 0: Search ──
        st.session_state.current_step = 0
        draw_steps(0)
        with col_results:
            with progress_ph:
                with st.spinner("Search agent is scouring the web…"):
                    search_agent  = build_search_agent()
                    search_result = search_agent.invoke({
                        "messages": [("user",
                            f"Find recent, reliable and detailed information about: {topic} "
                            f"and make sure to include urls that you find")]
                    })
                    state["search_results"] = extract_text(search_result["messages"][-1].content)

        # ── Step 1: Reader ──
        st.session_state.current_step = 1
        draw_steps(1)
        with col_results:
            with progress_ph:
                with st.spinner("Reader agent is scraping the top source…"):
                    reader_agent  = build_reader_agent()
                    reader_result = reader_agent.invoke({
                        "messages": [("user",
                            f"Based on the following search results on the '{topic}',"
                            f"pick the most relevant URL and scrape it for deeper content.\n\n"
                            f"Search Results:\n{state['search_results'][:800]}")] 
                    })
                    state["scraped_content"] = extract_text(reader_result["messages"][-1].content)

        # ── Step 2: Writer ──
        st.session_state.current_step = 2
        draw_steps(2)
        with col_results:
            with progress_ph:
                with st.spinner("Writer agent is drafting the report…"):
                    research_combined = (
                        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
                    )
                    state["report"] = writer_chain.invoke({
                        "topic":    topic,
                        "research": research_combined,
                    })

        # ── Step 3: Critic ──
        st.session_state.current_step = 3
        draw_steps(3)
        with col_results:
            with progress_ph:
                with st.spinner("Critic agent is reviewing the report…"):
                    state["feedback"] = critic_chain.invoke({"report": state["report"]})

        # Done
        st.session_state.result  = state
        st.session_state.running = False
        draw_steps(4)
        progress_ph.empty()

    except Exception as e:
        st.session_state.running = False
        st.session_state.error   = str(e)
        draw_steps(-1)


# ── Display error ─────────────────────────────────────────────────────────────
if st.session_state.error:
    with col_results:
        st.markdown(f"""
        <div class="result-panel" style="border-color:#e94560;">
            <h3><span class="dot" style="background:#e94560;"></span>Error</h3>
            <div class="content" style="color:#e94560;">{st.session_state.error}</div>
        </div>""", unsafe_allow_html=True)


# ── Display results ───────────────────────────────────────────────────────────
if st.session_state.result:
    res = st.session_state.result

    with col_results:
        tab_report, tab_search, tab_scraped = st.tabs(["📋 Report", "🔍 Search Results", "📄 Scraped Content"])

        with tab_report:
            st.markdown(f"""
            <div class="result-panel">
                <h3><span class="dot"></span>Final Report</h3>
                <div class="content">{res.get("report","")}</div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="feedback-panel" style="margin-top:1rem;">
                <h3 style="font-family:Syne,sans-serif;font-weight:700;font-size:0.85rem;
                           letter-spacing:0.12em;text-transform:uppercase;color:#e94560;
                           margin:0 0 1rem;display:flex;align-items:center;gap:0.5rem;">
                    <span style="display:inline-block;width:7px;height:7px;border-radius:50%;
                                 background:#e94560;"></span>Critic Feedback
                </h3>
                <div class="content">{res.get("feedback","")}</div>
            </div>""", unsafe_allow_html=True)

        with tab_search:
            st.markdown(f"""
            <div class="result-panel">
                <h3><span class="dot" style="background:#00d9b8;"></span>Raw Search Results</h3>
                <div class="content">{res.get("search_results","")}</div>
            </div>""", unsafe_allow_html=True)

        with tab_scraped:
            st.markdown(f"""
            <div class="result-panel">
                <h3><span class="dot" style="background:#e94560;"></span>Scraped Content</h3>
                <div class="content">{res.get("scraped_content","")}</div>
            </div>""", unsafe_allow_html=True)
            