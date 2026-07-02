#!/usr/bin/env python3
"""
Batch-convert .py files to reliably copy-pasteable PDFs.
Usage: python3 py_to_pdf.py /path/to/py_folder /path/to/pdf_output_folder
"""
import sys, os, html, subprocess, glob

def convert(py_path, out_dir):
    name = os.path.splitext(os.path.basename(py_path))[0]
    code = open(py_path, encoding="utf-8").read().replace("\t", "    ")  # tabs -> spaces, just in case
    escaped = html.escape(code)
    doc = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body {{ margin: 25px; }}
  h2 {{ font-family: sans-serif; font-size: 12pt; color: #333; }}
  pre {{
    font-family: "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 10pt;
    white-space: pre-wrap;   /* wrap long lines instead of cutting them off */
    word-break: break-word;
    line-height: 1.4;
  }}
</style></head>
<body><h2>{html.escape(name)}.py</h2><pre>{escaped}</pre></body></html>"""
    html_path = os.path.join(out_dir, name + ".html")
    pdf_path = os.path.join(out_dir, name + ".pdf")
    open(html_path, "w", encoding="utf-8").write(doc)
    subprocess.run(["wkhtmltopdf", "--quiet", html_path, pdf_path], check=True)
    os.remove(html_path)
    print(f"  -> {pdf_path}")

if __name__ == "__main__":
    src_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    py_files = sorted(glob.glob(os.path.join(src_dir, "*.py")))
    print(f"Converting {len(py_files)} files...")
    for f in py_files:
        convert(f, out_dir)
    print("Done.")
