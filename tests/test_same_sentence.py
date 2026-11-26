"""The optional same_sentence constraint on all_of_groups."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from check_facts import check_fact  # noqa: E402

FACT = {"check": {"type": "all_of_groups", "groups": [["inr"], ["pending", "awaiting result"]], "same_sentence": True}}
LOOSE = {"check": {"type": "all_of_groups", "groups": [["inr"], ["pending", "awaiting"]]}}


def test_unrelated_sentence_cannot_vouch():
    s = "69M awaiting colonoscopy tomorrow. INR fine."
    assert check_fact(LOOSE, s) == "kept"        # the old behaviour: a false 'kept'
    assert check_fact(FACT, s) == "lost"         # same-sentence: correctly lost


def test_same_sentence_kept_and_decimals_do_not_split():
    assert check_fact(FACT, "Repeat INR drawn 06:15 is PENDING; target below 1.5.") == "kept"
    assert check_fact(FACT, "Target INR 1.5 and result pending. Warfarin held.") == "kept"
    assert check_fact({"check": {"type": "all_of_groups", "groups": [["38.6"], ["febrile"]], "same_sentence": True}}, "Febrile, temp 38.6 at 15:30.") == "kept"
