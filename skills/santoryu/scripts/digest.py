#!/usr/bin/env python3
"""Santoryu: three swords, one clean cut: turn docx/pptx/xlsx/pdf/txt into a markdown digest, once.

Usage: digest.py <file>
Prints:  STATUS  <digest path>  ~<tokens> tokens
STATUS is UNCHANGED (same sha256 as last time), NEW or UPDATED.
Stdlib only, so it runs on any Mac with python3.
"""
import datetime
import hashlib
import os
import re
import subprocess
import sys
import zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "lib"))
from workspace import WS, link_line  # noqa: E402

PENDING = "<!-- summary pending -->"
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find(W + "body")

    def para(p):
        out = []
        for el in p.iter():
            if el.tag == W + "t":
                out.append(el.text or "")
            elif el.tag == W + "tab":
                out.append("\t")
            elif el.tag == W + "br":
                out.append("\n")
        text = "".join(out).strip()
        if not text:
            return ""
        style = p.find(f"{W}pPr/{W}pStyle")
        val = style.get(W + "val", "") if style is not None else ""
        m = re.match(r"Heading(\d)", val)
        if m:
            return "#" * min(int(m.group(1)) + 1, 6) + " " + text
        if val == "Title":
            return "# " + text
        if p.find(f"{W}pPr/{W}numPr") is not None:
            return "- " + text
        return text

    lines = []
    for child in body:
        if child.tag == W + "p":
            lines.append(para(child))
        elif child.tag == W + "tbl":
            for row in child.iter(W + "tr"):
                cells = []
                for cell in row.findall(W + "tc"):
                    cells.append(" ".join(para(p) for p in cell.iter(W + "p")).strip())
                lines.append("| " + " | ".join(cells) + " |")
        lines.append("")
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def pptx_text(path):
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
        names.sort(key=lambda n: int(re.search(r"(\d+)", n.split("/")[-1]).group(1)))
        out = []
        for i, n in enumerate(names, 1):
            root = ET.fromstring(z.read(n))
            paras = []
            for p in root.iter(A + "p"):
                t = "".join(x.text or "" for x in p.iter(A + "t")).strip()
                if t:
                    paras.append(t)
            out.append(f"## Slide {i}\n\n" + "\n".join(paras))
    return "\n\n".join(out)


def xlsx_text(path):
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.iter(S + "si"):
                shared.append("".join(t.text or "" for t in si.iter(S + "t")))
        names = []
        if "xl/workbook.xml" in z.namelist():
            wb = ET.fromstring(z.read("xl/workbook.xml"))
            names = [s.get("name") for s in wb.iter(S + "sheet")]
        sheets = [n for n in z.namelist() if re.match(r"xl/worksheets/sheet\d+\.xml$", n)]
        sheets.sort(key=lambda n: int(re.search(r"(\d+)", n.split("/")[-1]).group(1)))
        out = []
        for i, n in enumerate(sheets):
            title = names[i] if i < len(names) else f"Sheet {i + 1}"
            out.append(f"## {title}\n")
            root = ET.fromstring(z.read(n))
            for row in root.iter(S + "row"):
                vals = []
                for c in row.findall(S + "c"):
                    t = c.get("t")
                    v = c.find(S + "v")
                    if t == "s" and v is not None:
                        vals.append(shared[int(v.text)])
                    elif t == "inlineStr":
                        vals.append("".join(x.text or "" for x in c.iter(S + "t")))
                    else:
                        vals.append(v.text if v is not None and v.text else "")
                if any(vals):
                    out.append("| " + " | ".join(vals) + " |")
            out.append("")
    return "\n".join(out)


def pdf_text(path):
    try:
        return subprocess.run(
            ["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True
        ).stdout
    except FileNotFoundError:
        sys.exit("pdftotext not found. Run: brew install poppler")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    src = os.path.abspath(os.path.expanduser(sys.argv[1]))
    if not os.path.isfile(src):
        sys.exit(f"File not found: {src}")

    with open(src, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()

    stem = os.path.splitext(os.path.basename(src))[0]
    slug = re.sub(r"[^a-z0-9]+", "-", stem.lower()).strip("-") or "document"
    outdir = os.path.join(WS, "digests")
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, slug + ".md")

    status = "NEW"
    if os.path.exists(out):
        with open(out, encoding="utf-8") as f:
            head = f.read(600)
        if f"sha256: {sha}" in head:
            print(f"UNCHANGED  {out}")
            print(link_line(out))
            return
        status = "UPDATED"

    ext = os.path.splitext(src)[1].lower()
    readers = {".docx": docx_text, ".pptx": pptx_text, ".xlsx": xlsx_text, ".pdf": pdf_text}
    if ext in readers:
        text = readers[ext](src)
    elif ext in (".txt", ".md", ".csv"):
        with open(src, encoding="utf-8", errors="replace") as f:
            text = f.read()
    else:
        sys.exit(f"Unsupported file type: {ext}")

    doc = (
        f"---\ntags: [digest]\nsource: {src}\nsha256: {sha}\n"
        f"digested: {datetime.date.today().isoformat()}\n---\n\n"
        f"# {stem}\n\n## Summary\n\n{PENDING}\n\n## Full text\n\n{text}\n"
    )
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"{status}  {out}  ~{len(doc) // 4} tokens")
    print(link_line(out))


if __name__ == "__main__":
    main()
