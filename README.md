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
