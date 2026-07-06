"""
Deciveil — Hash Identifier
Identifies cryptographic hash types and security context.
"""

import re
import base64

HASH_PATTERNS = [
    {
        "name": "MD5",
        "regex": r"^[a-f0-9]{32}$",
        "bits": 128,
        "crackable": True,
        "security": "BROKEN",
        "note": "Deprecated — vulnerable to collision attacks. Never use for passwords."
    },
    {
        "name": "NTLM",
        "regex": r"^[a-f0-9]{32}$",
        "bits": 128,
        "crackable": True,
        "security": "BROKEN",
        "note": "Windows password hash — highly targeted by attackers. Use NTLMv2 or Kerberos."
    },
    {
        "name": "SHA-1",
        "regex": r"^[a-f0-9]{40}$",
        "bits": 160,
        "crackable": True,
        "security": "DEPRECATED",
        "note": "Deprecated by NIST. Collision attacks demonstrated by Google (SHAttered, 2017)."
    },
    {
        "name": "SHA-224",
        "regex": r"^[a-f0-9]{56}$",
        "bits": 224,
        "crackable": False,
        "security": "ACCEPTABLE",
        "note": "Truncated SHA-256. Rarely used. Consider SHA-256 instead."
    },
    {
        "name": "SHA-256",
        "regex": r"^[a-f0-9]{64}$",
        "bits": 256,
        "crackable": False,
        "security": "SECURE",
        "note": "Industry standard. Used in TLS, Bitcoin, code signing. Safe for most uses."
    },
    {
        "name": "SHA-384",
        "regex": r"^[a-f0-9]{96}$",
        "bits": 384,
        "crackable": False,
        "security": "VERY SECURE",
        "note": "Part of SHA-2 family. Used in TLS 1.3 certificates."
    },
    {
        "name": "SHA-512",
        "regex": r"^[a-f0-9]{128}$",
        "bits": 512,
        "crackable": False,
        "security": "VERY SECURE",
        "note": "Maximum SHA-2 strength. Overkill for most uses but extremely robust."
    },
    {
        "name": "bcrypt",
        "regex": r"^\$2[aby]\$\d{2}\$.{53}$",
        "bits": None,
        "crackable": False,
        "security": "GOLD STANDARD",
        "note": "Designed for passwords — deliberately slow. Recommended for auth systems."
    },
    {
        "name": "Argon2",
        "regex": r"^\$argon2",
        "bits": None,
        "crackable": False,
        "security": "GOLD STANDARD",
        "note": "Winner of Password Hashing Competition (2015). Best choice for new systems."
    },
    {
        "name": "MySQL v3.23",
        "regex": r"^[a-f0-9]{16}$",
        "bits": 64,
        "crackable": True,
        "security": "CRITICAL",
        "note": "Ancient algorithm — cracked instantly. Not a real cryptographic hash."
    },
    {
        "name": "CRC32",
        "regex": r"^[a-f0-9]{8}$",
        "bits": 32,
        "crackable": True,
        "security": "NOT CRYPTO",
        "note": "Error detection only — not a cryptographic hash. Never use for security."
    },
    {
        "name": "SHA3-256",
        "regex": r"^[a-f0-9]{64}$",
        "bits": 256,
        "crackable": False,
        "security": "SECURE",
        "note": "NIST-approved. Different design from SHA-2. Resistant to length-extension attacks."
    },
    {
        "name": "Whirlpool",
        "regex": r"^[a-f0-9]{128}$",
        "bits": 512,
        "crackable": False,
        "security": "SECURE",
        "note": "ISO/IEC 10118-3 standard. Strong but rarely implemented."
    },
]

SECURITY_COLORS = {
    "CRITICAL": "red",
    "BROKEN": "red",
    "DEPRECATED": "orange",
    "ACCEPTABLE": "yellow",
    "SECURE": "green",
    "VERY SECURE": "green",
    "GOLD STANDARD": "green",
    "NOT CRYPTO": "orange",
}


def identify_hash(text: str) -> dict:
    text = text.strip()
    matches = []

    for pattern in HASH_PATTERNS:
        if re.match(pattern["regex"], text, re.IGNORECASE):
            matches.append(pattern)

    is_base64 = False
    decoded_preview = None
    try:
        cleaned = text.rstrip('=')
        if re.match(r'^[A-Za-z0-9+/]+$', cleaned) and len(text) >= 16:
            padded = text + '=' * (4 - len(text) % 4) if len(text) % 4 else text
            decoded = base64.b64decode(padded).decode('utf-8', errors='replace')
            ratio = sum(1 for c in decoded if c.isprintable()) / max(len(decoded), 1)
            if ratio > 0.7:
                is_base64 = True
                decoded_preview = decoded[:80]
    except Exception:
        pass

    if not matches and not is_base64:
        return {
            "identified": False,
            "matches": [],
            "is_base64": False,
            "decoded_preview": None,
            "input_length": len(text),
            "input_preview": text[:48] + "..." if len(text) > 48 else text,
            "advice": "Could not identify this hash type. Check for spaces or extra characters.",
        }

    return {
        "identified": True,
        "matches": matches,
        "is_base64": is_base64,
        "decoded_preview": decoded_preview,
        "input_length": len(text),
        "input_preview": text[:48] + "..." if len(text) > 48 else text,
        "advice": "Never store MD5 or SHA-1 passwords in production. Use bcrypt or Argon2.",
        "security_colors": SECURITY_COLORS,
    }
