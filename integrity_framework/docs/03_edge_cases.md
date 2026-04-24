# 03 · 边界案例 · Edge Cases

> 实战中会遇到这些奇怪情况。每个都列出推荐处理 + 理由。

---

## 1. 承诺被部分撤回

> 公司 Q1 承诺"FY24 营收 25% 增长 + 海外业务占比 30%"。Q3 单独撤回海外业务占比目标,营收目标维持。

处理:**拆分为两条 promise**。
- `id: fy24-revenue-25pct` — 维持原始,后续按实际算 verdict
- `id: fy24-overseas-pct-30` — verdict outcome = `broken`(撤回 ≠ 不算),reasoning 写明 Q3 撤回

理由:一条 promise 含多个可独立验证的目标,本身就违反单一职责。Stage 4 的 schema 假设一条 promise 一个 outcome。

## 2. 一条承诺多个责任人

> 联合声明:CEO + CTO 共同承诺产品 GA。

处理:`made_by` 字段当前是单值。**填两人姓名用 `/` 分隔**:`@example-ceo / @example-cto`。

未来 schema v2 可能改为数组,但当前以最小变更为准。

## 3. 承诺到期前公司破产 / 退市

处理:outcome = `unverifiable`(框架不评估死人)。reasoning 写明退市/破产事实 + 链接。

## 4. 承诺数字是范围而非点

> "FY24 营收增长 20%-25%"

处理:把范围写在 `promise_zh` 文本中。verdict 时:
- 实际 ≥ 25% → `fulfilled`
- 20% ≤ 实际 < 25% → `fulfilled`(在范围内)
- 15% ≤ 实际 < 20% → `partial`(略低于范围下限)
- < 15% → `broken`(显著低于范围)

reasoning 必须显式标出"承诺范围下限是 X,实际是 Y"。

**框架本身不解析范围**,这是 verdict 判定者的职责。

## 5. 时间窗口极端宽松

> "未来 5 年内推出 AI Agent"

处理:**不接受**(见 docs/01 边界规则:时间窗口太宽 → 不记录)。如果坚持要记录,due_by 填 5 年后那天,等到期再 verdict;在那之前是 `pending`,对当前分数无影响。

## 6. 分拆 / 重组后承诺的归属

> A 公司 2023 年承诺业务 X 增长。2025 年 A 把业务 X 分拆给 B 公司上市。承诺归 A 还是 B?

推荐:**两边都跟**。
- A 公司档案中保留原 promise,verdict outcome 取决于"A 在分拆前的执行情况 + 分拆决策本身是否兑现承诺精神"
- B 公司档案中**新建**一条 promise,引用 A 的分拆公告 + B 的接续表述

reasoning 必须互相引用,避免读者只看一份档案得出片面结论。

## 7. 后续修订替代之前的承诺

> Q1 给 25% 指引,Q2 财报附带"上调至 30% 指引"。

处理:**两条 promise**:
- `fy24-revenue-25pct-q1` outcome = `fulfilled`(因为后续被上调,事实兑现)
- `fy24-revenue-30pct-q2` 按实际算

不要 silently overwrite 旧 promise——guidance 调整本身是诚信信号。

## 8. 跨年度的"年初目标"

> 2024 年 1 月发"FY24 增长 25%"。due_by 是 12 月底还是次年财报披露日?

约定:**due_by = FY end + 60 天**(给财报披露留窗口)。verdict 在财报实际披露后做。

## 9. Verdict 之后又出新证据

> 2025 年 5 月做 verdict = `fulfilled`。2026 年 1 月审计调整发现实际数字虚高 8%,真实增长 17%。

处理:**新增**第二条 verdict,不修改老的:
- 老 verdict (2025-05) 保留,标 `superseded_by`(若 schema 支持)或仅依赖 judged_at 排序
- 新 verdict (2026-01) outcome = `partial` 或 `broken`(取决于程度),reasoning 必须引用审计调整

`compute_integrity_score` 默认对每个 promise_id 处理所有 verdict——若同 id 有多条,**按 judged_at 最新一条为准**(framework 行为待 v0.2.0 明确,当前 caller 可在传入前 dedup)。

## 10. 跨市场上市的同一个发言

> 公司 H 股 + A 股双重主要上市。CEO 同一个发言被记录在两边的招股书。

处理:同一条 promise,只记录一次。`subject_ticker` 可填主要交易市场的 ticker(通常是流动性高的那个)。reasoning / source 可以引多个 URL。

## 11. 翻译歧义

> 中文电话会原文"我们争取实现",英文翻译"we are committed to achieving"。

处理:**以原文为准**(中国公司中文为原文,美国公司英文为原文)。promise_zh 必填,promise_en 选填,**禁止用翻译版做强度判定**。如发现翻译失真,reasoning 必须指出。

## 12. 历史 promise 的署名问题

> 2018 年的承诺,当时 CEO 已离任,无法 ping。现任管理层不愿背书。

处理:promise 仍然记录(事实是当时承诺过)。verdict 由现任研究者署名(`judged_by` 是研究者,不是承诺人)。reasoning 必须明确"该承诺由前任 CEO X 在 2018 年做出,本判定基于公开数据"。

---

**没在这里列出的边界案例?** 提 GitHub `methodology_discussion` issue,我们补进来。

**Last reviewed**: 2026-04-24 by Claude · finalize by @siwuya
