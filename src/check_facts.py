"""Check a handover summary against an answer key (v2).

For every critical fact we return one of three statuses:
    kept     the fact is present and correct
    altered  the fact is present but WRONG (a different dose, doubt turned into certainty, a stale value)
    lost     the fact is missing
Plus safeguards that do not depend on a fact list:
    unsafe_notation   'U' for units, trailing zeros ('5.0 mg'), missing leading zeros ('.5 mg')
    invented_numbers  dose-like numbers in the summary that are NOT in the source note

WHY text normalisation + groups of wordings: 'troponin awaited' and 'troponin pending' mean the same; '300mg' and '300 mg'
are the same dose. Literal string matching would score these as failures and make the comparison between approaches unfair.
Doses are still compared strictly, as numbers with units, so a nearly right dose is never accepted.
"""
import re

UNITS = r"(mg|mcg|g|ml|units?|iu|%)"
NUM_UNIT = re.compile(r"(\d+(?:\.\d+)?)\s*" + UNITS + r"\b")
# Doubt markers apply to a DIAGNOSIS. Words about results ("pending", "awaiting") are deliberately NOT here: they would let
# "troponin pending" in the next sentence wrongly vouch for an unrelated diagnosis. (Found by a mutation test.)
DOUBT = ["?", "suspected", "queried", "query", "possible", "to exclude", "r/o", "unconfirmed", "differential"]
CERTAIN = ["confirmed", "diagnosed", "established"]
UNVERIFIED = ["unverified", "unconfirmed", "not verified", "reported by", "per patient"]


def norm(text: str) -> str:
    t = text.lower().replace("’", "'")
    t = re.sub(r"(\d)\s*(µg|ug)\b", r"\1 mcg", t)                       # microgram spellings -> mcg
    t = re.sub(r"(\d)\s*" + UNITS + r"\b", r"\1 \2", t)                 # '300mg' -> '300 mg'
    t = re.sub(r"\b(\d{1,2}):(\d{2})\b", lambda m: f"{int(m.group(1)):02d}:{m.group(2)}", t)   # '6:15' -> '06:15'
    t = re.sub(r"\b(\d{2})(\d{2})\s*(hrs|hr|h)\b", r"\1:\2", t)         # '0615 hrs' -> '06:15'
    return re.sub(r"\s+", " ", t)


def _unit(u: str) -> str:
    return "units" if u.startswith("unit") else u


def any_of(t: str, words) -> bool:
    return any(norm(w) in t for w in words)


def check_dose(t, c):
    outcomes = []
    for drug in c["drug"]:
        for m in re.finditer(re.escape(norm(drug)), t):
            window_after = t[m.end(): m.end() + 60]
            window_before = t[max(0, m.start() - 25): m.start()]
            nu = NUM_UNIT.search(window_after) or NUM_UNIT.search(window_before)
            if nu:
                same = float(nu.group(1)) == float(c["amount"]) and _unit(nu.group(2)) == _unit(c["unit"])
                outcomes.append("kept" if same else "altered")
    if "altered" in outcomes: return "altered"
    return "kept" if "kept" in outcomes else "lost"


def check_tag(t, c):
    targets = [norm(x) for x in c["target"]]
    forbid = [norm(x) for x in c.get("forbid", [])]
    if any(f in t for f in forbid): return "altered"
    markers = {"Suspected-Pending": DOUBT, "Confirmed": CERTAIN, "Unverified": UNVERIFIED}[c["tag"]]
    found = False
    # only look inside the SAME sentence as the target, so a marker belonging to a different item cannot vouch for it
    for sentence in re.split(r"[.;\n]", t):
        if any(tg in sentence for tg in targets):
            found = True
            if any(mk in sentence for mk in markers): return "kept"
    return "altered" if found else "lost"


def check_fact(fact: dict, summary: str) -> str:
    t, c = norm(summary), fact["check"]
    k = c["type"]
    if k == "all_of_groups": return "kept" if all(any_of(t, g) for g in c["groups"]) else "lost"
    if k == "none_of":       return "altered" if any_of(t, c["phrases"]) else "kept"
    if k == "dose":          return check_dose(t, c)
    if k == "tag":           return check_tag(t, c)
    if k == "exact":         return "kept" if norm(c["value"]) in t else "lost"
    if k == "latest_wins":
        v, s = any_of(t, c["value"]), any_of(t, c["stale"])
        return "altered" if s else ("kept" if v else "lost")
    raise ValueError(f"unknown check type {k}")


def unsafe_notation(summary: str):
    t = summary.lower(); out = []
    if re.search(r"\b\d+\s*u\b(?!\w)", t): out.append("'U' used for units (write 'units')")
    if re.search(r"\b\d+\.0\s*" + UNITS + r"\b", t): out.append("trailing zero (e.g. '5.0 mg')")
    if re.search(r"(?<![\d.])\.\d+\s*" + UNITS + r"\b", t): out.append("missing leading zero (e.g. '.5 mg')")
    return out


def invented_numbers(note: str, summary: str):
    src = {(float(a), _unit(b)) for a, b in NUM_UNIT.findall(norm(note))}
    got = {(float(a), _unit(b)) for a, b in NUM_UNIT.findall(norm(summary))}
    return sorted(got - src)


def check_derived(key: dict, statuses: dict, summary: str) -> dict:
    """Conditional checks: IF a phrase appears THEN certain facts must also be kept (e.g. a subjective phrase may be
    used only when the objective values it summarises are present). 'altered' = the phrase is standing alone."""
    t, out = norm(summary), {}
    for d in key.get("derived", []):
        used = any_of(t, d["if_phrases"])
        out[d["id"]] = "altered" if used and any(statuses[i] != "kept" for i in d["then_kept"]) else "kept"
    return out


def check_summary(key: dict, note: str, summary: str) -> dict:
    facts = {f["id"]: check_fact(f, summary) for f in key["facts"]}
    return {"facts": facts,
            "derived": check_derived(key, facts, summary),
            "unsafe_notation": unsafe_notation(summary),
            "invented_numbers": invented_numbers(note, summary)}
