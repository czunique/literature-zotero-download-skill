# Automation Runbook

Use this reference when the user asks for full automation.

## Automation Levels

- Level 1: Plan automatically. Build database priority, query variants, target counts, and task folders.
- Level 2: Discover automatically. Use open APIs, database search pages, and user-authorized browser sessions to collect candidate records.
- Level 3: Acquire automatically. Download PDFs, export RIS/BibTeX, validate files, and record failures.
- Level 4: Integrate automatically. Import metadata/PDFs into Zotero and generate `literature_summary.xlsx`.
- Human gate: CAPTCHA, Cloudflare, SSO, 2FA, payment, SMS/email code, or explicit institutional confirmation. These cannot be automated; pause, record, and resume after the user completes them.

Never describe a workflow as fully automatic if a protected human gate is currently visible. Say it is "automatic with human verification checkpoints".

## State Machine

Each task should maintain `workflow_state.json` in the task folder.

Recommended statuses:

- `planned`: task parsed, search plan created.
- `searching`: currently querying databases.
- `candidate_review`: candidates collected and being ranked.
- `downloading`: PDFs or metadata exports are being acquired.
- `human_gate`: blocked on CAPTCHA/Cloudflare/SSO/2FA or similar.
- `validating`: files are being checked.
- `importing_zotero`: metadata/PDFs are being imported.
- `summarizing`: Excel matrix is being created.
- `complete`: task finished.
- `partial`: finished with unresolved failures.

When a gate appears, record:

- `database`
- `url`
- `gate_type`
- `message`
- `next_action`
- `blocked_at`

The next assistant turn should inspect `workflow_state.json` first and resume from `next_action`.

## Browser Automation Rules

- Prefer Chrome when the user's cookies, logged-in session, or school portal are needed.
- Use Computer Use for desktop browser work if Chrome extension control is unavailable.
- Do not read cookies, local storage, passwords, or token stores.
- Do not click CAPTCHA/Cloudflare/SSO verification controls.
- Do not use high-frequency Google Scholar automation.

## Practical Pattern

1. Build a search plan with `scripts/build_search_plan.py`.
2. Start a task state with `scripts/workflow_state.py init`.
3. For each database:
   - Mark the database as current.
   - Run the search.
   - Export or record candidate metadata.
   - Download PDFs only through visible authorized controls or OA links.
   - Validate each PDF.
4. If blocked, call `workflow_state.py gate` and stop.
5. After the user clears the gate, call `workflow_state.py status`, then continue from the recorded next action.
6. End with Zotero import logs and `literature_summary.xlsx`.

## What "Automatic" Means Here

The skill should remove repetitive work, not remove institutional security checks. A good fully-assisted run requires only occasional user action at security gates; everything around those gates is performed by Codex.
