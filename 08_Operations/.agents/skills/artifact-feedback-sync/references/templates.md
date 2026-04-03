# Templates For `artifact-feedback-sync`

Use these minimal blocks. Replace placeholders and avoid duplicate headings.

## 1) raw-dialogue index block

```md
## 关联版本与索引（本次发送）

- 本次发送链接（作为外发存档）：
  - `<external_archive_link>`
- repo 当前目标产物正文：
  - `<artifact_path>`
- 本次反馈独立记录：
  - `<feedback_log_path>`
- 目标产物 git 快照（记录时刻）：
  - recorded_at: `<recorded_at>`
  - repo: `<repo_root>`
  - branch: `<branch>`
  - head: `<head_full>` (`<head_short>`)
  - blob: `<artifact_blob_hash>`
```

## 2) feedback-log sections

```md
## 1) 关联文档（双向索引）

- 对话原文：`<raw_dialogue_path>`
- 当前目标产物：`<artifact_path>`

## 2) 发送版本说明（外发存档 + repo 对照）

- 外发链接（存档锚点）：
  - `<external_archive_link>`
- 说明：
  - 上述链接视为发送版本存档。
  - repo 中以 `<artifact_path>` 作为当前维护正文。

## 3) 目标产物 git 快照（记录时刻）

- 记录时刻：`<recorded_at>`
- Git 仓库根：`<repo_root>`
- 分支：`<branch>`
- 当前 HEAD：
  - short: `<head_short>`
  - full: `<head_full>`
- 目标产物文件路径（repo 相对）：
  - `<artifact_relpath>`
- 目标产物文件 blob hash（工作区）：
  - `<artifact_blob_hash>`
- 最近一次修改该文件的提交：
  - commit: `<last_commit_full>`
  - date: `<last_commit_date>`
  - subject: `<last_commit_subject>`

## 4) 本次反馈时间序（摘要）

1. `<YYYY-MM-DD HH:MM>` `<event>`
2. `<YYYY-MM-DD HH:MM>` `<event>`
```

## 3) artifact internal index block

```md
## 内部索引（仅内部）

- 本次反馈记录：`<feedback_log_path>`
- 对话原文：`<raw_dialogue_path>`
- 外发存档（飞书）：`<external_archive_link>`
```

## 4) private-notes INDEX insertion pattern

```md
内部对齐（先看）：
...
N. `<raw_dialogue_path>`

对外发送（后看）：
...
N. `<feedback_log_path>`（反馈记录）
```
