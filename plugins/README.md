# plugins

这里放 Codex 本地插件示例与可选扩展。

边界：

- 这类插件不是模板默认主链路的一部分
- 只有在你明确需要对应能力时才安装或启用
- 插件自身不应把私有 token、缓存或本机状态写入仓库

当前示例：

- `memo-audio-transcribe/`：离线音频转录到 `01_Inbox/`

Plugin Skills：

- `memo-audio-transcribe/skills/memo-audio-transcribe/SKILL.md`
  - 插件级本地音频转写入口

插件市场配置入口：

- `../.agents/plugins/marketplace.json`

和 `06_Infra/plugins/` 的区别：

- `plugins/`：更偏 Codex 本地插件与安装入口
- `06_Infra/plugins/`：更偏仓库内脚本链、bridge 与基础设施扩展
