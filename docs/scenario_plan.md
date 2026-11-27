# Scenario plan for the 18 synthetic ward notes (APPROVED by the owner; notes still to be written)

Every note is **fictional**: fictional patient, fictional hospital, illustrative doses and values (not clinical guidance). Style: a single general-ward note per patient, written the way a Queensland nurse or doctor might document it, including shorthand. **Not a clinical tool.**

Decisions (owner): list approved; second notes added for modes 7, 10 and 11 (N16, N17, N18); **the owner writes N10 and N11** in her own nursing voice; the rest are drafted by Claude and reviewed by the owner.

## The 18 notes

| ID | Scenario | The trap being tested | Failure modes | Who writes |
|---|---|---|---|---|
| N01 | Day 1 after left hip fracture repair, 84 y, mild dementia | LEFT side must survive; high falls risk and baseline confusion; enoxaparin last dose time | 8, 9, 3 | Claude drafts, you review |
| N02 | Day surgery: RIGHT eye cataract, on an anticoagulant | Eye side; anticoagulant withheld (with timing); regular BP drug given this morning | 8, 4, 3 | Claude drafts, you review |
| N03 | Pneumonia, penicillin allergy with a severe reaction | Allergen AND severity (anaphylaxis) must both survive; observations worsening during the shift | 1, 5 | Claude drafts, you review |
| N04 | Admission note that is silent about allergies | The summary must say 'allergies not documented', never 'no known allergies' | 11, 1 | Claude drafts, you review |
| N05 | Chest pain, '?NSTEMI', repeat troponin pending | Suspected must stay suspected; the pending result must be listed | 10, 6 | Claude drafts, you review |
| N06 | Insulin with a sliding scale and a 'U' vs 'units' abbreviation | Exact dose and unit; last dose time; no unit confusion | 2, 3 | Claude drafts, you review |
| N07 | Post-op opioid PRN (as needed) plus regular paracetamol | Exact dose, route, frequency; last given times so a double dose cannot happen | 2, 3 | Claude drafts, you review |
| N08 | Deteriorating patient: Q-ADDS rising over the shift, MET call made | The trend and the escalation must survive; an early note said 'stable' | 5, 13 | Claude drafts, you review |
| N09 | Conflicting times: morning 'afebrile', afternoon 38.6 C | The most recent value must win | 13, 5 | Claude drafts, you review |
| N10 | Vague language: 'rough night, seems a bit better' | Objective values elsewhere in the note must be restated, or the gap flagged | 12 | YOU write (nursing voice) |
| N11 | Not for CPR (ARP documented), baseline dementia, family meeting planned | Resuscitation status and goals of care must be explicit | 7, 9 | YOU write (nursing voice) |
| N12 | Warfarin withheld before a procedure, INR result pending | Change direction (withheld) and the pending result | 4, 6 | Claude drafts, you review |
| N13 | MRSA contact precautions, high falls risk, mobility aid | Isolation and falls risk are safety flags | 9 | Claude drafts, you review |
| N14 | Day 3 urinary catheter (IDC) in situ with removal planned; drain output charted | Planned task and device status must not drop out | 6 | Claude drafts, you review |
| N15 | Messy shorthand note: abbreviations, typos, mixed units | Robustness: the critical facts survive untidy wording | 2, 5, 12 | Claude drafts, you review |
| N16 | ARP changed from full resuscitation to Not for CPR yesterday; an older entry still says full | The CURRENT ARP must win | 7, 13 | Claude drafts, you review |
| N17 | Confusion and fever: '?UTI vs ?aspiration vs ?delirium', cultures sent | Differentials stay as possibilities; pending cultures listed | 10, 6 | Claude drafts, you review |
| N18 | Admission note silent on resuscitation plan and weight | 'ARP not documented' and 'weight not documented', never assumed | 11, 7 | Claude drafts, you review |

## Coverage check (verified by script)
All 13 failure modes are covered; every mode now has at least 2 notes.

| # | Failure mode | Notes |
|---|---|---|
| 1 | Allergy omitted / severity lost | N03, N04 |
| 2 | Dose, units or route altered | N06, N07, N15 |
| 3 | Last-given time lost | N01, N02, N06, N07 |
| 4 | Recent medication change not carried across | N02, N12 |
| 5 | Deterioration trend lost | N03, N08, N09, N15 |
| 6 | Pending results or tasks dropped | N05, N12, N14, N17 |
| 7 | Resuscitation status (ARP) missing or wrong | N11, N16, N18 |
| 8 | Laterality / site lost | N01, N02 |
| 9 | Baseline status lost (cognition, mobility, falls risk) | N01, N11, N13 |
| 10 | Uncertainty collapsed into fact | N05, N17 |
| 11 | "Not documented" read as "negative" | N04, N18 |
| 12 | Vague or subjective language passes through | N10, N15 |
| 13 | Stale information outranks recent | N08, N09, N16 |

## Status (27/11/2026): all 18 notes drafted; N16-N18 awaiting owner review

## Next steps
1. Owner approves the answer-key format (`answer_key_format.md`).
2. Owner writes N10 and N11 using the template in the chat; Claude drafts N01 to N09 and N12 to N18.
3. Pilot first: N05, N10 and N11 with answer keys, then the rest.
