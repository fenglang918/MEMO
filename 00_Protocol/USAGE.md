# Usage / 使用说明

## Search-first / 先检索

- People by keyword: `rg -n "diffusion|referral|GPU" 05_Resources/network/people`
- People by follow-up: `rg -n "^\\s*-\\s*Next follow-up|^\\s*-\\s*下次跟进" 05_Resources/network/people`
- Principles by tag: `rg -n "#scene/async-collab" 07_Principles`
- Principles by budget rule: `rg -n "budget|预算|probability" 07_Principles`
- Project docs by concept: `rg -n "decision|trade-off|复盘" 03_Goal-Projects`

## Projects / 项目目录约定

推荐两种放法：

- 时间归档项目：`03_Goal-Projects/YYYY/MM/<project>/`
- 常驻项目：`03_Goal-Projects/evergreen/<project>/`

每个项目目录遵循 TPCD：

- `README.md`：Target
- `PLAN.md`：Plan
- `cognition/`：Cognition
- `decisions/`：Decision

模板入口：

- `03_Goal-Projects/_TEMPLATE/`
- `03_Goal-Projects/_docs/concepts.md`

## People Cards / 人脉卡片

每人一张卡，放在 `05_Resources/network/people/`。

最小推荐字段：

- `Handle/ID`
- `关键词 / Keywords`
- `Tags`
- `状态 / Status`
- `最后联系 / Last contact`
- `下次跟进 / Next follow-up`（或明确写 `暂无`）

## Optional Indexing / 可选索引实验

模板默认不依赖独立 indexing。

- 主导航仍以目录结构、`README.md`、`index.md`、`AGENTS.md` 和文件命名为准
- 如需回看旧实验，再看：`06_Infra/indexing/README.md`
- 如需手动运行实验脚本，再执行：

```bash
python3 06_Infra/indexing/scripts/build_repo_concept_index.py \
  --profile v1_1 \
  --summary-json 06_Infra/indexing/reports/index-summary.v1_1.json
```

## Skills / Agent 技能

生效 skill 路径：

- `.agents/skills/`

推荐从这里看：

- `.agents/skills/me-network-crm/`
- `.agents/skills/prism/`
- `.agents/skills/inbox-folder-archiver/`

`../.agents/skills/repo-indexing-memory/` 仅在你明确想回看旧 indexing 实验时使用。

## Optional Plugins / 可选插件与桥接

公开模板当前保留三类可选扩展入口：

- Repo-local bridge：`06_Infra/plugins/lark-bridge/`
- Cloud sync mount：`06_Infra/plugins/Google-Drive/`
- Codex local plugins：`.agents/plugins/marketplace.json` + `plugins/`

常见入口：

- `bash 06_Infra/plugins/lark-bridge/scripts/doctor_lark.sh`
- `bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh docs-search --query "AgenQA" --format pretty`
- `python3 plugins/memo-audio-transcribe/scripts/run_transcribe.py /absolute/path/to/audio.mp3`

使用边界：

- 这些能力默认是可选扩展，不是每个模板用户都会启用
- 云盘挂载目录和本地缓存默认不进 Git
- 依赖本机登录态、客户端或额外环境时，应先做 doctor / bootstrap / 本机配置

## Principles / 原则库

推荐入口：

- `07_Principles/README.md`
- `07_Principles/_template.md`

检索示例：

- `rg -n "#scene/decision-making" 07_Principles`
- `rg -n "#trigger/context-switch" 07_Principles`
- `rg -n "Project-First|Reading Materials" 07_Principles`

## Operations / 运行模块

推荐阅读顺序：

1. `08_Operations/README.md`
2. `08_Operations/00_Master-Schedule/README.md`
3. `06_Infra/plugins/master-schedule/README.md`
4. `08_Operations/01_Time-Tracking/README.md`

最短闭环命令：

```bash
python3 06_Infra/plugins/master-schedule/scripts/build_month_calendar_feed.py \
  --calendar 08_Operations/00_Master-Schedule/calendar.md \
  --output 08_Operations/00_Master-Schedule/calendar-page-data.js

python3 06_Infra/plugins/master-schedule/scripts/time_tracking.py report
```
