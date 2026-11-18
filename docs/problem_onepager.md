# Problem one-pager (DRAFT: sources partly unverified, see "Evidence status")

## The problem
When care passes between clinicians (shift change, ward transfer, theatre to ward), a large
record is compressed into a short verbal or written handover. Information can be omitted,
altered, made vaguer, or misread in that step. "Miscommunication" is too broad to be useful, so
this project breaks it into specific, testable failure modes.

### Specific failure modes (what goes wrong, why it matters, how this project tests it)
| # | Failure mode | Possible clinical consequence | How it is tested |
|---|---|---|---|
| 1 | **Allergy omitted, or reaction severity lost** ("penicillin" without "anaphylaxis") | A contraindicated drug is prescribed or given | Allergen **and** severity must both appear |
| 2 | **Dose, units or route altered** (mg vs mcg, transposed digits, wrong route) | Overdose or underdose | **Exact match** on dose, unit, route, frequency |
| 3 | **Last-given time lost** | Double dose, or a dose missed | Last-given time must appear |
| 4 | **Recent medication change not carried across** (started, stopped, withheld) | A withheld drug is restarted, or a new one is missed. For example, an anticoagulant held before a procedure | Changes flagged with direction (started / stopped / withheld) |
| 5 | **Deterioration trend lost** (abnormal observations, Q-ADDS trigger, escalation already done) | Delayed recognition and rescue | Trigger score, trend direction and any escalation must appear |
| 6 | **Pending results or tasks dropped** | Delayed diagnosis, repeated tests | Every pending item listed |
| 7 | **Resuscitation status (ARP) missing or wrong** | Inappropriate resuscitation, or none when wanted | ARP status present and correct |
| 8 | **Laterality or site lost** (which eye or limb) | Wrong-site procedure | Side must appear wherever relevant |
| 9 | **Baseline status lost** (cognition, mobility, falls risk) | New confusion or a fall goes unrecognised | Baseline and risk flags present |
| 10 | **Uncertainty collapsed into fact** ("?pneumonia" becomes "pneumonia") | Anchoring on an unconfirmed diagnosis | Items tagged Confirmed / Suspected-Pending / Unverified |
| 11 | **"Not documented" read as "negative"** (no allergy recorded becomes "no allergies") | False reassurance carried to later shifts | Absent information is reported as *not documented*, never as normal or negative |
| 12 | **Vague or subjective language passes through** ("seems fine", "rough night") | Actionable detail is never communicated | Output restates observations as objective values, or flags the gap |
| 13 | **Stale information outranks recent** (an old summary beats a vital-sign drop 20 minutes ago) | Acting on outdated status | Notes with conflicting timestamps: the most recent must win |

## Evidence status
- **Verified (read directly):** WHO *Patient Safety Solutions*, vol. 1, solution 3, "Communication
  During Patient Hand-Overs" (May 2007). It states that breakdown in communication was the leading
  root cause of sentinel events reported to the Joint Commission (US) from 1995 to 2006, and that in
  Australia 11% of 25,000 to 30,000 preventable adverse events causing permanent disability were
  attributed to communication issues. It recommends a standardised approach, including SBAR,
  read-back, and information on status, medications, treatment plans and advance directives.
  *These are historical figures (data to 2006); they are not current statistics.*
- **Not yet verified (could not be read):** Australian Commission on Safety and Quality in Health
  Care, *OSSIE Guide to Clinical Handover Improvement*; BMJ Open Quality 2024;13(2):e002647;
  NCBI Bookshelf NBK259589. **To be checked before relying on them.**
- Blogs and videos are not used as evidence.

## Whose workflow
Nurses and doctors at shift change and ward transfer in a general inpatient ward. Handover is
commonly structured with a framework. WHO recommends **SBAR**; this project uses **iSoBAR**, a
framework used in Australian health services: **I**dentify, **S**ituation, **O**bservations,
**B**ackground, **A**greed plan, **R**ead back. _(Framework origin and use to be cited and verified.)_
See `handover_framework.md`.

## What this project does about it
It does not replace clinical judgement. It asks a narrow, measurable question: **when a handover
summary is generated automatically from a note, which safety-critical details survive, and which
are lost, altered or invented?** Three approaches are compared (each producing an iSoBAR summary) against an answer key:
1. **Rule-based baseline:** simple pattern matching.
2. **LLM only:** Claude summarises the whole note.
3. **Hybrid (approved):** critical fields (allergies, medications, resuscitation status, observation thresholds) extracted by deterministic code, with the LLM writing only the narrative. The reasoning: a language model can smooth over ambiguity or invent details, so facts that cannot be wrong should not pass through it.

## Risks specific to AI summaries (and how the design responds)
| Risk | Design response |
|---|---|
| False certainty: fluent prose hides doubt | Require Confirmed / Suspected-Pending / Unverified tags (failure mode 10) |
| Absent treated as negative | Explicit test notes where a field is missing (failure mode 11) |
| Outdated data prioritised | Test notes with conflicting timestamps (failure mode 13) |
| Over-trust of clean summaries ("automation bias") | Outputs include the supporting source sentence so a reader can verify; the evaluation reports errors that look authoritative |

## Out of scope (deliberately)
Ambient audio capture, integration with a real electronic medical record (for example FHIR), real-time use, any use with real patients.

## Governance and ethics
- **Synthetic data only.** No real notes, patients, staff or hospitals.
- **Not for clinical use.** Software that summarises clinical data may be regulated as a medical device (in Australia, by the TGA). This prototype is not, and must not be used clinically.
- **Privacy:** only synthetic notes may be sent to an external AI service; no real record ever.
- **Human review remains essential.** Real-world use would need clinical governance, privacy assessment and approval, none of which this project has.

## Limits
Small set of hand-written notes; one author's clinical view; not validated by clinicians.
