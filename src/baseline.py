"""Arm 1: rule-based baseline. Builds an ISOBAR handover summary from a ward note using fixed rules only.

No model, no network, no API key. IMPORTANT (leakage rule): this file must never read the answer keys; the rules
use the note's own layout (banner fields, tables, plan list) and one generic list of handover vocabulary below.
The rules are deliberately naive: they copy what the note says, so they inherit the note's stale entries and
shorthand. That is the point of a baseline: it shows what simple rules can and cannot protect.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# One generic vocabulary of words that nurses flag at handover (not derived from the answer keys).
VOCAB = re.compile(
    r"allerg|arp|cpr|resus|pending|awaiting|awaited|not yet|requested|review|informed|aware|due |held|withheld|hold|"
    r"nbm|precaution|falls|telemetry|isolation|suspected|\?|culture|result|plan|given|commenced|started|removal|planned|"
    r"drain|catheter|idc|oxygen|o2 |sedat|drows|confus|disorientat|pain|worse|deteriorat|escalat|met |icu|restart|recommence|"
    r"discharge|fluid|restrict|weight|wt |\bkg\b|mrsa|latex|nkda|q-adds|escort|shield|bloods|inr|troponin|ecg", re.I)


def banner(text: str) -> dict:
    out = {}
    for line in text.splitlines():
        if line.startswith("**"):
            for k, v in re.findall(r"\*\*([^*]+?):\*\*\s*(.*?)(?=\s{2,}\*\*|$)", line):
                out[k.strip().upper()] = v.strip()
    return out


def section(text: str, name: str) -> str:
    m = re.search(r"^## " + re.escape(name) + r".*?\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def table(block: str):
    rows = [r.strip().strip("|").split("|") for r in block.splitlines() if r.strip().startswith("|")]
    rows = [[c.strip() for c in r] for r in rows if not set("".join(r)) <= set("-: ")]
    return (rows[0], rows[1:]) if rows else ([], [])


def sentences(entry: str):
    return [s.strip() for s in re.split(r"(?<!\d)\.(?=\s|$)|(?<=\))\.(?=\s)|;|\n", entry) if s.strip()]


def field(b: dict, key: str) -> str:
    # Banner labels differ slightly between notes (for example 'ALLERGIES' vs 'ALLERGIES / ADVERSE REACTIONS'),
    # so match on the first word(s) of the label rather than the full text.
    v = b.get(key) or next((val for k, val in b.items() if k.split(" /")[0] == key.split(" /")[0]), "")
    return "not documented" if (not v or v.strip("() ").lower() in ("blank", "")) else v


def summarise(note: str) -> str:
    b = banner(note)
    notes = section(note, "Note")
    entries = [e.strip() for e in re.split(r"\n(?=\[\d)", notes) if e.strip()]
    hdr, obs = table(section(note, "Observations"))
    mh, meds = table(section(note, "Medications"))
    plan = [l.lstrip("- ").strip() for l in section(note, "Pending / plan").splitlines() if l.strip().startswith("-")]

    # Weight: banner if present, else a "Wt/weight NN kg" mention in the note text, else not documented.
    weight = b.get("WEIGHT", "")
    if not weight or weight.strip("() ").lower() == "blank":
        m = re.search(r"(?:wt|weight)\s*:?\s*([\d.]+)\s*kg", note, re.I)
        weight = f"{m.group(1)} kg" if m else "not documented"

    out = []
    out.append("I - IDENTIFICATION")
    out.append(f"{b.get('PATIENT','')}, {b.get('AGE/SEX','')}, {b.get('HOSPITAL (FICTIONAL)','')}, {b.get('WARD / BED','')}.")
    out.append("S - SITUATION AND STATUS")
    out.append(f"Admitted for: {field(b,'REASON FOR ADMISSION')}.")
    out.append(f"Resuscitation / ARP: {field(b,'ARP / RESUSCITATION STATUS')}.")
    out.append("O - OBSERVATIONS")
    if obs:
        last = obs[-1]
        out.append("Latest obs: " + ", ".join(f"{h} {v}" for h, v in zip(hdr, last)) + ".")
        qi = hdr.index("Q-ADDS") if "Q-ADDS" in hdr else None
        if qi is not None:
            sc = [r[qi] for r in obs if len(r) > qi]
            nums = [int(x) for x in sc if x.isdigit()]
            trend = " -> ".join(sc)
            out.append(f"Q-ADDS trend: {trend}" + (" (rising)" if len(nums) > 1 and nums[-1] > nums[0] else "") + ".")
    out.append("B - BACKGROUND AND HISTORY")
    out.append(f"Allergies: {field(b,'ALLERGIES / ADVERSE REACTIONS')}.")
    out.append(f"Baseline: {field(b,'BASELINE')}.")
    out.append(f"Weight: {weight}.")
    out.append("A - ASSESSMENT AND ACTIONS")
    for r in meds:
        out.append("Medication: " + " | ".join(f"{h}: {v}" for h, v in zip(mh, r)) + ".")
    kept = []
    for e in entries:
        for s in sentences(re.sub(r"^\[[^\]]*\]\s*", "", e)):
            if VOCAB.search(s) and s not in kept:
                kept.append(s)
    for s in kept:
        out.append("Note: " + s + ".")
    out.append("R - RESPONSIBILITY AND RISK MANAGEMENT (pending and plan)")
    for p in plan:
        out.append("- " + p)
    return "\n".join(out)


def main():
    outdir = ROOT / "results" / "baseline"; outdir.mkdir(parents=True, exist_ok=True)
    for p in sorted((ROOT / "data" / "synthetic_notes").glob("N*.md")):
        (outdir / p.name).write_text(summarise(p.read_text()) + "\n")
    print(f"wrote {len(list(outdir.glob('N*.md')))} baseline summaries to {outdir}")


if __name__ == "__main__":
    sys.exit(main())
