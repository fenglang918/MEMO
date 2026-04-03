# Indexing Contract Draft v1 (`on hold`)

> 本文件记录公开模板里保留的一版本地 indexing 实验接口草案。  
> 当前它不是模板的生效主协议，也不是默认工作流依赖。

## 1. 目标与范围

定义仓库级 `concept -> evidence` 的最小契约，确保：

- `00_Protocol` 与 `06_Infra/indexing` 使用同一套目录语义
- 产物既能给人读，也能给脚本消费

上游协议：

- [`repo-contents-contract.v1.md`](repo-contents-contract.v1.md)

实验入口：

- 脚本：[`../../06_Infra/indexing/scripts/build_repo_concept_index.py`](../../06_Infra/indexing/scripts/build_repo_concept_index.py)
- 种子：[`../../06_Infra/indexing/concept-seeds.yaml`](../../06_Infra/indexing/concept-seeds.yaml)

## 2. 输入契约

### 2.1 Scope

- 默认建议 scope：`00_Protocol`、`03_Goal-Projects`、`05_Resources/network`、`07_Principles`、`08_Operations`
- 支持通过 `--scope` 追加或覆盖

### 2.2 Concept Seeds

文件格式（YAML）：

```yaml
concepts:
  - id: goal-tracking
    concept: Goal Tracking
    aliases: [okr, milestone, target]
    scope: [03_Goal-Projects]
```

字段约束：

- `id`：必填，建议 kebab-case
- `concept`：必填，展示名
- `aliases`：可选，别名列表
- `scope`：可选，缺省时回退到当前构建 scope

### 2.3 文档扫描

- 扫描 scope 内全部 `*.md`
- 忽略：
  - 路径包含 `/.agents/`
  - 文件名以下划线开头

## 3. 匹配与打分契约

对 `concept + aliases` 中每个 term，按以下规则累计单文档最佳分数：

- `filename` 命中：`+3`
- `title` 命中：`+3`
- `heading` 命中：`+2`
- `path` 命中：`+1`
- `content` 命中：`+1`

仅保留 `score > 0` 的证据。

## 4. 证据类型（kind）归类契约

按路径顺序判定：

1. 包含 `/cognition/` -> `cognition`
2. 包含 `/decisions/` -> `decision`
3. 包含 `/04-review/` -> `review`
4. 包含 `/timeline/` -> `timeline`
5. 包含 `/plans/` -> `plan`
6. 文件名为 `README.md` 或 `index.md` -> `index`
7. 包含 `/notes/` -> `note`
8. 其他 -> `other`

## 5. 输出契约

### 5.1 JSON

默认路径：[`../../06_Infra/indexing/repo-concept-index.v1.json`](../../06_Infra/indexing/repo-concept-index.v1.json)

顶层字段：

- `version`
- `profile`
- `built_at`
- `scope`
- `files_scanned`
- `policy`
- `concepts[]`

### 5.2 Markdown

默认路径：[`../../06_Infra/indexing/repo-concept-index.v1.md`](../../06_Infra/indexing/repo-concept-index.v1.md)

每个 concept 展示：

- aliases
- evidence count
- top evidence（默认最多 8 条）

### 5.3 Link Check

默认输出目录：`../../06_Infra/indexing/reports/`

检查两类目标：

1. Markdown 本地链接
2. 反引号中的路径型片段

## 6. 运行契约

标准命令：

```bash
python3 06_Infra/indexing/scripts/build_repo_concept_index.py \
  --profile v1_1 \
  --summary-json 06_Infra/indexing/reports/index-summary.v1_1.json
```

## 7. 变更治理

1. 协议变化时同步脚本或 README
2. 脚本行为变化时回补本文件
3. 若未来重启该方向，建议新开版本文件，避免覆盖漂移
