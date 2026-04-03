# Google Drive Plugin

用于给 MEMO 模板提供一个“可配置的本地云盘挂载 / 同步入口”。

这个插件位点的目标不是把仓库主数据迁移到云盘里，而是给以下内容提供跨设备同步通道：

- 比较大的文件
- 临时但重要的资料包
- 不适合直接进 Git 的本地工作文件

## 目录

```text
06_Infra/plugins/Google-Drive/
├── README.md
└── sync-dir/
```

## 推荐用法

1. 在本机安装并登录云盘客户端。
2. 把 `06_Infra/plugins/Google-Drive/sync-dir/` 配置为本地挂载或同步目录。
3. 需要跨设备同步、但不适合直接进 Git 的文件，优先放到 `sync-dir/`。
4. 长期真源内容仍放回仓库正式内容域，例如：
   - `03_Goal-Projects/`
   - `04_Assets/`
   - `05_Resources/`

## 边界

- `sync-dir/` 只是同步入口，不是主知识库真源。
- `sync-dir/` 内容默认不纳入 Git 版本控制。
- 不要把账号密码、私钥、API keys 之类明文机密放进去。
- 公开模板只保留这个骨架，不假设任何具体云盘厂商、账号或私人目录结构。

## 最小验证

```bash
echo "# sync test" > 06_Infra/plugins/Google-Drive/sync-dir/sync-test.md
ls -la 06_Infra/plugins/Google-Drive/sync-dir/
```

如果你的云盘客户端显示该文件已同步，说明挂载 / 同步链路是通的。
