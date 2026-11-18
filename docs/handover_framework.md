# Handover framework: ISOBAR (as defined in the OSSIE Guide)

This project structures each handover summary with **ISOBAR**, defined in the Australian Commission
on Safety and Quality in Health Care's OSSIE Guide (2010). The column "Our critical elements" is
this project's own mapping and is a reasoned hypothesis, not something the guide prescribes.

| Letter | OSSIE definition (paraphrased) | Our critical elements placed here | How produced |
|---|---|---|---|
| **I**dentification | Correctly identify the patient using three identifiers (e.g. name, date of birth, medical record number) | Synthetic name, DOB, URN, ward | Deterministic |
| **S**ituation and status | Conditions being treated (or a clear statement that the diagnosis is unknown); current status (stable, deteriorating, improving); advance directives; patient-centred requirements | Reason for admission, ARP / resuscitation status, uncertainty tags (Confirmed / Suspected-Pending / Unverified) | Mixed |
| **O**bservation | The latest observations and **when they were taken**; a check that identifies deteriorating patients for emergency response | Vital signs with timestamps, Q-ADDS score and trend, whether escalation occurred | Deterministic values |
| **B**ackground and history | Presenting problem, background problems, current issues; findings and current diagnosis; management to date and whether it is working | Comorbidities, baseline status, allergies and reaction severity, medications (drug, dose, units, route, last given, recent changes), laterality, falls and pressure-injury risk | Mixed (critical facts deterministic) |
| **A**ssessment and actions | Clinician's assessment and actions | Narrative assessment and recommended actions | LLM or rules |
| **R**esponsibility and risk management | Tasks, abnormal or pending results clearly communicated; agreed management and escalation plan; transfer of responsibility accepted by the incoming team | Pending results and tasks, who does what and by when, escalation plan | Narrative with pending items listed |

## Read-back checklist (a feature, not a letter)
WHO and OSSIE both describe **read-back** (the receiver repeats critical information to confirm it was
understood). Software cannot do this for a nurse, so the tool ends each summary with a short checklist
of high-risk items for the receiving clinician to read back and tick off.

## Note on variants
OSSIE also describes **iSoBAR**, a variant developed in a Western Australian project, where the
final letters stand for *Agree to a plan* and *Readback*. This project follows the OSSIE **ISOBAR** definition above.
