"""
Deciveil — Deepfake Detector Module
Analyzes images for signs of AI manipulation using metadata + pixel analysis.
"""

from PIL import Image
import numpy as np


def analyze_image(image: Image.Image) -> dict:
    findings = []
    score = 0

    img_array = np.array(image.convert("RGB"))

    width, height = image.size
    if width == height and width in [256, 512, 1024]:
        findings.append("⚠️ Square dimensions common in AI-generated faces")
        score += 20

    r, g, b = img_array[:,:,0], img_array[:,:,1], img_array[:,:,2]
    r_std = float(np.std(r))
    g_std = float(np.std(g))
    b_std = float(np.std(b))

    channel_diff = abs(r_std - g_std) + abs(g_std - b_std)
    if channel_diff < 8:
        findings.append("⚠️ Unusually uniform color distribution detected")
        score += 25

    gray = np.array(image.convert("L"), dtype=float)
    noise = np.diff(gray, axis=0)
    noise_std = float(np.std(noise))

    if noise_std < 5:
        findings.append("⚠️ Very low noise — could indicate AI smoothing")
        score += 20
    elif noise_std > 60:
        findings.append("⚠️ Unusual noise pattern detected")
        score += 15

    exif_data = image._getexif() if hasattr(image, '_getexif') else None
    if exif_data is None:
        findings.append("⚠️ No camera metadata found — common in AI-generated images")
        score += 15

    ratio = width / height if height > 0 else 1
    if 0.95 <= ratio <= 1.05:
        findings.append("⚠️ Perfect square ratio common in face generators")
        score += 10

    score = min(score, 100)

    if not findings:
        findings.append("✅ No suspicious indicators found")

    if score >= 60:
        risk = "🔴 HIGH — Likely AI Generated / Deepfake"
        advice = "This image shows multiple signs of AI generation. Verify the source."
        color = "red"
    elif score >= 35:
        risk = "🟡 MEDIUM — Possibly Manipulated"
        advice = "Some suspicious indicators found. Use reverse image search to verify."
        color = "orange"
    elif score >= 15:
        risk = "🟠 LOW — Minor Flags"
        advice = "A few minor indicators. Likely real but worth double-checking."
        color = "yellow"
    else:
        risk = "🟢 LIKELY REAL — No Deepfake Detected"
        advice = "No significant deepfake indicators found."
        color = "green"

    return {
        "score": score,
        "risk_level": risk,
        "color": color,
        "findings": findings,
        "advice": advice,
        "image_size": f"{width} x {height}px",
    }
