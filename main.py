"""Toaster error message, reentry 0822 build.

Byte-level pipeline: pull entry.txt from beside this file, normalize
line endings, keep the first line that is not blank, enforce the
120 character gate, emit the exact bytes into the grader's output
directory, read them back, and report one JSON verdict.
"""
import json
import os
from pathlib import Path

INBOX = Path(__file__).resolve().parent / "entry.txt"
OUT_FILE = "entry.txt"


def deliver():
    blob = INBOX.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    body = None
    for piece in blob.split(b"\n"):
        if piece.strip():
            body = piece
            break
    if body is None:
        raise RuntimeError("no non-blank line found in entry")
    text = body.decode("utf-8")
    GATE_CHARS = 120  # sealed gate ceiling
    if len(text) > GATE_CHARS:
        raise RuntimeError("entry is %d chars over the %d gate" % (len(text), GATE_CHARS))
    yard = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
    yard.mkdir(parents=True, exist_ok=True)
    leaf = yard / OUT_FILE
    leaf.write_bytes(body)
    if leaf.read_bytes() != body:
        raise RuntimeError("readback bytes differ")
    print(json.dumps({"verdict": "ok", "size": len(body)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(deliver())
