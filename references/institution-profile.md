# Institution Profile

Use an institution profile after the user has shown how their library/database access works. The profile captures workflow memory, not credentials.

## Do Record

- School or organization name.
- Library electronic resources URL.
- Database entry path, e.g. `图书馆首页 -> 电子资源 -> CNKI -> 融合访问`.
- Access method: IP login, EZproxy, VPN, SSO, database account, or on-campus only.
- Which steps require user action: login, 2FA, CAPTCHA, VPN.
- Preferred download folder and clean output folder.
- Zotero collection naming preference.
- Database-specific notes, such as "CNKI PDF button appears on detail page".

## Never Record

- Student/staff ID.
- Passwords.
- Verification codes.
- Cookies, tokens, session IDs, browser profile secrets.
- Personal pages or unrelated private information.

## Template

```yaml
school_profile:
  name: ""
  library_home: ""
  access_method: ""
  preferred_download_folder: ""
  default_zotero_collection: ""

  databases:
    - name: "CNKI"
      entry_path:
        - ""
      login_required: true
      user_action_required:
        - "SSO or CAPTCHA if prompted"
      download_notes:
        - "Prefer PDF下载 over CAJ下载"

  safety:
    pause_on_captcha: true
    pause_on_sso: true
    do_not_store_credentials: true
    max_downloads_per_session: 20
```

## How To Use

1. If a profile exists, follow it before rediscovering the route.
2. If the route fails, inspect the current page and update only process notes.
3. Ask the user to handle credentials and verification.
4. Summarize any new stable route details at the end of the task so they can be added to the profile.
