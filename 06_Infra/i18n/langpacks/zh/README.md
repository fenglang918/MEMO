# MEMO

**Making Ephemeral Memories Objects**

An AI-native personal operating system protocol.

这个仓库是 MEMO 的 **公开模板产品**：保留 i18n、脱敏示例、`USAGE.md` 和 Agent 工作流入口，同时把私有工作仓里已经稳定下来的协议、目录语义与 skills 回流进来；`06_Infra/indexing/` 仅作为可选实验保留。

## 这是什么

MEMO 不是一个单一 App，而是一套“如何组织长期个人记录”的协议：

- 用 Markdown 和 Git 持有数据
- 用目录语义定义对象边界
- 用 Agent 和脚本在仓库上工作

核心立场：

- **Protocol first**
- **Agent agnostic**
- **Search before summary**

## 目录结构

```text
.
├── 00_Protocol/             # contracts / federation / usage / privacy
├── 01_Inbox/                # 临时输入
├── 02_Desires/              # 上游驱动
├── 03_Goal-Projects/        # TPCD + YYYY/MM/
├── 04_Assets/               # 稳定资产
├── 05_Resources/            # 外部可调用资源
├── 06_Infra/                # indexing / i18n / utilities
├── 07_Principles/           # 跨项目原则
├── 08_Operations/           # 日程 / 时间追踪 / 环境配置
├── .agents/skills/          # Agent 技能包
└── develop/                 # 模板开发工作区
```

## 项目结构

`03_Goal-Projects/` 现在有两种主入口：

- `YYYY/MM/<project>/`
- `evergreen/<project>/`

每个项目遵循 **TPCD**：

- `README.md` = Target
- `PLAN.md` = Plan
- `cognition/` = Cognition
- `decisions/` = Decision

## 快速开始

1. 用模板创建仓库，或 clone 到本地
2. 先从目标目录的 `README.md` / `index.md` / `AGENTS.md` 熟悉结构
3. 需要的话用 `cleanup_examples.py` 清理内置示例
4. 用 `00_Protocol/AGENTS.md.template` 生成你自己的仓库级 `AGENTS.md`
5. 如需回看旧 indexing 实验，再运行 `06_Infra/indexing/` 里的脚本

```bash
python3 06_Infra/cleanup_examples.py
```

## Agent 入口

- 协议入口：`00_Protocol/`
- Skills 入口：`.agents/skills/`
- 可选 indexing 实验：`06_Infra/indexing/`

推荐阅读顺序：

```text
仓库目录结构 / 文件命名
  -> 对应域 README / index / AGENTS
  -> 必要时再看 00_Protocol 总结层
```

## 多语言与示例

这个模板保留：

- `06_Infra/i18n/` 的中英文 langpacks
- 脱敏示例项目 / 人脉卡片 / principle 示例
- `08_Operations/` 下的总日程与时间追踪骨架
- `06_Infra/plugins/master-schedule/` 下的日历与报表脚本链
- `00_Protocol/USAGE.md` 作为上手页

如果你想从更干净的骨架开始：

- `python3 06_Infra/cleanup_examples.py`
- `python3 06_Infra/cleanup_examples.py --apply`

## 适合什么，不适合什么

更适合：

- 需要长期、可迁移、可检索的个人记录
- 想让 Code Agent 在本地仓库上工作
- 想把内容结构和工具能力分开维护

不适合：

- 被动堆笔记
- 完全无结构的日志仓库
- 存放可直接滥用的明文机密

## License

MIT
