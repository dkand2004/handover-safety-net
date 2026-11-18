# Handover Safety Net

> NLP handover assistant that turns synthetic clinical notes into SBAR summaries and checks whether safety-critical details survive.

**Status:** 🚧 In progress (started 18 Nov 2026).

## The healthcare problem
_To be written (see `docs/problem_onepager.md`): information is lost or distorted when care is handed over between clinicians._

## What this project does
1. Takes a **synthetic** clinical note and produces an **ISOBAR** handover summary
   (Identification, Situation and status, Observation, Background and history, Assessment and actions,
   Responsibility and risk management), the framework defined in the Australian OSSIE Guide (ACSQHC, 2010).
2. Does this three ways: a **rule-based** baseline, a **Claude API** version, and a **hybrid** (code extracts critical facts, Claude writes only the narrative).
3. Runs an automatic **safety-critical element check**: did the summary keep allergies, resuscitation
   status, falls risk, anticoagulants, a deterioration (Q-ADDS) trigger, and, for eye surgery, the correct eye?
4. Compares the three methods on how often critical items are kept, altered or lost.

## Safety, privacy and ethics
- **Synthetic notes only.** No real patient data, no real hospital names, no screenshots of real systems.
- **Not a clinical tool.** A research and portfolio prototype; it must never be used for real patient care.
- AI summaries can omit or invent details. The point of this project is to *measure* that, not to hide it.
- API keys live only in `.env` (ignored by Git).

## Repo structure
| Folder | Purpose |
|---|---|
| `data/synthetic_notes/` | Hand-written fictional clinical notes |
| `data/answer_keys/` | The safety-critical facts each note contains (ground truth) |
| `src/` | Rule-based baseline, Claude summariser, evaluation |
| `results/` | Evaluation outputs |
| `docs/` | One-pager, critical-elements list, ethics notes |
| `tests/` | Tests for the evaluation logic |

## How to run
_To be written._

## Licence
MIT, see [LICENSE](LICENSE).
