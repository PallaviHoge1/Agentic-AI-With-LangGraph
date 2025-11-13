import streamlit as st
import pandas as pd
import altair as alt
import os, sys
# ensure src package importable
sys.path.append(os.path.abspath("src"))

from rag_query import answer, retrieve  # uses functions from src/rag_query.py

from report_gen_reportlab import make_report

query = st.text_input("Ask about competitors or busiest times", value="List competitors and their busiest hours, suggest 3 actions", key="main_query_input")

# try:
#     from report_gen import make_report
# except Exception as e:
#     make_report = None
#     st.warning(f"Report generation disabled: {e}")

# # later
# if make_report:
#     make_report(query, answer)
# else:
#     st.info("Report generation is currently disabled (missing native libs).")

st.set_page_config(page_title="Clothing Competitor Assistant", layout="wide")

st.title("Clothing Competitor Assistant (Local RAG) — Koramangala Demo")

st.markdown(
    "Ask questions about competitors, busiest hours, and get a short report. "
    "If the model seems slow or errors, check the logs printed below."
)

# Sidebar config
with st.sidebar:
    st.header("Options")
    model_info = st.text_input("Model id (as shown by `ollama list`)", value="llama3.2b")
    top_k = st.slider("Top-k retrieved docs", min_value=1, max_value=8, value=4)
    gen_report = st.checkbox("Enable PDF report generation", value=True)

query = st.text_input("Ask about competitors or busiest times", value="List competitors and their busiest hours, suggest 3 actions")

if st.button("Run RAG"):
    if not query.strip():
        st.error("Please type a query.")
    else:
        with st.spinner("Retrieving relevant docs..."):
            try:
                # show retrieved docs first
                docs = retrieve(query, k=top_k)
            except Exception as e:
                st.error(f"Retrieval failed: {e}")
                docs = []

        st.subheader("Retrieved context (top documents)")
        if docs:
            for i, d in enumerate(docs, start=1):
                st.markdown(f"**Doc {i}:**")
                st.code(d, language="text")
        else:
            st.info("No docs retrieved. Check embeddings/FAISS files or run embeddings script again.")

        st.subheader("LLM response (from local Ollama)")
        with st.spinner("Calling local LLM..."):
            try:
                resp = answer(query)  # answer() internally does retrieval + LLM call
                st.markdown(resp.replace("\n", "  \n"))
            except Exception as e:
                st.error("LLM call failed. See error below and check Ollama CLI:")
                st.exception(e)
                # Helpful debug hints
                st.write(
                    "Debug tips: run `ollama list` to confirm model id; "
                    "if model OOM, try a smaller model or quantized variant; "
                    "inspect terminal where you launched Ollama for logs."
                )
                resp = ""

        # Show peaks table and chart
        try:
            peaks = pd.read_csv("data/store_peak_hours.csv").merge(pd.read_csv("data/stores.csv"), on="store_id")
            st.subheader("Store peak hours")
            st.dataframe(peaks)
            chart = alt.Chart(peaks).mark_bar().encode(x='name', y='peak_count').properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not load peak hours table: {e}")

        # PDF report generation
        if gen_report:
            if resp:
                out_pdf = "final_report.pdf"
                try:
                    make_report(query, resp, out_pdf="final_report.pdf")
                    with open(out_pdf, "rb") as f:
                        st.success(f"Report generated: {out_pdf}")
                        st.download_button("Download PDF report", f, file_name=out_pdf, mime="application/pdf")
                except Exception as e:
                    st.error(f"Report generation failed: {e}")
                    st.write("Make sure weasyprint is installed and working.")
            else:
                st.info("No LLM response to include in the report.")

st.write("---")
st.caption("If you hit errors calling Ollama, try running `ollama run <model>` directly in a terminal to confirm the model is available and working.")

