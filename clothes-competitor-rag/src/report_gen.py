# src/report_gen.py
import pandas as pd
import io
import tempfile
import os

try:
    from weasyprint import HTML
    WEASY_AVAILABLE = True
except Exception as e:
    WEASY_AVAILABLE = False
    WEASY_IMPORT_ERROR = e

def make_report(query, ai_answer, out_pdf="report.pdf"):
    md = f"# Competitor Report\n\n**Query:** {query}\n\n## AI Summary\n\n{ai_answer}\n"
    # if weasy is available, render PDF
    if WEASY_AVAILABLE:
        HTML(string=md).write_pdf(out_pdf)
        return out_pdf
    else:
        # fallback: save markdown or simple text file
        fallback_path = out_pdf.replace('.pdf', '.txt')
        with open(fallback_path, "w", encoding="utf8") as f:
            f.write(md)
            if 'WEASY_IMPORT_ERROR' in globals():
                f.write("\n\n[WeasyPrint was unavailable: " + repr(WEASY_IMPORT_ERROR) + "]")
        return fallback_path
