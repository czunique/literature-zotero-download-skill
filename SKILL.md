---
name: literature-zotero-download
description: Search academic literature, legally download available PDFs through open-access sources or user-authorized institutional databases, import metadata/PDFs into Zotero, and generate a literature summary spreadsheet. Use when the user asks Codex to find papers, download references, use CNKI/Web of Science/ScienceDirect/Google Scholar or a school library portal, create Zotero collections, attach PDFs to Zotero items, or produce an Excel literature matrix after downloading papers.
---

# Literature Zotero Download

## Core Rule

Help the user acquire literature only through open-access sources or access they are authorized to use. Do not bypass paywalls, solve CAPTCHA, automate SSO/2FA, store credentials, use Sci-Hub by default, or pretend a failed download succeeded.

## Automation Contract

Automate every step that is allowed and technically available: query planning, database routing, result triage, metadata export, PDF download clicks, file validation, Zotero import, attachment checks, logs, and spreadsheet generation.

Do not automate protected human gates. When CAPTCHA, Cloudflare Turnstile, SSO, 2FA, SMS/email verification, payment, or an institution access confirmation appears:

1. Record the gate in the workflow state with `scripts/workflow_state.py gate`.
2. Tell the user exactly which browser tab/page needs their action.
3. Stop interacting with that gate.
4. After the user says it is complete, resume from the recorded `next_action`.

For long or multi-database tasks, create a state file at the start:

```bash
python3 <skill-dir>/scripts/workflow_state.py init --task-dir <task-dir> --topic "..." --target-count 20 --databases "CNKI,SPE OnePetro"
```

Read `references/automation-runbook.md` before promising full automation or when adapting this skill to a new database.

## Workflow

1. Parse the task into: topic/keywords/titles/DOIs, target count, years, language, database priority, Zotero collection, and whether browser/institution access is allowed.
2. Create a task folder and workflow state. Use `scripts/build_search_plan.py` when a repeatable search plan is useful.
3. Follow the user's database priority exactly. If none is given, use: open-access/API routes, then user-authorized institutional databases, then Google Scholar only for discovery.
4. Try structured routes first for DOI/PMID/arXiv/title searches: Crossref/OpenAlex/Unpaywall/PubMed/PMC/arXiv or other available literature skills.
5. For subscribed databases, use Chrome with the user's active session or school library portal. Use Computer Use only for desktop tasks such as Zotero UI, system file pickers, VPN windows, and download-folder handling.
6. Pause and hand off when login, SSO, 2FA, CAPTCHA, Cloudflare, payment, or access confirmation appears. Continue after the user completes the action.
7. Validate every downloaded PDF before importing. Use `scripts/validate_pdf.py`.
8. Import metadata into Zotero, attach PDFs where possible, and place items in the requested collection.
9. Produce logs and a literature summary spreadsheet. Unknown analytic fields must be `待精读`, never invented.

## Database Priority

Treat user wording as routing instructions:

- "只查 CNKI" means use CNKI only unless the user later expands scope.
- "优先 CNKI，其次 WoS 和 ScienceDirect" means exhaust relevant CNKI results first, then use Web of Science, then ScienceDirect.
- "英文优先" means use English databases and English queries before Chinese databases.
- If a database is inaccessible, record `institution_access_required`, `login_required`, `captcha_required`, or the exact blocker, then move to the next allowed route.

For database-specific tactics, read `references/database-workflows.md`.

## Zotero Import

Use the existing Zotero plugin before considering other Zotero integrations.

1. Run the Zotero helper `status --json` to learn whether Zotero Desktop, the local API, and Connector are available.
2. Prefer RIS/BibTeX import through the Zotero plugin/Connector.
3. Use the currently selected Zotero collection when the user has prepared it; otherwise create/select the requested collection through Zotero Desktop if the plugin cannot create it safely.
4. Attach PDFs to their matching items. If the current plugin cannot attach PDFs directly, use Zotero Desktop with Computer Use.
5. Do not enable Zotero's local write API or restart Zotero unless the user explicitly approves that security-relevant setting change.

Read `references/zotero-import.md` before doing nontrivial Zotero work.

## PDF Validation

Run:

```bash
python3 <skill-dir>/scripts/validate_pdf.py <pdf-path> --json
```

Reject files that are HTML/error pages, empty files, partial downloads, CAJ files renamed as PDF, or metadata mismatches. If a non-PDF format such as CAJ is the only available format, tell the user and avoid treating it as Zotero-ready unless they explicitly accept it.

## Logs And Excel

Maintain a task folder with:

- `pdfs/` for clean downloaded PDFs.
- `search_results.csv` for candidates and sources.
- `download_log.csv` for attempted methods and blockers.
- `zotero_import_log.csv` for import/attachment outcomes.
- `literature_summary.xlsx` for the final matrix.

Use:

```bash
python3 <skill-dir>/scripts/write_literature_log.py --log download_log.csv --record-json '{"title":"...","download_status":"downloaded"}'
python3 <skill-dir>/scripts/write_literature_matrix.py --input literature_records.json --output literature_summary.xlsx
python3 <skill-dir>/scripts/workflow_state.py status --task-dir <task-dir>
```

The first spreadsheet columns are fixed unless the user changes them:

`作者年份`, `主题`, `方法`, `样本`, `理论`, `主要发现`, `局限`, `对我研究的启发`, `下载状态`

Read `references/literature-matrix.md` before generating the final spreadsheet.

## Institution Profiles

When the user repeatedly uses the same school/library, build a reusable institution profile containing only process information: library URL, database entry paths, access method, common blockers, download folder, and preferred Zotero collection naming. Never store student IDs, passwords, cookies, tokens, verification codes, or other secrets.

Read `references/institution-profile.md` when adapting to a new school or database portal.
