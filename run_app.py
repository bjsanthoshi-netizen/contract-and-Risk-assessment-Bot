#!/usr/bin/env python
"""Wrapper to run Streamlit app with proper module paths."""
import subprocess
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
subprocess.run([sys.executable, "-m", "streamlit", "run", "genai_legal_assistant/genai_legal_assistant/app.py"], check=False)
