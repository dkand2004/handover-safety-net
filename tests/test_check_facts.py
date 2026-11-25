"""Tests for the answer-key checker (all text here is synthetic)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from check_facts import check_summary, invented_numbers, unsafe_notation  # noqa: E402
from validate_keys import validate  # noqa: E402

KEY = json.loads((Path(__file__).resolve().parents[1] / "data/answer_keys/_example_N05.json").read_text())
NOTE = "Chest pain on arrival. ?NSTEMI. Repeat troponin due 0900. Aspirin 300 mg PO given 06:15."
F1, F2, F3 = "N05-F1", "N05-F2", "N05-F3"


def facts(summary):
    return check_summary(KEY, NOTE, summary)["facts"]


def test_good_summary_keeps_everything():
    assert facts("Chest pain, ?NSTEMI (suspected, not confirmed). Repeat troponin pending. Aspirin 300 mg PO given 06:15.") == {F1: "kept", F2: "kept", F3: "kept"}


def test_reworded_summary_is_not_penalised():
    assert facts("Chest pain, NSTEMI queried. Troponin awaited. Aspirin 300mg orally given at 0615 hrs.") == {F1: "kept", F2: "kept", F3: "kept"}


def test_doubt_collapsed_into_certainty_is_altered():
    r = facts("Confirmed NSTEMI. Troponin normal. Aspirin 300 mg given.")
    assert r[F1] == "altered" and r[F2] == "lost" and r[F3] == "kept"


def test_omission_is_lost():
    assert facts("Chest pain, observations stable.") == {F1: "lost", F2: "lost", F3: "lost"}


# ---- MUTATION TESTS: corrupt a good summary on purpose; the checker must notice each corruption ----
GOOD = "Chest pain, ?NSTEMI (suspected). Repeat troponin pending. Aspirin 300 mg PO given 06:15."


def test_mutation_wrong_dose_is_altered():
    for bad in ("600 mg", "30 mg", "3000 mg", "300 mcg", "300 g", "0.3 mg"):
        assert facts(GOOD.replace("300 mg", bad))[F3] == "altered", bad


def test_mutation_dropping_the_drug_is_lost():
    assert facts(GOOD.replace("Aspirin 300 mg PO given 06:15.", ""))[F3] == "lost"


def test_mutation_dropping_pending_is_lost():
    assert facts(GOOD.replace("Repeat troponin pending.", ""))[F2] == "lost"


def test_mutation_removing_doubt_is_altered():
    assert facts("Chest pain, NSTEMI. Repeat troponin pending. Aspirin 300 mg PO.")[F1] == "altered"


def test_two_conflicting_doses_count_as_altered():
    assert facts("Aspirin 300 mg given. Aspirin 600 mg given. ?NSTEMI. Troponin pending.")[F3] == "altered"


# ---- SAFEGUARDS that do not need a fact list ----
def test_invented_dose_number_is_flagged():
    assert invented_numbers(NOTE, "Aspirin 600 mg given.") == [(600.0, "mg")]
    assert invented_numbers(NOTE, "Aspirin 300mg given.") == []


def test_unsafe_notation_is_flagged():
    assert unsafe_notation("Insulin 10 U given") and unsafe_notation("morphine 5.0 mg") and unsafe_notation("digoxin .5 mg")
    assert unsafe_notation("Insulin 10 units given, morphine 5 mg, digoxin 0.5 mg") == []


# ---- THE VALIDATOR must reject malformed keys ----
def _bad(**over):
    k = json.loads(json.dumps(KEY)); k["facts"][0].update(over); return k


def test_validator_accepts_good_and_rejects_bad_keys():
    assert validate(KEY) == []
    assert validate(_bad(check={"type": "approx", "value": "x"}))
    assert validate(_bad(severity="urgent"))
    assert validate(_bad(section="Z"))
    assert validate(_bad(check={"type": "dose", "drug": ["x"], "amount": "300", "unit": "mg"}))


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try: t(); print("PASS", t.__name__)
        except AssertionError as e: failed += 1; print("FAIL", t.__name__, e)
    print(f"\n{len(tests)-failed}/{len(tests)} tests passed"); sys.exit(1 if failed else 0)
