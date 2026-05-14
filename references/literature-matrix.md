# Literature Matrix

Generate `literature_summary.xlsx` after the download/import run. This is a first-pass matrix, not a full literature review.

## Columns

1. `作者年份`
2. `主题`
3. `方法`
4. `样本`
5. `理论`
6. `主要发现`
7. `局限`
8. `对我研究的启发`
9. `下载状态`

## Filling Rules

- `作者年份`: derive from metadata, e.g. `霍瑶等，2016`, `Smith et al., 2024`.
- `主题`: summarize from title, keywords, and abstract when available.
- `方法`, `样本`, `理论`, `主要发现`, `局限`, `对我研究的启发`: extract only when supported by abstract/PDF text. If uncertain, write `待精读`.
- `下载状态`: use concrete states such as `PDF已下载并导入Zotero`, `仅导入题录`, `需用户登录`, `验证码暂停`, `无PDF权限`, `下载失败`.

## Do Not Invent

If the abstract/full text is unavailable or too vague, do not infer methods, theory, findings, or limitations from the title alone. Use `待精读` and note the blocker in the logs.

## Input Format For Script

`scripts/write_literature_matrix.py` accepts a JSON array of records. Each record may contain either the Chinese column names directly or common English keys:

```json
[
  {
    "author_year": "霍瑶等，2016",
    "topic": "气田开发方案编制",
    "method": "待精读",
    "sample": "待精读",
    "theory": "待精读",
    "findings": "待精读",
    "limitations": "待精读",
    "implications": "待精读",
    "download_status": "PDF已下载并导入Zotero"
  }
]
```
