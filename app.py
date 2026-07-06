"""
Deciveil v2.0 — Advanced Cybersecurity Analysis Platform
Built by Nico Graham | Open Source | $0 budget
"""

import streamlit as st
import sys, os

sys.path.append(os.path.dirname(__file__))
from modules.scam_detector import analyze_scam
from modules.lie_detector import analyze_manipulation
from modules.url_scanner import analyze_url
from modules.password_analyzer import analyze_password
from modules.hash_identifier import identify_hash
from modules.encoding_detector import analyze_encoding

st.set_page_config(
    page_title="Deciveil | Cybersecurity Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.stApp { background: #04040c; }
.main .block-container { padding: 2rem 2.5rem 2rem 2rem; max-width: 900px; }

[data-testid="stSidebar"] {
    background: #070710 !important;
    border-right: 1px solid #12122a !important;
    min-width: 240px !important;
    max-width: 240px !important;
}
[data-testid="stSidebar"] > div { padding: 0 !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 0 !important; }
[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    padding: 0.65rem 1.2rem !important;
    margin: 0 !important;
    color: #4a4a6a !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    cursor: pointer !important;
    border-left: 2px solid transparent !important;
    transition: all 0.15s ease !important;
    border-radius: 0 !important;
    background: transparent !important;
    width: 100% !important;
    letter-spacing: 0.01em;
}
[data-testid="stSidebar"] .stRadio label:hover {
    color: #9999cc !important;
    background: rgba(108,99,255,0.06) !important;
    border-left-color: #6C63FF55 !important;
}
[data-testid="stSidebar"] .stRadio input { display: none !important; }

.tool-title {
    font-family: 'Inter', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin-bottom: 0.25rem;
}
.tool-subtitle {
    font-size: 0.88rem;
    color: #4a4a6a;
    margin-bottom: 1.8rem;
    line-height: 1.5;
}

.stTextArea textarea, .stTextInput input {
    background: #0a0a18 !important;
    color: #c8d0e0 !important;
    border: 1px solid #1a1a30 !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.83rem !important;
    caret-color: #00f0ff !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #00f0ff55 !important;
    box-shadow: 0 0 0 3px rgba(0,240,255,0.07) !important;
    outline: none !important;
}
.stTextArea label, .stTextInput label { display: none !important; }

.stButton > button {
    background: transparent !important;
    color: #00f0ff !important;
    border: 1px solid #00f0ff44 !important;
    border-radius: 7px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 0.55rem 1.8rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: rgba(0,240,255,0.07) !important;
    border-color: #00f0ff99 !important;
    box-shadow: 0 0 20px rgba(0,240,255,0.12) !important;
}

.result-card {
    background: #07071a;
    border: 1px solid #12122a;
    border-radius: 10px;
    padding: 1.4rem 1.6rem;
    margin-top: 1.2rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
}
.card-red::before    { background: linear-gradient(90deg, transparent, #ef4444, transparent); }
.card-orange::before { background: linear-gradient(90deg, transparent, #f59e0b, transparent); }
.card-yellow::before { background: linear-gradient(90deg, transparent, #eab308, transparent); }
.card-green::before  { background: linear-gradient(90deg, transparent, #10b981, transparent); }

.threat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #2a2a4a;
    margin-bottom: 0.5rem;
}
.threat-value { font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 700; letter-spacing: 0.04em; margin-bottom: 1rem; }
.tv-red    { color: #ef4444; }
.tv-orange { color: #f59e0b; }
.tv-yellow { color: #eab308; }
.tv-green  { color: #10b981; }

.score-wrap { margin-bottom: 0.6rem; }
.score-meta { display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #2a2a4a; margin-bottom: 0.3rem; }
.score-track { background: #0f0f28; border-radius: 999px; height: 4px; overflow: hidden; }
.score-fill-red    { height: 4px; border-radius: 999px; background: linear-gradient(90deg, #991b1b, #ef4444); }
.score-fill-orange { height: 4px; border-radius: 999px; background: linear-gradient(90deg, #92400e, #f59e0b); }
.score-fill-yellow { height: 4px; border-radius: 999px; background: linear-gradient(90deg, #854d0e, #eab308); }
.score-fill-green  { height: 4px; border-radius: 999px; background: linear-gradient(90deg, #065f46, #10b981); }

.advice-text { font-size: 0.82rem; color: #4a4a6a; margin: 0.8rem 0 0 0; line-height: 1.6; border-top: 1px solid #0f0f28; padding-top: 0.8rem; }

.findings { margin-top: 0.8rem; }
.finding-item { font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: #5a5a8a; padding: 0.3rem 0; border-bottom: 1px solid #0c0c20; line-height: 1.5; }
.finding-red    { color: #f87171; }
.finding-yellow { color: #fbbf24; }
.finding-green  { color: #34d399; }

.chip-row { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.8rem; }
.chip { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; padding: 0.2rem 0.6rem; border-radius: 4px; font-weight: 500; }
.chip-red    { background: rgba(239,68,68,0.1);  color: #f87171; border: 1px solid rgba(239,68,68,0.2); }
.chip-cyan   { background: rgba(0,240,255,0.07); color: #00d0dd; border: 1px solid rgba(0,240,255,0.15); }
.chip-purple { background: rgba(139,92,246,0.1); color: #a78bfa; border: 1px solid rgba(139,92,246,0.2); }
.chip-green  { background: rgba(16,185,129,0.1); color: #34d399; border: 1px solid rgba(16,185,129,0.2); }
.chip-yellow { background: rgba(234,179,8,0.1);  color: #fbbf24; border: 1px solid rgba(234,179,8,0.2); }

.meta-row { display: flex; gap: 1.5rem; margin-top: 0.8rem; flex-wrap: wrap; }
.meta-key { font-family: 'JetBrains Mono', monospace; font-size: 0.6rem; letter-spacing: 0.12em; text-transform: uppercase; color: #2a2a4a; }
.meta-val { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #7070a0; font-weight: 600; }

.char-grid { display: flex; gap: 0.5rem; margin-top: 0.8rem; flex-wrap: wrap; }
.char-box { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; padding: 0.25rem 0.6rem; border-radius: 4px; font-weight: 600; display: flex; align-items: center; gap: 0.3rem; }
.char-on  { background: rgba(16,185,129,0.1); color: #34d399; border: 1px solid rgba(16,185,129,0.2); }
.char-off { background: rgba(239,68,68,0.07); color: #4a4a6a; border: 1px solid rgba(239,68,68,0.1); }

.hash-match { background: #09091f; border: 1px solid #1a1a35; border-radius: 8px; padding: 0.9rem 1.1rem; margin-top: 0.6rem; }
.hash-name { font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; font-weight: 700; color: #e2e8f0; margin-bottom: 0.2rem; }
.hash-security { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em; padding: 0.15rem 0.5rem; border-radius: 3px; display: inline-block; margin-bottom: 0.5rem; }
.hs-red    { background: rgba(239,68,68,0.15); color: #f87171; }
.hs-orange { background: rgba(245,158,11,0.15); color: #fbbf24; }
.hs-yellow { background: rgba(234,179,8,0.15); color: #fde68a; }
.hs-green  { background: rgba(16,185,129,0.15); color: #34d399; }
.hash-note { font-size: 0.78rem; color: #4a4a6a; line-height: 1.5; }

.enc-block { background: #09091f; border: 1px solid #1a1a35; border-left: 3px solid #f59e0b; border-radius: 8px; padding: 0.9rem 1.1rem; margin-top: 0.6rem; }
.enc-block-red { border-left-color: #ef4444; }
.enc-type { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; font-weight: 700; color: #f59e0b; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.3rem; }
.enc-original { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #3a3a5a; margin-bottom: 0.4rem; word-break: break-all; }
.enc-decoded { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #a0a0d0; background: #06060f; border-radius: 4px; padding: 0.4rem 0.6rem; word-break: break-all; margin-bottom: 0.4rem; }
.enc-note { font-size: 0.75rem; color: #3a3a5a; }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("""
    <div style="padding: 1.5rem 1.2rem 1rem 1.2rem; border-bottom: 1px solid #12122a;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:1.1rem; font-weight:700; color:#00f0ff; letter-spacing:0.05em;">DECIVEIL</div>
        <div style="display:flex; align-items:center; gap:0.4rem; margin-top:0.35rem;">
            <span style="width:6px; height:6px; border-radius:50%; background:#10b981; display:inline-block;"></span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#10b981; letter-spacing:0.1em;">SYSTEMS ONLINE</span>
        </div>
    </div>
    <div style="padding: 0.8rem 1.2rem 0.3rem 1.2rem;">
        <div style="font-family:'JetBrains Mono',monospace; font-size:0.6rem; letter-spacing:0.15em; color:#1e1e3a; text-transform:uppercase; margin-bottom:0.5rem;">Detection Modules</div>
    </div>
    """, unsafe_allow_html=True)

    tool = st.radio(
        "",
        [
            "🚨  Scam Shield",
            "🧠  Manipulation Detector",
            "🔗  URL Threat Scanner",
            "🔐  Password Analyzer",
            "🔍  Hash Identifier",
            "💀  Encoding Detector",
        ],
        label_visibility="collapsed"
    )

    st.markdown("""
    <div style="position:fixed; bottom:1.2rem; left:0; width:240px; padding:0 1.2rem;">
        <div style="border-top:1px solid #12122a; padding-top:0.8rem;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.62rem; color:#1e1e3a; line-height:1.8;">
                v2.0.0 · Open Source<br>
                Built by <span style="color:#6C63FF;">Nico Graham</span><br>
                <a href="https://github.com/nicofoxheart/deciveil" style="color:#2a2a4a; text-decoration:none;">github.com/nicofoxheart</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def color_class(c):
    return {"red":"tv-red","orange":"tv-orange","yellow":"tv-yellow","green":"tv-green"}.get(c,"tv-green")

def card_class(c):
    return {"red":"card-red","orange":"card-orange","yellow":"card-yellow","green":"card-green"}.get(c,"card-green")

def fill_class(c):
    return {"red":"score-fill-red","orange":"score-fill-orange","yellow":"score-fill-yellow","green":"score-fill-green"}.get(c,"score-fill-green")

def result_header(risk, score, color):
    return f"""
    <div class="result-card {card_class(color)}">
        <div class="threat-label">// THREAT ASSESSMENT</div>
        <div class="threat-value {color_class(color)}">{risk}</div>
        <div class="score-wrap">
            <div class="score-meta"><span>RISK SCORE</span><span>{score}/100</span></div>
            <div class="score-track"><div class="{fill_class(color)}" style="width:{score}%"></div></div>
        </div>
    """


if "Scam Shield" in tool:
    st.markdown('<div class="tool-title">🚨 Scam Shield</div>', unsafe_allow_html=True)
    st.markdown('<div class="tool-subtitle">Paste any suspicious message — SMS, email, DM, notification. Detects phishing, fraud, and social engineering patterns.</div>', unsafe_allow_html=True)
    text = st.text_area("", height=160, placeholder="Paste message here...", key="scam_input")
    if st.button("RUN ANALYSIS", key="scam_btn"):
        if text.strip():
            with st.spinner("Scanning..."):
                r = analyze_scam(text)
            chips = "".join([f'<span class="chip chip-red">{k}</span>' for k in r["matched_keywords"]])
            chips_html = f'<div class="chip-row">{chips}</div>' if chips else '<div style="font-family:JetBrains Mono,monospace;font-size:0.78rem;color:#10b981;margin-top:0.8rem;">✓ No scam keywords detected</div>'
            advice_map = {"red":"Do not engage. Block sender and report immediately.","orange":"Verify through official channels only. Do not click any links.","yellow":"Proceed cautiously. Confirm legitimacy before responding.","green":"No significant threats found. Stay vigilant."}
            st.markdown(f'{result_header(r["risk_level"],r["score"],r["color"])}<div class="advice-text">→ {advice_map.get(r["color"],"")}</div>{chips_html}</div>', unsafe_allow_html=True)
        else:
            st.warning("Paste a message to analyze.")

elif "Manipulation" in tool:
    st.markdown('<div class="tool-title">🧠 Manipulation Detector</div>', unsafe_allow_html=True)
    st.markdown('<div class="tool-subtitle">Detects gaslighting, guilt-tripping, emotional coercion, pressure tactics, and false urgency in any message.</div>', unsafe_allow_html=True)
    text = st.text_area("", height=160, placeholder="Paste message here...", key="lie_input")
    if st.button("RUN ANALYSIS", key="lie_btn"):
        if text.strip():
            with st.spinner("Analyzing..."):
                r = analyze_manipulation(text)
            patterns = r["detected_patterns"]
            chips = "".join([f'<span class="chip chip-purple">{p.replace("_"," ").title()}</span>' for p in patterns])
            chips_html = f'<div class="chip-row">{chips}</div>' if chips else '<div style="font-family:JetBrains Mono,monospace;font-size:0.78rem;color:#10b981;margin-top:0.8rem;">✓ No manipulation patterns detected</div>'
            details = ""
            for p, matches in patterns.items():
                label = p.replace("_", " ").title()
                examples = " · ".join([f'"{m}"' for m in matches[:2]])
                details += f'<div class="finding-item"><span style="color:#6C63FF;">[{label}]</span> {examples}</div>'
            findings_block = f'<div class="findings">{details}</div>' if details else ""
            st.markdown(f'{result_header(r["risk_level"],r["score"],r["color"])}<div class="advice-text">→ {r["advice"]}</div>{chips_html}{findings_block}</div>', unsafe_allow_html=True)
        else:
            st.warning("Paste a message to analyze.")

elif "URL" in tool:
    st.markdown('<div class="tool-title">🔗 URL Threat Scanner</div>', unsafe_allow_html=True)
    st.markdown('<div class="tool-subtitle">Analyzes any URL for phishing patterns, malicious TLDs, brand impersonation, redirect chains, and evasion techniques.</div>', unsafe_allow_html=True)
    url_input = st.text_input("", placeholder="https://example.com", key="url_input")
    if st.button("SCAN URL", key="url_btn"):
        if url_input.strip():
            with st.spinner("Scanning..."):
                r = analyze_url(url_input)
            findings_html = "".join([f'<div class="finding-item {"finding-red" if any(w in f for w in ["major","impersonation","IP address","@ symbol"]) else "finding-yellow" if any(w in f for w in ["Suspicious","Excessive","Multiple","encoded","long","Phishing","No HTTPS","shortener","Nested","dashes","keywords"]) else "finding-green"}">> {f}</div>' for f in r["findings"]])
            proto_color = "chip-green" if r["protocol"] == "HTTPS" else "chip-red"
            st.markdown(f'{result_header(r["risk_level"],r["score"],r["color"])}<div class="meta-row"><div class="meta-item"><div class="meta-key">Domain</div><div class="meta-val">{r["domain"][:40]}</div></div><div class="meta-item"><div class="meta-key">Protocol</div><div class="meta-val"><span class="chip {proto_color}">{r["protocol"]}</span></div></div></div><div class="advice-text">→ {r["advice"]}</div><div class="findings">{findings_html}</div></div>', unsafe_allow_html=True)
        else:
            st.warning("Enter a URL to scan.")

elif "Password" in tool:
    st.markdown('<div class="tool-title">🔐 Password Strength Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="tool-subtitle">Calculates entropy, estimates GPU crack time, and detects common patterns, keyboard walks, and character weaknesses.</div>', unsafe_allow_html=True)
    pw = st.text_input("", placeholder="Enter any password to analyze", key="pw_input", type="password")
    if st.button("ANALYZE PASSWORD", key="pw_btn"):
        if pw.strip():
            with st.spinner("Calculating..."):
                r = analyze_password(pw)
            findings_html = "".join([f'<div class="finding-item {"finding-red" if fc=="red" else "finding-yellow" if fc=="yellow" else "finding-green"}">> {ft}</div>' for fc, ft in r["findings"]])
            char_html = "".join([f'<div class="char-box {"char-on" if ok else "char-off"}">{"✓" if ok else "✗"} {label}</div>' for ok, label in [(r["has_lower"],"a-z"),(r["has_upper"],"A-Z"),(r["has_digit"],"0-9"),(r["has_special"],"!@#$")]])
            suggestions = "".join([f'<span class="chip chip-yellow">{s}</span>' for s in r["suggestions"]])
            st.markdown(f'{result_header(r["strength"],r["score"],r["color"])}<div class="meta-row"><div class="meta-item"><div class="meta-key">Entropy</div><div class="meta-val">{r["entropy"]} bits</div></div><div class="meta-item"><div class="meta-key">Crack Time (GPU)</div><div class="meta-val">{r["crack_time"]}</div></div><div class="meta-item"><div class="meta-key">Length</div><div class="meta-val">{r["length"]} chars</div></div></div><div class="char-grid">{char_html}</div><div class="findings">{findings_html}</div>{"<div class=chip-row style=margin-top:0.8rem>" + suggestions + "</div>" if suggestions else ""}<div class="advice-text">→ Use a passphrase or password manager to generate strong, unique passwords.</div></div>', unsafe_allow_html=True)
        else:
            st.warning("Enter a password to analyze.")

elif "Hash" in tool:
    st.markdown('<div class="tool-title">🔍 Hash Identifier</div>', unsafe_allow_html=True)
    st.markdown('<div class="tool-subtitle">Identifies cryptographic hash types (MD5, SHA-1, SHA-256, bcrypt, Argon2, and more) with security ratings and recommendations.</div>', unsafe_allow_html=True)
    hash_input = st.text_input("", placeholder="Paste a hash string...", key="hash_input")
    if st.button("IDENTIFY HASH", key="hash_btn"):
        if hash_input.strip():
            with st.spinner("Identifying..."):
                r = identify_hash(hash_input)
            if not r["identified"]:
                st.markdown(f'<div class="result-card card-orange"><div class="threat-label">// HASH IDENTIFICATION</div><div class="threat-value tv-orange">UNKNOWN HASH FORMAT</div><div class="advice-text">→ {r["advice"]}<br>Input length: {r["input_length"]} characters</div></div>', unsafe_allow_html=True)
            else:
                sc = r.get("security_colors", {})
                hs_map = {"red":"hs-red","orange":"hs-orange","yellow":"hs-yellow","green":"hs-green"}
                matches_html = "".join([f'<div class="hash-match"><div class="hash-name">{m["name"]}</div><span class="hash-security {hs_map.get(sc.get(m["security"],"green"),"hs-green")}">{m["security"]}</span><div style="margin-top:0.3rem;"><span class="chip chip-cyan" style="margin-right:0.3rem;">{str(m["bits"])+"-bit" if m["bits"] else "adaptive"}</span><span class="chip {"chip-red" if m["crackable"] else "chip-green"}">{"CRACKABLE" if m["crackable"] else "COLLISION-RESISTANT"}</span></div><div class="hash-note" style="margin-top:0.5rem;">{m["note"]}</div></div>' for m in r["matches"]])
                b64_html = f'<div class="enc-block" style="margin-top:0.8rem;"><div class="enc-type">Also matches: Base64</div><div class="enc-decoded">{r["decoded_preview"][:80]}</div><div class="enc-note">Decoded preview shown above</div></div>' if r["is_base64"] and r["decoded_preview"] else ""
                st.markdown(f'<div class="result-card"><div class="threat-label">// HASH IDENTIFICATION — {len(r["matches"])} MATCH{"ES" if len(r["matches"])>1 else ""}</div><div style="font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#2a2a4a;word-break:break-all;margin-bottom:1rem;">{r["input_preview"]}</div>{matches_html}{b64_html}<div class="advice-text">→ {r["advice"]}</div></div>', unsafe_allow_html=True)
        else:
            st.warning("Paste a hash string to identify.")

elif "Encoding" in tool:
    st.markdown('<div class="tool-title">💀 Encoding Detector</div>', unsafe_allow_html=True)
    st.markdown('<div class="tool-subtitle">Detects and decodes obfuscated content: Base64, hexadecimal, URL encoding, ROT13, and binary — exposing hidden payloads.</div>', unsafe_allow_html=True)
    enc_text = st.text_area("", height=160, placeholder="Paste any text to scan for hidden encoding...", key="enc_input")
    if st.button("SCAN FOR ENCODING", key="enc_btn"):
        if enc_text.strip():
            with st.spinner("Decoding..."):
                r = analyze_encoding(enc_text)
            enc_blocks = "".join([f'<div class="enc-block {"enc-block-red" if d["color"]=="red" else ""}"><div class="enc-type" style="color:{"#ef4444" if d["color"]=="red" else "#f59e0b"};">{d["type"]} · {d["severity"]}</div><div class="enc-original">INPUT: {d["original"]}</div><div class="enc-decoded">DECODED: {d["decoded"]}</div><div class="enc-note">{d["note"]}</div></div>' for d in r["detections"]]) or '<div style="font-family:JetBrains Mono,monospace;font-size:0.78rem;color:#10b981;margin-top:0.8rem;">✓ No encoding obfuscation detected</div>'
            st.markdown(f'{result_header(r["risk_level"],r["score"],r["color"])}<div class="meta-row"><div class="meta-item"><div class="meta-key">Detections</div><div class="meta-val">{r["detection_count"]}</div></div></div><div class="advice-text">→ {r["advice"]}</div>{enc_blocks}</div>', unsafe_allow_html=True)
        else:
            st.warning("Paste text to scan.")
