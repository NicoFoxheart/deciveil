"""
Deciveil — Lie & Manipulation Detector Module
Analyzes text for deceptive and manipulative language patterns.
"""

MANIPULATION_PATTERNS = {
    "gaslighting": [
        "you're crazy", "that never happened", "you're imagining",
        "you're being paranoid", "you're overreacting", "you're too sensitive",
        "i never said that", "you're making things up",
    ],
    "guilt_tripping": [
        "after everything i've done", "you don't care", "you never",
        "if you loved me", "you always", "nobody else would",
        "you're selfish", "you only think about yourself",
    ],
    "pressure_tactics": [
        "you have to", "you must", "you need to right now",
        "no other choice", "take it or leave it", "final offer",
        "this is your last chance", "everyone agrees",
    ],
    "false_urgency": [
        "right now", "immediately", "don't think about it",
        "no time to wait", "decide now", "before it's too late",
    ],
    "vague_claims": [
        "studies show", "everyone knows", "science says",
        "people are saying", "they say", "i heard that",
        "trust me", "believe me",
    ],
    "emotional_manipulation": [
        "you're breaking my heart", "i thought you were different",
        "you've changed", "i can't believe you", "you disappoint me",
        "how could you", "after all this time",
    ],
}


def analyze_manipulation(text: str) -> dict:
    text_lower = text.lower()
    detected_patterns = {}
    total_score = 0

    for pattern_type, phrases in MANIPULATION_PATTERNS.items():
        matches = [p for p in phrases if p in text_lower]
        if matches:
            detected_patterns[pattern_type] = matches
            total_score += len(matches) * 18

    total_score = min(total_score, 100)

    if total_score >= 65:
        risk = "🔴 HIGH — Strong Manipulation Detected"
        advice = "This message contains multiple manipulation tactics. Be very cautious."
        color = "red"
    elif total_score >= 35:
        risk = "🟡 MEDIUM — Possible Manipulation"
        advice = "Some manipulative language detected. Read carefully and trust your gut."
        color = "orange"
    elif total_score >= 10:
        risk = "🟠 LOW — Slightly Suspicious"
        advice = "A few concerning phrases found. Stay aware."
        color = "yellow"
    else:
        risk = "🟢 CLEAN — No Manipulation Detected"
        advice = "No manipulative patterns found in this message."
        color = "green"

    return {
        "score": total_score,
        "risk_level": risk,
        "color": color,
        "detected_patterns": detected_patterns,
        "pattern_count": len(detected_patterns),
        "advice": advice,
    }
