"""Arm 1: rule-based baseline. Builds an ISOBAR handover summary from a ward note using fixed rules only.

No model, no network, no API key. IMPORTANT (leakage rule): this file must never read the answer keys; the rules
use the note's own layout (banner fields, tables, plan list) and one generic list of handover vocabulary below.
The rules are deliberately naive: they copy what the note says, so they inherit the note's stale entries and
shorthand. That is the point of a baseline: it shows what simple rules can and cannot protect.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from budget import budget_for  # noqa: E402

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
    """Build the summary within the shared word budget (src/budget.py), keeping the highest-priority items first."""
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

    # Each item is (priority, ISOBAR section, text). Lower priority number = kept first when words run out.
    items = [
        (1, "I", f"{b.get('PATIENT','')}, {b.get('AGE/SEX','')}, {b.get('WARD / BED','')}."),
        (1, "S", f"Admitted: {field(b,'REASON FOR ADMISSION')}."),
        (1, "S", f"ARP/resuscitation: {field(b,'ARP / RESUSCITATION STATUS')}."),
        (1, "B", f"Allergies: {field(b,'ALLERGIES / ADVERSE REACTIONS')}."),
        (1, "B", f"Weight: {weight}."),
    ]
    for r in meds:
        d = dict(zip((h.lower() for h in mh), r))
        reg = d.get("regular/prn", "")
        items.append((2, "A", f"{d.get('drug','')} {d.get('dose','')} {d.get('route','')} {d.get('frequency','')} {reg}; last given {d.get('last given','')}.".replace("  ", " ")))
    for p in plan:
        items.append((3, "R", "Plan: " + p + ("" if p.endswith(".") else ".")))
    if obs:
        last = obs[-1]
        items.append((4, "O", "Latest obs: " + ", ".join(f"{h} {v}" for h, v in zip(hdr, last)) + "."))
        if "Q-ADDS" in hdr:
            qi = hdr.index("Q-ADDS"); sc = [r[qi] for r in obs if len(r) > qi]
            nums = [int(x) for x in sc if x.isdigit()]
            items.append((4, "O", "Q-ADDS trend: " + " -> ".join(sc) + (" (rising)." if len(nums) > 1 and nums == sorted(nums) and nums[-1] > nums[0]
                                                    else f" (peak {max(nums)})." if len(nums) > 1 and max(nums) > nums[-1] else ".")))
    items.append((5, "B", f"Baseline: {field(b,'BASELINE')}."))
    # Remaining note sentences: more handover words first, and later entries before earlier ones when tied.
    cand = []
    for ei, e in enumerate(entries):
        for s_ in sentences(re.sub(r"^\[[^\]]*\]\s*", "", e)):
            hits = len(set(m.lower() for m in VOCAB.findall(s_)))
            if hits and s_ not in [c[2] for c in cand]:
                cand.append((-hits, -ei, s_))
    for _, _, s_ in sorted(cand):
        items.append((6, "A", s_ + ("" if s_.endswith(".") else ".")))

    budget = budget_for(note)
    heads = {"I": "I:", "S": "S:", "O": "O:", "B": "B:", "A": "A:", "R": "R:"}
    used, chosen = 0, []
    for pr, sec, text in sorted(items, key=lambda x: x[0]):          # stable: keeps source order inside a priority
        cost = len(text.split()) + (0 if any(c[1] == sec for c in chosen) else 1)   # a section heading costs one word
        if used + cost <= budget:
            chosen.append((pr, sec, text)); used += cost
    out = []
    for sec in "ISOBAR":
        txt = [t for _, sc, t in chosen if sc == sec]
        if txt:
            out.append(heads[sec] + " " + " ".join(txt))
    return "\n".join(out)


def main():
    outdir = ROOT / "results" / "baseline"; outdir.mkdir(parents=True, exist_ok=True)
    for p in sorted((ROOT / "data" / "synthetic_notes").glob("N*.md")):
        (outdir / p.name).write_text(summarise(p.read_text()) + "\n")
    print(f"wrote {len(list(outdir.glob('N*.md')))} baseline summaries to {outdir}")


if __name__ == "__main__":
    sys.exit(main())
