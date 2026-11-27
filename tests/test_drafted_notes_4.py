"""Tests for the Claude-drafted notes N16-N18 (batch 4)."""
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
 "N16": ("NOVAK, Franz, 83M, infective exacerbation of COPD, severe COPD on home oxygen 2 L/min. ALLERGY: amoxicillin (hives). CURRENT ARP: NOT for CPR, completed and signed 26/11/2026. "
         "For MET call and ward-based treatment including NIV; not for intubation or ICU. Oxygen target SpO2 88-92%. Prednisolone 40 mg PO daily. Palliative care review today."),
 "N17": ("BELL, Joan, 81F from aged care, fever and NEW confusion (baseline alert and orientated). Differentials: ?UTI vs ?aspiration pneumonia vs ?delirium, none confirmed. NKDA. Full resuscitation. "
         "Temp 38.1 at 10:00. Urine MC&S and blood cultures sent, PENDING. CXR report PENDING. Ceftriaxone 1 g IV given 11:05 after cultures. High falls risk, delirium and falls precautions."),
 "N18": ("COOPER, William, 74M, AF with rapid ventricular response, on telemetry. ALLERGY: penicillin (rash). Resuscitation plan (ARP) NOT DOCUMENTED. Weight NOT DOCUMENTED. "
         "Metoprolol 25 mg PO given 12:00. Troponin and TFTs PENDING. Cardiology review requested, not yet seen."),
}
BAD = {
 "N16": "83M with COPD, full resuscitation, for full resuscitation at this time. Prednisolone given.",
 "N17": "81F with confirmed UTI and confirmed delirium, on antibiotics.",
 "N18": "74M with AF, for full resuscitation, weight 80 kg. Allergies: penicillin.",
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
    assert run("N16", BAD["N16"])[1]["facts"]["N16-F1"] == "altered"      # stale full resuscitation wins
    f = run("N17", BAD["N17"])[1]["facts"]
    assert f["N17-F1"] == "altered" and f["N17-F3"] == "altered"          # suspected became confirmed
    r = run("N18", BAD["N18"])[1]
    assert r["facts"]["N18-F1"] == "altered" and r["facts"]["N18-F3"] != "kept"   # ARP assumed, weight not flagged
    assert r["invented_numbers"]                                          # 'weight 80 kg' is an invented number


def test_mutations():
    assert run("N16", GOOD["N16"].replace("NOT for CPR", "for full resuscitation"))[1]["facts"]["N16-F1"] == "altered"
    assert run("N17", GOOD["N17"].replace("?UTI", "UTI confirmed"))[1]["facts"]["N17-F1"] == "altered"
    assert run("N17", GOOD["N17"].replace("blood cultures sent, PENDING", "blood cultures normal"))[1]["facts"]["N17-F4"] != "kept"
    assert run("N18", GOOD["N18"].replace("Weight NOT DOCUMENTED.", ""))[1]["facts"]["N18-F3"] == "lost"
