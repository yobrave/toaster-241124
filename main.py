"""Toaster error line, fresh reentry build."""
import json
import os
from pathlib import Path

FAULT = ("ERROR: crumbs have achieved quorum and are now self-governing. "
         "Toasting is suspended until further notice.")
CEILING = 120
BASELINE = 1


def place(home):
    bay = Path(home)
    bay.mkdir(parents=True, exist_ok=True)
    leaf = bay / "entry.txt"
    leaf.write_text(FAULT, encoding="utf-8")
    try:
        stored = leaf.read_text(encoding="utf-8")
    except OSError as why:
        raise SystemExit("cannot read back: %s" % why)
    if stored != FAULT or len(stored) > CEILING or len(stored) < BASELINE:
        raise SystemExit("gate check failed")
    return leaf


slot = place(os.environ.get("MAKEFUN_OUTPUT_DIR") or "output")
print(json.dumps({"ok": True, "where": str(slot), "count": len(FAULT)}))
