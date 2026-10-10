"""Build browser_comparison.json from run_summary.jsonl."""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

art = Path(sys.argv[1] if len(sys.argv) > 1 else "selenium/artifacts/kt10")
rows: list[dict] = []
p = art / "run_summary.jsonl"
if p.exists():
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))

by_browser: dict[str, list] = defaultdict(list)
for r in rows:
    by_browser[r.get("browser") or "unknown"].append(r)

summary = {
    "total": len(rows),
    "passed": sum(1 for r in rows if r.get("outcome") == "passed"),
    "failed": sum(1 for r in rows if r.get("outcome") == "failed"),
    "browsers": {
        b: {
            "count": len(items),
            "passed": sum(1 for i in items if i.get("outcome") == "passed"),
            "failed": sum(1 for i in items if i.get("outcome") == "failed"),
            "versions": sorted({i.get("browserVersion") for i in items if i.get("browserVersion")}),
        }
        for b, items in by_browser.items()
    },
    "rows": rows,
}
(art / "browser_comparison.json").write_text(
    json.dumps(summary, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(json.dumps({k: summary[k] for k in ("total", "passed", "failed", "browsers")}, ensure_ascii=False, indent=2))
