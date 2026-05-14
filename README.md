# literature-zotero-download

这是一个面向 Codex 的文献工作流 Skill，用来辅助完成“检索文献 -> 合法下载 PDF -> 校验文件 -> 导入 Zotero -> 生成文献汇总表”的流程。

## 能做什么

- 按用户指定的数据库或优先级检索文献。
- 支持开放获取来源和用户已授权访问的学校/机构数据库。
- 只通过合法授权路径下载可用 PDF，不绕过付费墙、验证码、SSO 或 2FA。
- 校验下载文件，避免把 HTML 错误页、空文件或非 PDF 文件当作文献保存。
- 通过 Zotero 插件/Connector 导入 RIS 或 BibTeX 题录，并在可行时绑定 PDF 附件。
- 生成 `literature_summary.xlsx` 文献矩阵，包含方法、样本、理论、主要发现、局限、研究启发和下载状态等字段。

## 安装

把这个目录复制到 Codex 的 skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R literature-zotero-download ~/.codex/skills/
```

然后重启 Codex，让新 skill 生效。

## 使用方式

在 Codex 对话中直接点名或引用：

```text
[$literature-zotero-download] 帮我查找近 5 年关于碳酸盐岩气藏复杂渗流机理的文献，下载 PDF，导入 Zotero，并生成 Excel 汇总表。
```

也可以指定数据库优先级：

```text
优先 CNKI，其次 Web of Science 和 ScienceDirect，中文 10 篇、英文 10 篇。
```

## 安全边界

这个 skill 只用于合法访问：

- 不破解或绕过付费墙。
- 不自动处理验证码、Cloudflare、SSO、短信/邮箱验证码或 2FA。
- 不保存账号、密码、Cookie、Token 或验证码。
- 不默认使用 Sci-Hub 或其他非授权来源。
- 遇到需要用户确认或登录的页面时，应暂停并让用户手动完成。
- 下载失败、无权限、需要登录等情况必须记录，不能伪造成功。

## 输出

典型输出包括：

- `pdfs/`：通过校验的 PDF 文件。
- `search_results.csv`：检索结果记录。
- `download_log.csv`：下载尝试和失败原因。
- `zotero_import_log.csv`：Zotero 导入和附件绑定状态。
- `literature_summary.xlsx`：文献汇总 Excel。

默认 Excel 字段：

| 作者年份 | 主题 | 方法 | 样本 | 理论 | 主要发现 | 局限 | 对我研究的启发 | 下载状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

无法可靠判断的内容应填写 `待精读`，不能凭标题硬编。

## 入口文件

完整工作流请阅读 [`SKILL.md`](SKILL.md)。
