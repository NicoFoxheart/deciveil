"""
Deciveil — AI-Powered Truth Platform
Detects scams, manipulation, and deepfakes.
Built by Nico | $0 stack: Python + Streamlit + HuggingFace
"""

import streamlit as st
from PIL import Image
import sys
import os

# Add modules to path
sys.path.append(os.path.dirname(__file__))
from modules.scam_detector import analyze_scam
from modules.lie_detector import analyze_manipulation
from modules.deepfake_detector import analyze_image

# --- Page Config ---
st.set_page_config(
    page_title="Deciveil",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #0e0e14;
        color: #f0f0f0;
    }

    .stApp {
        background: linear-gradient(135deg, #0e0e14 0%, #12121c 100%);
    }

    h1 {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
    }

    .result-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-top: 1rem;
    }

    .risk-high   { color: #ff4d4d; font-weight: 700; font-size: 1.1rem; }
    .risk-medium { color: #ffaa00; font-weight: 700; font-size: 1.1rem; }
    .risk-low    { color: #ff8800; font-weight: 700; font-size: 1.1rem; }
    .risk-safe   { color: #00cc88; font-weight: 700; font-size: 1.1rem; }

    .stButton > button {
        background: linear-gradient(90deg, #6C63FF, #9b5de5);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 2rem;
        width: 100%;
    }

    .stTextArea textarea {
        background-color: #1a1a2e;
        color: #f0f0f0;
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        color: #aaa;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #6C63FF33, #9b5de533);
        color: #ffffff;
        border: 1px solid #6C63FF88;
    }
</style>
""", unsafe_allow_html=True)


# --- Header ---
st.markdown("# 🛡️ Deciveil")
st.markdown("**AI-powered protection against scams, manipulation, and deepfakes.**")
st.markdown("---")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🚨 Scam Shield", "🧠 Lie Detector", "🖼️ Deepfake Scan"])


# ============================
# TAB 1 — SCAM SHIELD
# ============================
with tab1:
    st.subheader("Scam Shield")
    st.caption("Paste a suspicious message — text, email, DM, anything.")

    scam_text = st.text_area(
        "Message to analyze:",
        height=160,
        placeholder="Paste a suspicious text message, email, or DM here...",
        key="scam_input"
    )

    if st.button("Analyze for Scams", key="scam_btn"):
        if scam_text.strip():
            with st.spinner("Analyzing..."):
                result = analyze_scam(scam_text)

            risk = result["risk_level"]
            score = result["score"]
            keywords = result["matched_keywords"]

            # Risk color class
            if result["color"] == "red":
                css_class = "risk-high"
            elif result["color"] == "orange":
                css_class = "risk-medium"
            elif result["color"] == "yellow":
                css_class = "risk-low"
            else:
                css_class = "risk-safe"

            st.markdown(f"""
            <div class="result-card">
                <p class="{css_class}">{risk}</p>
                <p>Risk Score: <strong>{score}/100</strong></p>
            </div>
            """, unsafe_allow_html=True)

            if keywords:
                st.markdown("**🚩 Suspicious phrases found:**")
                cols = st.columns(3)
                for i, kw in enumerate(keywords):
                    cols[i % 3].markdown(f"• `{kw}`")
            else:
                st.success("No suspicious keywords detected.")
        else:
            st.warning("Please paste a message to analyze.")


# ============================
# TAB 2 — LIE DETECTOR
# ============================
with tab2:
    st.subheader("Lie & Manipulation Detector")
    st.caption("Detect gaslighting, pressure tactics, guilt-tripping, and more.")

    lie_text = st.text_area(
        "Message to analyze:",
        height=160,
        placeholder="Paste a message you feel uncomfortable about...",
        key="lie_input"
    )

    if st.button("Analyze for Manipulation", key="lie_btn"):
        if lie_text.strip():
            with st.spinner("Analyzing..."):
                result = analyze_manipulation(lie_text)

            risk = result["risk_level"]
            score = result["score"]
            patterns = result["detected_patterns"]
            advice = result["advice"]

            if result["color"] == "red":
                css_class = "risk-high"
            elif result["color"] == "orange":
                css_class = "risk-medium"
            elif result["color"] == "yellow":
                css_class = "risk-low"
            else:
                css_class = "risk-safe"

            st.markdown(f"""
            <div class="result-card">
                <p class="{css_class}">{risk}</p>
                <p>Manipulation Score: <strong>{score}/100</strong></p>
                <p style="color:#aaa; font-size:0.9rem">{advice}</p>
            </div>
            """, unsafe_allow_html=True)

            if patterns:
                st.markdown("**🚩 Detected manipulation tactics:**")
                for ptype, matches in patterns.items():
                    label = ptype.replace("_", " ").title()
                    with st.expander(f"⚠️ {label} ({len(matches)} match{'es' if len(matches) > 1 else ''})"):
                        for m in matches:
                            st.markdown(f'• *"{m}"*')
            else:
                st.success("No manipulation patterns detected.")
        else:
            st.warning("Please paste a message to analyze.")


# ============================
# TAB 3 — DEEPFAKE DETECTOR
# ============================
with tab3:
    st.subheader("Deepfake Scanner")
    st.caption("Upload an image to check for AI generation or deepfake indicators.")

    uploaded_file = st.file_uploader(
        "Upload image (JPG, PNG, WEBP)",
        type=["jpg", "jpeg", "png", "webp"],
        key="deepfake_upload"
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded image", use_column_width=True)

        if st.button("Scan for Deepfakes", key="deepfake_btn"):
            with st.spinner("Scanning image..."):
                result = analyze_image(image)

            risk = result["risk_level"]
            score = result["score"]
            findings = result["findings"]
            advice = result["advice"]
            size = result["image_size"]

            if result["color"] == "red":
                css_class = "risk-high"
            elif result["color"] == "orange":
                css_class = "risk-medium"
            elif result["color"] == "yellow":
                css_class = "risk-low"
            else:
                css_class = "risk-safe"

            st.markdown(f"""
            <div class="result-card">
                <p class="{css_class}">{risk}</p>
                <p>Suspicion Score: <strong>{score}/100</strong> &nbsp;|&nbsp; Size: {size}</p>
                <p style="color:#aaa; font-size:0.9rem">{advice}</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**🔍 Analysis findings:**")
            for f in findings:
                st.markdown(f"• {f}")

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#444; font-size:0.8rem'>Deciveil — Built with 💙 by Nico | $0 open-source stack</p>",
    unsafe_allow_html=True
)
