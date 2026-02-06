from fpdf import FPDF
from typing import Dict, Any


def export_analysis_pdf(analysis: Dict[str, Any], out_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(True, margin=12)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, "Contract Analysis Report", ln=True)
    pdf.ln(4)
    pdf.multi_cell(0, 6, f"Composite risk: {analysis.get('composite_risk')}")
    pdf.ln(2)
    ent = analysis.get('entities', {})
    pdf.multi_cell(0, 6, f"Parties: {', '.join(ent.get('parties', [])[:5])}")
    pdf.multi_cell(0, 6, f"Amounts: {', '.join(ent.get('amounts', [])[:5])}")
    pdf.ln(4)
    pdf.multi_cell(0, 6, "Clause-level details:")
    for i, c in enumerate(analysis.get('clauses', [])[:50], start=1):
        text = c.get('text', '')
        risk = c.get('risk')
        pdf.multi_cell(0, 6, f"{i}. Risk: {risk} | {text[:400]}")
        pdf.ln(1)
    pdf.output(out_path)
