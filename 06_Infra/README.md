# 06_Infra

基础设施区（可选），用于放脚本、插件、bridge、语言切换与其他低依赖工具；其中 `indexing/` 仅作为实验候选保留。

## 当前入口

- Skills（生效）：`../.agents/skills/`
- Plugins：`06_Infra/plugins/`
- Optional indexing：`06_Infra/indexing/`
- i18n：`06_Infra/i18n/`
- Scripts / utilities：`06_Infra/cleanup_examples.py` 等

## 推荐先看

- `06_Infra/plugins/master-schedule/`
  - 对应 `08_Operations/00_Master-Schedule/` 与 `08_Operations/01_Time-Tracking/`
  - 提供月视图、Apple Calendar 同步与 time tracking 脚本
  - 对应 Agent 入口：`../.agents/skills/master-schedule-sync/`
- `06_Infra/plugins/lark-bridge/`
  - 提供 read-first 的本机 Lark/Feishu CLI bridge
  - 默认只封装 docs / chats / messages / mail / calendar / contact 查询
  - 对应局部 skill：`06_Infra/plugins/lark-bridge/.agents/skills/lark-bridge/`
- `06_Infra/plugins/Google-Drive/`
  - 提供可配置的本地云盘挂载 / 同步入口
  - 适合跨设备同步较大文件、本地工作文件和临时资料包
  - `sync-dir/` 默认不纳入 Git
- `06_Infra/i18n/`
  - 提供 zh / en langpacks 与语言切换脚本

## 常用命令

如需回看旧 indexing 实验：

```bash
python3 06_Infra/indexing/scripts/build_repo_concept_index.py \
  --profile v1_1 \
  --summary-json 06_Infra/indexing/reports/index-summary.v1_1.json
```

切换语言（dry-run 默认）：

```bash
python3 06_Infra/i18n/switch_language.py --lang en
python3 06_Infra/i18n/switch_language.py --lang zh
```

清理内置示例：

```bash
python3 06_Infra/cleanup_examples.py
python3 06_Infra/cleanup_examples.py --apply
```

Lark bridge 自检：

```bash
bash 06_Infra/plugins/lark-bridge/scripts/doctor_lark.sh
bash 06_Infra/plugins/lark-bridge/scripts/lark_bridge.sh docs-search --query "AgenQA" --format pretty
```
