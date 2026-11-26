# Answer-key format, version 2 (approved in principle by the owner; revised after testing)

Each synthetic note has one JSON file in `data/answer_keys/` listing the **critical facts** that must survive in a handover summary. `src/check_facts.py` scores each fact for each approach (rule-based, Claude only, hybrid) as **kept**, **altered** (present but wrong) or **lost**.

## Why version 2 (what testing showed)
Version 1 matched literal text. On five hand-written summaries of one pilot note it agreed with a careful reader on **10 of 15** checks (66%), because it failed on rewording ("awaited" vs "pending", "300mg" vs "300 mg") and could not tell a **wrong** dose from a **missing** one. Version 2 agreed on 15 of 15. That is a small demonstration written by the same author, **not validation**; real validation needs actual model outputs plus a human spot-check.
Mutation tests then found a flaw in the first v2 draft (a doubt marker from a *different* sentence wrongly vouched for a diagnosis). It is fixed and has a regression test.

## Structure
```json
{"id": "N05-F3", "category": "medication", "section": "B", "severity": "critical",
 "description": "Aspirin 300 mg, exact dose and unit",
 "check": {"type": "dose", "drug": ["aspirin"], "amount": 300, "unit": "mg"}}
```
`severity` is **critical** (harm if lost: allergy, dose, resuscitation status, laterality, deterioration) or **important**. Results are reported for critical facts separately.

## Check types
| Type | Kept when | Altered when | Lost when |
|---|---|---|---|
| `all_of_groups` (groups of acceptable wordings, AND of ORs; optional `"same_sentence": true`) | every group has a wording present (with `same_sentence`: inside one sentence) | n/a | a group is missing |
| `dose` (drug, amount, unit) | the number and unit next to the drug match exactly | a different number or unit is next to the drug (also if two conflicting doses appear) | the drug or its dose is absent |
| `tag` (target terms, tag, forbid) | the target appears with a doubt/certainty marker **in the same sentence** | a "forbid" phrase appears, or the target appears without the marker | the target is absent |
| `none_of` (phrases) | none appear | one appears (for example "no known allergies" when allergies are not documented) | n/a |
| `latest_wins` (value wordings, stale wordings) | the recent value appears and the stale one does not | the stale value appears | neither appears |
| `exact` | the text appears after normalisation (times, identifiers) | n/a | it is absent |

Text is normalised before matching (case, spacing, "300mg" to "300 mg", "µg/ug" to mcg, "6:15" and "0615 hrs" to 06:15).

## Derived (conditional) checks
A key may contain a `derived` list: **IF** one of `if_phrases` appears in the summary, **THEN** the listed facts must also be kept. If not, the result is "altered". Example (N10): a subjective phrase such as "feels better" is allowed only when the critical objective values (Q-ADDS, heart rate and respiratory rate, temperature) are also kept, so a vague phrase never stands alone.

## Safeguards that do not depend on the fact list
- **Invented numbers:** any dose-like number in the summary that is not in the source note is flagged.
- **Unsafe notation:** "U" for units, trailing zeros ("5.0 mg") and missing leading zeros (".5 mg") are flagged.
- **Mutation tests:** good summaries are deliberately corrupted (wrong dose, wrong unit, dropped drug, removed doubt) and the checker must catch each corruption.
- **Validator:** `src/validate_keys.py` rejects malformed keys (tested against deliberately bad ones).
Run everything with `python tests/test_check_facts.py` (12 tests) and `python tests/test_owner_notes.py` (4 tests).

## Known limits and open decisions
1. **Free-text matching stays approximate.** The most fragile checks are the doubt/certainty (`tag`) ones, because the sentence-level rule is a heuristic. **Decision for the owner:** have each approach return **structured output** (each item with a field `certainty`), so the check becomes a field comparison and not a text search. Recommended, because it removes the fragility and also makes "which section did it go in" measurable.
2. **Human spot-check.** Review a sample (suggest 10%) of kept/altered/lost decisions by hand, and report the agreement rate.
3. **Repeated runs.** Model output varies; run each note a few times (for example 3) and report consistency.
4. **Placeholder keys:** `_example_N05.json` is illustrative only.
