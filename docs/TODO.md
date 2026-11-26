
## Learning guide (requested by the owner)
- [ ] Write `docs/how_it_works.md`: a plain-language teaching guide to Project 2 (ISOBAR, the 13 failure modes, the three arms, the safety-critical checks, likely questions with answers, glossary). Design version written; **complete each [TO COMPLETE] section as it is built** (prompts, hybrid split, scoring code, results).

## Demo video (stretch, only if time allows)
- [ ] One short video (about 3 minutes) for ONE scenario: a single synthetic ward note passed through the three arms (rule-based, Claude only, hybrid), then the critical-element check showing which items each kept or lost. Highlight one failure, for example "not documented" turned into "no known allergies".
- Synthetic notes only; no real hospital names; do not show `.env` or the API key.

## Project 2 build plan
- [x] `docs/scenario_plan.md` approved: 18 notes (second notes N16 to N18 added); owner writes N10 and N11
- [x] Answer-key format v2 approved in principle and tested (`docs/answer_key_format.md`, `src/check_facts.py`, 12 tests)
- [x] Decided: structured outputs with a `certainty` field per item; targeted human review (all 'altered', critical disagreements between approaches, ~10 random 'kept'); run each note once and repeat 3x on 4 notes
- [x] Owner wrote N10 and N11 (`data/synthetic_notes/`); keys converted and tested (`data/answer_keys/`, `tests/test_owner_notes.py`)
- [x] Owner's N10/N11 review decisions applied (N11 stamp 12:30, ARP wording, ARP in S, codeine intolerance, dated 22:00 row, derived check for vague phrases)
- [x] Pilot: N05, N10 and N11 with answer keys (N05 clinically reviewed by the owner and updated)
- [ ] Remaining notes and keys: N01-N15 drafted; N12-N15 awaiting owner review; N16-N18 still to draft
- [ ] Rule-based baseline, Claude arm, hybrid arm, scoring, tests, results
