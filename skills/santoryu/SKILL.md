---
name: santoryu
description: Digest a docx, pdf, pptx or xlsx once, then work from the digest. Use whenever such a file is attached, named, or about to be read, e.g. "We-Do-GMV-campaign-brief.docx".
model: sonnet
---

Three Sword Style: one clean cut turns a heavy document into a digest, and the original stays sheathed afterwards.

Workspace: the path in the session start notice (default `~/Desktop/Zoro-Files/`)

1. Run `python3 scripts/digest.py "<full path to file>"` from this skill's base directory. It prints a status (`UNCHANGED`, `NEW` or `UPDATED`), the digest path and its approximate token size.
2. `UNCHANGED`: read only the `## Summary` block at the top of the digest.
   `NEW` or `UPDATED`: read the digest, then replace the `<!-- summary pending -->` marker with a summary of at most 150 words: what the document is, the key facts and numbers, and a list of its section headings.
3. Answer from the summary. For detail, read the matching section of the digest by heading.
4. Finish when the digest has a written summary and the user's question is answered from it.

The script handles docx, pptx, xlsx, pdf (needs `pdftotext`) and plain text. If `pdftotext` is missing, tell the user to run `brew install poppler`.

Close with one line. After a first digest: "🗡️🗡️🗡️ Santoryu done. One cut, no need to read it again." When the status was `UNCHANGED`: "🗡️🗡️🗡️ Nothing happened. Already read it."
