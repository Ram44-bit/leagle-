from pathlib import Path
import re

def summarize_text(text: str) -> dict:
    """A safe, local fallback summary. It does not provide legal advice."""
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return {"summary": "No text was provided to summarize.", "key_points": [], "notice": "Organizational aid only; verify all details."}
    sentences = re.split(r"(?<=[.!?])\s+", cleaned)
    summary = " ".join(sentences[:3])[:1200]
    points = [s.strip() for s in sentences if len(s.strip()) > 25][:5]
    return {
        "summary": summary,
        "key_points": points,
        "notice": "AI-style local summary only; not legal advice. Verify facts, dates, and citations against the original."
    }

def extract_text_from_file(path: Path, suffix: str) -> str:
    if suffix.lower() == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore")
    return ""
