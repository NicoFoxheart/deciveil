"""
Deciveil — Password Strength Analyzer
Entropy calculation, pattern detection, crack time estimate.
"""

import re
import math

COMMON_PASSWORDS = [
    "password", "123456", "password123", "admin", "letmein", "qwerty",
    "abc123", "monkey", "1234567890", "iloveyou", "princess", "welcome",
    "shadow", "sunshine", "master", "dragon", "baseball", "football",
    "superman", "batman", "trustno1", "hello", "charlie", "password1",
    "12345678", "passw0rd", "p@ssword", "p@ssw0rd", "qwerty123", "admin123"
]

KEYBOARD_WALKS = [
    "qwerty", "qwertyu", "asdfgh", "zxcvbn", "12345", "123456",
    "1234567", "12345678", "abcdef", "abcdefg"
]


def calculate_entropy(password: str) -> float:
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[0-9]', password): charset += 10
    if re.search(r'[^a-zA-Z0-9]', password): charset += 32
    if charset == 0:
        return 0.0
    return len(password) * math.log2(charset)


def crack_time(entropy: float) -> str:
    guesses = 2 ** entropy
    seconds = guesses / 10_000_000_000

    if seconds < 1:           return "Instantly"
    elif seconds < 60:        return f"{int(seconds)} seconds"
    elif seconds < 3600:      return f"{int(seconds/60)} minutes"
    elif seconds < 86400:     return f"{int(seconds/3600)} hours"
    elif seconds < 31536000:  return f"{int(seconds/86400)} days"
    elif seconds < 3.15e10:   return f"{int(seconds/31536000)} years"
    elif seconds < 3.15e13:   return f"{int(seconds/3.15e10)} thousand years"
    else:                     return "Millions+ years"


def analyze_password(password: str) -> dict:
    findings = []
    suggestions = []
    score = 0

    length = len(password)
    if length < 8:
        findings.append(("red", "Too short — minimum 8 characters required"))
    elif length < 12:
        findings.append(("yellow", f"Acceptable length ({length} chars) — 12+ recommended"))
        score += 10
        suggestions.append("Use 12+ characters")
    elif length < 16:
        findings.append(("green", f"Good length ({length} characters)"))
        score += 20
    else:
        findings.append(("green", f"Excellent length ({length} characters)"))
        score += 30

    has_lower   = bool(re.search(r'[a-z]', password))
    has_upper   = bool(re.search(r'[A-Z]', password))
    has_digit   = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[^a-zA-Z0-9]', password))

    if has_lower:   score += 5
    else:           suggestions.append("Add lowercase letters (a-z)")
    if has_upper:   score += 10
    else:           suggestions.append("Add uppercase letters (A-Z)")
    if has_digit:   score += 10
    else:           suggestions.append("Add numbers (0-9)")
    if has_special: score += 20
    else:           suggestions.append("Add special characters (!@#$%^&*)")

    charset_count = sum([has_lower, has_upper, has_digit, has_special])
    if charset_count == 4:
        findings.append(("green", "All 4 character types used — excellent variety"))
    elif charset_count == 3:
        findings.append(("yellow", "3 of 4 character types — missing one"))
    else:
        findings.append(("red", f"Only {charset_count} character type(s) — very predictable"))

    if password.lower() in COMMON_PASSWORDS:
        findings.append(("red", "This is one of the world's most common passwords"))
        score = max(score - 60, 0)

    for walk in KEYBOARD_WALKS:
        if walk in password.lower():
            findings.append(("red", f"Keyboard pattern detected: '{walk}'"))
            score = max(score - 20, 0)
            suggestions.append("Avoid keyboard walks (qwerty, 12345)")
            break

    if re.search(r'(.)\1{2,}', password):
        findings.append(("yellow", "Repeated characters detected (aaa, 111)"))
        score = max(score - 10, 0)
        suggestions.append("Avoid repeating characters")

    if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
        findings.append(("yellow", "Sequential numbers detected"))
        score = max(score - 10, 0)

    entropy = calculate_entropy(password)
    crack = crack_time(entropy)
    score = min(score, 100)

    if score >= 70:
        strength = "STRONG"
        color = "green"
    elif score >= 45:
        strength = "MODERATE"
        color = "orange"
    elif score >= 20:
        strength = "WEAK"
        color = "yellow"
    else:
        strength = "CRITICAL"
        color = "red"

    return {
        "score": score,
        "strength": strength,
        "color": color,
        "entropy": round(entropy, 1),
        "crack_time": crack,
        "findings": findings,
        "suggestions": suggestions,
        "has_lower": has_lower,
        "has_upper": has_upper,
        "has_digit": has_digit,
        "has_special": has_special,
        "length": length,
    }
