# Q-ADDS scoring reference used for the synthetic notes

Source (read directly): *Clinical Practice Procedures: Assessment / QAS Adult Deterioration Assessment*, Queensland Ambulance Service, policy code CPP_AS_QAD_0326, March 2026, chart page "Adult Q-ADDS v3.00 02/2026". This is the **QAS transfer-of-care version** of the chart for patients delayed offloading at a public hospital; the wards' own Q-ADDS charts are assumed to use the same adult scores but this has not been checked. The PDF is not stored in this repo (licence: CC BY-NC-ND, and it is the owner's upload).

| Parameter | Score 0 | Score 1 | Score 2 | Score 3 | Score 4 | E (emergency call) |
|---|---|---|---|---|---|---|
| Respiratory rate | 13-20 | 9-12, 21-24 | 25-30 | - | 31-35 | at or above 36, at or below 8 |
| SpO2 (%) | 92 and above | 90-91 | 85-89 | - | 84 and below | - |
| Oxygen (L/min) | below 2 | 2-5 | above 5 to 11 | - | above 11 to 14 | 15 |
| Systolic BP | 110-159 | 100s, 160s | 90s, 170s-190s | - | 80s, 200 and above | 70s and below |
| Heart rate | 50-99 | 100-109 | 110-129, 40s | 130-139 | 140-159 | 160 and above, 30s |
| Temperature (C) | 36.1-37.9 | 38.0-38.4, 35.1-36.0 | 38.5 and above, 34.1-35.0 | - | 34.0 and below | - |
| Behaviour / consciousness | Alert | Voice | - | - | Changing behaviour or new confusion | Pain, Unresponsive |

Rule on the chart: a total score of 3 or more means the patient must be reviewed by the Triage Nurse or Nursing Team Leader (and the on-duty supervisor notified); any E means an emergency call.

Check log (scores in every drafted note were recomputed against this table on 25/11/2026):
- N01, N02, N04, N05: all 0, correct.
- N03: corrected to 0, 3, 7 (an earlier reviewer's table scored SpO2 92-94 as 1 and gave 4 and 8; the chart disagrees).
- N06-N09, N10: correct (N10 matches the owner's own 0, 2, 4).
- **N11 (owner's note): the chart gives 1 at 08:00 (2 L/min oxygen = 1; SpO2 94% = 0) and 0 at 12:00 (1 L/min = 0), but the note says 2 and 1.** Left unchanged, for the owner to decide.
