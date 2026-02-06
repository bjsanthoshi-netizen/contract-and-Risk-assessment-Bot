# GenAI Legal Assistant (SME-focused)

This repository provides a local, privacy-first GenAI-powered legal assistant tailored for Indian SMEs. It analyzes contracts (PDF/DOCX/TXT), extracts clauses/entities, scores risks, explains clauses in plain language, suggests alternative clauses, supports English and Hindi (internal normalization via LLM), and exports reports.

Quick start

1. Create a virtual environment and install deps:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r genai_legal_assistant/requirements.txt
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt')"
```

2. Set an LLM provider key (optional but recommended for richer outputs):

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY = 'sk-...'
# or set environment variable in system settings
```

3. Run the Streamlit app:

```bash
streamlit run genai_legal_assistant/app.py
```

Notes
- The app supports offline heuristics when no LLM key is present.
- No external legal databases or APIs are used.
- Audit logs and exports are saved locally under `genai_legal_assistant/logs/`.

Files added
- `app.py` — Streamlit UI
- `nlp.py` — parsing, clause extraction, heuristics
- `llm.py` — wrapper for OpenAI/Anthropic (uses env keys)
- `utils.py` — logging and helpers
- `report.py` — PDF export helper

Replace or extend LLM wrappers in `llm.py` if using Claude/Anthropic.