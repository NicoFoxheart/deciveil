"""
Deciveil — Encoding Detector
Detects hidden/obfuscated content: Base64, Hex, URL encoding, ROT13, Binary.
"""

import re
import base64
import urllib.parse
import binascii


def decode_rot13(text: str) -> str:
    result = []
    for c in text:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)


def analyze_encoding(text: str) -> dict:
    text = text.strip()
    detections = []

    for match in re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', text):
        try:
            pad = match + '=' * (-len(match) % 4)
            decoded = base64.b64decode(pad).decode('utf-8', errors='replace')
            ratio = sum(1 for c in decoded if c.isprintable()) / max(len(decoded), 1)
            if ratio > 0.75 and len(decoded) > 8:
                detections.append({
                    "type": "Base64",
                    "severity": "MEDIUM",
                    "original": match[:50] + "..." if len(match) > 50 else match,
                    "decoded": decoded[:120],
                    "note": "Encoded content hidden in plain sight — common in phishing payloads",
                    "color": "orange"
                })
        except Exception:
            pass

    if '%' in text and re.search(r'%[0-9a-fA-F]{2}', text):
        try:
            decoded_url = urllib.parse.unquote(text)
            if decoded_url != text:
                detections.append({
                    "type": "URL Encoding",
                    "severity": "MEDIUM",
                    "original": text[:60] + "..." if len(text) > 60 else text,
                    "decoded": decoded_url[:120],
                    "note": "URL-encoded characters used — often to bypass filters",
                    "color": "orange"
                })
        except Exception:
            pass

    for match in re.findall(r'\b[0-9a-fA-F]{8,}\b', text):
        if len(match) % 2 == 0:
            try:
                decoded_hex = binascii.unhexlify(match).decode('utf-8', errors='replace')
                ratio = sum(1 for c in decoded_hex if c.isprintable()) / max(len(decoded_hex), 1)
                if ratio > 0.8 and len(decoded_hex) > 3:
                    detections.append({
                        "type": "Hex Encoding",
                        "severity": "MEDIUM",
                        "original": match,
                        "decoded": decoded_hex[:120],
                        "note": "Hexadecimal encoding — frequently used to hide payloads in malware",
                        "color": "orange"
                    })
            except Exception:
                pass

    words = text.split()
    if 4 <= len(words) <= 100:
        rot13 = decode_rot13(text)
        common = ['the', 'and', 'for', 'you', 'are', 'this', 'that', 'with',
                  'have', 'from', 'they', 'your', 'click', 'link', 'send',
                  'money', 'free', 'win', 'urgent', 'account', 'bank']
        rot_score = sum(1 for w in common if w in rot13.lower())
        orig_score = sum(1 for w in common if w in text.lower())
        if rot_score > orig_score + 2:
            detections.append({
                "type": "ROT13",
                "severity": "HIGH",
                "original": text[:60] + "..." if len(text) > 60 else text,
                "decoded": rot13[:120],
                "note": "ROT13 obfuscation — classic technique to evade content filters",
                "color": "red"
            })

    for match in re.findall(r'\b[01]{8,}\b', text):
        if len(match) % 8 == 0:
            try:
                chars = [chr(int(match[i:i+8], 2)) for i in range(0, len(match), 8)]
                decoded_bin = ''.join(chars)
                if all(c.isprintable() for c in decoded_bin) and len(decoded_bin) > 2:
                    detections.append({
                        "type": "Binary",
                        "severity": "MEDIUM",
                        "original": match[:40] + "..." if len(match) > 40 else match,
                        "decoded": decoded_bin[:120],
                        "note": "Binary-encoded message — uncommon but used in obfuscation",
                        "color": "orange"
                    })
            except Exception:
                pass

    score = min(len(detections) * 30, 100)

    if score >= 60:
        risk = "HIGH — Multiple Encoding Layers"
        color = "red"
        advice = "Serious red flag. Multi-layered encoding is a classic malware evasion technique."
    elif score >= 30:
        risk = "MEDIUM — Encoded Content Detected"
        color = "orange"
        advice = "Encoded data found. Review decoded output — it may contain hidden instructions."
    elif score > 0:
        risk = "LOW — Minor Encoding Found"
        color = "yellow"
        advice = "Some encoded content detected. May be benign but worth reviewing."
    else:
        risk = "CLEAN — No Encoding Detected"
        color = "green"
        advice = "No encoding obfuscation found in this message."

    return {
        "score": score,
        "risk_level": risk,
        "color": color,
        "detections": detections,
        "detection_count": len(detections),
        "advice": advice,
    }
