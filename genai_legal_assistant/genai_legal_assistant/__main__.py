"""Entry point for running the Streamlit app as a module."""
import subprocess
import sys
import os

# Get the directory of this package
pkg_dir = os.path.dirname(os.path.abspath(__file__))
app_file = os.path.join(pkg_dir, "app.py")

# Run streamlit with the app.py file
subprocess.run([sys.executable, "-m", "streamlit", "run", app_file], check=False)
