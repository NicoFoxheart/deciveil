"""
Deciveil — AI-Powered Truth Platform
Built by Nico Graham | $0 stack
"""

import streamlit as st
import sys, os

sys.path.append(os.path.dirname(__file__))
from modules.scam_detector import analyze_scam
from modules.lie_detector import analyze_manipulation

st.set_page_config(
    page_title="Deciveil | Truth Platform",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif; }

.stApp {
    background: #080810;
    color: #f0f0f0;
}

#MainMenu, footer, header { visibility: hidden; }

.hero {
    text-align: center;
    padding: 3rem 0 2rem 0;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(90deg, #6C63FF22, #9b5de522);
    border: 1px solid #6C63FF55;
    color: #a89cff;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.35rem 1rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #a89cff 60%, #6C63FF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 1rem 0;
}
.hero-sub {
    font-size: 1.1rem;
    color: #888;
    font-weight: 400;
    max-width: 480px;
    margin: 0 auto 2rem auto;
    line-height: 1.6;
}
.stats-row {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 2.5rem;
}
.stat { text-align: center; }
.stat-num { font-size: 1.6rem; font-weight: 800; color: #a89cff; }
.stat-label { font-size: 0.75rem; color: #555; text-transform: uppercase; letter-spacing: 0.08em; }

.divider { border: none; border-top: 1px solid #1a1a2e; margin: 0 0 2rem 0; }

.tool-header { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.4rem; }
.tool-icon { width: 40px; height: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
.icon-scam { background: linear-gradient(135deg, #ff4d4d22, #ff4d4d44); border: 1px solid #ff4d4d33; }
.icon-lie  { background: linear-gradient(135deg, #6C63FF22, #9b5de544); border: 1px solid #6C63FF33; }
.tool-title { font-size: 1.15rem; font-weight: 700; color: #fff; margin: 0; }
.tool-desc { font-size: 0.85rem; color: #666; margin: 0 0 1.2rem 0; }

.result-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-top: 1rem;
}
.result-label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.12em; color: #555; margin-bottom: 0.3rem; }
.result-risk { font-size: 1.05rem; font-weight: 700; margin: 0 0 0.8rem 0; }
.risk-red    { color: #ff5555; }
.risk-orange { color: #ffaa00; }
.risk-yellow { color: #ffcc44; }
.risk-green  { color: #00cc88; }

.score-bar-bg { background: rgba(255,255,255,0.06); border-radius: 999px; height: 6px; margin: 0.4rem 0 0.8rem 0; overflow: hidden; }
.score-bar-fill-red    { height: 6px; border-radius: 999px; background: linear-gradient(90deg, #ff5555, #ff0000); }
.score-bar-fill-orange { height: 6px; border-radius: 999px; background: linear-gradient(90deg, #ffaa00, #ff6600); }
.score-bar-fill-yellow { height: 6px; border-radius: 999px; background: linear-gradient(90deg, #ffcc44, #ffaa00); }
.score-bar-fill-green  { height: 6px; border-radius: 999px; background: linear-gradient(90deg, #00cc88, #00aa66); }

.result-advice { font-size: 0.85rem; color: #777; margin: 0; line-height: 1.5; }

.chip-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.8rem; }
.chip { background: rgba(255,85,85,0.1); border: 1px solid rgba(255,85,85,0.25); color: #ff8888; font-size: 0.75rem; font-weight: 500; padding: 0.2rem 0.7rem; border-radius: 999px; }
.chip-purple { background: rgba(108,99,255,0.1); border: 1px solid rgba(108,99,255,0.25); color: #a89cff; font-size: 0.75rem; font-weight: 500; padding: 0.2rem 0.7rem; border-radius: 999px; }

.stTextArea textarea {
    background: #0e0e1a !important;
    color: #e0e0e0 !important;
    border: 1px solid #1e1e30 !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
}
.stTextArea textarea:focus {
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.15) !important;
}

.stButton > button {
    background: linear-gradient(90deg, #6C63FF, #9b5de5) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover { opacity: 0.88 !important; }

.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; background: transparent; border-bottom: 1px solid #1a1a2e; padding-bottom: 0; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #555; font-weight: 600; font-size: 0.9rem; border: none; padding: 0.6rem 1.2rem; border-radius: 0; }
.stTabs [aria-selected="true"] { background: transparent; color: #a89cff !important; border-bottom: 2px solid #6C63FF !important; }

.footer { text-align: center; margin-top: 3rem; padding: 2rem 0 1rem 0; border-top: 1px solid #111; }
.footer-text { font-size: 0.8rem; color: #333; }
.footer-link { color: #6C63FF; text-decoration: none; }
</style>
""", unsafe_allow_html=True)


# ─── HERO ───────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">🛡️ AI Truth Platform</div>
    <h1 class="hero-title">Deciveil</h1>
    <p class="hero-sub">Protect yourself from scams, manipulation, and deceptive messages — powered by AI, completely free.</p>
    <div class="stats-row">
        <div class="stat">
            <div class="stat-num">2</div>
            <div class="stat-label">Detection Engines</div>
        </div>
        <div class="stat">
            <div class="stat-num">$0</div>
            <div class="stat-label">Cost</div>
        </div>
        <div class="stat">
            <div class="stat-num">100%</div>
            <div class="stat-label">Open Source</div>
        </div>
    </div>
</div>
<hr class="divider">
""", unsafe_allow_html=True)


# ─── TABS ───────────────────────────────────────────────
tab1, tab2 = st.tabs(["🚨  Scam Shield", "🧠  Lie Detector"])


# ══════════════════════════════════════════
# TAB 1 — SCAM SHIELD
# ══════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="tool-header" style="margin-top:1.5rem">
        <div class="tool-icon icon-scam">🚨</div>
        <div>
            <p class="tool-title">Scam Shield</p>
        </div>
    </div>
    <p class="tool-desc">Paste any suspicious message — text, email, DM, or notification. We'll scan it instantly.</p>
    """, unsafe_allow_html=True)

    scam_text = st.text_area(
        "",
        height=150,
        placeholder="Paste a suspicious message here...",
        key="scam_input",
        label_visibility="collapsed"
    )

    if st.button("Analyze Message", key="scam_btn"):
        if scam_text.strip():
            with st.spinner("Scanning..."):
                result = analyze_scam(scam_text)

            score = result["score"]
            color = result["color"]
            risk = result["risk_level"]
            keywords = result["matched_keywords"]

            color_class = f"risk-{color}" if color in ["red","green"] else ("risk-orange" if color == "orange" else "risk-yellow")
            bar_class = f"score-bar-fill-{color}"

            chips = "".join([f'<span class="chip">{kw}</span>' for kw in keywords]) if keywords else ""
            chips_html = f'<div class="chip-row">{chips}</div>' if chips else '<p style="color:#00cc88; font-size:0.85rem; margin-top:0.8rem">✅ No suspicious keywords found.</p>'

            advice_map = {
                "red": "Do not engage. Block the sender and report if possible.",
                "orange": "Proceed with caution. Verify through official channels.",
                "yellow": "A few flags detected. Stay alert.",
                "green": "Looks clean. No scam indicators detected."
            }

            st.markdown(f"""
            <div class="result-card">
                <p class="result-label">Scan Result</p>
                <p class="result-risk {color_class}">{risk}</p>
                <div class="score-bar-bg"><div class="{bar_class}" style="width:{score}%"></div></div>
                <p style="font-size:0.78rem; color:#444; margin:0 0 0.5rem 0">Risk Score: {score}/100</p>
                <p class="result-advice">{advice_map.get(color, "")}</p>
                {chips_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Paste a message first.")


# ══════════════════════════════════════════
# TAB 2 — LIE DETECTOR
# ══════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="tool-header" style="margin-top:1.5rem">
        <div class="tool-icon icon-lie">🧠</div>
        <div>
            <p class="tool-title">Lie & Manipulation Detector</p>
        </div>
    </div>
    <p class="tool-desc">Detects gaslighting, guilt-tripping, pressure tactics, emotional manipulation, and more.</p>
    """, unsafe_allow_html=True)

    lie_text = st.text_area(
        "",
        height=150,
        placeholder="Paste a message that felt off or uncomfortable...",
        key="lie_input",
        label_visibility="collapsed"
    )

    if st.button("Analyze Message", key="lie_btn"):
        if lie_text.strip():
            with st.spinner("Analyzing..."):
                result = analyze_manipulation(lie_text)

            score = result["score"]
            color = result["color"]
            risk = result["risk_level"]
            patterns = result["detected_patterns"]
            advice = result["advice"]

            color_class = f"risk-{color}" if color in ["red","green"] else ("risk-orange" if color == "orange" else "risk-yellow")
            bar_class = f"score-bar-fill-{color}"

            pattern_chips = ""
            for ptype in patterns:
                label = ptype.replace("_", " ").title()
                pattern_chips += f'<span class="chip-purple">{label}</span>'
            chips_html = f'<div class="chip-row">{pattern_chips}</div>' if pattern_chips else '<p style="color:#00cc88; font-size:0.85rem; margin-top:0.8rem">✅ No manipulation patterns found.</p>'

            details_html = ""
            for ptype, matches in patterns.items():
                label = ptype.replace("_", " ").title()
                examples = ", ".join([f'"{m}"' for m in matches[:2]])
                details_html += f'<p style="font-size:0.8rem; color:#666; margin:0.3rem 0">⚠️ <strong style="color:#888">{label}</strong> — {examples}</p>'

            st.markdown(f"""
            <div class="result-card">
                <p class="result-label">Analysis Result</p>
                <p class="result-risk {color_class}">{risk}</p>
                <div class="score-bar-bg"><div class="{bar_class}" style="width:{score}%"></div></div>
                <p style="font-size:0.78rem; color:#444; margin:0 0 0.5rem 0">Manipulation Score: {score}/100</p>
                <p class="result-advice">{advice}</p>
                {chips_html}
                {details_html}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Paste a message first.")


# ─── FOOTER ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p class="footer-text">
        Built with 💙 by <strong style="color:#6C63FF">Nico Graham</strong> &nbsp;·&nbsp;
        <a class="footer-link" href="https://github.com/nicofoxheart/deciveil" target="_blank">GitHub</a>
        &nbsp;·&nbsp; Open Source · Free Forever
    </p>
    <p style="font-size:0.72rem; color:#222; margin-top:0.3rem">Deciveil does not store any messages. Everything runs locally.</p>
</div>
""", unsafe_allow_html=True)
