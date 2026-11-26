"""Tests for the Claude-drafted notes N12-N15 (batch 3)."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from check_facts import check_summary  # noqa: E402


def run(n, s):
    key = json.loads((ROOT / f"data/answer_keys/{n}.json").read_text())
    note = (ROOT / f"data/synthetic_notes/{n}.md").read_text()
    return key, check_summary(key, note, s)


GOOD = {
 "N12": ("PETERSEN, Alan, 69M, admitted for colonoscopy with polypectomy on 27/11 at 08:00. Atrial fibrillation on warfarin. NKDA. Full resuscitation. "
         "Warfarin HELD, last dose 21/11 (evening), do not give tonight. Repeat INR drawn 06:15 is PENDING; target INR below 1.5. Proceduralist to advise when to restart warfarin. NBM from midnight."),
 "N13": ("WALSH, Eileen, 79F, infected sacral pressure injury, stage 3. MRSA CONTACT PRECAUTIONS: single room 12, gown and gloves. ALLERGY: latex (contact dermatitis), use nitrile gloves. "
         "HIGH falls risk, bed alarm on; mobilises with 4WW and 1 assist. Doxycycline 100 mg PO BD, last given 08:00. Full resuscitation. Wound care nurse review 27/11."),
 "N14": ("DIMITROV, Katarina, 68F, Day 3 post total abdominal hysterectomy. NKDA. Full resuscitation. Urinary catheter (IDC) in situ, urine 1450 mL over 24 h; IDC removal planned 27/11 at 06:00, "
         "then trial of void with a bladder scan if no void in 6 hours. Redivac drain in situ, 30 mL serous over 24 h; surgical team to review the drain tomorrow."),
 "N15": ("MCKENZIE, Ray, 77M, decompensated heart failure, AF. NKDA. Full resuscitation. Breathlessness WORSE this afternoon: Q-ADDS 1 at 08:00, now 6 at 14:00 (RR 26, SpO2 91% RA, HR 112, BP 100/60). "
         "O2 2 L/min NP started 15:00. Furosemide 40 mg IV BD, last given 14:00. K 3.4, repeat UEC at 06:00 tomorrow. Fluid restriction 1.5 L. Weight 82 kg (85.5 kg on admission). RMO Dr Lee informed, review awaited."),
}
BAD = {
 "N12": "69M awaiting colonoscopy tomorrow. On warfarin. INR fine. NKDA.",
 "N13": "79F with a sacral wound, on doxycycline. Mobilises independently. NKDA.",
 "N14": "68F day 3 after hysterectomy, doing well, mobilising.",
 "N15": "77M with heart failure, feels much better after furosemide, clinically stable. NKDA.",
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
    assert run("N12", BAD["N12"])[1]["facts"]["N12-F3"] != "kept"          # pending INR dropped
    assert run("N13", BAD["N13"])[1]["facts"]["N13-F1"] != "kept"          # MRSA precautions dropped
    assert run("N14", BAD["N14"])[1]["facts"]["N14-F2"] != "kept"          # IDC removal plan dropped
    assert run("N15", BAD["N15"])[1]["facts"]["N15-F6"] == "altered"       # vague/subjective passes through


def test_mutations():
    bad = GOOD["N12"].replace("Warfarin HELD, last dose 21/11 (evening), do not give tonight", "Warfarin continued, last dose 21/11 (evening)")
    f = run("N12", bad)[1]["facts"]
    assert f["N12-F1"] != "kept" and f["N12-F11"] == "altered"
    assert run("N13", GOOD["N13"].replace("doxycycline 100 mg", "doxycycline 200 mg").replace("Doxycycline 100 mg", "Doxycycline 200 mg"))[1]["facts"]["N13-F6"] == "altered"
    assert run("N14", GOOD["N14"].replace("IDC removal planned 27/11 at 06:00, ", ""))[1]["facts"]["N14-F2"] != "kept"
    assert run("N15", GOOD["N15"].replace("40 mg", "4 mg"))[1]["facts"]["N15-F1"] == "altered"
