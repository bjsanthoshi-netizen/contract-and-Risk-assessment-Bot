# How to Run GenAI Legal Assistant

This document provides step-by-step instructions to set up and run the GenAI Legal Assistant project.

## Project Overview

GenAI Legal Assistant is a local, privacy-first application that analyzes legal contracts using AI. It extracts clauses, identifies risks, explains contract terms, and generates PDF reports. Designed for Indian SMEs, it supports English and Hindi languages.

**Key Features:**
- Contract analysis (PDF, DOCX, TXT formats)
- Automatic clause extraction and entity recognition
- Risk scoring and composite risk analysis
- LLM-powered clause explanations and summaries
- PDF report generation
- Audit logging

---

## Prerequisites

- **Python 3.8+** installed on your system
- **Windows, macOS, or Linux** OS
- **4GB+ RAM** recommended
- (Optional) OpenAI API key for enhanced LLM features

---

## Setup Instructions

### Step 1: Navigate to the Project Directory

```powershell
cd C:\Users\welcome\Desktop\data_science
```

### Step 2: Create a Virtual Environment

```powershell
python -m venv venv
```

### Step 3: Activate the Virtual Environment

**On Windows (PowerShell):**

```powershell
venv\Scripts\Activate.ps1
```

**On Windows (Command Prompt):**

```cmd
venv\Scripts\activate.bat
```

**On macOS/Linux:**

```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```powershell
pip install -r genai_legal_assistant/requirements.txt
```

### Step 5: Download Required NLP Models

```powershell
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt')"
```

---

## Configure LLM Provider (Optional but Recommended)

### Option A: Set Environment Variable (Recommended)

**Windows PowerShell:**

```powershell
$env:OPENAI_API_KEY = 'sk-your-openai-api-key-here'
```

**Windows Command Prompt:**

```cmd
set OPENAI_API_KEY=sk-your-openai-api-key-here
```

**Permanently (Windows System Settings):**

1. Press `Win + X` and select "System"
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Click "New" under User variables
5. Variable name: `OPENAI_API_KEY`
6. Variable value: `sk-your-openai-api-key-here`
7. Click OK and restart PowerShell

### Option B: Set via Streamlit UI

You can also set the API key directly in the application once it's running using the Settings panel in the sidebar.

### Option C: Offline Mode (No API Key)

The application works offline with built-in heuristics if no API key is provided. LLM features will be unavailable, but basic analysis will still work.

---

## Running the Application

### Method 1: Using the Wrapper Script (Recommended)

```powershell
python run_app.py
```

This automatically handles module paths and launches the Streamlit application.

### Method 2: Direct Streamlit Command

```powershell
streamlit run genai_legal_assistant/genai_legal_assistant/app.py
```

### Method 3: Using Python Module

```powershell
python -m streamlit run genai_legal_assistant/genai_legal_assistant/app.py
```

---

## What To Expect

Once running, the application will:

1. **Start a local web server** (typically at `http://localhost:8501`)
2. **Launch your default browser** automatically
3. **Display the GenAI Legal Assistant interface** with:
   - Settings panel (top-left sidebar)
   - File upload area for contracts
   - Analysis buttons and results

---

## Using the Application

### Upload and Analyze a Contract

1. **Upload a file**: Click "Browse files" and select a contract (PDF, DOCX, or TXT)
2. **View preview**: The first 1000 characters of the contract appear
3. **Run analysis**: Click "Run analysis" button
4. **View results**:
   - **Composite Risk**: Overall risk score
   - **LLM Summary**: AI-generated contract summary
   - **Entities Extracted**: Key entities identified (parties, dates, amounts, etc.)
   - **Clauses**: Extracted clauses with risk scores
   - **Clause Explanations**: Click "Explain clause X" for detailed explanations

### Sample Contracts

Sample contracts are included in the project for testing:

```
genai_legal_assistant/sample_contracts/
├── employment_contract.txt
├── lease_agreement.txt
└── vendor_service_contract.txt
```

---

## Project Structure

```
genai_legal_assistant/
├── README.md                          # Project overview
├── requirements.txt                   # Python dependencies
│
├── genai_legal_assistant/
│   ├── __init__.py
│   ├── __main__.py
│   ├── app.py                         # Main Streamlit application
│   ├── llm.py                         # LLM integration (OpenAI/Anthropic)
│   ├── nlp.py                         # Text parsing & clause extraction
│   ├── report.py                      # PDF report generation
│   ├── utils.py                       # Logging & utility functions
│   ├── templates.json                 # Clause templates for matching
│   └── __pycache__/
│
├── logs/                              # Audit logs (created automatically)
│   └── audit_2026-02-06.jsonl
│
└── sample_contracts/                  # Example contracts for testing
    ├── employment_contract.txt
    ├── lease_agreement.txt
    └── vendor_service_contract.txt
```

---

## Troubleshooting

### Issue: Module Import Errors

**Error:** `ModuleNotFoundError: No module named 'streamlit'`

**Solution:**
```powershell
pip install -r genai_legal_assistant/requirements.txt
```

### Issue: Spacy Model Not Found

**Error:** `OSError: [E050] Can't find model 'en_core_web_sm'`

**Solution:**
```powershell
python -m spacy download en_core_web_sm
```

### Issue: NLTK Data Missing

**Error:** `Resource punkt not found`

**Solution:**
```powershell
python -c "import nltk; nltk.download('punkt')"
```

### Issue: Streamlit Port Already in Use

**Error:** `Port 8501 is already in use`

**Solution:** Use a different port:
```powershell
streamlit run genai_legal_assistant/genai_legal_assistant/app.py --server.port 8502
```

### Issue: API Key Not Recognized

**Symptom:** LLM features unavailable even after setting key

**Solutions:**
1. Verify the key is correct and valid
2. For Windows PowerShell, set the variable from PowerShell terminal (not Command Prompt)
3. Use the Settings panel in the Streamlit UI to set the key for the session
4. Ensure you've activated the virtual environment

### Issue: Protocol Error When Running Streamlit

**Error:** `Address already in use` or connection refused

**Solution:**
```powershell
# Close any existing Streamlit processes and try again
Get-Process streamlit | Stop-Process -Force
python run_app.py
```

---

## Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `OPENAI_API_KEY` | OpenAI API authentication | `sk-...` |
| `ANTHROPIC_API_KEY` | Anthropic API authentication (if using Claude) | `sk-ant-...` |

---

## Logs and Outputs

- **Audit logs**: Saved in `genai_legal_assistant/logs/audit_YYYY-MM-DD.jsonl`
- **Temporary files**: `temp_upload.txt` (cleaned up per session)
- **PDF reports**: Generated and available for download in the UI

---

## Stopping the Application

To stop the Streamlit server:

1. **In the terminal**: Press `Ctrl + C`
2. **Deactivate virtual environment** (optional):
   ```powershell
   deactivate
   ```

---

## Performance Tips

- **First run**: Initial setup with model downloads takes 2-3 minutes
- **Contract size**: Works best with contracts under 50 pages
- **LLM API calls**: Slower with free OpenAI tier; consider rate limits
- **Offline mode**: 10-100x faster than LLM mode for basic analysis

---

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [spaCy Documentation](https://spacy.io/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [NLTK Documentation](https://www.nltk.org/)

---

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review audit logs in `genai_legal_assistant/logs/`
3. Verify all dependencies are installed: `pip list`
4. Test with sample contracts first
