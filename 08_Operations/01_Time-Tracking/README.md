# Time Tracking

这个模块用于记录“时间段 - 做了什么”，并自动尝试挂钩 `03_Goal-Projects` 里的项目，方便看时间花在哪里、各项目投入占比。

## 你每次只需要做什么

1. 记录 1 行或多行：
   - `2026-03-03 09:30-11:00 MEMO 模板文档收口`
   - `2026-03-03 14:00-15:20 读博与工作路径复盘`
   - `2026-03-03 20:00-21:00 篮球训练 #proj/Fitness`
2. 运行 `add` 追加。
3. 运行 `report` 看投入统计。

## 命令（最短闭环）

```bash
python3 06_Infra/plugins/master-schedule/scripts/time_tracking.py add \
  --entry "2026-03-03 09:30-11:00 MEMO 模板文档收口" \
  --entry "2026-03-03 14:00-15:20 读博与工作路径复盘"

python3 06_Infra/plugins/master-schedule/scripts/time_tracking.py report
```

## 数据文件

- 原始记录：`time_entries.csv`
- 报表输出：`reports/latest.md`

## 自动挂钩规则（简版）

1. 如果文本里有 `#proj/<name>` 或 `#project/<name>`，优先用它。
2. 否则脚本会扫描 `03_Goal-Projects/**/README.md` 推断项目名，并做文本匹配。
3. 不确定就记为 `UNLINKED`。

## 相关入口

- 跨项目总日程：`../00_Master-Schedule/README.md`
- 插件与脚本：`../../06_Infra/plugins/master-schedule/README.md`
