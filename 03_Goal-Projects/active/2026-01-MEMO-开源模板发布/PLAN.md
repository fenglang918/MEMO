# MEMO 开源模板（示例项目 / Plan）

> 说明：脱敏示例项目。用于展示一个“开源模板化”项目如何落到 TPCD。

## 总体策略

- 先定义稳定 outputs（对象模型/最小字段/可检索约定），再把 inputs 当作可变来源；通过“编译”把碎片沉淀为记忆资产。
- 坚持 search-first（rg/目录/命名）作为默认路径；脚本工具只做加速，不做绑定。
- 把隐私与发布制度化：不入库可直接滥用的明文机密；示例全部虚构/脱敏；发布前做一次安全检查。

## 里程碑与阶段

### 阶段 1：定位与协议（2026-01）

- [x] 写清开源版定位：人生 memory 的协议/参考实现（非产品、非数据源、非 LLM API）
- [x] 明确输出对象：People / Projects / Decisions / Signals（先有最小可用）
- [x] 给出 1–2 条“从输入到输出”的工作流（截图/聊天 → PRISM → 卡片/Signals）

### 阶段 2：可发布的模板仓库（2026-01 ~ 2026-02）

- [ ] 补齐发布所需文件：LICENSE / CONTRIBUTING / 版本发布方式
- [x] 准备脱敏示例与演示 walkthrough（可复制、可跑通）
- [x] 给出“如何从私库导出 public 子树”的说明（可选：subtree / filter-repo）
- [x] GitHub：把“协议/工作流/skills/prompts/demo”组织成可复用目录，并给出最小上手路径（clone → 跑 demo → 写回文件）
- [ ] 可选：做一个无状态 Web Playground 用于传播（不存数据/无注册/BYOK 或低成本兜底），只负责展示“输入碎片 → 输出结构化 Markdown”
- [x] 决策：双轨发布（GitHub 协议仓库 + Web Playground）→ `decisions/001-dual-track-repo-and-web-playground.md`
- [ ] Web：支持 BYOK（用户自带 key）作为默认；兜底提供少量免费额度（若有赞助/免费 API），额度耗尽就引导 BYOK/clone

## 已落地的关键资产（当前仓库快照）

- PRISM ingest prompt：`06_Infra/skills/portable/prism.md`
- 核心 native skill：`06_Infra/skills/native/me-network-crm/SKILL.md`
- People cards + design doc + CLI：`05_Resources/network/`
- Me profile + signals：`04_Assets/profile/`
- 双语切换（langpacks + apply）：`06_Infra/i18n/`
- 示例项目（TPCD）：`03_Goal-Projects/active/`

## 风险与应对

- 风险：用户把它当成“自动化产品” → 应对：在 README 明确非目标与边界（无数据源、无托管服务）
- 风险：开源示例泄露个人信息 → 应对：隐私基线 + 示例全部虚构/脱敏 + `.gitignore` 作为底线防护
- 风险：协议过重导致维护成本上升 → 应对：最小字段 + 可选字段 + 允许逐步完善
- 风险：Web 演示站被当成 SaaS、带来成本与合规压力 → 应对：坚持无状态；默认不存任何输入；免费额度耗尽就导流到 GitHub/BYOK
- 风险：“免费 API”不稳定/质量不可控 → 应对：把“免费”定位为可选兜底；核心体验始终可由 BYOK 保证；必要时改为低成本模型+限流

## 决策关联（可选）

- 是否引入“Events/Signals”作为一级对象 → `decisions/001-events-and-signals.md`
- 双轨发布（GitHub + Web）与 API 策略 → `decisions/001-dual-track-repo-and-web-playground.md`
