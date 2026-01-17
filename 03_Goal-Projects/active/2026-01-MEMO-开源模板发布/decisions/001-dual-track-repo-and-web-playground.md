# ADR 001：双轨发布（GitHub 协议仓库 + Web Playground）

## 背景

目标是传播一套 “AI-native personal OS / memory protocol” 的方法与参考实现，而不是上线一个需要长期运维的 SaaS 产品。现实约束包括：

- 没有自动化数据源（输入来自用户的碎片：文本/截图/链接/命令输出等）
- 不希望承担用户隐私、账号体系、数据存储与合规的长期责任
- 传播上又需要“低门槛体验”（30 秒理解价值，而不是先读长文）

## 选项

### A. 只做 GitHub repo（模板/协议/CLI）

- 优点：最小运维；价值清晰（文件协议 + 可复用工作流）；对 power users 友好
- 缺点：传播门槛较高（需要 clone/跑命令/理解结构）

### B. 只做 Web（在线应用）

- 优点：传播与体验门槛最低
- 缺点：容易走向 SaaS（存储/账号/费用/合规/运维）；与“本地落盘 + Git”核心理念偏离

### C. 双轨：GitHub repo + 无状态 Web Playground

- GitHub repo = source of truth（协议、目录、workflow、skills、prompts、demo）
- Web = 传播入口（在线体验编译过程），但不承担存储与账号

## 决策

选择 **C：双轨发布**。

## 决策细节（边界）

- GitHub repo
  - 交付：协议说明、目录规范、workflow、skills、prompts、CLI、脱敏 demo
  - 原则：输出永远写回 Markdown 文件（可 git diff / 可 PR）
- Web Playground
  - 形态：无状态（stateless），不保存用户输入、不做登录、不做数据库
  - 默认：BYOK（用户自带 API key）保证可用性与成本可控
  - 可选：少量免费额度/免费模型兜底（若有赞助或稳定低成本渠道），额度耗尽则引导 BYOK/clone
  - 目标：30 秒展示“输入碎片 → 输出结构化 Markdown → 可复制写回”

## 理由

- 传播与工程价值分离：Web 负责“看见价值”，repo 负责“落地复用”
- 避免 SaaS 运维地狱：不背数据存储与账号体系
- 与核心理念一致：个人记忆资产以文件协议+版本控制为主，而非平台锁定

## 后续动作

- [ ] 在 repo README 增加 “Try Online” 链接位（网页上线后补）
- [ ] 明确 Web 的隐私声明（No DB / No Auth / BYOK / LocalStorage）
- [ ] 定义“免费额度兜底”的策略与熔断（限流、总 token 上限、耗尽提示）

