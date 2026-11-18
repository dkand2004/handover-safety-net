# Handover framework: iSoBAR (DRAFT)

| Step | Meaning | Critical elements that belong here | Automated? |
|---|---|---|---|
| **I**dentify | Who is the patient, who is handing over | Name/URN (synthetic), ward, allergies and alerts banner, ARP status | Yes (deterministic) |
| **S**ituation | Why they are here, what is happening now | Reason for admission, current concern | Narrative (LLM or rules) |
| **O**bservations | Vital signs and trends | Q-ADDS score and trend, abnormal observations, escalation done | Yes (deterministic values) |
| **B**ackground | Relevant history | Comorbidities, baseline cognition/mobility, falls and pressure-injury risk, medications (drug, dose, units, route, last given, recent changes), laterality | Mixed |
| **A**greed plan | What happens next | Pending results and tasks, who does what, by when | Narrative with pending items listed |
| **R**ead back | Receiver confirms what they heard | Checklist of high-risk items to confirm | **Human step.** The tool only presents the checklist |

Source note: WHO (2007) recommends SBAR; iSoBAR is an Australian framework. Citations to be added and verified.
