"""Tests for the Claude-drafted notes N06-N09 (batch 2)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from check_facts import check_summary  # noqa: E402


def load(n):
    return json.loads((ROOT / f"data/answer_keys/{n}.json").read_text()), (ROOT / f"data/synthetic_notes/{n}.md").read_text()


def run(n, s):
    key, note = load(n)
    return key, check_summary(key, note, s)


GOOD = {
 "N06": ("ROSSI, Anthony, 62M, type 2 diabetes on insulin, lower leg cellulitis. NKDA. Full resuscitation. Insulin glargine 20 units SC last given 22:00 on 24/11. "
         "BGL 12.1 mmol/L at 11:30: NovoRapid 4 units SC given 11:45 per correction scale (10.1-14.0 = 4 units). Next BGL due 16:00."),
 "N07": ("ANDERSEN, Sophie, 47F, day 1 post laparoscopic cholecystectomy. ALLERGY: NSAIDs and ibuprofen cause an asthma exacerbation, avoid. Full resuscitation. "
         "Oxycodone IR 5 mg PO PRN 4-hourly, last given 13:10 (not before 17:10); drowsy after that dose but rousable. Paracetamol 1 g PO regular QID (max 4 g/24 h), last given 12:00, next due 18:00. "
         "Surgical team plan discharge tomorrow if pain controlled."),
 "N08": ("MORETTI, Giuseppe, 72M, day 2 post small bowel resection. NKDA. Full resuscitation. DETERIORATING over the shift: Q-ADDS 0, 2, 5, now 10 at 15:30 "
         "(RR 28, HR 124, BP 94/58, SpO2 91% on 4 L/min NP, T 38.7). MET call 15:40, ICU review requested. Hartmann's 500 mL IV bolus started 15:45. "
         "?Anastomotic leak vs ?sepsis, not confirmed; urgent CT abdomen/pelvis requested, NOT yet done."),
 "N09": ("HUGHES, Linda, 58F, pyelonephritis day 2. ALLERGY: sulfonamides (rash). Full resuscitation. Now FEBRILE with rigors, Temp 38.6 at 15:30, Q-ADDS 3 (was 36.9 at 08:00). "
         "Ceftriaxone 2 g IV given 08:00. RMO review requested 15:40. Repeat blood cultures sent 15:45, pending. Discharge plan on HOLD."),
}
BAD = {
 "N06": "62M with cellulitis. Glargine 20 U at night and NovoRapid 4 U given. NKDA.",
 "N07": "47F day 1 post cholecystectomy. Oxycodone and paracetamol given as needed. NKDA.",
 "N08": "72M post bowel resection, clinically stable, obs within normal limits. NKDA.",
 "N09": "58F with pyelonephritis, afebrile and is afebrile today, plan discharge tomorrow.",
}


def test_good_keeps_every_fact():
    for n, g in GOOD.items():
        _, r = run(n, g)
        assert {k: v for k, v in r["facts"].items() if v != "kept"} == {}, n
        assert r["invented_numbers"] == [] and r["unsafe_notation"] == [], (n, r)


def test_bad_loses_critical_facts():
    for n, b in BAD.items():
        key, r = run(n, b)
        crit = [f["id"] for f in key["facts"] if f["severity"] == "critical"]
        kept = [i for i in crit if r["facts"][i] == "kept"]
        assert len(kept) <= 2, (n, kept)


def test_traps():
    _, r = run("N06", BAD["N06"])
    assert r["facts"]["N06-F1"] != "kept" and r["unsafe_notation"]          # 'U' is flagged and the dose is not accepted
    assert run("N08", BAD["N08"])[1]["facts"]["N08-F4"] == "altered"        # stale 'stable' passed through
    assert run("N09", BAD["N09"])[1]["facts"]["N09-F1"] == "altered"        # stale 'afebrile' beats the 38.6
    assert run("N07", BAD["N07"])[1]["facts"]["N07-F1"] != "kept"           # dose not stated


def test_mutations():
    assert run("N06", GOOD["N06"].replace("20 units", "10 units"))[1]["facts"]["N06-F1"] == "altered"
    assert run("N07", GOOD["N07"].replace("last given 13:10", "last given 09:00"))[1]["facts"]["N07-F4"] != "kept"
    assert run("N08", GOOD["N08"].replace("Q-ADDS 0, 2, 5, now 10", "Q-ADDS 2, now 5"))[1]["facts"]["N08-F1"] != "kept"
    assert run("N08", GOOD["N08"].replace("?Anastomotic leak vs ?sepsis, not confirmed", "Confirmed sepsis"))[1]["facts"]["N08-F6"] == "altered"
    assert run("N09", GOOD["N09"].replace("Discharge plan on HOLD", "Discharge tomorrow"))[1]["facts"]["N09-F5"] != "kept"
