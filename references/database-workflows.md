# Database Workflows

Use this reference when open-access/API routes are insufficient or the user names a database. The goal is to mimic normal authorized human use, not to scrape aggressively.

## Common Pattern

1. Open the user-specified database or school library entry page.
2. Confirm the access route: direct site, EZproxy, VPN, library portal, or database navigation page.
3. Search with the user's exact query first; then use controlled variants in the database's language.
4. Inspect titles, abstracts, authors, dates, source quality, and relevance before downloading.
5. Prefer RIS/BibTeX/EndNote export for metadata and PDF download for attachments.
6. Record each attempt and blocker in `download_log.csv`.

## CNKI

Reference project: <https://github.com/cookjohn/cnki-skills>

Use CNKI when the user asks for Chinese literature, CNKI, 知网, 学位论文, 中文期刊, 会议论文, or Chinese institutional access.

Practical guidance:

- Enter through the school library when off-campus access or "融合访问" is required.
- Search in Chinese first; add domain synonyms such as `开发方案`, `方案编制`, `气藏开发`, `碳酸盐岩气藏`.
- On result pages, prefer `PDF下载` over `CAJ下载`; use CAJ only if the user accepts it.
- For each selected item, open the detail page, use `PDF下载`, and if redirected to login choose the authorized institutional/IP login route only when already available.
- If CAPTCHA appears, pause and let the user solve it.
- Export/record title, authors, source, year, database type, URL, and downloaded filename.

## ScienceDirect

Reference project: <https://github.com/cookjohn/sd-skills>

Use ScienceDirect for Elsevier journals/books and English engineering/science literature.

Practical guidance:

- Prefer advanced search with title/abstract/keyword filters when the topic is broad.
- On article pages, use `Download PDF` only when access is available through the user's institution or the article is OA.
- Export citations as RIS/BibTeX when available.
- If Cloudflare, institution sign-in, or SSO appears, pause for the user.
- Record access blockers separately from "no relevant result".

## Web Of Science

Reference project: <https://github.com/cookjohn/wos-skills>

Use WoS for high-quality discovery, citation filtering, and finding publisher links. WoS often provides metadata and "Full Text" links rather than the PDF itself.

Practical guidance:

- Use topic search for discovery and title search for known papers.
- Sort/filter by relevance, publication year, document type, and citation count if useful.
- Export selected results as RIS/BibTeX for Zotero.
- Follow full-text/publisher links only when authorized and within the user's requested scope.

## Google Scholar

Reference project: <https://github.com/cookjohn/gs-skills>

Use Google Scholar as a discovery and full-text locator, not as a high-volume scraping source.

Practical guidance:

- Use it to find titles, citation trails, all versions, and PDF links from repositories.
- Avoid high-frequency automated searches.
- If CAPTCHA or unusual traffic warnings appear, stop and ask the user to take over or choose another route.
- Do not treat Scholar metadata as authoritative when a publisher or database record is available.

## Database Adaptation Checklist

For a new database or school-specific portal:

- Identify the entry route from the library page to the database.
- Determine whether access is by IP, EZproxy, SSO, VPN, personal login, or a combination.
- Locate search, result, detail, citation export, and PDF download controls.
- Test one low-risk item before batch work.
- Record the path in an institution profile so future sessions can reuse it.
