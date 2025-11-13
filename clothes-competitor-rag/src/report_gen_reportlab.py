from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import pandas as pd

def make_report(query, ai_answer, out_pdf="final_report.pdf"):
    doc = SimpleDocTemplate(out_pdf, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("Competitor Analysis Report", styles['Title']))
    story.append(Spacer(1, 12))

    # Query
    story.append(Paragraph("<b>Query:</b>", styles['Heading2']))
    story.append(Paragraph(query, styles['BodyText']))
    story.append(Spacer(1, 12))

    # AI answer
    story.append(Paragraph("<b>AI-Generated Summary:</b>", styles['Heading2']))
    for line in ai_answer.splitlines():
        story.append(Paragraph(line, styles['BodyText']))
    story.append(Spacer(1, 12))

    # Peak hours table
    try:
        peaks = pd.read_csv("data/store_peak_hours.csv").merge(pd.read_csv("data/stores.csv"), on="store_id")
        story.append(Paragraph("<b>Peak Hours Table:</b>", styles['Heading2']))
        # table header
        data = [list(peaks.columns)]
        # rows
        for _, row in peaks.iterrows():
            data.append([row[c] for c in peaks.columns])
        t = Table(data, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))
    except Exception as e:
        story.append(Paragraph(f"Could not load peak hours table: {e}", styles['BodyText']))
        story.append(Spacer(1, 12))

    # Screenshot placeholders
    story.append(Paragraph("<b>Visualizations / Screenshots:</b>", styles['Heading2']))
    # placeholders = [
    #     "Peak Hour Chart: [Insert screenshot here]",
    #     "Streamlit UI: [Insert screenshot here]",
    #     "RAG Pipeline / FAISS Index: [Insert screenshot here]"
    # ]
    # for p in placeholders:
    #     story.append(Paragraph(p, styles['BodyText']))
    #     story.append(Spacer(1, 8))

    # Conclusion
    story.append(Paragraph("<b>Conclusion</b>", styles['Heading2']))
    story.append(Paragraph("This report was generated locally with free tools. Replace placeholders with screenshots before submission.", styles['BodyText']))

    doc.build(story)
    print(f"Saved PDF: {out_pdf}")

# quick test
if __name__ == "__main__":
    make_report("Sample query", "This is a sample AI answer.\nLine2 of answer.")
