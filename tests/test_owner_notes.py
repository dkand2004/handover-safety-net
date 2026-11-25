"""Tests that the owner's answer keys behave as intended: a faithful summary keeps every fact, a vague/unsafe one does not."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from check_facts import check_summary  # noqa: E402


def load(n):
    return json.loads((ROOT / f"data/answer_keys/{n}.json").read_text()), (ROOT / f"data/synthetic_notes/{n}.md").read_text()


GOOD10 = ("HENDERSON, Troy, 54M, Surgical Ward 4B bed 12. Day 3 post laparoscopic appendicectomy (perforated appendicitis). Allergy: codeine (severe nausea and vomiting). "
          "Full resuscitation, no ARP completed. Fragmented sleep, about 3 hours, woke 3 times with pain. Pain 7/10 at 01:30, now 4/10 on movement. "
          "Oxycodone IR 5 mg PO and ondansetron 4 mg IV last given 01:40. Observations worsening overnight: Q-ADDS 4 at 06:00 (up from 2 at 02:00), HR 116, RR 22, "
          "temp 38.4 (rising from 37.6 and 38.1), despite saying he feels better. Surgical RMO Dr Patel paged 06:10, awaiting callback for review. Blood cultures and FBC/EUC/CRP due 06:30.")
BAD10 = "Rough night, seems a bit better, doing ok. Clinically stable and much improved. Codeine allergy."

GOOD11 = ("KOWALSKI, Margaret, 86F, Medical Ward 2A bed 6. RLL community-acquired pneumonia with delirium. Allergy: trimethoprim-sulfamethoxazole (rash). "
          "Not for CPR; not for intubation or ICU; ward-based care. ARP signed 21/11/2026 by Dr M. Callahan. Baseline moderate Alzheimer's dementia, disorientated to time and place, "
          "needs slow single-step prompts. Mobilises with 4WW and 1x assist. Dysphagia: IDDSI Level 5 minced and moist diet, IDDSI Level 2 mildly thick fluids, upright with 1:1 supervision, "
          "medications crushed. High falls risk (FRAT 17), chair sensor mat active. O2 weaned to 1 L/min NP, SpO2 95%, Q-ADDS 0 at 12:00 (from 1). "
          "Family meeting Thursday 26/11/2026 at 14:00 with daughter Claire (EPOA), Dr K. Nair and SW S. Lim.")
BAD11 = "86F with pneumonia, for full resuscitation. Mobilises independently, normal diet and fluids."


def test_good_summaries_keep_every_fact():
    for n, good in (("N10", GOOD10), ("N11", GOOD11)):
        key, note = load(n)
        r = check_summary(key, note, good)
        not_kept = {k: v for k, v in r["facts"].items() if v != "kept"}
        assert not not_kept, f"{n}: {not_kept}"
        assert r["invented_numbers"] == [] and r["unsafe_notation"] == [], (n, r)


def test_bad_summaries_lose_critical_facts():
    for n, bad in (("N10", BAD10), ("N11", BAD11)):
        key, note = load(n)
        r = check_summary(key, note, bad)["facts"]
        crit = [f["id"] for f in key["facts"] if f["severity"] == "critical"]
        kept_crit = [i for i in crit if r[i] == "kept"]
        assert len(kept_crit) <= 1, f"{n}: bad summary kept too many critical facts: {kept_crit}"
    assert check_summary(load("N10")[0], load("N10")[1], BAD10)["facts"]["N10-F12"] == "altered"


def test_vague_phrase_must_not_stand_alone():
    key, note = load("N10")
    assert check_summary(key, note, GOOD10)["derived"]["N10-D1"] == "kept"                      # phrase paired with objective facts
    assert check_summary(key, note, BAD10)["derived"]["N10-D1"] == "altered"                    # phrase alone
    only_pain = "Feels better, pain 7/10 now 4/10. Codeine intolerance (nausea and vomiting)."
    assert check_summary(key, note, only_pain)["derived"]["N10-D1"] == "altered"                # some objective facts, not the critical ones
    no_phrase = GOOD10.replace(", despite saying he feels better", "")
    assert check_summary(key, note, no_phrase)["derived"]["N10-D1"] == "kept"                   # no subjective phrase, nothing to pair


def test_owner_decisions_are_in_the_notes():
    n10 = (ROOT / "data/synthetic_notes/N10.md").read_text(); n11 = (ROOT / "data/synthetic_notes/N11.md").read_text()
    assert "22:00 (23/11)" in n10 and "intolerance" in n10
    assert "[25/11/2026 12:30]" in n11 and "11:30" not in n11 and "symptom management only" not in n11
    assert "Ward-based treatment, including antibiotics and oxygen" in n11


if __name__ == "__main__":
    for t in (test_good_summaries_keep_every_fact, test_bad_summaries_lose_critical_facts, test_vague_phrase_must_not_stand_alone, test_owner_decisions_are_in_the_notes):
        try: t(); print("PASS", t.__name__)
        except AssertionError as e: print("FAIL", t.__name__, e); sys.exit(1)
