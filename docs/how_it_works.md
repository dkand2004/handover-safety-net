# How Project 2 works: a teaching guide (design first; completed as we build)

Status: the **design is settled**; the code, notes and results are **not built yet**. Sections marked
**[TO COMPLETE]** get filled in as each piece is built. Everything here is **synthetic**; this is **not a clinical tool**.

---

## 1. The one-minute version
When a nurse hands over a patient at shift change, a long record is squeezed into a short summary. Important details
can be lost, changed or misread. This project builds a prototype that **turns a synthetic clinical note into a structured
handover summary**, and then **measures which safety-critical details survived**. The novelty is in the measuring:
most tools are judged on how well the summary reads, but harm comes from what is missing or wrong.

Say it like this: *"I didn't just build a summariser. I built a way to test whether the summary keeps the details that
cause harm when they are lost, and compared three approaches."*

---

## 2. The problem, in specific terms
"Miscommunication" is too vague to test, so we break it into 13 specific failure modes (full table in
`problem_onepager.md`). The most important ones:
| Failure mode | Why it matters |
|---|---|
| Allergy omitted or severity lost ("penicillin" without "anaphylaxis") | A contraindicated drug could be given |
| Dose, units or route altered (mg vs mcg) | Overdose or underdose |
| Last-given time lost | Double dose or missed dose |
| Deterioration trend lost (Q-ADDS) | Delayed rescue |
| Resuscitation status missing | Wrong response in an emergency |
| Wrong side (eye or limb) | Wrong-site procedure |
| Doubt turned into fact ("?pneumonia" becomes "pneumonia") | Anchoring on an unconfirmed diagnosis |
| "Not documented" read as "negative" | False reassurance |

---

## 3. What the evidence says (and doesn't)
Three sources were read directly and are cited in `problem_onepager.md`:
- **OSSIE Guide (ACSQHC, 2010):** handover failures are "a major preventable cause of patient harm"; defines ISOBAR; says the evidence base is limited.
- **WHO (2007):** communication breakdown was the leading root cause of sentinel events reported to the Joint Commission (US) from 1995 to 2006. These figures are historical.
- **BMJ Open Quality (2024, BRIEF-C):** structured tools help; keeping differential diagnoses visible supports our uncertainty tagging. One Canadian hospital, no comparison group.

**Honest limits:** none of them discusses allergies, and the OSSIE Guide itself says nobody knows which handover items
matter most. So **our list of critical elements is a reasoned hypothesis, not an evidence-based standard.**

---

## 4. The framework: ISOBAR
From the OSSIE Guide. Each summary has six parts:
| Letter | Meaning | What we put there |
|---|---|---|
| **I** | Identification (three identifiers) | Name, DOB, URN (all synthetic), ward |
| **S** | Situation and status | Why they are here, current status, resuscitation status, how certain each diagnosis is |
| **O** | Observation | Latest observations with times, Q-ADDS score and trend |
| **B** | Background and history | History, baseline status, allergies, medications, side, risks |
| **A** | Assessment and actions | The clinician's assessment and actions |
| **R** | Responsibility and risk management | Pending results and tasks, escalation plan |

A **read-back checklist** is added at the end. Read-back (the receiver repeats critical items) is a human step; the
tool only presents the checklist.

---

## 5. The three approaches we compare
| Approach | How it works | Strength | Weakness |
|---|---|---|---|
| **1. Rule-based baseline** | Simple pattern matching pulls out the facts | Predictable, free, explainable | Brittle with unusual wording |
| **2. Claude only** | A language model (via an API) writes the whole summary | Flexible, reads messy notes | Can smooth over doubt or invent details |
| **3. Hybrid** | Code extracts the critical facts exactly; the model writes only the narrative | Critical facts cannot be "hallucinated" | More work to build |

The hybrid follows a principle from safety engineering: **do not pass facts that cannot be wrong through a
component that sometimes is.**

**[TO COMPLETE]** exact prompts, the model chosen, and how the hybrid splits the work.

---

## 6. How we measure it
1. Each synthetic note has an **answer key** listing the critical facts it contains (ground truth).
2. Each approach produces a summary. We check, fact by fact, whether the summary kept it.
3. **Strict rules:** a dose must match **exactly** (a nearly right dose is still wrong); "not documented" must never
   become "negative"; suspected items must stay marked suspected; when notes conflict in time, the most recent wins.
4. We report, per approach and per failure mode, how often each fact was kept, altered or lost.

**[TO COMPLETE]** the scoring code, tests, and results table.

---

## 7. Setup facts
- **API key:** a password that lets your code call the model. It lives only in a private `.env` file that Git ignores.
- **Synthetic notes only** may ever be sent to the model.
- A model call costs a small amount per note; 15 to 20 notes is cheap.

---

## 8. Limits (so far)
- A small set of hand-written notes, written by one person.
- Not validated by clinicians.
- Our critical-elements list is a hypothesis.
- Not a medical device and must never be used on real patients.

---

## 9. Questions you might be asked (answers valid now)
**What problem does this solve?** Information loss in clinical handover. Specifically, I measure whether critical
details survive automatic summarisation.

**Why compare three approaches?** To show where an AI helps and where it can hurt. A rule-based baseline gives the
floor, and the hybrid tests whether keeping critical facts out of the model's hands is worth the extra work.

**Why ISOBAR and not SBAR?** SBAR is recommended by WHO, but ISOBAR, defined in the Australian OSSIE Guide, adds
Identification and Observation, which matter for patient safety (stale observations were found to be frequently
handed over).

**Is this safe to use in a hospital?** No. It is a prototype on synthetic data. A real system would need clinical
governance, privacy assessment and, in Australia, possibly regulation as a medical device by the TGA.

**How do you know your critical elements are the right ones?** I don't. The OSSIE Guide itself says the evidence on
which handover items matter most is limited. The list is my reasoned hypothesis from the literature and my
experience as a student nurse.

**What is a hallucination?** When a language model states something that is not in the source, with confidence.

**What does "deterministic vs probabilistic" mean?** Deterministic code gives the same answer every time (a rule).
A language model is probabilistic: its output can vary.

**Why strict exact-match for doses?** Because 10 mg and 100 mg are both "a number", but only one is safe.

---

## 10. Glossary
- **ISOBAR:** the Australian handover framework used here.
- **LLM:** large language model, the kind of AI that writes text.
- **API:** a way for code to call a service over the internet.
- **Prompt:** the instructions given to the model.
- **Answer key / ground truth:** the correct facts for a note, written in advance.
- **Baseline:** a simple method used as a point of comparison.
- **Hallucination:** invented content stated as fact.
- **Deterministic:** always gives the same result for the same input.
- **Q-ADDS:** Queensland Adult Deterioration Detection System, a score used to spot a worsening patient.
- **ARP:** Acute Resuscitation Plan.
- **Read-back:** the receiver repeats critical information to confirm it was understood.
