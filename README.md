# literature-zotero-download

面向 Codex 的文献检索、下载、Zotero 导入和 Excel 汇总 Skill。

它可以帮助 Codex 按用户指定数据库检索文献，合法下载可用 PDF，校验文件有效性，导入 Zotero，并生成结构化文献矩阵。适合中文/英文文献混合检索、学校图书馆数据库访问、CNKI/ScienceDirect/Web of Science/Google Scholar 辅助发现，以及批量整理研究资料。

> 这个 Skill 的目标不是绕过数据库限制，而是把用户已有合法访问权限内的重复操作自动化。

## 功能概览

| 功能 | 说明 |
| --- | --- |
| 数据库优先级 | 支持“只查 CNKI”“优先 CNKI，其次 WoS/ScienceDirect”“英文优先”等指令 |
| 文献检索 | 根据主题、关键词、年份、语言、数据库范围生成检索计划 |
| 合法下载 | 通过开放获取来源或用户授权的学校/机构数据库下载 PDF |
| PDF 校验 | 使用脚本识别 HTML 错误页、空文件、伪 PDF、CAJ 误命名等问题 |
| Zotero 导入 | 优先使用 Codex Zotero 插件/Connector 导入 RIS/BibTeX，并尽量绑定 PDF |
| Excel 汇总 | 生成 `literature_summary.xlsx`，记录主题、方法、样本、理论、发现、局限和启发 |
| 断点续跑 | 用 `workflow_state.json` 记录当前数据库、阻塞点和下一步动作 |
| 安全暂停 | 遇到 SSO、2FA、验证码、Cloudflare、付费确认等人工门槛时暂停并让用户接管 |

## 前置要求

建议在 Codex App 中启用下面三个插件。它们可以替代许多传统 MCP 配置，让本 Skill 不必额外安装 Chrome DevTools MCP、Computer Use MCP 或 Zotero MCP。

| Codex 插件 | 作用 | 可替代的传统 MCP/能力 |
| --- | --- | --- |
| Chrome | 使用用户 Chrome 登录态访问学校图书馆、CNKI、ScienceDirect、Web of Science 等网页 | Chrome DevTools MCP、浏览器会话 MCP |
| Computer Use | 控制 macOS 桌面应用、文件选择器、Zotero UI、下载窗口等 | Computer Use MCP、桌面 UI 自动化 MCP |
| Zotero | 检查 Zotero 状态、导入 RIS/BibTeX、检索本地文库和导出引用 | zotero-mcp、Zotero Connector 脚本的一部分 |

### 插件启用方式

在 Codex App 的插件/连接器设置中启用：

1. `Chrome`：Control Chrome with Codex
2. `Computer Use`：Control Mac apps from Codex
3. `Zotero`：Find papers and add citations from Zotero

启用后，Codex 就可以优先调用这些插件完成浏览器、桌面和 Zotero 操作。若某个插件不可用，Skill 会退回到可用工具，并明确说明阻塞点。

## 安装 Skill

克隆仓库：

```bash
git clone https://github.com/czunique/literature-zotero-download-skill.git
```

复制到 Codex skills 目录：

```bash
mkdir -p ~/.codex/skills
cp -R literature-zotero-download-skill ~/.codex/skills/literature-zotero-download
```

然后重启 Codex，让 Skill 生效。

## 快速使用

在 Codex 对话中直接引用：

```text
[$literature-zotero-download] 帮我查找近 5 年关于碳酸盐岩气藏复杂渗流机理的文献，下载 PDF，导入 Zotero，并生成 Excel 汇总表。
```

指定数据库优先级：

```text
[$literature-zotero-download] 优先 CNKI，其次 Web of Science 和 ScienceDirect，找 10 篇中文和 10 篇英文文献，只下载 PDF，导入 Zotero。
```

只查某个数据库：

```text
[$literature-zotero-download] 只在 CNKI 检索“碳酸盐岩气藏开发方案编制”，近 5 年，下载 5 篇 PDF。
```

## 工作流程

