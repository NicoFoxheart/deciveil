"""
Deciveil — URL Threat Scanner
Analyzes URLs for phishing, malicious patterns, and suspicious indicators.
"""

import re
from urllib.parse import urlparse

SUSPICIOUS_TLDS = [
    '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.click',
    '.download', '.stream', '.loan', '.win', '.racing', '.accountant',
    '.science', '.date', '.faith', '.review', '.trade', '.webcam', '.zip'
]

SHORTENERS = [
    'bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd',
    'buff.ly', 'adf.ly', 'j.mp', 'short.io', 'rb.gy', 'tiny.cc', 'cutt.ly'
]

PHISHING_KEYWORDS = [
    'login', 'signin', 'verify', 'verification', 'secure', 'security',
    'update', 'confirm', 'account', 'password', 'credential', 'banking',
    'paypal', 'apple', 'microsoft', 'google', 'amazon', 'netflix',
    'support', 'alert', 'suspended', 'unusual', 'activity', 'validate', 'recover'
]

BRANDS = ['paypal', 'apple', 'microsoft', 'google', 'amazon', 'netflix',
          'facebook', 'instagram', 'twitter', 'chase', 'wellsfargo', 'citibank']


def analyze_url(url: str) -> dict:
    findings = []
    score = 0

    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
    except Exception:
        return {
            "score": 0, "risk_level": "INVALID URL", "color": "gray",
            "findings": ["Could not parse URL — check format."],
            "advice": "Enter a valid URL.", "domain": "unknown", "protocol": "unknown"
        }

    if url.startswith('http://'):
        findings.append("No HTTPS — connection is unencrypted")
        score += 20

    if re.match(r'\d+\.\d+\.\d+\.\d+', domain):
        findings.append("IP address used as domain — major red flag")
        score += 40

    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            findings.append(f"Suspicious TLD: {tld} — common in phishing campaigns")
            score += 25
            break

    for s in SHORTENERS:
        if s in domain:
            findings.append(f"URL shortener ({s}) — hides real destination")
            score += 20
            break

    for brand in BRANDS:
        if brand in domain and not any(domain == f"{brand}.com" or domain.endswith(f".{brand}.com") for _ in [1]):
            findings.append(f"Brand impersonation attempt: '{brand}' in suspicious domain")
            score += 35
            break

    kw_hits = [kw for kw in PHISHING_KEYWORDS if kw in path or kw in domain]
    if kw_hits:
        findings.append(f"Phishing keywords in URL: {', '.join(kw_hits[:4])}")
        score += min(len(kw_hits) * 8, 25)

    subs = len(domain.split('.')) - 2
    if subs >= 3:
        findings.append(f"Excessive subdomains ({subs}) — unusual for legitimate sites")
        score += 15

    if '@' in url:
        findings.append("@ symbol in URL — browser ignores everything before @")
        score += 40

    if len(url) > 200:
        findings.append(f"Extremely long URL ({len(url)} chars) — used to obscure destination")
        score += 15

    if url.count('http') > 1:
        findings.append("Nested URLs detected — possible redirect chain attack")
        score += 20

    if '%' in url:
        findings.append("URL-encoded characters — may hide malicious content")
        score += 10

    if domain.count('-') >= 3:
        findings.append(f"Multiple dashes in domain ({domain.count('-')}) — common phishing pattern")
        score += 15

    score = min(score, 100)
    if not findings:
        findings.append("No suspicious indicators detected")

    if score >= 65:
        risk = "HIGH RISK — Likely Phishing / Malicious"
        advice = "Do NOT visit this URL. Block and report immediately."
        color = "red"
    elif score >= 35:
        risk = "MEDIUM RISK — Suspicious URL"
        advice = "Proceed with extreme caution. Verify through official channels only."
        color = "orange"
    elif score >= 15:
        risk = "LOW RISK — Minor Flags"
        advice = "Some indicators found. Double-check before visiting."
        color = "yellow"
    else:
        risk = "LIKELY SAFE — No Threats Detected"
        advice = "No significant threats found in this URL."
        color = "green"

    return {
        "score": score,
        "risk_level": risk,
        "color": color,
        "findings": findings,
        "advice": advice,
        "domain": parsed.netloc or url,
        "protocol": "HTTPS" if url.startswith('https') else "HTTP",
    }
