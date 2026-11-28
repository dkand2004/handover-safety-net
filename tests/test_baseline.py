"""Tests for the rule-based baseline (arm 1)."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from baseline import summarise  # noqa: E402


def s(n):
    return summarise((ROOT / f"data/synthetic_notes/{n}.md").read_text())


def test_baseline_never_reads_answer_keys():
    code = (ROOT / "src/baseline.py").read_text()
    assert "answer_keys" not in code.replace("never read the answer keys", "") and ".json" not in code   # leakage guard


def test_not_documented_is_said_not_assumed():
    t = s("N18")
    assert "Resuscitation / ARP: not documented" in t and "Weight: not documented" in t
    assert "Allergies: not documented" in s("N04")


def test_label_variants_still_found():
    assert "maculopapular" in s("N11")               # N11's banner says 'ALLERGIES', not 'ALLERGIES / ADVERSE REACTIONS'


def test_has_every_isobar_section_and_is_shorter_than_note():
    for n in ("N05", "N10", "N16"):
        t = s(n)
        for h in ("I - ", "S - ", "O - ", "B - ", "A - ", "R - "):
            assert h in t
        assert len(t.split()) < len((ROOT / f"data/synthetic_notes/{n}.md").read_text().split())


def test_known_baseline_limits_are_real():
    assert "full resuscitation" in s("N16").lower()   # naive rules copy the stale 25/11 entry
    assert "much better" in s("N15").lower()           # and the subjective quote
