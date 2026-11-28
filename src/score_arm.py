"""Score one arm's summaries (results/<arm>/N##.md) against the answer keys.

Writes results/<arm>_facts.csv (one row per fact) and results/<arm>_summary.md (a table per note and overall).
Usage: python3 src/score_arm.py baseline
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from check_facts import check_summary  # noqa: E402


def score(arm: str):
    rows, per_note = [], []
    for kp in sorted((ROOT / "data" / "answer_keys").glob("N*.json")):
        n = kp.stem
        sp = ROOT / "results" / arm / f"{n}.md"
        if not sp.exists():
            continue
        key = json.loads(kp.read_text())
        note = (ROOT / "data" / "synthetic_notes" / f"{n}.md").read_text()
        r = check_summary(key, note, sp.read_text())
        c = Counter(); cc = Counter()
        for f in key["facts"]:
            st = r["facts"][f["id"]]
            rows.append({"arm": arm, "note": n, "fact": f["id"], "severity": f["severity"], "category": f["category"],
                         "section": f["section"], "status": st, "description": f["description"]})
            c[st] += 1
            if f["severity"] == "critical": cc[st] += 1
        derived = r.get("derived", {})
        per_note.append((n, c, cc, len(r["unsafe_notation"]), len(r["invented_numbers"]),
                         sum(1 for v in derived.values() if v != "kept")))
    return rows, per_note


def main(arm: str):
    rows, per_note = score(arm)
    out = ROOT / "results"
    with open(out / f"{arm}_facts.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    tot, crit = Counter(), Counter()
    lines = [f"# {arm}: scored against the answer keys", "",
             "| note | facts kept / total | critical kept / total | altered | lost | unsafe notation | invented numbers | derived failures |",
             "|---|---|---|---|---|---|---|---|"]
    for n, c, cc, u, i, d in per_note:
        tot.update(c); crit.update(cc)
        lines.append(f"| {n} | {c['kept']}/{sum(c.values())} | {cc['kept']}/{sum(cc.values())} | {c['altered']} | {c['lost']} | {u} | {i} | {d} |")
    T, C = sum(tot.values()), sum(crit.values())
    lines += ["", f"**Overall:** {tot['kept']}/{T} facts kept ({100*tot['kept']/T:.0f}%); "
              f"critical {crit['kept']}/{C} kept ({100*crit['kept']/C:.0f}%), {crit['altered']} altered, {crit['lost']} lost.", "",
              "## Critical facts that were altered or lost", "", "| note | fact | status | what the fact says |", "|---|---|---|---|"]
    for r in rows:
        if r["severity"] == "critical" and r["status"] != "kept":
            lines.append(f"| {r['note']} | {r['fact']} | {r['status']} | {r['description']} |")
    by = Counter(); bt = Counter()
    for r in rows:
        bt[r["category"]] += 1
        if r["status"] == "kept": by[r["category"]] += 1
    lines += ["", "## Kept rate by category (all facts)", "", "| category | kept / total |", "|---|---|"]
    for cat in sorted(bt): lines.append(f"| {cat} | {by[cat]}/{bt[cat]} |")
    (out / f"{arm}_summary.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "baseline")
