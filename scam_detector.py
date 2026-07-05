"""
Deciveil — Scam Shield Module
Detects scam patterns in text messages using rule-based + keyword analysis.
"""

SCAM_KEYWORDS = [
    # Urgency & pressure
    "act now", "limited time", "expires today", "urgent", "immediately",
    "don't wait", "last chance", "final notice", "respond now",
    # Money & prizes
    "you've won", "you have been selected", "claim your prize",
    "free gift", "cash prize", "lottery", "inheritance", "million dollars",
    "wire transfer", "western union", "gift card", "bitcoin", "crypto payment",
    # Personal info requests
    "social security", "ssn", "bank account", "credit card number",
    "verify your account", "confirm your identity", "pin number",
    "password", "login credentials",
    # Threats & fear
    "arrest warrant", "irs", "legal action", "lawsuit", "deportation",
    "virus detected", "your computer", "hacked", "suspended account",
    # Too good to be true
    "work from home", "make money fast", "get rich", "no experience needed",
    "guaranteed income", "double your money", "risk free",
    # Fake authority
    "microsoft support", "apple support", "amazon", "government",
    "federal agent", "police", "customs officer",
]

RISK_WEIGHTS = {
    "critical": ["ssn", "social security", "bank account", "wire transfer",
                 "gift card", "bitcoin", "arrest warrant", "password"],
    "high": ["you've won", "claim your prize", "lottery", "inheritance",
             "verify your account", "virus detected"],
    "medium": ["urgent", "act now", "limited time", "free gift",
               "work from home", "guaranteed income"],
}


def analyze_scam(text: str) -> dict:
    """
    Analyzes text for scam indicators.
    Returns a dict with score, risk level, and matched keywords.
    """
    text_lower = text.lower()
    matched = []
    score = 0

    for keyword in SCAM_KEYWORDS:
        if keyword in text_lower:
            matched.append(keyword)

    # Weight the score
    for keyword in matched:
        if keyword in RISK_WEIGHTS["critical"]:
            score += 40
        elif keyword in RISK_WEIGHTS["high"]:
            score += 25
        elif keyword in RISK_WEIGHTS["medium"]:
            score += 15
        else:
            score += 8

    score = min(score, 100)

    if score >= 70:
        risk = "🔴 HIGH RISK — Likely Scam"
        color = "red"
    elif score >= 40:
        risk = "🟡 MEDIUM RISK — Suspicious"
        color = "orange"
    elif score >= 15:
        risk = "🟠 LOW RISK — Be Careful"
        color = "yellow"
    else:
        risk = "🟢 SAFE — No Scam Detected"
        color = "green"

    return {
        "score": score,
        "risk_level": risk,
        "color": color,
        "matched_keywords": matched,
        "keyword_count": len(matched),
    }
