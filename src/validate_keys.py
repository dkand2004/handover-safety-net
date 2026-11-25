"""Validate answer-key files (the 'ground truth' of critical facts for each synthetic note).

WHY: the evaluation is only as trustworthy as its answer keys. A key with a typo (wrong check type,
missing field, duplicate id) would silently corrupt the results, so keys are validated before use.
Run:  python src/validate_keys.py            (validates every data/answer_keys/*.json)
"""
import json
import sys
from pathlib import Path

SECTIONS = {"I", "S", "O", "B", "A", "R"}          # ISOBAR sections
CATEGORIES = {"allergy", "medication", "last_given", "med_change", "deterioration", "pending", "arp",
              "laterality", "baseline", "uncertainty", "not_documented", "objective_value", "isolation", "device"}
# Each check type and the fields it requires:
#   all_of_groups: "groups" = list of lists; every group needs at least one wording present (AND of ORs)
#   none_of      : none of "phrases" may appear (e.g. 'no known allergies' when allergies are not documented)
#   dose         : "drug" (names), "amount", "unit": number and unit are compared strictly (kept / altered / lost)
#   tag          : "target" terms must carry the certainty "tag" (Confirmed / Suspected-Pending / Unverified)
#   latest_wins  : "value" wordings (most recent) must appear and "stale" wordings must not
#   exact        : "value" must appear (after normalisation): times, identifiers
CHECKS = {"all_of_groups": {"groups"}, "none_of": {"phrases"}, "dose": {"drug", "amount", "unit"},
          "tag": {"target", "tag"}, "latest_wins": {"value", "stale"}, "exact": {"value"}}
SEVERITIES = {"critical", "important"}
TAGS = {"Confirmed", "Suspected-Pending", "Unverified"}


def validate(key: dict) -> list:
    errs = []
    nid = key.get("note_id", "")
    if not (isinstance(nid, str) and nid.startswith("N") and nid[1:].isdigit()):
        errs.append("note_id must look like 'N05'")
    fms = key.get("failure_modes")
    if not (isinstance(fms, list) and fms and all(isinstance(x, int) and 1 <= x <= 13 for x in fms)):
        errs.append("failure_modes must be a non-empty list of integers 1 to 13")
    facts = key.get("facts")
    if not (isinstance(facts, list) and facts):
        return errs + ["facts must be a non-empty list"]
    seen = set()
    for f in facts:
        fid = f.get("id", "?")
        if fid in seen: errs.append(f"{fid}: duplicate id")
        seen.add(fid)
        if not str(fid).startswith(nid + "-"): errs.append(f"{fid}: id must start with '{nid}-'")
        if f.get("category") not in CATEGORIES: errs.append(f"{fid}: unknown category {f.get('category')!r}")
        if f.get("section") not in SECTIONS: errs.append(f"{fid}: section must be one of I,S,O,B,A,R")
        if not f.get("description"): errs.append(f"{fid}: description required")
        chk = f.get("check", {})
        t = chk.get("type")
        if t not in CHECKS: errs.append(f"{fid}: unknown check type {t!r}"); continue
        missing = CHECKS[t] - set(chk)
        if missing: errs.append(f"{fid}: check '{t}' missing {sorted(missing)}")
        if f.get("severity") not in SEVERITIES: errs.append(f"{fid}: severity must be 'critical' or 'important'")
        if t == "all_of_groups" and not (isinstance(chk.get("groups"), list) and chk["groups"] and all(isinstance(g, list) and g for g in chk["groups"])):
            errs.append(f"{fid}: 'groups' must be a non-empty list of non-empty lists")
        if t == "none_of" and not (isinstance(chk.get("phrases"), list) and chk["phrases"]):
            errs.append(f"{fid}: 'phrases' must be a non-empty list")
        if t == "dose" and not isinstance(chk.get("amount"), (int, float)):
            errs.append(f"{fid}: dose 'amount' must be a number")
        if t == "tag" and chk.get("tag") not in TAGS: errs.append(f"{fid}: tag must be one of {sorted(TAGS)}")
    return errs


if __name__ == "__main__":
    bad = 0
    for p in sorted(Path("data/answer_keys").glob("*.json")):
        e = validate(json.loads(p.read_text(encoding="utf-8")))
        print(("OK   " if not e else "FAIL ") + p.name)
        for m in e: print("     -", m)
        bad += bool(e)
    sys.exit(1 if bad else 0)
