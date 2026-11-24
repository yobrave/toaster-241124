"""Toaster error message entry builder.

Stage the appliance's latest grievance into output/entry.txt, echo its
length, and audit the gate's 120-character ceiling before the judge does.
The toaster remains unavailable for comment.
"""
import os
from pathlib import Path

LINES = (
    "Firmware update 7.1: toast now 3% crisper, "
    "40% more emotionally distant. This is not a bug."
)
CEILING = 120


def stage(root):
    out = Path(root)
    out.mkdir(parents=True, exist_ok=True)
    target = out / "entry.txt"
    target.write_text(LINES, encoding="utf-8")
    return target


if __name__ == "__main__":
    placed = stage(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
    shown = placed.read_text(encoding="utf-8")
    assert shown == LINES and 0 < len(shown) <= CEILING, "gate audit failed"
    print(f"staged {len(shown)} chars: {shown}")
