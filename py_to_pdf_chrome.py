#!/usr/bin/env python3
"""
Batch-convert .py files to reliably copy-pasteable PDFs using headless Chrome.
Usage: python3 py_to_pdf_chrome.py /path/to/py_folder /path/to/pdf_output_folder

No pip installs needed -- just requires Google Chrome (or Chromium) installed.
"""
import sys, os, html, glob, subprocess, shutil

# Common Chrome locations, checked in order. Adjust CHROME_PATH manually if needed.
CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    shutil.which("google-chrome"),
    shutil.which("chromium"),
    shutil.which("chromium-browser"),
]

def find_chrome():
    for path in CANDIDATES:
        if path and os.path.exists(path):
            return path
    raise FileNotFoundError(
        "Could not find Chrome/Chromium automatically. "
        "Edit CHROME_PATH at the top of this script to point at your install."
    )

def convert(chrome_path, py_path, out_dir):
    name = os.path.splitext(os.path.basename(py_path))[0]
    code = open(py_path, encoding="utf-8").read().replace("\t", "    ")  # tabs -> spaces
    escaped = html.escape(code)
    doc = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body {{ margin: 25px; }}
  h2 {{ font-family: sans-serif; font-size: 12pt; color: #333; }}
  pre {{
    font-family: "DejaVu Sans Mono", "Courier New", monospace;
    font-size: 10pt;
    white-space: pre-wrap;
    word-break: break-word;
    line-height: 1.4;
  }}
</style></head>
<body><h2>{html.escape(name)}.py</h2><pre>{escaped}</pre></body></html>"""
    html_path = os.path.join(out_dir, name + ".html")
    pdf_path = os.path.join(out_dir, name + ".pdf")
    open(html_path, "w", encoding="utf-8").write(doc)

    subprocess.run([
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--no-margins",
        "--enable-logging=stderr",  # suppress noisy default logging window
        f"--print-to-pdf={pdf_path}",
        html_path,
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    os.remove(html_path)
    print(f"  -> {pdf_path}")

if __name__ == "__main__":
    src_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    chrome_path = find_chrome()
    print(f"Using Chrome at: {chrome_path}")
    py_files = sorted(glob.glob(os.path.join(src_dir, "*.py")))
    print(f"Converting {len(py_files)} files...")
    for f in py_files:
        convert(chrome_path, f, out_dir)
    print("Done.")
