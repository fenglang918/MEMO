# Module Instructions: 00_Master-Schedule

## 模块定位

- 本目录只放跨项目时间决策信息与人工主看板。
- `calendar.md` 是主真源；自动抽取、页面数据和日历导出都属于派生产物。
- 不在这里复制项目细节，优先用来源链接回到 `03_Goal-Projects/`、`01_Inbox/` 或 `07_Principles/`。

## 读写顺序

1. 先看 `README.md`
2. 再看 `calendar.md` / `weekly.md` / `milestones.md`
3. 需要脚本链路时看 `../../06_Infra/plugins/master-schedule/README.md`
4. 需要 Agent 流程时看 `../../.agents/skills/master-schedule-sync/SKILL.md`

## 默认工作规则

- 手工看板优先于自动抽取视图。
- `calendar.md` 只保留真正承诺推进、值得持续盯住的节点。
- 每条节点尽量附来源链接。
- 如果只是临时想到的时间项，先放 `inbox.md`，不要直接污染主看板。
- 如果一个事项已经演化成长期推进主题，再为它建立 `03_Goal-Projects/YYYY/MM/<project>/`。

## 同步与导出边界

- Apple Calendar、ICS、月视图页面都属于派生链路，不替代 Markdown 真源。
- 模板默认只提供脚本和流程，不假设你已经有任何线上个人站点或固定部署环境。
- 涉及本机日历、hooks 或网页发布时，先 dry-run / 先本机验证，再按你的环境启用。
