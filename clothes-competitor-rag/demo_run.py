# demo_run.py
# 1. generate synthetic (if not generated)
# 2. preprocess
# 3. build embeddings
# 4. run a sample query and save report

import os
os.system("python src/generate_synthetic.py")
os.system("python src/preprocess.py")
os.system("python src/embeddings_faiss.py")
# sample query
from src.rag_query import answer
resp = answer("List competitors and their busiest hours, suggest 3 actions")
print(resp)
from src.report_gen_reportlab import make_report
make_report("List competitors and their busiest hours", resp, out_pdf="demo_report.pdf")
