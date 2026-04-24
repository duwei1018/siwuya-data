# 诚信评分框架 · Integrity Framework

> 一套用于评估上市公司**管理层公开承诺兑现度**的算法 + 方法论。

**Stage 4 待实施**(当前 Stage 1 仅占位)。

## 目录

- `METHODOLOGY.md` — 方法论说明(为什么这么打分)— **待写**
- `src/` — 算法实现(MIT 协议)— **待写**

## 设计原则(预告)

详细设计将在 Stage 4 实施。当前先记录设计原则:

1. **结构化承诺** — 算法消费 schema 中 `integrity_tracking.tracked_promises[*]`
2. **可解释** — 每个评分必须有可追溯的推理过程
3. **署名制** — 每个判定带 `judged_by`,责任明确
4. **可挑战** — 提供反例输入,任何人可以提出异议(GitHub Issue)
5. **方法论开源,数据闭源** — 算法在本仓库,具体公司当前评分在 [siwuya.org](https://siwuya.org) 主站