1. 解析用户任务：主题、关键词、年份、语言、目标数量、数据库优先级、Zotero collection。
2. 生成检索计划：必要时调用 `scripts/build_search_plan.py`。
3. 按数据库优先级执行检索。
4. 优先尝试开放获取/API 来源；再使用用户授权的学校数据库或浏览器登录态。
5. 下载 PDF 后运行 `scripts/validate_pdf.py` 校验。
6. 通过 Zotero 插件或 Zotero Desktop 导入题录和附件。
7. 写入日志：检索结果、下载状态、Zotero 导入状态。
8. 生成 `literature_summary.xlsx`。

## 输出结构

典型任务目录如下：

```text
task-folder/
├── pdfs/
├── search_results.csv
├── download_log.csv
├── zotero_import_log.csv
├── literature_records.json
├── literature_summary.xlsx
└── workflow_state.json
```

默认 Excel 字段：

| 作者年份 | 主题 | 方法 | 样本 | 理论 | 主要发现 | 局限 | 对我研究的启发 | 下载状态 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

无法可靠判断的内容应填写 `待精读`，不能凭标题硬编。

## 相关项目

下面这些项目可以作为本 Skill 的生态参考。后续如果收集到新的文献下载、Zotero、Obsidian 或 Codex skills 项目，可以继续追加到这个表格中。

| 项目 | 类型 | 主要用途 | 和本 Skill 的关系 |
| --- | --- | --- | --- |
| [codex-skills-workbench](https://github.com/Jinze-Lee/codex-skills-workbench) | Codex skills 工作台 | 偏向公开文献下载和 skills 工作流组织 | 可参考其公开文献下载思路；本 Skill 进一步强调学校订阅数据库、合法登录态和 Zotero/Excel 闭环 |
| [MindCite](https://github.com/YYCCCHAOOO/MindCite) | 研究流程模板 | Zotero + Obsidian + Codex 的文献阅读、笔记质检和分类治理 | 可作为下载后的阅读、笔记和知识库治理补充 |
| [cnki-skills](https://github.com/cookjohn/cnki-skills) | 数据库专项 Skill | CNKI 搜索、浏览期刊、下载 PDF，并通过 Chrome DevTools MCP 导出到 Zotero | 可参考 CNKI 页面流程和导出习惯；本 Skill 默认用 Codex Chrome/Computer Use/Zotero 插件替代部分 MCP 能力 |
| [gs-skills](https://github.com/cookjohn/gs-skills) | 数据库专项 Skill | Google Scholar 搜索、引用追踪、全文访问和 Zotero 导出 | 可作为 Google Scholar 辅助发现流程参考；本 Skill 会限制高频抓取并优先合法全文来源 |
| [wos-skills](https://github.com/cookjohn/wos-skills) | 数据库专项 Skill | Web of Science 搜索、浏览、导出和下载学术论文 | 可参考 WoS 的检索、筛选、导出流程 |
| [sd-skills](https://github.com/cookjohn/sd-skills) | 数据库专项 Skill | ScienceDirect 搜索、浏览、导出和下载学术论文 | 可参考 ScienceDirect 的 PDF 下载和题录导出流程 |
| [zotero-mcp](https://github.com/cookjohn/zotero-mcp) | Zotero MCP 插件 | 通过 MCP 协议让 AI 助手访问和操作 Zotero 文献库 | 可作为未来增强方案；本 Skill 第一版优先使用 Codex Zotero 插件，不强制安装 zotero-mcp |

## 安全边界

本 Skill 只用于合法访问：

- 不破解或绕过付费墙。
- 不自动处理验证码、Cloudflare、SSO、短信/邮箱验证码或 2FA。
- 不保存账号、密码、Cookie、Token 或验证码。
- 不默认使用 Sci-Hub 或其他非授权来源。
- 不高频抓取 Google Scholar。
- 遇到需要用户确认或登录的页面时，暂停并让用户手动完成。
- 下载失败、无权限、需要登录等情况必须记录，不能伪造成功。

## 项目结构

```text
.
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── examples/
│   └── sample_literature_matrix.json
├── references/
│   ├── automation-runbook.md
│   ├── database-workflows.md
│   ├── institution-profile.md
│   ├── literature-matrix.md
│   └── zotero-import.md
└── scripts/
    ├── build_search_plan.py
    ├── validate_pdf.py
    ├── workflow_state.py
    ├── write_literature_log.py
    └── write_literature_matrix.py
```

## 入口文件

完整 Skill 行为定义见 [`SKILL.md`](SKILL.md)。
