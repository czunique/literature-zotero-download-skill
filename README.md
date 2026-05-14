# literature-zotero-download

Codex skill for academic literature workflows:

- Search literature across open access sources and user-authorized institutional databases.
- Legally download available PDFs without bypassing paywalls or CAPTCHA/SSO gates.
- Validate downloaded PDFs to avoid saving HTML error pages as papers.
- Import RIS/BibTeX records into Zotero where the local Zotero connector supports it.
- Generate a literature summary spreadsheet with method, sample, theory, findings, limitations, implications, and download status fields.

## Install

Copy this folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R literature-zotero-download ~/.codex/skills/
```

Then restart Codex so the skill is loaded.

## Safety

This skill is designed for legal access only. It does not store passwords, cookies, tokens, or verification codes, and it should pause for the user when a database requires SSO, two-factor authentication, CAPTCHA, or other manual confirmation.

## Entry Point

Read `SKILL.md` for the full workflow.
