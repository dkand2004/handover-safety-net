"""Pilot tests for N05: a faithful summary keeps every fact; collapsed / wrong / incomplete summaries are caught."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from check_facts import check_summary  # noqa: E402

KEY = json.loads((ROOT / "data/answer_keys/N05.json").read_text())
NOTE = (ROOT / "data/synthetic_notes/N05.md").read_text()

GOOD = ("TAYLOR, Robert, 63M, Medical Ward 3C bed 8. Central chest pain, ?NSTEMI, not yet confirmed; differentials include unstable angina and musculoskeletal pain. "
        "NKDA. Pain-free since 23:10. ECG: ST depression V5-V6. First hs-troponin 28 ng/L (ref <14). Aspirin 300 mg PO given 23:15; GTN 400 mcg SL given 22:50. "
        "On telemetry, sinus rhythm. Repeat hs-troponin drawn 01:45 is PENDING; cardiology reg Dr Okafor to review once back. Bloods due 06:00, NBM from 04:00.")
# Typical failure: suspected becomes confirmed, pending result becomes 'normal', pain/ECG/telemetry dropped.
COLLAPSED = "63M with confirmed NSTEMI. Troponin normal. Aspirin 300 mg given. No known allergies."
WRONG_DOSE = GOOD.replace("Aspirin 300 mg", "Aspirin 150 mg")
NO_PENDING = GOOD.replace("is PENDING; cardiology reg Dr Okafor to review once back", "was done")


def res(s):
    return check_summary(KEY, NOTE, s)


def test_good_keeps_every_fact():
    r = res(GOOD)
    assert {k: v for k, v in r["facts"].items() if v != "kept"} == {}
    assert r["invented_numbers"] == [] and r["unsafe_notation"] == []


def test_collapsed_summary_loses_critical_facts():
    f = res(COLLAPSED)["facts"]
    assert f["N05-F1"] != "kept"      # suspected -> confirmed
    assert f["N05-F3"] != "kept"      # pending troponin lost
    kept_crit = [x["id"] for x in KEY["facts"] if x["severity"] == "critical" and f[x["id"]] == "kept"]
    assert kept_crit == ["N05-F7", "N05-F10"]  # only aspirin dose and NKDA survive


def test_wrong_dose_is_altered():
    assert res(WRONG_DOSE)["facts"]["N05-F7"] == "altered"


def test_pending_lost_when_result_not_marked_pending():
    f = res(NO_PENDING)["facts"]
    assert f["N05-F3"] != "kept" and f["N05-F4"] != "kept"


def test_suspected_tag_survives_when_doubt_in_same_sentence():
    assert res("Chest pain, ?NSTEMI.")["facts"]["N05-F1"] == "kept"
    assert res("Suspected NSTEMI, awaiting repeat troponin.")["facts"]["N05-F1"] == "kept"
