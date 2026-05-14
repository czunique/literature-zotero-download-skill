# Zotero Import

Use the Codex Zotero plugin as the first integration path. It is enough for the MVP: readiness checks, local library search, RIS/BibTeX import through Connector, citation export, and attachment/full-text inspection when available.

## Preferred Route

1. Resolve the plugin's Zotero helper from the active Zotero skill:
   `python3 <plugin-root>/skills/zotero/scripts/zotero.py status --json`
2. If Connector is available, import metadata with:
   `import-ris --file <file> --yes` or `import-bibtex --file <file> --yes`
3. Put imported items in the selected or requested collection.
4. Verify visible Zotero items and attached PDFs.

## PDF Attachments

The current Zotero plugin may not expose a one-command "attach this PDF to this existing item" operation in every environment.

Fallback:

- Use Zotero Desktop UI.
- Select the target item.
- Add attachment -> File.
- Choose the validated PDF from the clean `pdfs/` folder.
- Confirm the item now shows a PDF child.

Use Computer Use for this only when the user requested Zotero import or attachment work. Keep actions local and avoid deleting or overwriting library content.

## Local Write API

Do not enable Zotero's local write API, restart Zotero, or change security-relevant settings unless the user explicitly approves after being told what will change. If not approved, use Connector import and Zotero Desktop UI.

## Duplicates

Before importing a large set, search Zotero by DOI or exact title when practical. If duplicates are found, prefer updating/attaching to the existing item rather than creating duplicates, unless the user wants a separate collection copy.
