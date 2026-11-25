"""Toaster error relay: counts the message the slow way, then relays it on."""
STAMP = "onebug-11251142-tst3"
import json
import os
import shutil
from pathlib import Path

BOARD = Path(__file__).resolve().parent
CEILING = 120
TOAST = ("Error: bread inserted with confidence. "
         "Confidence is not a supported setting. Ejecting.")


def slow_count(text):
    seen = 0
    for _ in text.strip():
        seen += 1
    return seen


def relay():
    slot = BOARD / "entry.txt"
    body = slot.read_text(encoding="utf-8")
    n = slow_count(body)
    fits = 1 <= n <= CEILING
    if fits:
        bay = os.environ.get("MAKEFUN_OUTPUT_DIR")
        if bay:
            Path(bay).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(slot, Path(bay) / "entry.txt")
    print(json.dumps({"fits": fits, "stamp": STAMP, "count": n, "ceiling": CEILING}))


if __name__ == "__main__":
    relay()
