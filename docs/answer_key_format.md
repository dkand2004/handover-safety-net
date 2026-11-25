# Answer-key format (PROPOSED: needs the owner's approval)

Each synthetic note has one JSON file in `data/answer_keys/` listing the **critical facts** that must survive in a handover summary. The evaluation checks each fact against each approach's output (rule-based, Claude only, hybrid).

## Structure
```json
{
  "note_id": "N05",
  "failure_modes": [10, 6],
  "facts": [
    {"id": "N05-F1", "category": "uncertainty", "section": "S",
     "description": "NSTEMI is suspected, not confirmed",
     "check": {"type": "tag", "target": "NSTEMI", "tag": "Suspected-Pending"}}
  ]
}
```
- `failure_modes`: which of the 13 failure modes this note tests (see `problem_onepager.md`).
- `section`: the ISOBAR section where the fact belongs (I, S, O, B, A, R).
- `category`: allergy, medication, last_given, med_change, deterioration, pending, arp, laterality, baseline, uncertainty, not_documented, objective_value, isolation, device.

## The five check types
| Type | Passes when | Typical use |
|---|---|---|
| `exact` | the exact string appears (no "nearly right") | doses, units, times |
| `all_of` | every listed string appears | allergen **and** severity; "troponin" and "pending" |
| `none_of` | none of the listed strings appears | "no known allergies" when allergies are not documented |
| `tag` | the named item carries the tag Confirmed, Suspected-Pending or Unverified | uncertainty kept visible |
| `latest_wins` | the most recent value appears and the stale value does not | conflicting timestamps, changed resuscitation plan |

## Safeguards
`src/validate_keys.py` checks every key before it is used (required fields, known check types, unique ids, failure modes 1 to 13, valid sections). It was tested against both a valid example and five deliberately malformed keys, which it rejected. `data/answer_keys/_example_N05.json` is an **illustration only**.

## Known limits (to decide)
- String matching is literal. A summary that says "troponin level awaited" would fail `all_of ["troponin","pending"]`. Options: allow synonym lists per fact, or add a small human check on disagreements.
- Counting "kept, altered or lost" needs a rule for "altered" (for example a dose that is present but different). `exact` plus a `none_of` list of wrong variants covers the main cases.
