# Instructions for Claude Code (handover-safety-net)

## Git rules
- **Do not add attribution lines** to commit messages or pull request descriptions: no `Co-Authored-By`,
  no `Claude-Session`, no "Generated with Claude Code". Write the message and stop.
- **Author identity:** before the first commit of every session, set this repo's git identity (a fresh cloud container
  starts as "Claude", which is wrong here):
  `git config user.name "Dreshti Kandpal"` and `git config user.email "202130774+dkand2004@users.noreply.github.com"`.
  Every commit must be authored and committed as Dreshti Kandpal. Never commit as Claude.
- Never force-push or rewrite history unless the owner explicitly asks.
- **Before every push:** confirm `.env` is not tracked and scan staged files for API keys or tokens.

## Secrets
- The Claude API key lives only in `.env` (ignored by Git). Never print it, log it, hard-code it or put it in `.env.example`.
- Only **synthetic** notes may ever be sent to an external AI service. Never send anything resembling a real record.

## Safety and ethics
- This is a research and portfolio prototype, **not a clinical tool**. Do not describe it as safe for patient care.
- No real patients, staff, hospitals or screenshots of real systems. Do not use real hospital names in notes.
- Claims need sources: only cite what has actually been read. Mark anything unverified as such (see `docs/problem_onepager.md`).
- The list of critical elements is a reasoned hypothesis, not an evidence-based standard; keep that caveat.

## Working style (the owner is a student and still learning)
- Explain what you are about to do and why, and summarise afterwards. Define new terms in plain language.
- Do not make design, tooling, model or naming decisions silently: present options, recommend one, and wait for the answer.
- Go step by step; keep it a small prototype.
- **Sanity-check before instructing:** before asking the owner to build or run anything (a metric, a check, a prompt, an evaluation), test the idea on a small sample of the data first and report what the check found.
- Comments in code should explain *why*, not only *what*.

## Project facts worth knowing
- Framework: ISOBAR as defined in the OSSIE Guide (ACSQHC, 2010); see `docs/handover_framework.md`.
- Three arms are compared: rule-based baseline, Claude only, and a hybrid (code extracts critical facts, the LLM writes only the narrative).
- Evaluation is strict: doses must match exactly, "not documented" must never become "negative", doubt must stay visible.
- The owner wants to be able to explain this project: keep `docs/how_it_works.md` accurate and complete its [TO COMPLETE] sections as things are built. A short demo video (one scenario) is a stretch goal; see `docs/TODO.md`.
