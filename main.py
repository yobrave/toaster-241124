"""tst6 mover. Reads the toast complaint, checks the slot, ships one file."""
import json
import os
import sys
from pathlib import Path

BOUND = 120
WHO = "tst6-toast-desk-r6"


def lift(raw: str):
    text = raw.strip()
    size = len(text)
    ok = (size > 0) and (size <= BOUND) and (size == len(text.rstrip())) and not text.isspace()
    return text, size, ok


def main(argv):
    home = Path(argv[1]).resolve().parent if len(argv) > 1 else Path(__file__).resolve().parent
    src = home / "entry.txt"
    slot = os.environ.get("MAKEFUN_OUTPUT_DIR") or "out"
    text, size, ok = lift(src.read_text(encoding="utf-8"))
    receipt = {"who": WHO, "size": size, "bound": BOUND, "ok": ok}
    if ok:
        target = Path(slot)
        target.mkdir(parents=True, exist_ok=True)
        (target / "entry.txt").write_bytes(text.encode("utf-8"))
        receipt["landed"] = str(target / "entry.txt")
    print("VERDICT", json.dumps(receipt))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
