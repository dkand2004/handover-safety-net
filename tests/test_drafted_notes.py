"""Tests for the Claude-drafted notes N01-N04: a faithful summary keeps every fact; typical failure summaries are caught."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from check_facts import check_summary  # noqa: E402


def load(n):
    return json.loads((ROOT / f"data/answer_keys/{n}.json").read_text()), (ROOT / f"data/synthetic_notes/{n}.md").read_text()


GOOD = {
 "N01": ("BRENNAN, Dorothy, 84F, Orthopaedic Ward 5A bed 3. Day 1 post LEFT hemiarthroplasty for fractured neck of femur, LEFT hip. NKDA. Full resuscitation. "
         "Mild dementia, intermittently confused, HIGH falls risk: bed alarm on, 2 staff assist, WBAT. Enoxaparin 40 mg SC last given 06:00, next due 06:00 26/11. "
         "Oxycodone IR 2.5 mg PO PRN last 11:30. Orthogeriatric review PENDING."),
 "N02": ("NGUYEN, Peter, 71M, day surgery for RIGHT eye cataract extraction. NKDA. Full resuscitation. Apixaban WITHHELD per anaesthetist, last dose 23/11 20:00; "
         "surgeon plans to recommence apixaban on 26/11 at 08:00 if no bleeding. Amlodipine 5 mg given 07:00. RIGHT eye pad and shield stay on. Discharge 14:00 with an adult escort."),
 "N03": ("SANDHU, Priya, 66F, LLL pneumonia. ALLERGY: PENICILLIN, ANAPHYLAXIS. Full resuscitation. Obs worsening over the shift: RR 28, SpO2 91% RA, HR 118, Temp 38.9. "
         "O2 2 L/min NP started 14:15. Moxifloxacin 400 mg IV daily, last given 09:30 24/11. Medical RMO informed 14:10, review awaited. Blood and sputum cultures sent, pending."),
 "N04": ("FLETCHER, Margaret, 78F, AKI with dehydration. Allergies NOT DOCUMENTED (unknown, to be obtained from family or GP). Full resuscitation. History limited and medications unverified. "
         "Ramipril and metformin HELD. Hartmann's 1 L IV over 4 h from 15:00. Ondansetron 4 mg IV given 14:45. Repeat UEC due 20:00, pending. Strict fluid balance chart."),
}
BAD = {
 "N01": "84F day 1 post hip repair on the RIGHT hip. No known allergies. Doing well.",
 "N02": "71M had cataract surgery on the left eye. Apixaban given as usual. NKDA.",
 "N03": "66F with pneumonia, stable, mild penicillin intolerance. Antibiotics given.",
 "N04": "78F with AKI. NKDA. Fluids running.",
}


def run(n, s):
    key, note = load(n)
    return key, check_summary(key, note, s)


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


def test_specific_traps():
    assert run("N01", BAD["N01"])[1]["facts"]["N01-F2"] == "altered"          # wrong side
    assert run("N02", BAD["N02"])[1]["facts"]["N02-F1"] != "kept"             # eye side lost
    assert run("N03", BAD["N03"])[1]["facts"]["N03-F3"] == "altered"          # anaphylaxis softened
    assert run("N04", BAD["N04"])[1]["facts"]["N04-F1"] == "altered"          # unknown became NKDA
    assert run("N04", BAD["N04"])[1]["facts"]["N04-F2"] != "kept"


def test_mutations():
    # Dose changed -> altered; withheld -> given; allergy statement removed.
    assert run("N01", GOOD["N01"].replace("40 mg", "20 mg"))[1]["facts"]["N01-F3"] == "altered"
    assert run("N02", GOOD["N02"].replace("WITHHELD", "given"))[1]["facts"]["N02-F3"] != "kept"
    assert run("N03", GOOD["N03"].replace("ANAPHYLAXIS", "rash"))[1]["facts"]["N03-F2"] != "kept"
    assert run("N04", GOOD["N04"].replace("Ramipril and metformin HELD", "Ramipril and metformin continued"))[1]["facts"]["N04-F4"] != "kept"
