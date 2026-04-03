# master-schedule operations log

> 记录范围：`00_Master-Schedule` 相关页面与 Apple Calendar 同步链路的发布、验证与回退动作。

## 2026-03-11（模板首次回流）

- 变更内容：
  - 将 `master-schedule` 插件、页面资源、Apple Calendar 同步脚本与时间追踪脚本回流到公开模板。
  - 将 `08_Operations/00_Master-Schedule/` 与 `08_Operations/01_Time-Tracking/` 接入模板目录。
- 验证动作：
  - 运行 `build_month_calendar_feed.py`
  - 运行 `time_tracking.py report`
  - 运行 `cleanup_examples.py` dry-run
- 风险项：
  - Apple Calendar 直接同步依赖 macOS 本机日历权限
  - 页面发布目录与服务重启命令需按你的环境自行补齐

## 2026-03-11（页面发布占位）

- 目标目录：
  - `<docs-site-dir>/calendar-page.html`
  - `<docs-site-dir>/calendar-page.css`
  - `<docs-site-dir>/calendar-page.js`
  - `<docs-site-dir>/calendar-page-data.js`
- 建议动作：
  - 先备份旧文件
  - 覆盖静态资源
  - 重启你的静态站点或文档服务
  - 用浏览器和命令行做可达性检查
- 回退预案：
  - 恢复备份文件并重启服务
