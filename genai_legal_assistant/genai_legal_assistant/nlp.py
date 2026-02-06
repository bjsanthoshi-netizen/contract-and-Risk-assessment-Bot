import re
from typing import List, Dict, Any
import spacy
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math

# Import llm with fallbacks so module works when run as script or package
try:
    from . import llm
except Exception:
    try:
        from genai_legal_assistant import llm
    except Exception:
        import llm

try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    nlp = None


def extract_text_from_docx(docx_path: str) -> str:
    from docx import Document
    doc = Document(docx_path)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text_from_pdf(pdf_path: str) -> str:
    import pdfplumber
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return "\n".join(text)


def simple_clause_split(text: str) -> List[str]:
    # Split on numbered clauses or double newlines
    clauses = re.split(r"(?m)^\s*\d+\.|\n\n+", text)
    clauses = [c.strip() for c in clauses if c and len(c.strip()) > 20]
    if not clauses:
        # fallback to sentence tokens
        clauses = sent_tokenize(text)[:200]
    return clauses


def contains_devanagari(text: str) -> bool:
    # Check for Devanagari Unicode block characters (Hindi script)
    return any('\u0900' <= ch <= '\u097F' for ch in text)


def normalize_text_for_nlp(text: str, use_llm_for_translation: bool = True) -> str:
    """If the text contains Hindi script, translate to English using the LLM (optional).

    Falls back to returning original text when no LLM key is present.
    """
    if contains_devanagari(text):
        if use_llm_for_translation:
            try:
                translated = llm.translate_hindi_to_english(text)
                # If LLM returns an error message, fallback
                if translated and not translated.startswith("[No API key") and not translated.startswith("[LLM Error"):
                    return translated
            except Exception:
                pass
    return text


def extract_entities(text: str) -> Dict[str, Any]:
    res = {"parties": [], "dates": [], "amounts": [], "jurisdiction": []}
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ("PERSON", "ORG"):
                res["parties"].append(ent.text)
            if ent.label_ in ("DATE",):
                res["dates"].append(ent.text)
            if ent.label_ in ("MONEY",):
                res["amounts"].append(ent.text)
            if ent.label_ in ("GPE", "LOC"):
                res["jurisdiction"].append(ent.text)
    # regex for amounts
    amounts = re.findall(r"\b(?:Rs\.?|INR|₹)\s?[\d,]+(?:\.\d+)?", text)
    for a in amounts:
        if a not in res["amounts"]:
            res["amounts"].append(a)
    return res


def detect_clause_types(clause: str) -> Dict[str, bool]:
    l = clause.lower()
    return {
        "penalty": bool(re.search(r"penalt|late fee|liquidated damages", l)),
        "indemnity": "indemn" in l,
        "unilateral_termination": bool(re.search(r"terminate.*without|terminate.*unilater|terminate.*solely", l)),
        "arbitration": "arbitration" in l or "jurisdiction" in l or "court" in l,
        "auto_renewal": "auto-renew" in l or "renew automatically" in l,
        "non_compete": "non-compete" in l or "restrict" in l and "competition" in l,
        "ip_transfer": "intellectual property" in l or "assign" in l or "ownership" in l,
    }


def obligation_vs_right_vs_prohibition(clause: str) -> str:
    l = clause.lower()
    if any(w in l for w in ["shall", "must", "oblig", "responsib"]):
        return "Obligation"
    if any(w in l for w in ["may", "can", "allowed"]):
        return "Right"
    if any(w in l for w in ["shall not", "must not", "prohibit", "prohibited"]):
        return "Prohibition"
    return "Neutral"


def clause_risk_score(clause: str) -> str:
    types = detect_clause_types(clause)
    score = 0
    if types.get("indemnity"):
        score += 2
    if types.get("unilateral_termination"):
        score += 2
    if types.get("auto_renewal"):
        score += 1
    if types.get("non_compete"):
        score += 2
    if types.get("penalty"):
        score += 1
    if score >= 4:
        return "High"
    if score >= 2:
        return "Medium"
    return "Low"


def similarity_to_templates(clauses: List[str], templates: List[str]) -> List[float]:
    corpus = templates + clauses
    tf = TfidfVectorizer().fit_transform(corpus)
    tmat = cosine_similarity(tf[len(templates):], tf[:len(templates)])
    # return max similarity per clause
    return [float(max(row)) if len(row) else 0.0 for row in tmat]


def analyze_contract_text(text: str, templates: List[str] = None, use_llm_for_translation: bool = True) -> Dict[str, Any]:
    # Normalize Hindi to English if needed before analysis
    norm_text = normalize_text_for_nlp(text, use_llm_for_translation=use_llm_for_translation)
    clauses = simple_clause_split(norm_text)
    entities = extract_entities(norm_text)
    clause_items = []
    similarities = []
    if templates:
        similarities = similarity_to_templates(clauses, templates)
    for i, c in enumerate(clauses):
        types = detect_clause_types(c)
        role = obligation_vs_right_vs_prohibition(c)
        risk = clause_risk_score(c)
        sim = similarities[i] if templates and i < len(similarities) else 0.0
        clause_items.append({
            "text": c,
            "types": types,
            "role": role,
            "risk": risk,
            "template_similarity": sim,
        })
    # contract-level composite risk (simple avg mapping)
    mapping = {"Low": 1, "Medium": 2, "High": 3}
    avg = 0
    if clause_items:
        avg = sum(mapping[it["risk"]] for it in clause_items) / len(clause_items)
    composite = "Low"
    if avg >= 2.5:
        composite = "High"
    elif avg >= 1.5:
        composite = "Medium"

    return {
        "entities": entities,
        "clauses": clause_items,
        "composite_risk": composite,
        "summary": (text[:1000] + "...") if len(text) > 1000 else text,
    }
