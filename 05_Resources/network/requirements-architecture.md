# Personal CRM: Requirements & Architecture / 人脉库：需求与架构

English:
- First priority is retrieval: you should be able to find “the right person” in seconds.
- Second priority is sustainability: minimum required fields, append-only logs.
- Third priority is action: each card should land in “next follow-up” or “no action”.

中文：
- 第一优先级是可检索：几秒内找到“该问谁”。
- 第二优先级是可持续：最小必填字段 + 增量记录。
- 第三优先级是行动：每张卡落到“下次跟进/暂无动作”。

Non-goals / 非目标：
- Full CRM automation (email pipelines, graph visualization, etc.)
- Heavy database schema before you feel pain

