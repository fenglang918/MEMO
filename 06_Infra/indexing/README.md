# 06_Infra/indexing

本目录保留仓库级 indexing 实验：把“概念”映射到“证据文档”。当前它不是模板的默认依赖。

默认口径：

- 目录结构、README、AGENTS、命名约定本身就是主要索引层
- Agent 不预设固定 indexing 流程，应按任务自行导航
- 若未来需要更强的索引能力，可评估自研脚本或外部服务；本目录仅作为候选样本保留

## 当前状态

- 状态：`experimental / on hold`
- 用途：保留脚本、样例产物与评估思路
- 非目标：不再作为模板上手流程的前置条件

## 保留内容

- 种子词：`concept-seeds.yaml`
- 构建脚本：`scripts/build_repo_concept_index.py`
- Markdown 索引：`repo-concept-index.v1.md`
- JSON 索引：`repo-concept-index.v1.json`
- 链接报告：`reports/link-check.v1.md`
- 构建摘要：`reports/index-summary.v1_1.json`

## 如需回看实验

```bash
python3 06_Infra/indexing/scripts/build_repo_concept_index.py \
  --profile v1_1 \
  --summary-json 06_Infra/indexing/reports/index-summary.v1_1.json
```

## 何时才需要运行

- 想了解旧的 concept -> evidence 方案
- 想比较模板内实验与外部 indexing 服务
- 想借用其 link-check 思路做一次性检查
