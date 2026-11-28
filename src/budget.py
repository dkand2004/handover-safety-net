"""Word budget shared by every arm: a summary may use at most 40% of the note's words, rounded down to a multiple of 5.

Words are plain space-separated tokens, headings included. The draft banner line ('# N05 (drafted by ...)') is
not part of the note and is not counted. Decided with the owner on 28/11/2026.
"""
import re

SHARE = 0.40


def note_words(note: str) -> int:
    return len(re.sub(r"^# .*\n", "", note, count=1).split())


def budget_for(note: str) -> int:
    return int(SHARE * note_words(note)) // 5 * 5


def words(summary: str) -> int:
    return len(summary.split())
