---
name: me-network-crm
description: 在 MEMO 仓库中维护个人人脉库（Personal CRM）：录入/更新/检索 `05_Resources/network/people/` 的人物卡片，并在 ingest 截图/聊天/简介页时用 PRISM 折射为 Facts/Inferences/Actions/Me-Info；支持阶段锚点（`阶段锚点`）与相对 Me 的差分（年龄/毕业等）。
---

# Me Network CRM（个人人脉库）

## 约定文件（source of truth）

- 入口与标签列表：`05_Resources/network/index.md`
- 设计/约束：`05_Resources/network/requirements-architecture.md`
- 人物卡片模板：`05_Resources/network/people/_template.md`
- 查询脚本（agent-friendly）：`05_Resources/network/_cli/network.py`
- 校验脚本：`05_Resources/network/_cli/validate_people.py`
- PRISM（portable ingest prompt）：`06_Infra/skills/portable/prism.md`
- 外部信息源 ingest 备注：`06_Infra/skills/native/me-network-crm/references/external-source-ingest.md`
- 字段/标签参考：`06_Infra/skills/native/me-network-crm/references/fields-and-tags.md`

## 工作流

### A) 录入新联系人（Add / ingest）

1) 选择一个稳定的 `Handle/ID`（ASCII、长期不变）。建议用 `primary-handle` 便于快速检索（Ctrl+P）。
2) 从模板创建：`05_Resources/network/people/<handle>.md`（模板：`05_Resources/network/people/_template.md`）。
3) 填写最小可检索字段（检索 + 行动）：
   - 必填：`Handle/ID`、`关键词`、`Tags`
   - 推荐：`状态`、`最后联系`、`下次跟进`（没有就写 `暂无`）
   - 可选但很有用：`阶段锚点`（例如 `2026-01-13（本科大三）`）
   - 可选（用于相对计算）：`出生日期`、`预计毕业`
4) 把原始信息变成可检索 token：
   - `关键词` 尽量包含 “domain + resource + scenario”
   - Tags 只用统一前缀：`#domain/ #resource/ #role/ #city/ #rel/ #status/`（避免大小写漂移）
5) 不要存可直接滥用的机密（密码/API keys/私钥等）。

### B) 更新已有联系人（Update）

1) 先检索定位：
   - `python3 05_Resources/network/_cli/network.py <keywords>`
   - `python3 05_Resources/network/_cli/network.py --tag '#resource/intro' <keywords> --json`
2) 在卡片的 `互动记录（流水）` 里追加 1 条本次事件/结果。
3) 更新 `最后联系`，设置/调整 `下次跟进`（日期 + 动作）。
4) 必要时调整 `状态`（`#status/active|warmup|dormant|archived`）。

### C) 为一个问题找人（Find / match）

1) 把需求翻译成 Tags + 2–5 个关键词（domain + resource + scenario）。
2) 查询：
   - `python3 05_Resources/network/_cli/network.py --tag '#domain/ml' --tag '#resource/intro' <keywords> --json`
   - 若卡片包含 `阶段锚点`：`python3 05_Resources/network/_cli/network.py --as-of 2026-09-01 --json`
   - 相对你（年龄/毕业差分）：`python3 05_Resources/network/_cli/network.py --relative-to-me --json`
     - 默认读取 `04_Assets/profile/Me.md`（可用 `--me-path` 覆盖）
     - 联系人若缺少 `出生日期/预计毕业`，部分字段会为空（允许）
3) 输出 Top candidates：
   - 匹配理由（tags/keywords）
   - 建议的触达角度（1–2 句）
   - 下一步行动（必要时把 `下次跟进` 写回卡片）

## 校验（可选但推荐）

- `python3 05_Resources/network/_cli/validate_people.py`

如果 `python3` 在环境里异常（例如 shim/conda），可尝试 `/usr/bin/python3`。

### D) 用 PRISM ingest 外部信息源（截图/聊天/简介页）

目标：把混沌的 raw context 折射为 **Facts / Inferences / Actions / Me-Info**，并写入 `05_Resources/network/people/<handle>.md`。

1) 识别来源类型与抽取约束（聊天/简介页/邮件/混合 bundle）。
2) 抽取“可检索 token”，不要过度解读；不确定内容标注为待确认。
3) 按 `06_Infra/skills/portable/prism.md` 的契约输出（Facts vs Inferences 分离）。
4) 落盘规则：
   - 更新顶部字段：`关键词/Tags/状态/最后联系/下次跟进`（以及 `阶段锚点/出生日期/预计毕业` 如适用）
   - 追加一个带日期的 `## Prism（...，YYYY-MM-DD）` 块（Facts/Inferences/Actions/Me-Info）
   - 如果抽取到稳定的“关于我”的信号（偏好/边界/策略），同步追加到 `04_Assets/profile/signals.md`（没有就创建）

