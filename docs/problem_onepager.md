# Problem one-pager (DRAFT: not yet reviewed or cited)

## The problem
When care passes between clinicians (shift change, ward transfer, theatre to ward), information
is summarised from a large record into a short verbal or written handover. Details can be
dropped, altered or misunderstood in that step. The failures that cause the most harm are:

1. **Medication dosage errors**: wrong dose, units, route or timing, or "last dose given" not communicated.
2. **Allergy errors**: an allergy or reaction severity not carried across the handover.
3. **Miscommunication**: ambiguous, incomplete or inconsistent information, including shorthand read differently by different people.

_Evidence to add: Australian Commission on Safety and Quality in Health Care (NSQHS Standards:
Communicating for Safety; Medication Safety), Queensland Health clinical handover guidance,
peer-reviewed studies on handover information loss. [citations needed, to be verified before publishing]_

## Whose workflow
Nurses and doctors at shift change and transfer in an inpatient setting. Handover is commonly
structured with a framework; **SBAR** (Situation, Background, Assessment, Recommendation) is used
in this project. Australian services also commonly use **ISBAR**, which adds an *Identify* step
(confirming who the patient is). _Decision pending: whether to add the "I" step._

## What this project does about it
It does not try to replace clinical judgement. It asks a narrower, testable question:
**when a handover summary is generated automatically from a note, which safety-critical details
survive?** It measures this against an answer key for each synthetic note, comparing a Claude-based
summariser with a simple rule-based baseline.

## Why this evaluation
Summaries are usually judged on how well they read. Harm comes from what is *missing or wrong*.
The check is therefore built around critical elements (allergy, medication dose, resuscitation
status, falls risk, deterioration score, laterality) and is strict: a dose must match exactly.

## Clinical, ethical and privacy considerations
- **Synthetic data only.** No real notes, patients, staff or hospitals.
- **Not for clinical use.** A prototype for learning and portfolio purposes.
- **AI can omit or invent.** The evaluation exists to expose this, and findings must not be overstated.
- **Human review remains essential.** Any real-world use would need clinical governance, privacy
  assessment and approval, none of which this project has.
- **Data handling.** Notes sent to an external AI service must be synthetic; no real record should ever be sent.

## Limits
Small set of hand-written notes; one author's clinical view; not validated by clinicians.
