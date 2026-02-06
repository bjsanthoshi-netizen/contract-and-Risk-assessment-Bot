import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import nlp, llm, utils, report

st.set_page_config(page_title="GenAI Legal Assistant (SME)")

st.title("GenAI Legal Assistant — SME Contract Analyzer")

# Sidebar settings: allow pasting API key so Streamlit process can use it
st.sidebar.header("Settings")
api_key_input = st.sidebar.text_input("OpenAI API Key (optional)", type="password")
if api_key_input:
    os.environ["OPENAI_API_KEY"] = api_key_input
    st.sidebar.success("API key set for this session")

uploaded = st.file_uploader("Upload contract (PDF / DOCX / TXT)", type=["pdf", "docx", "txt"])
templates = utils.read_templates(os.path.join(os.path.dirname(__file__), "templates.json"))

if uploaded:
    raw_text = ""
    fname = uploaded.name
    st.write(f"Uploaded: {fname}")
    ext = fname.split('.')[-1].lower()
    with open(os.path.join("temp_upload.txt"), "wb") as f:
        f.write(uploaded.getbuffer())
    path = os.path.abspath("temp_upload.txt")
    if ext == 'pdf':
        raw_text = nlp.extract_text_from_pdf(path)
    elif ext == 'docx':
        raw_text = nlp.extract_text_from_docx(path)
    else:
        raw_text = open(path, encoding='utf-8', errors='ignore').read()

    st.subheader("Contract summary (heuristic)")
    st.write(raw_text[:1000] + "...")

    if st.button("Run analysis"):
        with st.spinner("Analyzing..."):
            analysis = nlp.analyze_contract_text(raw_text, templates)
            # try LLM summary if available
            try:
                llm_summary = llm.summarize_contract(raw_text)
            except Exception as e:
                llm_summary = "[LLM summary unavailable] " + str(e)
            analysis['llm_summary'] = llm_summary
            utils.write_audit({"action": "analyze", "file": fname, "result_summary_len": len(analysis.get('summary',''))})

        st.success("Analysis complete")
        st.subheader("Composite Risk")
        st.write(analysis.get('composite_risk'))
        st.subheader("LLM Summary (if available)")
        st.write(analysis.get('llm_summary'))

        st.subheader("Entities Extracted")
        st.json(analysis.get('entities'))

        st.subheader("Clauses")
        for i, c in enumerate(analysis.get('clauses', []), start=1):
            cols = st.columns([6,1])
            with cols[0]:
                st.write(f"{i}. {c.get('text')[:400]}")
            with cols[1]:
                st.metric("Risk", c.get('risk'))
            if st.button(f"Explain clause {i}"):
                with st.spinner("Explaining with LLM..."):
                    try:
                        explanation = llm.explain_clause(c.get('text'))
                    except Exception as e:
                        explanation = "[LLM unavailable] " + str(e)
                    st.write(explanation)

        # Create filename without original extension
        fname_base = os.path.splitext(fname)[0]
        logs_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
        os.makedirs(logs_dir, exist_ok=True)
        out_pdf = os.path.join(logs_dir, f"report_{fname_base}.pdf")
        report.export_analysis_pdf(analysis, out_pdf)
        st.success("Exported report to logs folder")
        st.write(f"Report saved: {out_pdf}")
