# Usage / 使用说明

## Search-first / 先检索

- Find people by keyword: `rg -n "diffusion|referral|GPU" 05_Resources/network/people`
- Find follow-ups: `rg -n "^\\s*-\\s*Next follow-up|^\\s*-\\s*下次跟进" 05_Resources/network/people`

## People cards / 人脉卡片

Create one file per person under `05_Resources/network/people/` using `_template.md`.

Minimum recommended fields:

- `Handle/ID`
- `Keywords / 关键词`
- `Tags`
- `Status / 状态`
- `Last contact / 最后联系`
- `Next follow-up / 下次跟进` (or explicitly “None / 暂无”)

## Projects / 项目

Each project folder under `03_Goal-Projects/active/` follows:

- `README.md` (Target)
- `PLAN.md` (Plan)
- `cognition/` (Cognition notes)
- `decisions/` (ADR-style decisions)
