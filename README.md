How to Run GenAI Legal Assistant
This document provides step-by-step instructions to set up and run the GenAI Legal Assistant project.

Project Overview
GenAI Legal Assistant is a local, privacy-first application that analyzes legal contracts using AI. It extracts clauses, identifies risks, explains contract terms, and generates PDF reports. Designed for Indian SMEs, it supports English and Hindi languages.

Key Features:

Contract analysis (PDF, DOCX, TXT formats)
Automatic clause extraction and entity recognition
Risk scoring and composite risk analysis
LLM-powered clause explanations and summaries
PDF report generation
Audit logging
Prerequisites
Python 3.8+ installed on your system
Windows, macOS, or Linux OS
4GB+ RAM recommended
(Optional) OpenAI API key for enhanced LLM features
Setup Instructions
Step 1: Navigate to the Project Directory
cd C:\Users\welcome\Desktop\data_science
Step 2: Create a Virtual Environment
python -m venv venv
Step 3: Activate the Virtual Environment
On Windows (PowerShell):

venv\Scripts\Activate.ps1
On Windows (Command Prompt):

venv\Scripts\activate.bat
On macOS/Linux:

source venv/bin/activate
Step 4: Install Dependencies
pip install -r genai_legal_assistant/requirements.txt
Step 5: Download Required NLP Models
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt')"
Configure LLM Provider (Optional but Recommended)
Option A: Set Environment Variable (Recommended)
Windows PowerShell:

$env:OPENAI_API_KEY = 'sk-your-openai-api-key-here'
Windows Command Prompt:

set OPENAI_API_KEY=sk-your-openai-api-key-here
Permanently (Windows System Settings):

Press Win + X and select "System"
Click "Advanced system settings"
Click "Environment Variables"
Click "New" under User variables
Variable name: OPENAI_API_KEY
Variable value: sk-your-openai-api-key-here
Click OK and restart PowerShell
Option B: Set via Streamlit UI
You can also set the API key directly in the application once it's running using the Settings panel in the sidebar.

Option C: Offline Mode (No API Key)
The application works offline with built-in heuristics if no API key is provided. LLM features will be unavailable, but basic analysis will still work.

Running the Application
Method 1: Using the Wrapper Script (Recommended)
python run_app.py
This automatically handles module paths and launches the Streamlit application.

Method 2: Direct Streamlit Command
streamlit run genai_legal_assistant/genai_legal_assistant/app.py
Method 3: Using Python Module
python -m streamlit run genai_legal_assistant/genai_legal_assistant/app.py
